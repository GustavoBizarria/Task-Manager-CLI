# Task Manager CLI

A simple command-line task manager built with Python and SQLite.

## Features

- Add, list, update, and delete tasks
- Mark tasks as done
- Filter tasks by status
- Export tasks to CSV or JSON

## Project Structure

```
Task-Manager-CLI/
├── task_manager/
│   ├── __init__.py
│   ├── db.py         # Database connection and table setup
│   ├── tasks.py       # CRUD operations for tasks
│   └── export.py      # Export tasks to CSV/JSON
├── main.py            # CLI entry point
└── README.md
```

## Requirements

- Python 3.10+
- No external dependencies — uses only the Python standard library (`sqlite3`, `csv`, `json`, `argparse`)

## Installation

```bash
git clone https://github.com/GustavoBizarria/Task-Manager-CLI.git
cd Task-Manager-CLI
```

No virtual environment or `pip install` is needed.

## Usage

The database file (`tasks.db`) is created automatically the first time you run the CLI.

```bash
# Add a task
python main.py add "Study SQL" -d "Review joins" -p high --due 2026-07-25
 
# List all tasks
python main.py list
 
# List only pending tasks
python main.py list --status pending
 
# Update a task
python main.py update 1 -t "New title" -p low --due 2026-08-01
 
# Remove a task's due date
python main.py update 1 --due ""
 
# Mark a task as done
python main.py done 1
 
# Delete a task
python main.py delete 1
 
# Export tasks
python main.py export --format csv --output tasks.csv
python main.py export --format json --output tasks.json
```

## Task Status

- `pending`
- `in_progress`
- `done`

## Task Priority

- `low`
- `medium`
- `high`
 
## Due Dates
 
- Format: `YYYY-MM-DD` (e.g. `2026-07-25`)
- Optional — tasks without a due date show `-` in the list
- Tasks past their due date that aren't marked `done` are highlighted in red with a ⚠ warning
- Pass an empty string (`--due ""`) to `update` to clear a task's due date

## Language (New Feature)
 
- Supported: `pt` (Portuguese, default) and `en` (English)
- Switch anytime with `--lang`: `python main.py --lang en list`
- Your choice is saved to `config.json` and becomes the default for future runs — no need to repeat the flag every time

## Changelog

### v0.1.0
- Initial release: add, list, update, delete, and export tasks (CSV/JSON)

### v0.2.0
- Added due dates for tasks (`--due` flag on `add` and `update`)
- Overdue tasks are now highlighted in the terminal
- Colored, table-based CLI output using `rich`
- Automatic database migration for existing `tasks.db` files created before this version

### v0.3.0
- Added `--lang` flag for switching the CLI language (English/Portuguese), with the preference saved to `config.json`

## License

This project is open source and available under the MIT License.
