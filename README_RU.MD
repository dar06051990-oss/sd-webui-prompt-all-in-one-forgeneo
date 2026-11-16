## Forge Neo — обновление v1.1.10 (16.11.2026)

- Единый раздел **Settings → Prompt All-in-One** вместо отдельной вкладки импорта.
- Резервная копия ZIP, перенос настроек, истории и избранного из ZIP или папки `storage` любой установки Forge.
- **Перенести всё** заменяет совпадающие JSON с резервной копией. **Добавить историю и избранное** объединяет записи без дубликатов, не меняя настройки.
- Настраиваемый лимит истории для каждого типа: 100, 200, 500, 1000, 5000 либо без ограничения. Избранное не ограничено.
- Компактное оформление и современный выбор папки в Windows.
- Исправлено наложение длинных тегов и переводов, а также исчезновение крестиков при изменении масштаба.
- Данные пользователя в папке `storage` **не включены в релиз**.

Для обновления воспользуйся вкладкой Extensions в Forge Neo и полностью перезапусти Forge. Перед обновлением желательно сохранить свою папку `storage`.


# sd-webui-prompt-all-in-one

[![GitHub звезды](https://img.shields.io/github/stars/Physton/sd-webui-prompt-all-in-one?style=flat-square)](https://github.com/Physton/sd-webui-prompt-all-in-one/stargazers)
[![GitHub вилки](https://img.shields.io/github/forks/Physton/sd-webui-prompt-all-in-one?style=flat-square)](https://github.com/Physton/sd-webui-prompt-all-in-one/network/members)
[![GitHub вопросы](https://img.shields.io/github/issues/Physton/sd-webui-prompt-all-in-one?style=flat-square)](https://github.com/Physton/sd-webui-prompt-all-in-one/issues)
[![GitHub закрытые вопросы](https://img.shields.io/github/issues-closed/Physton/sd-webui-prompt-all-in-one?style=flat-square)](https://github.com/Physton/sd-webui-prompt-all-in-one/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub лицензия](https://img.shields.io/github/license/Physton/sd-webui-prompt-all-in-one?style=flat-square)](https://github.com/Physton/sd-webui-prompt-all-in-one/blob/master/LICENSE.md)
[![GitHub коммиты](https://img.shields.io/github/last-commit/Physton/sd-webui-prompt-all-in-one?style=flat-square)](https://github.com/Physton/sd-webui-prompt-all-in-one/commits/main)
[![Netlify Статус](https://api.netlify.com/api/v1/badges/1441a696-a1a4-4ad7-b520-4abfd96acc76/deploy-status)](https://app.netlify.com/sites/aiodoc/deploys)

<div align="center">

### [🇺🇸 English](README.MD) | [🇷🇺 Русский](README_RU.MD) | [🇨🇳 简体中文](README_CN.MD) | [🇯🇵 日本語](README_JP.MD) | [🇰🇷 한국어](README_KR.MD) | [🇨🇳 繁體中文](README_TW.MD)

</div>

sd-webui-prompt-all-in-one - это расширение, основанное на [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui), которое предназначено для улучшения опыта использования полей ввода подсказок/обратных подсказок. Оно имеет более интуитивный и мощный функционал интерфейса ввода, предоставляет функции автоматического перевода, истории и избранного, поддерживает несколько языков и удовлетворяет потребностям разных пользователей.

---

**📮📮📮 Мне очень жаль, но из-за ограниченных личных ресурсов этот проект больше не будет поддерживаться. Однако, если кто-то улучшит код, не стесняйтесь отправить Pull Request, и я постараюсь найти время, чтобы объединить его в основную ветку.**

---

<div align="center">

### Инструкции по установке, подробное описание функций, инструкции по использованию, часто задаваемые вопросы и т.д. см.: [Документация](https://aiodoc.physton.com/ru/).

</div>

----

**📢📢📢️ Этот проект разработал самостоятельную автономную версию, которая может работать без зависимости от stable-diffusion-webui. Он легкий и компактный, с фокусом на редактировании и организации ключевых слов. Посетите [Physton/sd-webui-prompt-all-in-one-app](https://github.com/Physton/sd-webui-prompt-all-in-one-app) для просмотра руководства по использованию.**

----

> Если вам понравилось это расширение, пожалуйста, поставьте звезду на GitHub!
> Вы также можете угостить меня чашкой кофе: [donate](#пожертвования)

----

## Описание API перевода

1. `API-ключ не требуется`: они очень нестабильны и не все API могут быть использованы на вашем компьютере. Если перевод не удался, попробуйте переключиться на другое API, ⚠️⚠️⚠️**не создавайте issue!**
2. `API-ключ необходим`: необходимо получить API KEY самостоятельно. После переключения на соответствующий интерфейс появится инструкция по его получению. ⚠️⚠️⚠️**Они в основном `бесплатны`!**
3. `Офлайн-перевод`: при инициализации необходимо автоматически загрузить языковую модель. Если у вас плохое интернет-соединение, может быть невозможно выполнить автоматическую загрузку и инициализацию.

## [Документация](https://aiodoc.physton.com/ru/)

- [Установка](https://aiodoc.physton.com/ru/Installation.html)
- [Описание обновлений расширения](https://aiodoc.physton.com/ru/ExtensionUpdateDescription.html)
- [Описание API перевода](https://aiodoc.physton.com/ru/TranslationApiConfiguration.html#описание-интерфеиса-перевода)
- [Помощь в разработке](https://aiodoc.physton.com/ru/Contributing.html)
- [Настройка пользовательской темы](https://aiodoc.physton.com/ru/Contributing.html#ннастроика-темы)
- [Часто задаваемые вопросы](https://aiodoc.physton.com/ru/FAQ.html)
- [Угостить меня чашкой кофе](#пожертвования)

## Поддерживаемые языки

Поддержка перевода практически на всех языках мира, но большинство интерфейсов пользователя отображаются на английском языке. Если вам нужна локализация на ваш язык, вы можете перевести и предоставить PR.

<details>
<summary>Поддерживаемые языки пользовательского интерфейса</summary>

`简体中文` `繁體中文` `English` ` Русский` `日本語` `한국어` ` Français` `Deutsch` ` Español` `Português` `Italiano` `العربية`
</details>

<details>
<summary>Поддерживаемые языки перевода</summary>

`简体中文 (中国)` `繁體中文 (中國香港)` `繁体中文 (中國台灣)` `English (US)` `Afrikaans (South Africa)` `Shqip (Shqipëria)` `አማርኛ (ኢትዮጵያ)` `العربية (السعودية)` `Հայերեն (Հայաստան)` `অসমীয়া (ভাৰত)` `Azərbaycan dili (Latın, Azərbaycan)` `বাংলা (বাংলাদেশ)` `Башҡорт (Россия)` `Euskara (Espainia)` `Bosanski (Latinski, Bosna i Hercegovina)` `Български (България)` `Català (Espanya)` `Hrvatski (Hrvatska)` `Čeština (Česká republika)` `Dansk (Danmark)` `درى (افغانستان)` `ދިވެހިބަސް (ދިވެހިރާއްޖެ)` `Nederlands (Nederland)` `Eesti (Eesti)` `Føroyskt (Føroyar)` `vosa Vakaviti (Viti)` `Filipino (Pilipinas)` `Suomi (Suomi)` `Français (France)` `Français (Canada)` `Galego (España)` `ქართული (საქართველო)` `Deutsch (Deutschland)` `Ελληνικά (Ελλάδα)` `ગુજરાતી (ભારત)` `Kreyòl ayisyen (Ayiti)` `עברית (ישראל)` `हिन्दी (भारत)` `Hmong Daw (Latn, United States)` `Magyar (Magyarország)` `Íslenska (Ísland)` `Bahasa Indonesia (Indonesia)` `Inuktitut (Kanatami)` `Inuktitut (Latin, Canada)` `ᐃᓄᒃᑎᑐᑦ (ᑲᓇᑕᒥ)` `Gaeilge (Éire)` `Italiano (Italia)` `日本語 (日本)` `ಕನ್ನಡ (ಭಾರತ)` `Қазақ (Қазақстан)` `ភាសាខ្មែរ (កម្ពុជា)` `Klingon (Latn)` `Klingon (plqaD)` `한국어 (대한민국)` `کوردی (عێراق)` `Kurmancî (Latînî, Tirkiye)` `Кыргызча (Кыргызстан)` `ລາວ (ລາວ)` `Latviešu (Latvija)` `Lietuvių (Lietuva)` `Македонски (Северна Македонија)` `Malagasy (Madagasikara)` `Bahasa Melayu (Latin, Malaysia)` `മലയാളം (ഇന്ത്യ)` `Malti (Malta)` `Māori (Aotearoa)` `मराठी (भारत)` `Монгол (Кирилл, Монгол улс)` `ᠮᠣᠩᠭᠣᠯ ᠤᠯᠤᠰ (ᠨᠢᠭᠡᠳᠦᠯ ᠤᠨᠤᠭ᠎ᠠ)` `မြန်မာ (မြန်မာ)` `नेपाली (नेपाल)` `Norsk bokmål (Norge)` `ଓଡ଼ିଆ (ଭାରତ)` `پښتو (افغانستان)` `فارسی (ایران)` `Polski (Polska)` `Português (Brasil)` `Português (Portugal)` `ਪੰਜਾਬੀ (ਗੁਰਮੁਖੀ, ਭਾਰਤ)` `Querétaro Otomi (Latn, México)` `Română (România)` `Русский (Россия)` `Samoan (Latn, Samoa)` `Српски (ћирилица, Србија)` `Srpski (latinica, Srbija)` `Slovenčina (Slovensko)` `Slovenščina (Slovenija)` `Soomaali (Soomaaliya)` `Español (España)` `Kiswahili (Kenya)` `Svenska (Sverige)` `Reo Tahiti (Polynésie française)` `தமிழ் (இந்தியா)` `Татарча (латин, Россия)` `తెలుగు (భారత)` `ไทย (ไทย)` `བོད་ཡིག (རྒྱ་གར།)` `ትግርኛ (ኢትዮጵያ)` `lea fakatonga (Tonga)` `Türkçe (Türkiye)` `Українська (Україна)` `اردو (پاکستان)` `ئۇيغۇرچە (ئۇيغۇرچە، جۇڭگو)` `O'zbekcha (Lotin, O'zbekiston)` `Tiếng Việt (Việt Nam)` `Cymraeg (Y Deyrnas Unedig)` `Yucatec Maya (México)` `isiZulu (iNingizimu Afrika)`
</details>

## Особенности

- `Интуитивный интерфейс ввода` обеспечивает более интуитивное и мощное взаимодействие с пользователем, отображая двуязычное сравнение слов-подсказок для лучшего понимания.
- `Автоматический перевод` автоматически переводит слова-подсказки/обратные слова-подсказки, поддерживая несколько языков.
- `Десятки сервисов перевода` с десятками онлайн-переводчиков и офлайн-моделей перевода.
- `Мультиязычная поддержка` поддерживает перевод для большинства языков, используемых в мире, позволяя вводить слова-подсказки на любом языке.
- `История записей` автоматически записывает изменения слов-подсказок/обратных слов-подсказок.
- `Избранное` позволяет быстро добавлять в закладки и пакетно добавлять в закладки ваши любимые слова-подсказки/обратные слова-подсказки.
- `Быстрые настройки` перетаскивание и настройка положения слов-подсказок, одним нажатием увеличение или уменьшение веса слов-подсказок, одним нажатием удаление, отключение, перевод или добавление в закладки и т. д.
- `Массовые операции` выделение нескольких слов-подсказок/обратных слов-подсказок в рамке, одним нажатием удаление, перевод или добавление в закладки и т. д.
- `ChatGPT` интеллектуально генерирует слова-подсказки с помощью ChatGPT.
- `Черный список слов-подсказок` позволяет установить черный список для автоматической фильтрации слов-подсказок.
- `Одним нажатием добавить слова-подсказки` тысячи доступных слов-подсказок, просто одно нажатие.
- `Выделение ключевых слов` выделение и обнаружение ключевых слов Lora, LyCORIS, Textual Inversion.
- `Настройка цвета ключевых слов` различные типы ключевых слов могут отображаться разными цветами.
- `Настройка темы` настраиваемые темы и расширяемые стили.
- `...` Больше функций ждут вас для открытия.

## Демонстрация

- [Переключение языка](https://aiodoc.physton.com/ru/LanguageSelection.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.switch_language.gif)

- [Настройка API перевода](https://aiodoc.physton.com/ru/TranslationApiConfiguration.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.translate_setting.gif)

- [Отображение/скрытие контента](https://aiodoc.physton.com/ru/OtherFeatures.html#показать-скрыть-расширенную-панель)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.fold.gif)

- [Отображение/скрытие поля ввода WebUI](https://aiodoc.physton.com/ru/OtherFeatures.html#показать-скрыть-поле-ввода-webui)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.show_input.gif)

- [Автоматический перевод](https://aiodoc.physton.com/ru/AutomaticTranslation.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.auto_translate.gif)

- [Однокнопочный перевод](https://aiodoc.physton.com/ru/BatchTranslation.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.translate.gif)

- [Элегантный ввод](https://aiodoc.physton.com/ru/KeywordInputBox.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.elegant_input.gif)

- [Быстрая настройка](https://aiodoc.physton.com/ru/ListOfKeywords.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.quick_adjust.gif)

- [Избранное и история](https://aiodoc.physton.com/ru/History.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.history_favorite.gif)

- [Генерация подсказок с помощью ChatGPT](https://aiodoc.physton.com/ru/UsingChatgptToGeneratePrompts.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.chatgpt.gif)

- [Написание в поле ввода WebUI](https://aiodoc.physton.com/ru/WritingInWebUIInputBox.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.writing_webui.gif)

- Поддержка[a1111-sd-webui-tagcomplete](https://github.com/DominikDoom/a1111-sd-webui-tagcomplete)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.tagcomplete.gif)

- [Подсветка и обнаружение ключевых слов Lora, LyCORIS и Textual Inversion](https://aiodoc.physton.com/ru/ListOfKeywords.html#подсветка-ключевых-слов)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.keyword_detection.gif)

- [Формат подсказок](https://aiodoc.physton.com/ru/FormatOfPrompts.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.prompt_format.gif)

- [Массовые операции]https://aiodoc.physton.com/ru/BatchTranslation.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.batch_operation.gif)

- [Настройка пользовательской темы/стиля расширения](https://aiodoc.physton.com/ru/ThemeStyle.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.custom_theme.gif)

- [Добавление ключевых слов в один клик](https://aiodoc.physton.com/ru/GroupTags.html)

  ![](https://s1.imagehub.cc/images/2023/08/15/demo.group_tags.gif)

## Пожертвования

[Список пожертвований](https://aiodoc.physton.com/ru/Donate.html)

### Угостить меня чашкой кофе

| ko-fi (EN) | [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/physton) |
|:-----------:| :----: |
| Paypal (EN) | [https://paypal.me/physton](https://paypal.me/physton) |
| 爱发电 (CN) | [https://afdian.net/a/physton/thank](https://afdian.net/a/physton/thank) |
| 支付宝 (CN) | ![](https://s1.imagehub.cc/images/2023/07/05/alipay.jpeg) |
| 微信赞赏 (CN) | ![](https://s1.imagehub.cc/images/2023/07/05/wechat.jpeg) |