from nara.llm.check_and_install import check_and_install
check_and_install('openai')

from nara.llm.base import LLM, Model, ModelType, Role

from typing import Optional, List, Dict, Generator
from dotenv import load_dotenv
from rich import print
from copy import deepcopy

import os
import openai



load_dotenv()

GPT4OMINI = Model(name="gpt-4o-mini", typeof=ModelType.textandimage)

# TODO: Add more models here

class OpenAI(LLM):
    def __init__(
        self,
        model: Model,
        apiKey: Optional[str] = None,
        messages: List[Dict[str, str]] = [],
        temperature: float = 0.0,
        systemPrompt: Optional[str] = None,
        maxTokens: int = 2048,
        cheatCode: Optional[str] = None,
        logFile: Optional[str] = None,
        extra: Dict[str, str] = {},
    ):
        super().__init__(model, apiKey, messages, temperature, systemPrompt, maxTokens, logFile)
        
        self.extra = extra
        self.cheatCode = cheatCode
        self.client: openai.OpenAI = self.constructClient()
        
        if cheatCode is None:
            p = self.testClient()
            if p:
                self.logger.info("Test successful for Openai API key. Model found.")
        else:
            self.logger.info("Cheat code provided. Model found.")

    def constructClient(self):
        try:
            client = openai.OpenAI(
            api_key=os.environ["OPENAI_API_KEY"] if self.apiKey is None else self.apiKey,
            )
            return client
        except Exception as e:
            print(e)
            self.logger.error(e)
    
    def testClient(self) -> bool:
        try:
            modelListResponse = self.client.models.list()
            models = modelListResponse.data
            for modelinfo in models:
                if modelinfo.id == self.model.name:
                    break
            else:
                self.logger.error("Model not found")
                raise Exception("Model not found in OpenAI, please add it to the code.")
            return True
        except Exception as e:
            print(e)
            self.logger.error(e)
    
    def streamRun(self, prompt: str = "", imageUrl: Optional[str] = None, save: bool = True) -> Generator[str, None, None]:
        toSend = []
        if save and prompt:
            self.addMessage(Role.user, prompt, imageUrl)
        elif not save and prompt:
            toSend.append(self.getMessage(Role.user, prompt, imageUrl))

        try:
            extra = {}
            if self.cheatCode is not None:
                extra["seed"] = 0

            chat_completion = self.client.chat.completions.create(
                messages=self.messages + toSend,
                model=self.model.name,
                temperature=self.temperature,
                max_tokens=self.maxTokens,
                stream=True,
                **extra,
                **self.extra
            )
        except Exception as e:
            self.logger.error(e)
            return "Please check log file some error occured."
        
        final_response = ""
        
        for completion in chat_completion:
            if completion.choices[0].delta.content is None:
                self.logger.info(completion)
                break

            if completion.choices[0].delta is not None:
                final_response += completion.choices[0].delta.content
                yield completion.choices[0].delta.content
        if save:
            self.addMessage(Role.assistant, final_response)

    def run(self, prompt: str = "", imageUrl: Optional[str] = None, save: bool = True) -> str:
        toSend = []
        if save and prompt:
            self.addMessage(Role.user, prompt, imageUrl)
        elif not save and prompt:
            toSend.append(self.getMessage(Role.user, prompt, imageUrl))

        try:
            extra = {}
            if self.cheatCode is not None:
                extra["seed"] = 0

            chat_completion = self.client.chat.completions.create(
                messages=self.messages + toSend,
                model=self.model.name,
                temperature=self.temperature,
                max_tokens=self.maxTokens,
                **extra,
                **self.extra
            )
        except Exception as e:
            self.logger.error(e)
            return "Please check log file some error occured."

        log_completion = deepcopy(chat_completion)
        log_completion.choices[0].message.content = log_completion.choices[0].message.content[:20]
        self.logger.info(log_completion)

        
        if save:
            self.addMessage(Role.assistant, chat_completion.choices[0].message.content)
        
        
        return chat_completion.choices[0].message.content


if __name__ == "__main__":
    llm = OpenAI(GPT4OMINI)
    for i in llm.streamRun("what is 2+2 reply in 1 char"):
        print(i)
    
    llm.addMessage("user", "Hello, how are you?")
    llm.addMessage("assistant", "I'm doing well, thank you!")
    # r = llm.run("what is in the image", "data:image/webp;base64,....")
    # print(llm.messages)
    # print(r)
    