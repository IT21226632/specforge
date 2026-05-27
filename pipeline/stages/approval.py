def approval_gate(stage_name: str):

    print("\n[WARNING] Some quality checks failed (non-critical):")

    decision = input().strip().lower()

    if decision != "y":
        raise Exception(f"{stage_name} rejected")

    print(f"[OK] {stage_name} approved", flush=True)