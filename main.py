import typer
import os
from typing_extensions import Annotated


def main(root_dir: Annotated[str, typer.Argument()] = os.getcwd()):
    print(f"Recursing from: {root_dir}")


if __name__ == "__main__":
    typer.run(main)