
from time import time as get_time
import os
from rich.console import Console

def init():
    """
    Initialize or update the Groq API key and save it to a .env file.

    This function prompts the user to input their Groq API key, which is then
    saved to a `.env` file located in the same directory as the script. If the
    `.env` file does not exist, it will be created. This function also informs
    the user how to change their API key by calling this function again.

    Parameters
    ----------
    None

    Returns
    -------
    str
        The API key provided by the user.

    Notes
    -----
    The function prints a message indicating that the API key can be changed by
    calling the `init` function again. The API key is saved in the `.env` file
    with the key `GROQ_API`.

    Examples
    --------
    >>> from Nara import init
    >>> api_key = init()
    Let Begin with Groq API (https://console.groq.com/keys): <user inputs API key>
    
    YOU CAN CHANGE YOUR API Calling init() :  
    >>> from Nara import init
    >>> init()
    
    """
    current_dir = os.path.dirname(__file__)

    # Get the full path of a file in the same directory
    file_path = os.path.join(current_dir, '.env')
    
    console = Console()
    API = console.input("[bold #e6a330]Let Begin with Groq [/bold #e6a330][green]API[/green][bold #0b7ce6] (https://console.groq.com/keys): [/bold #0b7ce6]")
    with open(file_path, "w") as f:
        f.write(f"GROQ_API = {API}")
    console.print("\nYou can change your API Calling init() function : \n[purple]>>>[/purple] from Nara import init\n[purple]>>>[/purple] init()",style=" #0b7ce6")
    return API
