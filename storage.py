import json
import uuid
from datetime import datetime
from pathlib import Path

STORAGE_DIR = Path("analyses")
STORAGE_DIR.mkdir(exist_ok=True)


def save_analysis(filename: str, word_count: int, agents: list, results: dict):
    record = {
        "id": str(uuid.uuid4())[:8],
        "filename": filename,
        "word_count": word_count,
        "agents": agents,
        "results": results,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    path = STORAGE_DIR / f"{record['id']}.json"
    with open(path, "w") as f:
        json.dump(record, f, indent=2)
    return record


def load_all_analyses() -> list:
    records = []
    for path in sorted(STORAGE_DIR.glob("*.json")):
        try:
            with open(path) as f:
                records.append(json.load(f))
        except Exception:
            pass
    return records


def clear_all_analyses():
    for path in STORAGE_DIR.glob("*.json"):
        path.unlink()
