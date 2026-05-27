import re
import subprocess
import sys
from pathlib import Path


# Map import root → pip package name (including extras where needed)
PACKAGE_ALIASES = {
    # auth / crypto
    "jwt":          "pyjwt",
    "jose":         "python-jose[cryptography]",
    "passlib":      "passlib[bcrypt]",
    "bcrypt":       "bcrypt",
    "cryptography": "cryptography",

    # web
    "fastapi":      "fastapi",
    "starlette":    "starlette",
    "uvicorn":      "uvicorn[standard]",
    "httpx":        "httpx",
    "requests":     "requests",
    "aiohttp":      "aiohttp",

    # pydantic — always install with email extra
    "pydantic":     "pydantic[email]",

    # database
    "sqlalchemy":   "sqlalchemy",
    "alembic":      "alembic",
    "databases":    "databases",
    "pymongo":      "pymongo",
    "redis":        "redis",

    # data
    "pandas":       "pandas",
    "numpy":        "numpy",

    # testing (shouldn't appear in generated code, but just in case)
    "pytest":       "pytest",
    "hypothesis":   "hypothesis",

    # utilities
    "dotenv":       "python-dotenv",
    "yaml":         "pyyaml",
    "toml":         "toml",
    "click":        "click",
    "typer":        "typer",
    "rich":         "rich",
    "pydash":       "pydash",
    "arrow":        "arrow",
}


# Complete Python standard library roots — nothing here should go to pip
STANDARD_LIBS = {
    # builtins / core
    "abc", "ast", "asyncio", "builtins", "cgi", "cmd",
    "code", "codecs", "codeop", "collections", "colorsys",
    "compileall", "concurrent", "contextlib", "contextvars",
    "copy", "copyreg", "csv", "ctypes",

    # data formats
    "dataclasses", "datetime", "decimal", "difflib",

    # email / net (stdlib)
    "email", "encodings", "enum",

    # file system
    "filecmp", "fnmatch", "fractions", "ftplib", "functools",

    # generics / typing
    "gc", "getopt", "getpass", "gettext", "glob",
    "gzip", "hashlib", "heapq", "hmac", "html",
    "http", "idlelib", "imaplib", "importlib",
    "inspect", "io", "ipaddress", "itertools",

    # json / logging
    "json", "keyword", "linecache", "locale", "logging",

    # math
    "math", "mimetypes", "multiprocessing",

    # os / path
    "operator", "os", "pathlib", "pickle", "pkgutil",
    "platform", "pprint", "profile", "pstats",

    # queue / re
    "queue", "quopri", "random", "re",

    # signal / socket
    "select", "shelve", "shlex", "shutil", "signal",
    "site", "smtplib", "socket", "socketserver", "sqlite3",
    "ssl", "stat", "statistics", "string", "stringprep",
    "struct", "subprocess", "sys", "sysconfig",

    # tempfile / threading
    "tarfile", "tempfile", "textwrap", "threading",
    "time", "timeit", "tkinter", "token", "tokenize",
    "tomllib", "traceback", "tracemalloc", "types", "typing",

    # unittest / urllib
    "unicodedata", "unittest", "urllib", "uuid",

    # warnings / xml
    "warnings", "weakref", "webbrowser",
    "xml", "xmlrpc", "zipfile", "zipimport", "zlib",
    "zoneinfo", "_thread",
}


def extract_imports(code_file: Path) -> set[str]:
    """Extract all unique top-level import roots from a Python file."""
    content = code_file.read_text(encoding="utf-8")

    # Matches both:  import X   and   from X import Y
    raw_imports = re.findall(
        r"^(?:from|import)\s+([a-zA-Z0-9_]+)",
        content,
        re.MULTILINE,
    )

    packages = set()
    for root in raw_imports:
        if root in STANDARD_LIBS:
            continue
        # Resolve alias (e.g. pydantic → pydantic[email])
        resolved = PACKAGE_ALIASES.get(root, root)
        packages.add(resolved)

    return packages


def install_dependencies(code_file: Path) -> set[str]:
    """
    Parse imports from generated file, resolve aliases,
    install missing packages, and return the set installed.
    """
    packages = extract_imports(code_file)

    if not packages:
        print("[INFO] No external dependencies detected")
        return set()

    print(f"\n[INFO] Installing dependencies: {packages}")

    subprocess.run(
        [sys.executable, "-m", "pip", "install", *packages],
        check=True,
    )

    print("[OK] Dependencies installed")
    return packages


def validate_imports(code_file: Path) -> tuple[bool, str]:
    """
    Try importing the generated module in a subprocess.
    Returns (success, error_message).
    Catches missing deps that slipped through alias resolution.
    """
    result = subprocess.run(
        [
            sys.executable, "-c",
            (
                "import importlib.util, sys; "
                f"spec = importlib.util.spec_from_file_location('_mod', r'{code_file}'); "
                "mod = importlib.util.module_from_spec(spec); "
                "spec.loader.exec_module(mod)"
            ),
        ],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0, result.stderr


def install_with_validation(code_file: Path, max_retries: int = 3) -> bool:
    """
    Install deps, then validate imports.
    If import fails due to a missing module, install it and retry.
    Returns True if the module imports cleanly.
    """
    install_dependencies(code_file)

    for attempt in range(max_retries):
        ok, stderr = validate_imports(code_file)

        if ok:
            print("[OK] Import validation passed")
            return True
            return True

        # Try to extract the missing module name from the error
        match = re.search(r"No module named '([^']+)'", stderr)
        if not match:
            print(f"[FAIL] Import validation failed (non-recoverable):\n{stderr}")
            return False

        missing_root = match.group(1).split(".")[0]
        resolved = PACKAGE_ALIASES.get(missing_root, missing_root)

        print(f"[INFO] Auto-fixing missing dep (attempt {attempt + 1}): {resolved}")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", resolved],
            check=True,
        )

    print("[FAIL] Import validation failed after max retries")
    return False