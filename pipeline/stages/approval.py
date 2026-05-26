def approval_gate(stage_name: str):

    approval = input(f"\nApprove {stage_name}? (y/n): ")

    if approval.lower() != "y":
        raise Exception(f"{stage_name} rejected by user.")

    print(f"[✓] {stage_name} approved")