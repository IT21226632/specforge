import sys


def approval_gate(stage_name: str):

    print(f"\nApprove {stage_name}? (y/n):", flush=True)

    decision = input().strip().lower()

    if decision != "y":
        raise Exception(f"{stage_name} rejected")

    print(f"[OK] {stage_name} approved", flush=True)