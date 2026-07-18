import json
from pathlib import Path
 
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"
DEFAULT_LANGUAGE = "pt"
SUPPORTED_LANGUAGES = ("pt", "en")
 
TRANSLATIONS = {
    "pt": {
        "task_created": "✔ Tarefa criada com sucesso (id={id}).",
        "no_tasks_found": "Nenhuma tarefa encontrada.",
        "task_not_found": "✘ Tarefa {id} não encontrada.",
        "task_updated": "✔ Tarefa {id} atualizada com sucesso.",
        "task_done": "✔ Tarefa {id} marcada como concluída.",
        "task_deleted": "✔ Tarefa {id} removida com sucesso.",
        "tasks_exported": "✔ Tarefas exportadas para {path}",
        "error_prefix": "✘ Erro: {message}",
        "lang_set": "Idioma definido como: {lang}",
        "table_title": "Tarefas",
        "col_id": "ID",
        "col_title": "Título",
        "col_description": "Descrição",
        "col_status": "Status",
        "col_priority": "Prioridade",
        "col_due": "Vencimento",
        "cli_description": "Task Manager CLI",
        "help_lang": "Idioma da interface (pt ou en)",
        "help_add": "Adiciona uma nova tarefa",
        "help_title_arg": "Título da tarefa",
        "help_description_arg": "Descrição da tarefa",
        "help_priority_arg": "Prioridade da tarefa",
        "help_due_arg": "Data de vencimento (formato YYYY-MM-DD)",
        "help_list": "Lista as tarefas",
        "help_status_arg": "Filtra por status",
        "help_update": "Atualiza uma tarefa existente",
        "help_id_arg": "ID da tarefa",
        "help_new_title": "Novo título",
        "help_new_description": "Nova descrição",
        "help_due_update_arg": "Nova data de vencimento (YYYY-MM-DD, ou '' para remover)",
        "help_done": "Marca uma tarefa como concluída",
        "help_delete": "Remove uma tarefa",
        "help_export": "Exporta as tarefas",
        "help_format_arg": "Formato de exportação",
        "help_output_arg": "Caminho do arquivo de saída",
    },
    "en": {
        "task_created": "✔ Task successfully created (id={id}).",
        "no_tasks_found": "No tasks found.",
        "task_not_found": "✘ Task {id} not found.",
        "task_updated": "✔ Task {id} successfully updated.",
        "task_done": "✔ Task {id} marked as complete.",
        "task_deleted": "✔ Task {id} successfully removed.",
        "tasks_exported": "✔ Tasks exported to {path}",
        "error_prefix": "✘ Error: {message}",
        "lang_set": "Language set to: {lang}",
        "table_title": "Tasks",
        "col_id": "ID",
        "col_title": "Title",
        "col_description": "Description",
        "col_status": "Status",
        "col_priority": "Priority",
        "col_due": "Due Date",
        "cli_description": "Task Manager CLI",
        "help_lang": "Interface language (pt or en)",
        "help_add": "Adds a new task",
        "help_title_arg": "Task title",
        "help_description_arg": "Task description",
        "help_priority_arg": "Task priority",
        "help_due_arg": "Due date (format YYYY-MM-DD)",
        "help_list": "Lists the tasks",
        "help_status_arg": "Filter by status",
        "help_update": "Updates an existing task",
        "help_id_arg": "Task id",
        "help_new_title": "New title",
        "help_new_description": "New description",
        "help_due_update_arg": "New due date (YYYY-MM-DD, or '' to clear)",
        "help_done": "Marks a task as done",
        "help_delete": "Removes a task",
        "help_export": "Exports the tasks",
        "help_format_arg": "Export format",
        "help_output_arg": "Output file path",
    },
}

def load_language() -> str:
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            lang = data.get("language")
            if lang in SUPPORTED_LANGUAGES:
                return lang
        except (json.JSONDecodeError, OSError):
            pass
    return DEFAULT_LANGUAGE
 
 
def save_language(lang: str) -> None:
    CONFIG_PATH.write_text(json.dumps({"language": lang}, indent=2), encoding="utf-8")
 
 
def t(key: str, _lang: str, **kwargs) -> str:
    template = TRANSLATIONS.get(_lang, TRANSLATIONS[DEFAULT_LANGUAGE]).get(key, key)
    return template.format(**kwargs)
 