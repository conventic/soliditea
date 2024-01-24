import typer


def main(root_dir: str):
    print(f"Recursing from: {root_dir}")


if __name__ == "__main__":
    typer.run(main)