import json
from pathlib import Path
from datetime import datetime


RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")

RUN_DIR = Path(f"audit_runs/{RUN_ID}")
RUN_DIR.mkdir(parents=True, exist_ok=True)


def save_artifact(filename: str, data):

    file_path = RUN_DIR / filename

    with open(file_path, "w", encoding="utf-8") as file:

        if isinstance(data, (dict, list)):
            json.dump(data, file, indent=2)

        else:
            file.write(str(data))

    print(f"[AUDIT] Saved: {file_path}")