import argparse
import sys

from rich.console import Console
from rich.table import Table

from task_manager.db import init_db
from task_manager import tasks
from task_manager import export

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
    task_id = tasks.add_task(args.title, args.description or "", args.priority)
    console.print(f"[green]✔[/green] Tarefa criada com sucesso (id=[bold]{task_id}[/bold]).")


def cmd_list(args):
    task_list = tasks.list_tasks(status=args.status)
    if not task_list:
        console.print("[yellow]Nenhuma tarefa encontrada.[/yellow]")
        return

    table = Table(title="Tarefas", show_lines=False, header_style="bold magenta")
    table.add_column("ID", justify="right", style="bold")
    table.add_column("Título")
    table.add_column("Descrição")
    table.add_column("Status", justify="center")
    table.add_column("Prioridade", justify="center")

    for task in task_list:
        status_style = STATUS_STYLES.get(task["status"], "white")
        priority_style = PRIORITY_STYLES.get(task["priority"], "white")
        table.add_row(
            str(task["id"]),
            task["title"],
            task["description"] or "-",
            f"[{status_style}]{task['status']}[/{status_style}]",
            f"[{priority_style}]{task['priority']}[/{priority_style}]",
        )

    console.print(table)

def cmd_update(args):
    updated = tasks.update_task(
        args.id,
        title=args.title,
        description=args.description,
        priority=args.priority,
    )
    if updated is None:
        console.print(f"[red]✘ Tarefa {args.id} não encontrada.[/red]")
        sys.exit(1)
    console.print(f"[green]✔[/green] Tarefa {args.id} atualizada com sucesso.")


def cmd_done(args):
    updated = tasks.set_status(args.id, "done")
    if updated is None:
        console.print(f"[red]✘ Tarefa {args.id} não encontrada.[/red]")
        sys.exit(1)
    console.print(f"[green]✔[/green] Tarefa {args.id} marcada como [bold green]concluída[/bold green].")


def cmd_delete(args):
    deleted = tasks.delete_task(args.id)
    if not deleted:
        console.print(f"[red]✘ Tarefa {args.id} não encontrada.[/red]")
        sys.exit(1)
    console.print(f"[green]✔[/green] Tarefa {args.id} removida com sucesso.")


def cmd_export(args):
    if args.format == "csv":
        path = export.export_to_csv(args.output)
    else:
        path = export.export_to_json(args.output)
    console.print(f"[green]✔[/green] Tarefas exportadas para [bold]{path}[/bold]")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)


    p_add = subparsers.add_parser("add", help="Adiciona uma nova tarefa")
    p_add.add_argument("title", help="Título da tarefa")
    p_add.add_argument("-d", "--description", help="Descrição da tarefa")
    p_add.add_argument(
        "-p", "--priority", choices=["low", "medium", "high"], default="medium"
    )
    p_add.set_defaults(func=cmd_add)

    p_list = subparsers.add_parser("list", help="Lista as tarefas")
    p_list.add_argument(
        "--status", choices=["pending", "in_progress", "done"], default=None
    )
    p_list.set_defaults(func=cmd_list)


    p_update = subparsers.add_parser("update", help="Atualiza uma tarefa existente")
    p_update.add_argument("id", type=int, help="ID da tarefa")
    p_update.add_argument("-t", "--title", help="Novo título")
    p_update.add_argument("-d", "--description", help="Nova descrição")
    p_update.add_argument("-p", "--priority", choices=["low", "medium", "high"])
    p_update.set_defaults(func=cmd_update)

    p_done = subparsers.add_parser("done", help="Marca uma tarefa como concluída")
    p_done.add_argument("id", type=int, help="ID da tarefa")
    p_done.set_defaults(func=cmd_done)

    p_delete = subparsers.add_parser("delete", help="Remove uma tarefa")
    p_delete.add_argument("id", type=int, help="ID da tarefa")
    p_delete.set_defaults(func=cmd_delete)

    # export
    p_export = subparsers.add_parser("export", help="Exporta as tarefas")
    p_export.add_argument("--format", choices=["csv", "json"], default="csv")
    p_export.add_argument("--output", required=True, help="Caminho do arquivo de saída")
    p_export.set_defaults(func=cmd_export)

    return parser


def main():
    init_db()
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except ValueError as error:
        console.print(f"[red]✘ Erro: {error}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()