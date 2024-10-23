import os
import pathlib
from rich.console import Console
from rich.tree import Tree
from rich.text import Text

def displayFileStructure(
    directory: pathlib.Path = os.getcwd(),
    tree: Tree = None,
    console: Console = None
) -> None:
    """Recursively build and print a Tree with directory contents."""
    if tree is None:
        tree = Tree(f":open_file_folder: [link file://{directory}]{directory}")
        console = Console()

    paths = sorted(
        pathlib.Path(directory).iterdir(),
        key=lambda path: (path.is_file(), path.name.lower()),
    )
    for path in paths:
        if path.name.startswith("."):
            continue
        if path.is_dir():
            style = "dim" if path.name.startswith("__") else ""
            branch = tree.add(
                f"[bold magenta]:open_file_folder: [link file://{path}]{path.name}",
                style=style,
                guide_style=style,
            )
            displayFileStructure(path, branch, console)
        else:
            text_filename = Text(path.name, "green")
            text_filename.highlight_regex(r"\..*$", "bold red")
            text_filename.stylize(f"link file://{path}")
            file_size = path.stat().st_size / (1024 * 1024)  # Convert bytes to megabytes
            text_filename.append(f" ({file_size:.2f} megabytes)", "blue")
            icon = "🐍 " if path.suffix == ".py" else "📄 "
            tree.add(Text(icon) + text_filename)

    if console:
        console.print(tree)