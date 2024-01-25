import typer
import os
import glob
from typing_extensions import Annotated


def main(root_dir: Annotated[str, typer.Argument()] = os.getcwd()):
    print(f"Recursing from: {root_dir}")
    # list to store txt files
    res = []
    # os.walk() returns subdirectories, file from current directory and 
    # And follow next directory from subdirectory list recursively until last directory
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".sol"):
                res.append(os.path.join(root, file))
    print(res)


if __name__ == "__main__":
    typer.run(main)