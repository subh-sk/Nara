import re
from groq import Groq
import functools
import inspect
import os
from dotenv import load_dotenv
from rich.console import Console
from nara.nara.init import init


current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, '.env')

load_dotenv(dotenv_path=file_path)

System = [
    {"role": "system", "content": "write code in ```python\n<code>\n``` format"},
    {"role": "system", "content": "you are a Ai which create funcs src in python whatever user instruct and if any imports of module is needed then write import <module> inside the function."},
    {"role": "system", "content": "only provide func code DO not run it."},
    {"role": "user", "content": "# Instruction Create This function\n\ndef add(a: int = 0, b: int = 0) -> int:"},
    {"role": "user", "content": "Sure, here's the Python function code for the add function as per your instructions:\n\n```python\ndef add(a: int = 0, b: int = 0) -> int:\n    return a + b\n```"},
]


def Filter(txt:str) -> str|None:
    pattern = r"```python(.*?)```"
    matches = re.findall(pattern, txt, re.DOTALL)

    if matches:
        python_code = matches[0].strip()
        return python_code
    else:
        return None
 
def GroqGen(Prompt:str):
    API = os.getenv("GROQ_API")

    if not API:
        API = init()

    client = Groq(api_key=API)

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


def update_source_file(file_path, old_code, new_code):
    with open(file_path, 'r') as file:
        file_data = file.read()

    file_data = file_data.replace(old_code, new_code)

    with open(file_path, 'w') as file:
        file.write(file_data)


def CreateFunc():
    """
    Generates a new function based on the provided function using the GROQ model.

    Parameters
    ----------
    func : callable
        The original function for which a new function will be generated.

    Returns
    -------
    callable
        The wrapper function that replaces the original function with the generated code.

    Raises
    ------
    Exception
        If no code is generated due to improper instruction.

    Notes
    -----
    This function utilizes the GROQ model to generate Python code based on the provided 
    function's source code. It extracts the function definition, updates the source file 
    with the new code, and replaces the original function definition with the generated code.

    Example
    -------
    >>> @CreateFunc()
    ... def Addition(x, y):
    ...     pass

        ######### OR ##########
    >>> @CreateFunc()
    ... def test():
    ...     '''code for calucltor in tikinter'''
    """
    def wrapper(func):
        # Get the source code of the function
        source_lines, _ = inspect.getsourcelines(func)
        source_code = ''.join(source_lines).strip()

        # Get the signature of the function
        signature = inspect.signature(func)

        # Prepare the function prompt
        func_definition = f"{source_code}"
        raw_code = GroqGen(f"# Instruction Create This function\n\n{func_definition}")
        generated_code = Filter(raw_code)

        if generated_code:
            # Get the file path of the original function
            file_path = inspect.getfile(func)

            # Replace the function definition with the generated code
            update_source_file(file_path, func_definition, generated_code)

        else:
            raise Exception("No code generated due to improper instruction. Try adding a docstring.")

        # Execute the original function
        return func()

    return wrapper
