import argparse
import sys
 
from rich.console import Console
from rich.table import Table

from task_manager.db import init_db
from task_manager import tasks
from task_manager import export
from task_manager import i18n
 
console = Console()
 
STATUS_STYLES = {
    "pending": "yellow",
    "in_progress": "cyan",
    "done": "green",
}
PRIORITY_STYLES = {
    "low": "dim",
    "medium": "white",
    "high": "bold red",
}
 
def cmd_add(args):
    task_id = tasks.add_task(args.title, args.description or "", args.priority, args.due)
    console.print(i18n.t("task_created", args.lang, id=task_id))
 
 
def cmd_list(args):
    task_list = tasks.list_tasks(status=args.status)
    if not task_list:
        console.print("[yellow]Nenhuma tarefa encontrada.[/yellow]")
        return
 
    table = Table(title=i18n.t("table_title", args.lang), show_lines=False, header_style="bold magenta")
    table.add_column(i18n.t("col_id", args.lang), justify="right", style="bold")
    table.add_column(i18n.t("col_title", args.lang))
    table.add_column(i18n.t("col_description", args.lang))
    table.add_column(i18n.t("col_status", args.lang), justify="center")
    table.add_column(i18n.t("col_priority", args.lang), justify="center")
    table.add_column(i18n.t("col_due", args.lang), justify="center")
 
    for task in task_list:
        status_style = STATUS_STYLES.get(task["status"], "white")
        priority_style = PRIORITY_STYLES.get(task["priority"], "white")
 
        due_display = task["due_date"] or "-"
        if tasks.is_overdue(task):
            due_display = f"[bold red]{due_display} ⚠[/bold red]"
 
        table.add_row(
            str(task["id"]),
            task["title"],
            task["description"] or "-",
            f"[{status_style}]{task['status']}[/{status_style}]",
            f"[{priority_style}]{task['priority']}[/{priority_style}]",
            due_display,
        )
 
    console.print(table)
 
 
def cmd_update(args):
    updated = tasks.update_task(
        args.id,
        title=args.title,
        description=args.description,
        priority=args.priority,
        due_date=args.due,
    )
    if updated is None:
        console.print(f"[red]{i18n.t('task_not_found', args.lang, id=args.id)}[/red]")
        sys.exit(1)
    console.print(i18n.t("task_updated", args.lang, id=args.id))
 
 
def cmd_done(args):
    updated = tasks.set_status(args.id, "done")
    if updated is None:
        console.print(f"[red]{i18n.t('task_not_found', args.lang, id=args.id)}[/red]")
        sys.exit(1)
    console.print(i18n.t("task_done", args.lang, id=args.id))
 
 
def cmd_delete(args):
    deleted = tasks.delete_task(args.id)
    if not deleted:
        console.print(f"[red]{i18n.t('task_not_found', args.lang, id=args.id)}[/red]")
        sys.exit(1)
    console.print(i18n.t("task_deleted", args.lang, id=args.id))
 
 
def cmd_export(args):
    if args.format == "csv":
        path = export.export_to_csv(args.output)
    else:
        path = export.export_to_json(args.output)
    console.print(i18n.t("tasks_exported", args.lang, path=path))
 
 
def build_parser(lang: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=i18n.t("cli_description", lang))
    parser.add_argument(
        "--lang",
        choices=i18n.SUPPORTED_LANGUAGES,
        default=lang,
        help=i18n.t("help_lang", lang),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
 
# add
    p_add = subparsers.add_parser("add", help=i18n.t("help_add", lang))
    p_add.add_argument("title", help=i18n.t("help_title_arg", lang))
    p_add.add_argument("-d", "--description", help=i18n.t("help_description_arg", lang))
    p_add.add_argument(
        "-p", "--priority", choices=["low", "medium", "high"], default="medium",
        help=i18n.t("help_priority_arg", lang),
    )
    p_add.add_argument("--due", help=i18n.t("help_due_arg", lang))
    p_add.set_defaults(func=cmd_add)
 
    # list
    p_list = subparsers.add_parser("list", help=i18n.t("help_list", lang))
    p_list.add_argument(
        "--status", choices=["pending", "in_progress", "done"], default=None,
        help=i18n.t("help_status_arg", lang),
    )
    p_list.set_defaults(func=cmd_list)
 
    # update
    p_update = subparsers.add_parser("update", help=i18n.t("help_update", lang))
    p_update.add_argument("id", type=int, help=i18n.t("help_id_arg", lang))
    p_update.add_argument("-t", "--title", help=i18n.t("help_new_title", lang))
    p_update.add_argument("-d", "--description", help=i18n.t("help_new_description", lang))
    p_update.add_argument("-p", "--priority", choices=["low", "medium", "high"])
    p_update.add_argument("--due", help=i18n.t("help_due_update_arg", lang))
    p_update.set_defaults(func=cmd_update)
 
    # done
    p_done = subparsers.add_parser("done", help=i18n.t("help_done", lang))
    p_done.add_argument("id", type=int, help=i18n.t("help_id_arg", lang))
    p_done.set_defaults(func=cmd_done)
 
    # delete
    p_delete = subparsers.add_parser("delete", help=i18n.t("help_delete", lang))
    p_delete.add_argument("id", type=int, help=i18n.t("help_id_arg", lang))
    p_delete.set_defaults(func=cmd_delete)
 
    # export
    p_export = subparsers.add_parser("export", help=i18n.t("help_export", lang))
    p_export.add_argument("--format", choices=["csv", "json"], default="csv", help=i18n.t("help_format_arg", lang))
    p_export.add_argument("--output", required=True, help=i18n.t("help_output_arg", lang))
    p_export.set_defaults(func=cmd_export)
 
    return parser

 
def main():
    init_db()
    saved_lang = i18n.load_language()
    parser = build_parser(saved_lang)
    args = parser.parse_args()

    if args.lang != saved_lang:
        i18n.save_language(args.lang)
        console.print(i18n.t("lang_set", args.lang, lang=args.lang))

    try:
        args.func(args)
    except ValueError as error:
        console.print(f"[red]{i18n.t('error_prefix', args.lang, message=error)}[/red]")
        sys.exit(1)
 
 
if __name__ == "__main__":
    main()