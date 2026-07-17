import csv
import json
from pathlib import Path
from task_manager.tasks import list_tasks


def export_to_csv(filepath: str) -> str:
    tasks = list_tasks()
    path = Path(filepath)

    with open(path, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "title", "description", "status", "priority", "created_at"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for task in tasks:
            writer.writerow(task)

    return str(path)


def export_to_json(filepath: str) -> str:
    tasks = list_tasks()
    path = Path(filepath)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

    return str(path)