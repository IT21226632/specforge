def approval_gate(stage_name: str):

    print("\nApprove plan? (y/n):")

    decision = input().strip().lower()

    if decision != "y":
        raise Exception(f"{stage_name} rejected")

    print(f"[OK] {stage_name} approved", flush=True)