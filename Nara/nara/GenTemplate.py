import re
from groq import Groq
import inspect
import os
from dotenv import load_dotenv
from rich.console import Console

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, '.env')

load_dotenv(dotenv_path=file_path)

System = [
    {"role": "system", "content": "write code in ```python\n<code>\n``` format"},
    {"role": "system", "content": "you are a Ai which create templates src in python whatever user instruct and if any imports of module is needed then write import <module>."},
    {"role": "user", "content": "# Instruction Create Flask Template"},
    {"role": "user", "content": "Sure, here's the Python template code for the flask template as per your instructions:\n\n```python\nfrom flask import Flask, render_template\napp = Flask(__name__)\n\n@app.route('/')\ndef index():\n    return 'Hello World'\n\nif __name__ == '__main__':\n    app.run(debug=True)\n```"},
]

API = os.getenv("GROQ_API")

if not API:
    # Get the directory of the current script
    current_dir = os.path.dirname(__file__)

    # Get the full path of a file in the same directory
    file_path = os.path.join(current_dir, '.env')
    
    console = Console()
    API = console.input("[bold #e6a330]Let Begin with Groq [/bold #e6a330][green]API[/green][bold #0b7ce6] (https://console.groq.com/keys): [/bold #0b7ce6]")
    with open(file_path, "w") as f:
        f.write(f"GROQ_API = {API}")
    console.print("\nYOU CAN CHANGE YOUR API USING init() from Nara")

client = Groq(api_key=API)

def Filter(txt:str) -> str|None:
    pattern = r"```python(.*?)```"
    matches = re.findall(pattern, txt, re.DOTALL)

    if matches:
        python_code = matches[0].strip()
        return python_code
    else:
        return None

def GroqGen(Prompt:str):
    completion = client.chat.completions.create(
    model="llama3-70b-8192",
    messages = System + [{ "role": "user", "content": Prompt }],
    temperature=0.1,
    max_tokens=4096,
    top_p=1,
    stream=True,
    stop=None)
    r=""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            r += chunk.choices[0].delta.content
    return r


def update_source_file(file_path, new_code):
    with open(file_path, 'w') as file:
        file.write(new_code)


def CreateTemplate(prompt):
    """
    Generates a Python template based on the provided prompt using the GROQ model.

    Parameters
    ----------
    prompt : str
        The prompt or instruction for generating the Python template.

    Raises
    ------
    Exception
        If no code is generated due to improper instruction.

    Notes
    -----
    This function utilizes the GROQ model to generate Python code based on the provided prompt. 
    It extracts the generated Python code, updates the source file with the new code, and 
    replaces the function definition with the generated code.

    Example
    -------
    >>> CreateTemplate("Create a Flask template with a route that returns 'Hello World'")
    """
    raw_code = GroqGen(f"# Instruction Create This Template\n\n{prompt}")
    generated_code = Filter(raw_code)

    if generated_code:
        # Get the file path of the original function
        caller_frame = inspect.stack()[1]
        filepath = caller_frame.filename
        # Replace the function definition with the generated code
        update_source_file(filepath, generated_code)

    else:
        raise Exception("No code generated due to improper instruction.")