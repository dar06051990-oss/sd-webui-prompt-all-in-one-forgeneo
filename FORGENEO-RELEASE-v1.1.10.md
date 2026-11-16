## Forge Neo — обновление v1.1.10 (16.11.2026)

- Единый раздел **Settings → Prompt All-in-One** вместо отдельной вкладки импорта.
- Резервная копия ZIP, перенос настроек, истории и избранного из ZIP или папки `storage` любой установки Forge.
- **Перенести всё** заменяет совпадающие JSON с резервной копией. **Добавить историю и избранное** объединяет записи без дубликатов, не меняя настройки.
- Настраиваемый лимит истории для каждого типа: 100, 200, 500, 1000, 5000 либо без ограничения. Избранное не ограничено.
- Компактное оформление и современный выбор папки в Windows.
- Исправлено наложение длинных тегов и переводов, а также исчезновение крестиков при изменении масштаба.
- Данные пользователя в папке `storage` **не включены в релиз**.

Для обновления воспользуйся вкладкой Extensions в Forge Neo и полностью перезапусти Forge. Перед обновлением желательно сохранить свою папку `storage`.


---

## Forge Neo release v1.1.10 (2026-11-16)

- Consolidates Prompt AIO controls into **Settings → Prompt All-in-One**; removes the separate **Prompt AIO Import** tab.
- Backup and restore ZIP files, or import from any old Forge install's **storage** folder; no old extension installation is needed.
- **Transfer all** replaces source-matching JSON with an automatic backup. **Add history and favorites** merges records without duplicate IDs, leaving current settings intact.
- History maximum per type: 100 / 200 / 500 / 1000 / 5000 / unlimited; favorites are unrestricted.
- Modern Windows folder picker; compact transfer controls.
- Responsive prompt tags: fixes text and translation overlap and disappearing delete controls on long prompts or browser zoom.
- Original prompt editor, translator, LoRA processing and image generation behavior unchanged.
- The actual user data in `storage/` is **not part of the release**.

**Update:** In Forge Neo Extensions, update this repository and fully restart Forge Neo. Before updating, consider backing up your own `storage/` folder.
