import re
from groq import Groq
import functools
import inspect

System = [
    {"role": "system", "content": "write code in ```python\n<code>\n``` format"},
    {"role": "system", "content": "you are a Ai which create funcs src in python whatever user instruct and if any imports of module is needed then write import <module> inside the function."},
    {"role": "system", "content": "only provide func code DO not run it."},
    {"role": "user", "content": "# Instruction Create This function\n\ndef add(a: int = 0, b: int = 0) -> int:"},
    {"role": "user", "content": "Sure, here's the Python function code for the add function as per your instructions:\n\n```python\ndef add(a: int = 0, b: int = 0) -> int:\n    return a + b\n```"},
]

client = Groq(api_key="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")

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


def update_source_file(file_path, old_code, new_code):
    with open(file_path, 'r') as file:
        file_data = file.read()

    file_data = file_data.replace(old_code, new_code)

    with open(file_path, 'w') as file:
        file.write(file_data)


def CreateFunc(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
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
        return func(*args, **kwargs)

    return wrapper