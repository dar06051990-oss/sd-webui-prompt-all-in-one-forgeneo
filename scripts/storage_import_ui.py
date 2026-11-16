"""Prompt All-in-One portable data tools in Forge Neo Settings.

The former separate "Prompt AIO Import" tab is intentionally not registered.
"""
import base64
import subprocess
import sys

import gradio as gr
from modules import script_callbacks, shared
from scripts.physton_prompt import portable


def _export():
    try:
        return portable.create_backup()
    except Exception as exc:
        return None, f'Ошибка создания копии: {exc}'


def _import_zip(blob):
    try:
        return portable.import_backup(blob)
    except Exception as exc:
        return f'Ошибка импорта ZIP: {exc}'


def _merge_zip(blob):
    try:
        return portable.import_backup(blob, merge=True)
    except Exception as exc:
        return f'Ошибка объединения из ZIP: {exc}'


def _merge_path(path):
    try:
        return portable.import_folder(path, merge=True)
    except Exception as exc:
        return f'Ошибка объединения из папки: {exc}'


def _import_path(path):
    try:
        return portable.import_folder(path)
    except Exception as exc:
        return f'Ошибка импорта из папки: {exc}'


def _choose_storage_folder():
    """Open the *local Forge host* Windows folder picker.

    A browser upload control does not expose a real absolute folder path, but
    a locally installed Forge process may invoke Windows' native dialog.
    The Windows Shell IFileOpenDialog is invoked from an STA PowerShell process.
    A Unicode path is transported as
    base64-encoded UTF-16LE to avoid console-codepage corruption.
    """
    if sys.platform != 'win32':
        return gr.update(), 'Выбор папки через Windows доступен только при запуске Forge в Windows. Можно ввести путь вручную.'

    ps_script = r"""
# Use the native Windows Vista+ shell dialog with FOS_PICKFOLDERS.
# FolderBrowserDialog (WinForms) falls back to the old tree-style selector
# on some Windows configurations, unlike the modern file picker for ZIPs.
$ErrorActionPreference = 'Stop'
$source = @'
using System;
using System.Runtime.InteropServices;

[ComImport]
[Guid("43826D1E-E718-42EE-BC55-A1E261C37BFE")]
[InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
internal interface IPromptAioShellItem
{
    void BindToHandler(IntPtr pbc, ref Guid bhid, ref Guid riid, out IntPtr ppv);
    void GetParent(out IPromptAioShellItem ppsi);
    void GetDisplayName(uint sigdnName, [MarshalAs(UnmanagedType.LPWStr)] out string ppszName);
    void GetAttributes(uint sfgaoMask, out uint psfgaoAttribs);
    void Compare(IPromptAioShellItem psi, uint hint, out int piOrder);
}

[ComImport]
[Guid("D57C7288-D4AD-4768-BE02-9D969532D960")]
[InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
internal interface IPromptAioFileOpenDialog
{
    [PreserveSig] int Show(IntPtr hwndOwner);
    void SetFileTypes(uint cFileTypes, IntPtr rgFilterSpec);
    void SetFileTypeIndex(uint iFileType);
    void GetFileTypeIndex(out uint piFileType);
    void Advise(IntPtr pfde, out uint pdwCookie);
    void Unadvise(uint dwCookie);
    void SetOptions(uint fos);
    void GetOptions(out uint pfos);
    void SetDefaultFolder(IPromptAioShellItem psi);
    void SetFolder(IPromptAioShellItem psi);
    void GetFolder(out IPromptAioShellItem ppsi);
    void GetCurrentSelection(out IPromptAioShellItem ppsi);
    void SetFileName([MarshalAs(UnmanagedType.LPWStr)] string pszName);
    void GetFileName([MarshalAs(UnmanagedType.LPWStr)] out string pszName);
    void SetTitle([MarshalAs(UnmanagedType.LPWStr)] string pszTitle);
    void SetOkButtonLabel([MarshalAs(UnmanagedType.LPWStr)] string pszText);
    void SetFileNameLabel([MarshalAs(UnmanagedType.LPWStr)] string pszLabel);
    void GetResult(out IPromptAioShellItem ppsi);
    void AddPlace(IPromptAioShellItem psi, int fdap);
    void SetDefaultExtension([MarshalAs(UnmanagedType.LPWStr)] string pszDefaultExtension);
    void Close(int hr);
    void SetClientGuid(ref Guid guid);
    void ClearClientData();
    void SetFilter(IntPtr pFilter);
}

public static class PromptAioModernFolderPicker
{
    // FOS_PICKFOLDERS | FOS_FORCEFILESYSTEM: select directories, not files.
    const uint FOS_PICKFOLDERS = 0x20;
    const uint FOS_FORCEFILESYSTEM = 0x40;
    const uint SIGDN_FILESYSPATH = 0x80058000;
    const int HRESULT_CANCELLED = unchecked((int)0x800704C7);

    public static string Pick()
    {
        Type dialogType = Type.GetTypeFromCLSID(
            new Guid("DC1C5A9C-E88A-4DDE-A5A1-60F82A20AEF7"), true);
        IPromptAioFileOpenDialog dialog = (IPromptAioFileOpenDialog)
            Activator.CreateInstance(dialogType);
        IPromptAioShellItem item = null;
        try
        {
            uint options;
            dialog.GetOptions(out options);
            dialog.SetOptions(options | FOS_PICKFOLDERS | FOS_FORCEFILESYSTEM);
            dialog.SetTitle("Выберите папку storage старой установки Forge");
            dialog.SetOkButtonLabel("Выбрать папку");

            int hr = dialog.Show(IntPtr.Zero);
            if (hr == HRESULT_CANCELLED) return null;
            if (hr < 0) Marshal.ThrowExceptionForHR(hr);

            dialog.GetResult(out item);
            string chosen;
            item.GetDisplayName(SIGDN_FILESYSPATH, out chosen);
            return chosen;
        }
        finally
        {
            if (item != null) Marshal.FinalReleaseComObject(item);
            if (dialog != null) Marshal.FinalReleaseComObject(dialog);
        }
    }
}
'@
try {
    Add-Type -TypeDefinition $source -ErrorAction Stop
    $chosen = [PromptAioModernFolderPicker]::Pick()
    if ($chosen) {
        [Console]::Out.WriteLine([Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($chosen)))
    }
} catch {
    [Console]::Error.WriteLine($_.Exception.ToString())
    exit 1
}
"""
    encoded = base64.b64encode(ps_script.encode('utf-16-le')).decode('ascii')
    command = [
        'powershell.exe', '-NoProfile', '-NonInteractive', '-Sta',
        '-EncodedCommand', encoded,
    ]
    flags = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
    try:
        completed = subprocess.run(
            command, capture_output=True, text=True, encoding='utf-8',
            errors='replace', creationflags=flags, timeout=600,
            check=False,
        )
        if completed.returncode != 0:
            message = (completed.stderr or '').strip().splitlines()
            detail = message[0][:300] if message else 'Ошибка системного диалога.'
            raise RuntimeError(f'Не удалось открыть современный выбор папки Windows: {detail}')
        lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
        if not lines:
            return gr.update(), 'Выбор папки отменён.'
        chosen_path = base64.b64decode(lines[-1], validate=True).decode('utf-16-le')
        if not chosen_path:
            return gr.update(), 'Выбор папки отменён.'
        return gr.update(value=chosen_path), f'Выбрана папка: {chosen_path}'
    except subprocess.TimeoutExpired:
        return gr.update(), 'Истекло время ожидания выбора папки.'
    except Exception as exc:
        return gr.update(), f'Не удалось выбрать папку: {exc}. Можно ввести путь вручную.'


def _export_compact():
    """Create a backup first; reveal its download button only on success."""
    try:
        path, message = portable.create_backup()
        return gr.update(value=path, visible=True), message
    except Exception as exc:
        return gr.update(value=None, visible=False), f'Ошибка создания копии: {exc}'


def _zip_selected():
    return 'ZIP выбран. Нажми «Перенести всё» или «Добавить историю и избранное».'


def create_data_panel(*args, **kwargs):
    """Compact native Gradio Settings UI, no custom component subclasses.

    The three transfer workflows are separated into short horizontal rows.
    Unlike gr.File upload/download slots, UploadButton and DownloadButton do
    not reserve large drag/drop preview areas. The hidden native Textbox below
    is still required by Forge's Settings OptionInfo component factory.
    """
    gr.Markdown(
        '### Перенос данных\n'
        'Резервная копия настроек, истории и избранного. '
        'Старое расширение устанавливать не нужно. '
        '«Перенести всё» заменяет совпадающие JSON, включая настройки. '
        '«Добавить историю и избранное» объединяет записи без дубликатов и не меняет настройки. '
        'Перед изменением создаётся резервная копия. '
        '**После импорта перезапусти Forge Neo.**'
    )

    # Keep each action compact: buttons do not stretch to fill an entire row.
    gr.Markdown('**Резервная копия**')
    with gr.Row():
        create_btn = gr.Button(
            'Создать ZIP', size='sm', scale=0, min_width=130,
        )
        download_btn = gr.DownloadButton(
            'Скачать ZIP', size='sm', scale=0, min_width=130,
            visible=False,
        )

    gr.Markdown('**Импорт из ZIP**')
    with gr.Row():
        uploaded = gr.UploadButton(
            'Выбрать ZIP', file_types=['.zip'], type='binary',
            size='sm', scale=0, min_width=130,
        )
        import_zip_btn = gr.Button(
            'Перенести всё', size='sm', scale=0, min_width=140,
        )

        merge_zip_btn = gr.Button(
            'Добавить историю и избранное', size='sm', scale=0, min_width=230,
        )

    gr.Markdown('**Импорт из папки storage**')
    with gr.Row():
        old_storage = gr.Textbox(
            label='Путь к старой папке', show_label=False,
            placeholder=r'D:\Forge_old\extensions\sd-webui-prompt-all-in-one\storage',
            lines=1, scale=6, min_width=250,
            container=False,
        )
        choose_folder_btn = gr.Button(
            'Выбрать папку…', size='sm', scale=0, min_width=155,
        )
        folder_btn = gr.Button(
            'Перенести всё', size='sm', scale=0, min_width=140,
        )

        merge_folder_btn = gr.Button(
            'Добавить историю и избранное', size='sm', scale=0, min_width=230,
        )

    status = gr.Textbox(
        label='Результат', interactive=False, lines=1, max_lines=2,
        placeholder='Результат операции появится здесь.',
    )

    create_btn.click(
        fn=_export_compact, inputs=[], outputs=[download_btn, status],
        show_progress=False, queue=False,
    )
    uploaded.upload(
        fn=_zip_selected, inputs=[], outputs=[status],
        show_progress=False, queue=False,
    )
    import_zip_btn.click(
        fn=_import_zip, inputs=[uploaded], outputs=[status],
        show_progress=False,
    )
    merge_zip_btn.click(
        fn=_merge_zip, inputs=[uploaded], outputs=[status],
        show_progress=False,
    )
    choose_folder_btn.click(
        fn=_choose_storage_folder, inputs=[], outputs=[old_storage, status],
        show_progress=False, queue=False,
    )
    folder_btn.click(
        fn=_import_path, inputs=[old_storage], outputs=[status],
        show_progress=False,
    )

    merge_folder_btn.click(
        fn=_merge_path, inputs=[old_storage], outputs=[status],
        show_progress=False,
    )

    # Forge Settings expects a component return value. This is a native
    # component rather than a custom class, avoiding KeyError on startup.
    kwargs['visible'] = False
    return gr.Textbox(*args, **kwargs)


def register_settings():
    shared.opts.add_option(
        'prompt_aio_history_limit',
        shared.OptionInfo(
            100,
            'Максимум записей истории на каждый тип',
            gr.Dropdown,
            {
                'choices': [
                    ('100 записей', 100),
                    ('200 записей', 200),
                    ('500 записей', 500),
                    ('1000 записей', 1000),
                    ('5000 записей', 5000),
                    ('Без ограничения', 0),
                ],
            },
            section=('prompt_aio_settings', 'Prompt All-in-One'),
            category_id='ui',
        ).info(
            'Лимит для txt2img/img2img и положительных/отрицательных промптов. '
            '0 — без ограничения. Избранное не ограничивается; существующая '
            'история при смене лимита не удаляется. Применяется к новым записям.'
        )
    )

    shared.opts.add_option(
        'prompt_aio_portable_data_tools',
        shared.OptionInfo(
            '', 'Prompt AIO data transfer', create_data_panel,
            section=('prompt_aio_settings', 'Prompt All-in-One'),
            category_id='ui',
        )
    )


script_callbacks.on_ui_settings(register_settings)
