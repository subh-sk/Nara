import collections
import pdb
try:
    import pdbp  # (Pdb+) --- Python Debugger Plus
except Exception:
    pass
import sys

from Nara.nara.GenFunc import CreateFunc
from Nara.nara.GenTemplate import CreateTemplate
from rich.console import Console
import os

def init():
    current_dir = os.path.dirname(__file__)

    # Get the full path of a file in the same directory
    file_path = os.path.join(current_dir, '.env')
    
    console = Console()
    API = console.input("[bold #e6a330]Let Begin with Groq [/bold #e6a330][green]API[/green][bold #0b7ce6] (https://console.groq.com/keys): [/bold #0b7ce6]")
    with open(file_path, "w") as f:
        f.write(f"GROQ_API = {API}")
    console.print("\nYOU CAN CHANGE YOUR API USING init() from Nara")