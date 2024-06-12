import os
import json
import random

def LoadJson(FileName: str = "Json.json", PickRandom: int | None = None) -> dict | list:
    """
    Loads JSON data from a file and optionally selects random items from the data.

    Parameters
    ----------
    FileName : str, optional
        The name of the JSON file to load. Default is "Json.json".
    PickRandom : int or None, optional
        If provided, specifies the number of random items to select from the loaded JSON data. 
        If None, all items are returned. Default is None.

    Returns
    -------
    dict or list
        The loaded JSON data. If PickRandom is None, the return type matches the type of the loaded data.
        If PickRandom is not None, returns a dictionary or list containing the randomly selected items.

    Raises
    ------
    FileNotFoundError
        If the specified JSON file does not exist.
    ValueError
        If the JSON file is invalid or if PickRandom is larger than the number of items in the data.

    Examples
    --------
    >>> LoadJson(FileName="data.json")
    {'name': 'Alice', 'age': 30, 'city': 'New York'}

    >>> LoadJson(FileName="data.json", PickRandom=2)
    {'name': 'Alice', 'city': 'New York'}

    This function loads JSON data from a file and optionally selects random items if PickRandom is provided.
    If the file does not exist or the JSON data is invalid, appropriate exceptions are raised.
    """
    # Check if the file exists
    if not os.path.exists(FileName):
        raise FileNotFoundError("File does not exist")

    # Load the JSON file
    with open(FileName, 'r') as f:
        try:
            # Attempt to decode the JSON data
            data: dict | list = json.load(f)
        except json.JSONDecodeError as e:
            # If JSON decoding fails, raise an exception
            raise ValueError("Invalid JSON file") from e

    # Check if random picking is requested
    if PickRandom is not None:
        # Ensure PickRandom is within the bounds of the data
        if PickRandom >= len(data):
            raise ValueError("PickRandom is larger than the number of items in the data")

        # If the data is a dictionary
        if isinstance(data, dict):
            # Get a list of keys from the dictionary
            keys = list(data.keys())
            # Pick random keys
            random_keys = random.sample(keys, PickRandom)
            # Create a new dictionary with the selected random items
            random_items = {key: data[key] for key in random_keys}
            # Update data with the randomly selected items
            data = random_items
        # If the data is a list
        elif isinstance(data, list):
            # Pick random items
            random_items = random.sample(data, PickRandom)
            # Update data with the randomly selected items
            data = random_items
        else:
            # If data is neither a dictionary nor a list, raise an exception
            raise ValueError("Data is neither a dictionary nor a list")

    # Return the loaded data
    return data
