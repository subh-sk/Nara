import ollama
import importlib
import subprocess
import sys

def check_and_install(package):
    try:
        # Check if the package is already installed
        importlib.import_module(package)
        print(f"{package} is already installed.")
    except ImportError:
        # If not installed, install the package
        print(f"{package} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{package} has been installed.")

stream = ollama.chat(
    model='llama3.1',
    messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)
  
  
# TODO ye mere mi chal hi nhi