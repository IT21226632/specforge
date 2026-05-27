from pathlib import Path


def initialize_packages():

    package_files = [
        Path("sandbox/__init__.py"),
        Path("sandbox/generated/__init__.py"),
        Path("sandbox/generated/tests/__init__.py"),
    ]

    for file_path in package_files:

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path.touch(exist_ok=True)

    print("[OK] Package structure initialized")