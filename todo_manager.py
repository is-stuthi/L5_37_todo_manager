"""A small to-do list and task manager demo."""
import json
import random
import subprocess
from datetime import datetime

tasks = {}
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def add_task(title, priority="medium", labels=None):
    """Add a task and return its id (fresh labels list per call)."""
    task_id=len(tasks) + 1
    labels = [] if labels is None else list(labels)
    labels.append(priority)
    tasks[task_id] = {"title": title, "priority": priority, "labels": labels,
                      "done": False, "created": datetime.now().isoformat()}
    return task_id


def complete_task(task_id):
    """Mark a task as done. Return True if it exists, otherwise False."""
    if task_id in tasks:
        tasks[task_id]["done"] = True
        return True
    print("No task with id", task_id)
    return False


def pending_tasks():
    """Return titles of unfinished tasks, highest priority first."""
    pending = [task for task in tasks.values() if not task["done"]]
    pending.sort(key=lambda task: PRIORITY_ORDER[task["priority"]])
    return [task["title"] for task in pending]


def find_task(keyword):
    """Return the id of the first task matching keyword, or None."""
    for task_id, task in tasks.items():
        if keyword.lower() in task["title"].lower():
            return task_id
    return None



def save_tasks(file_name="tasks_saved.json"):
    """Save tasks to a JSON file (JSON replaces pickle, which is unsafe)."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)


def load_tasks(file_name="tasks_saved.json"):
    """Load tasks from a JSON file."""
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)


def export_json(file_name="tasks.json"):
    """Export tasks to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)


def remind_by_email(address):
    """Mail the exported tasks to address (not called by the demo)."""
    if not address or address.startswith("-") or any(c.isspace() for c in address):
        raise ValueError("Invalid email address")
    with open("tasks.json", "rb") as file:
        subprocess.run(["mail", "-s", "Pending tasks", address],
                       stdin=file, check=True)


def main():
    """Run a short demonstration."""
    add_task("Submit lab report", "high")
    add_task("Buy groceries")
    add_task("Call plumber", "low")
    add_task("Book train tickets", "high")
    complete_task(2)
    complete_task(99)
    print("Pending tasks:", pending_tasks())
    print("Task id for 'plumber':", find_task("plumber"))
    print("Task id for 'gym':", find_task("gym")) # None: no match
    pending = pending_tasks()
    if pending:
        # Not security-sensitive: only picks a suggestion.
        suggestion = random.choice(pending)  # nosec B311
        print("Try this next:", suggestion)
    save_tasks()
    restored = load_tasks()
    print("Tasks restored from file:",len(restored))
    export_json()
    print("Exported tasks to tasks.json")


if __name__ == "__main__":
    main()
