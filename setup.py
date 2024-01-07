import os
import shutil
from mypy import api
from argparse import ArgumentParser
import PyInstaller.__main__


def check_types() -> None:
    print("> mypy pitd.py pitd/")
    results = api.run(["game.py", "pitd/"])
    if results[0]:
        print("Type checking results:")
        print(results[0])
    if results[1]:
        print("Error report:")
        print(results[1])


def check_all() -> None:
    check_types()
    print()


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="Rouge", description="A Rogue-like written in pygame-ce"
    )

    parser.add_argument("--build", action="store_true")
    parser.add_argument("--check-all", action="store_true")
    parser.add_argument("--check-types", action="store_true")

    args = parser.parse_args()

    if args.check_all:
        check_all()
    else:
        if args.check_types:
            check_types()

    if args.build:
        PyInstaller.__main__.run(["pitd.spec"])
        resources_src = "resources"
        resources_dest = os.path.join("pitd", "resources")
        shutil.copytree(resources_src, resources_dest)
