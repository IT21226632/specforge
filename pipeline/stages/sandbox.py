from pathlib import Path


ALLOWED_ROOT = Path("sandbox/generated").resolve()


def validate_safe_path(target_path: Path):

    resolved = target_path.resolve()

    if not str(resolved).startswith(str(ALLOWED_ROOT)):
        raise PermissionError(
            f"Unsafe write blocked: {resolved}"
        )

    return resolved