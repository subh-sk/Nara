import os
import shutil


def clearPycacheDirectories(directory: str, display_status=False) -> None:
    """
    Recursively removes all '__pycache__' directories found within the specified directory.

    Args:
        - directory (str): The root directory path to start searching for '__pycache__' directories.
        - display_status (bool, optional): If True, displays status messages indicating which directories
            were deleted. Defaults to False.

    Returns:
        None
    """
    count = 0
    for root, dirs, files in os.walk(directory):
        if "__pycache__" in dirs:
            full_path = os.path.join(root, "__pycache__" )
            shutil.rmtree(full_path)
            if display_status:
                print(f">>> Deleted {full_path}")
            count += 1
    
    if display_status and not count:
        print(">>> No __pycache__ directories found.")