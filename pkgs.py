import os
from rich import print

def get_all_directories(root_dir):
    directory_paths = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        directory_paths.append(dirpath)
    return directory_paths

# Example usage:
root_directory = r'.'
all_directories = get_all_directories(root_directory)

formatted_paths = []

for path in all_directories:
    # Remove leading './' and replace '\' with '.'
    formatted_path = path.removeprefix(root_directory).replace('\\', '.').lstrip('.')
    formatted_paths.append(formatted_path)

formatted_paths.remove("")
# Print formatted paths
print(formatted_paths)
