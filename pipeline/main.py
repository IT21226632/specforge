import typer
from pipeline.stages.intake import load_spec
from pipeline.stages.planner import generate_plan
from pipeline.stages.approval import approval_gate
from pipeline.audit.logger import save_artifact
from pipeline.stages.codegen import generate_code
from pipeline.stages.testgen import generate_tests
from pipeline.stages.quality import run_quality_checks
from pipeline.stages.dependency_manager import install_dependencies
from pipeline.stages.package_initializer import initialize_packages
from pathlib import Path


def main(spec_path: str) -> None:

    spec = load_spec(spec_path)

    print("\n[OK] Spec validation passed")
    save_artifact("spec.txt", str(spec))

    print("\n===== FEATURE SPEC =====")
    print(f"Feature: {spec.feature['name']}")
    print(f"Objective: {spec.feature['objective']}")

    print("\nAcceptance Criteria:")
    for item in spec.acceptance_criteria:
        print(f" - {item}")

    print("\n[INFO] Generating implementation plan...")

    plan = generate_plan(str(spec))

    print("\n[OK] Plan generated")
    print(plan)

    save_artifact("plan.json", plan)

    # ── APPROVAL GATE ─────────────────────────────────────────────
    approval_gate("implementation_plan")

    save_artifact("approval.txt", "Implementation plan approved")

    print("\n[INFO] Generating implementation code...")

    generated_file = generate_code(plan)

    print(f"\n[OK] Code generated: {generated_file}")

    save_artifact("generated_file.txt", str(generated_file))

    generated_code = Path(generated_file).read_text()

    save_artifact("generated_code.py", generated_code)

    install_dependencies(generated_file)
    initialize_packages()

    print("\n[INFO] Generating tests...")

    test_file = generate_tests(generated_code)

    print(f"\n[OK] Tests generated: {test_file}")

    save_artifact("generated_tests.py", Path(test_file).read_text())

    print("\n[INFO] Running quality checks...")

    run_quality_checks()

    save_artifact("quality_status.txt", "All quality checks passed")


if __name__ == "__main__":
    typer.run(main)