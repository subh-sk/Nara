import json
import os
from rich.console import Console

console = Console()

def JsonList(FileName="JsonList.json", **kwargs) -> None:
    """
    Updates a JSON file with new key-value pairs provided as keyword arguments. If the file does not exist, it creates a new empty JSON file. If the file is empty or contains invalid data, appropriate warnings are displayed.

    Parameters
    ----------
    FileName : str, optional
        The name of the JSON file to be updated. Default is "JsonList.json".
    **kwargs : dict
        Key-value pairs to be added to the JSON file.

    Raises
    ------
    ValueError
        If the JSON file is empty or does not contain a list.

    Examples
    --------
    >>> JsonList(FileName="data.json", name="Alice", age=30)
    >>> JsonList(FileName="data.json", city="New York")

    This will create or update the file "data.json" with the provided key-value pairs.
    """

    # Check if the file exists
    if not os.path.exists(FileName):
        # Create an empty JSON file
        console.print("[bold red]Warning:[/bold red] [italic green]File does not exist:[/italic green] {}".format(FileName))
        with open(FileName, 'w') as f:
            json.dump([], f)
        old_data = []
    else:
        # Load the existing JSON data
        with open(FileName, 'r') as f:
            try:
                old_data = json.load(f)
            except json.decoder.JSONDecodeError:
                console.print("[bold red]Warning:[/bold red] [italic green]File is empty:[/italic green] {}".format(FileName))
                raise ValueError("File is empty")
        if not isinstance(old_data, list):
            console.print("[bold red]Warning:[/bold red] [italic green]File is not a list:[/italic green] {}".format(FileName))
            raise ValueError("JSON data must be a list")
    tosave = {}
    # Update the JSON data with the new values
    for var_name, var_value in kwargs.items():
        tosave[var_name] = var_value

    # Write the updated JSON data back to the file
    with open(FileName, 'w') as f:
        old_data.append(tosave)
        json.dump(old_data, f, indent=4)

def JsonDict(Key, Value, FileName="JsonDict.json") -> None:
    """
    Updates a JSON file with a new key-value pair. If the file does not exist, it creates a new empty JSON file. If the file is empty or contains invalid data, appropriate warnings are displayed.

    Parameters
    ----------
    Key : str
        The key to be added or updated in the JSON file.
    Value : any
        The value to be associated with the key in the JSON file.
    FileName : str, optional
        The name of the JSON file to be updated. Default is "JsonDict.json".

    Raises
    ------
    ValueError
        If the JSON file is empty or does not contain a dictionary.

    Examples
    --------
    >>> JsonDict(key="username", value="johndoe", FileName="config.json")
    >>> JsonDict(key="timeout", value=30, FileName="settings.json")

    This will create or update the file "config.json" or "settings.json" with the provided key-value pairs.
    """

    # Check if the file exists
    if not os.path.exists(FileName):
        # Create an empty JSON file
        console.print("[bold red]Warning:[/bold red] [italic green]File does not exist:[/italic green] {}".format(FileName))
        with open(FileName, 'w') as f:
            json.dump({}, f)
        olddata = {}
    else:
        # Load the existing JSON data
        with open(FileName, 'r') as f:
            try:
                olddata = json.load(f)
            except json.decoder.JSONDecodeError:
                console.print("[bold red]Warning:[/bold red] [italic green]File is empty:[/italic green] {}".format(FileName))
                raise ValueError("File is empty")
    if not isinstance(olddata, dict):
        console.print("[bold red]Warning:[/bold red] [italic green]File is not a dictionary:[/italic green] {}".format(FileName))
        raise ValueError("JSON data must be a dictionary")

    # Update the JSON data with the new values
    olddata[Key] = Value

    # Write the updated JSON data back to the file
    with open(FileName, 'w') as f:
        json.dump(olddata, f, indent=4)