from datetime import date, datetime
from typing import Optional
from task_manager.db import get_connection

VALID_STATUSES = ("pending", "in_progress", "done")
VALID_PRIORITIES = ("low", "medium", "high")
DATE_FORMAT = "%Y-%m-%d"


def _validate_due_date(due_date: Optional[str]) -> Optional[str]:
    if due_date is None or due_date == "":
        return None
    try:
        datetime.strptime(due_date, DATE_FORMAT)
    except ValueError:
        raise ValueError(f"Invalid date: '{due_date}'. Use the format YYYY-MM-DD.")
    return due_date

def is_overdue(task: dict) -> bool:
    if not task.get("due_date") or task["status"] == "done":
        return False
    return datetime.strptime(task["due_date"], DATE_FORMAT).date() < date.today()


def add_task(
    title: str,
    description: str = "",
    priority: str = "medium",
    due_date: Optional[str] = None,
) -> int:
    """Adiciona uma nova tarefa e retorna o id gerado."""
    if priority not in VALID_PRIORITIES:
        raise ValueError(f"Prioridade inválida: {priority}")
    due_date = _validate_due_date(due_date)
 
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, priority, due_date) VALUES (?, ?, ?, ?)",
        (title, description, priority, due_date),
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id
 


def list_tasks(status: Optional[str] = None) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    if status:
        cursor.execute("SELECT * FROM tasks WHERE status = ? ORDER BY id", (status,))
    else:
        cursor.execute("SELECT * FROM tasks ORDER BY id")

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_task(task_id: int) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
) -> Optional[dict]:
    task = get_task(task_id)
    if task is None:
        return None

    new_title = title if title is not None else task["title"]
    new_description = description if description is not None else task["description"]
    new_priority = priority if priority is not None else task["priority"]

    if new_priority not in VALID_PRIORITIES:
        raise ValueError(f"Invalid Priority: {new_priority}")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET title = ?, description = ?, priority = ? WHERE id = ?",
        (new_title, new_description, new_priority, task_id),
    )
    conn.commit()
    conn.close()
    return get_task(task_id)


def set_status(task_id: int, status: str) -> Optional[dict]:
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid Priority: {status}")

    task = get_task(task_id)
    if task is None:
        return None

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()
    return get_task(task_id)


def delete_task(task_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted