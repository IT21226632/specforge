import typer
from pipeline.stages.intake import load_spec
from pipeline.stages.planner import generate_plan
from pipeline.stages.approval import approval_gate
from pipeline.audit.logger import save_artifact


def main(spec_path: str) -> None:
    """Run the SpecForge pipeline on a specification file."""
    spec = load_spec(spec_path)

    print("\n[✓] Spec validation passed")
    save_artifact("spec.txt", str(spec))
    
    print("\n===== FEATURE SPEC =====")
    print(f"Feature: {spec.feature['name']}")
    print(f"Objective: {spec.feature['objective']}")

    print("\nAcceptance Criteria:")
    for item in spec.acceptance_criteria:
        print(f" - {item}")

    print("\n[INFO] Generating implementation plan...")

    plan = generate_plan(str(spec))

    print("\n[✓] Plan generated")
    print(plan)
    save_artifact("plan.json", plan)

    approval_gate("Implementation Plan")
    save_artifact(
    "approval.txt",
    "Implementation plan approved"
)


if __name__ == "__main__":
    typer.run(main)