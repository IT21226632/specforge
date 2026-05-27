import subprocess
import shutil


def run_quality_checks():
    """Run quality assurance checks on generated code"""
    
    commands = [
        (["ruff", "check", "--fix", "sandbox/generated"], True),
        (["mypy","--explicit-package-bases","--ignore-missing-imports", "sandbox/generated"], False),
        (["pytest", "sandbox/generated/tests"], False),
        (["bandit","-r","sandbox/generated","-x","sandbox/generated/tests"], False),
    ]

    failed_checks = []

    for command, required in commands:
        tool_name = command[0]
        
        # Check if tool is installed
        if not shutil.which(tool_name):
            print(f"\n[WARNING] {tool_name} not found, skipping...")
            if required:
                raise Exception(f"Required tool '{tool_name}' is not installed")
            continue

        print(f"\n[QUALITY] Running: {' '.join(command)}")

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        print(result.stdout)

        if result.returncode != 0:
            print(result.stderr)
            if required:
                raise Exception(
                    f"Quality check failed: {' '.join(command)}"
                )
            else:
                failed_checks.append(command)

    if failed_checks:
        print(f"\n[WARNING] Some quality checks failed (non-critical):")
        for cmd in failed_checks:
            print(f"  - {' '.join(cmd)}")

    if failed_checks:
    print("\n[WARNING] Some quality checks failed:")
    for fail in failed_checks:
        print(f" - {fail}")
else:
    print("\n[✓] All quality checks passed")