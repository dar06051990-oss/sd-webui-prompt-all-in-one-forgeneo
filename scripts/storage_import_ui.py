import gradio as gr

from modules import script_callbacks
from scripts.physton_prompt.storage import Storage


def _format_result(result, overwrite):
    sources = result.get("sources_found", [])
    imported = result.get("imported", [])
    overwritten = result.get("overwritten", [])
    skipped = result.get("skipped", [])

    if not sources:
        return (
            "Старое расширение не найдено рядом с новой версией.\n\n"
            "Ожидаемые папки:\n"
            "- sd-webui-prompt-all-in-one/storage\n"
            "- sd-webui-prompt-all-in-one-forgeneo/storage"
        )

    lines = ["Импорт завершён."]

    if imported:
        lines.append(f"Новых файлов импортировано: {len(imported)}")
    if overwrite and overwritten:
        lines.append(f"Файлов перезаписано: {len(overwritten)}")
    if skipped and not overwrite:
        lines.append(f"Существующих файлов оставлено без изменений: {len(skipped)}")

    if not imported and not overwritten:
        lines.append("Нечего переносить: нужные JSON уже есть в текущем storage.")

    return "\n".join(lines)


def _run_import(overwrite):
    try:
        result = Storage.import_from_old(overwrite=bool(overwrite))
        return _format_result(result, bool(overwrite))
    except Exception as e:
        return f"Ошибка импорта: {e}"


def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui:
        gr.Markdown(
            "## Prompt All-in-One — перенос данных\n"
            "Переносит историю, избранное и настройки из старой версии расширения."
        )

        overwrite = gr.Checkbox(
            label="Перезаписать существующие данные",
            value=False,
            info="Оставь выключенным для безопасного импорта только недостающих файлов."
        )

        import_button = gr.Button("Import from old extension", variant="primary")
        result = gr.Textbox(label="Результат", lines=6, interactive=False)

        import_button.click(
            fn=_run_import,
            inputs=[overwrite],
            outputs=[result],
            show_progress=False,
        )

    return [(ui, "Prompt AIO Import", "prompt_aio_import")]


script_callbacks.on_ui_tabs(on_ui_tabs)
