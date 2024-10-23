from abc import ABC, abstractmethod
from typing import Optional, Union, List, Dict, Any, Tuple, Callable
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv
from pythonjsonlogger import jsonlogger

import logging
import os

load_dotenv()

class Role(Enum):
    """Enumeration for the roles in the messaging system."""
    system = "system"
    user = "user"
    assistant = "assistant"

class ModelType(Enum):
    """Enumeration for the types of models."""
    textonly = "textonly"
    textandimage = "textandimage"

@dataclass
class Model:
    """Data class representing a model.

    Attributes:
        name (str): The name of the model.
        typeof (ModelType): The type of the model (text-only or text-and-image).
    """
    name: str
    typeof: ModelType

class LLM(ABC):
    """Abstract base class for Language Models (LLMs).

    Attributes:
        apiKey (str): API key for accessing the model.
        messages (List[Dict[str, str]]): List of messages exchanged with the model.
        temperature (float): Sampling temperature for generating responses.
        systemPrompt (Optional[str]): System prompt to guide the model's behavior.
        maxTokens (int): Maximum number of tokens for the model's responses.
        model (Model): The model being used.
        logger (logging.Logger): Logger for recording events and messages.
    """
    
    def __init__(
        self,
        model: Model,
        apiKey: str,
        messages: List[Dict[str, str]] = [],
        temperature: float = 0.0,
        systemPrompt: Optional[str] = None,
        maxTokens: int = 2048,
        logFile: Optional[str] = None,
    ) -> None:
        """Initializes the LLM with the given parameters.

        Args:
            model (Model): The model object to use for generating responses.
            apiKey (str): The API key for the model.
            messages (List[Dict[str, str]], optional): Initial messages to set context.
            temperature (float, optional): The sampling temperature.
            systemPrompt (Optional[str], optional): An optional system prompt.
            maxTokens (int, optional): The maximum number of tokens for responses.
            logFile (Optional[str], optional): Optional log file for logging events.
        """
        
        self.apiKey = apiKey
        self.messages = messages
        self.temperature = temperature
        self.systemPrompt = systemPrompt
        self.maxTokens = maxTokens
        self.model = model

        # logger setup
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)  # Set default log level
        
        # Create a JSON formatter
        json_formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s %(name)s %(funcName)s')
        
        # Check if logFile is None, in that case use console logging (pseudo-logging)
        if logFile is None:
            # Pseudo-logging with RichHandler (for console output)
            from rich.logging import RichHandler
            rich_handler = RichHandler()
            self.logger.addHandler(rich_handler)
        else:
            # If logFile is provided, log to a file in JSON format
            LOG_FILE = logFile
            file_handler = logging.FileHandler(LOG_FILE)
            file_handler.setFormatter(json_formatter)
            self.logger.addHandler(file_handler)

        # Handle case where `model` is passed as a string
        if type(model) is str:
            self.logger.error("Model name must be a Model object. Fixed temporarily.")
            self.model = Model(model, ModelType.textandimage)
            model = self.model
        
        self.logger.info(
            {   
                "message": "Initializing LLM",
                "model": model.name,
                "modelType": model.typeof.value,
                "temperature": temperature
            }
        )

        # Set the appropriate message handler based on the model type
        self.addMessage = self.addMessageTextOnly if model.typeof == ModelType.textonly else self.addMessageVision
        
        if systemPrompt:
            self.addMessage(Role.system, systemPrompt)

    @abstractmethod
    def run(self, prompt: str, save: bool = True) -> str:
        """Generates a response based on the given prompt.

        Args:
            prompt (str): The input prompt to generate a response for.
            save (bool, optional): Whether to save the response. Defaults to True.

        Returns:
            str: The generated response from the model.
        """
        raise NotImplementedError

    @abstractmethod
    def streamRun(self, prompt: str, save: bool = True) -> str:
        """Generates a response based on the given prompt using streaming.

        Args:
            prompt (str): The input prompt to generate a response for.
            save (bool, optional): Whether to save the response. Defaults to True.

        Returns:
            str: The generated response from the model.
        """
        raise NotImplementedError
    
    @abstractmethod
    def constructClient(self) -> None:
        """Constructs the client to interact with the model."""
        raise NotImplementedError

    @abstractmethod
    def testClient(self) -> None:
        """Tests the client to ensure it is set up correctly."""
        raise NotImplementedError

    def addMessage(self, role: Role, content: str, imageUrl: Optional[str] = None) -> None:
        """Adds a message to the message history.

        Args:
            role (Role): The role of the message sender.
            content (str): The content of the message.
            imageUrl (Optional[str], optional): Optional image URL to include in the message.
        """
        ...
    
    def addMessageVision(self, role: Role, content: str, imageUrl: Optional[str] = None) -> None:
        """Adds a message that may include an image URL to the message history.

        Args:
            role (Role): The role of the message sender.
            content (str): The content of the message.
            imageUrl (Optional[str], optional): URL of the image to include in the message.
        """
        
        if imageUrl is None:
            return self.addMessageTextOnly(role, content, imageUrl)
        if type(role) is str:
            role = Role[role]

        message: Dict[str, list] = {"role": role.value, "content": []}

        if content:
            message["content"].append(
                {
                    "type": "text",
                    "text": content
                }
            )

        if imageUrl:
            message["content"].append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": imageUrl
                    }
                }
            )

        self.messages.append(message)

    def addMessageTextOnly(self, role: Role, content: str, imageUrl: Optional[str] = None) -> None:
        """Adds a text-only message to the message history.

        Args:
            role (Role): The role of the message sender.
            content (str): The content of the message.
            imageUrl (Optional[str], optional): Optional image URL (ignored for text-only).
        """
        if type(role) is str:
            role = Role[role]

        if imageUrl is not None:
            self.logger.error("Image URL is not supported for text-only model. Ignoring the image URL.")
            
        self.messages.append({
            "role": role.value,
            "content": content
        })

    def getMessage(self, role: Role, content: str, imageUrl: Optional[str] = None) -> List[Dict[str, str]]:
        """Constructs a message dictionary for the given role and content.

        Args:
            role (Role): The role of the message sender.
            content (str): The content of the message.
            imageUrl (Optional[str], optional): Optional image URL to include in the message.

        Returns:
            List[Dict[str, str]]: A dictionary representation of the message.
        """
        
        if type(role) is str:
            role = Role[role]

        if imageUrl is not None:
            message: Dict[str, list] = {"role": role.value, "content": []}

            if content:
                message["content"].append(
                    {
                        "type": "text",
                        "text": content
                    }
                )

            if imageUrl:
                message["content"].append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": imageUrl
                        }
                    }
                )
            return message
        else:
            return {
                "role": role.value,
                "content": content
            }
        
    def log(self, **kwargs) -> None:
        """Logs the provided keyword arguments as an info message.

        Args:
            **kwargs: Additional context information to log.
        """
        self.logger.info(kwargs)

if __name__ == "__main__":
    print(Role.system.value)
