import importlib
import subprocess
import sys


def check_and_install(package):
    try:
        # Check if the package is already installed
        importlib.import_module(package)
    except ImportError:
        # If not installed, install the package
        print(f"{package} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{package} has been installed.")