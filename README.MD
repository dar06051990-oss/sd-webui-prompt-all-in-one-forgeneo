This is sd-webui-prompt-all-in-one for the latest version of [Forge Neo](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo), adapted for the latest Python 3.13 fixes, using Vibe coding.

## Forge Neo local mBART + data migration fixes

This fork adds several Forge Neo compatibility and migration improvements:

- fixes local mBART50 model discovery;
- supports local mBART weights stored as `pytorch_model.bin`, `model.safetensors`,
  or sharded index files;
- can reuse the mBART model from a sibling `sd-webui-prompt-all-in-one` install;
- prints mBART initialization and translation tracebacks to the Forge console;
- fixes the wait logic when mBART initialization is already in progress;
- automatically imports missing JSON storage data from older sibling installs once;
- adds a **Prompt AIO Import** tab for manual import;
- manual import can optionally overwrite existing JSON data.

The safe default is non-destructive: existing files are preserved unless overwrite
is explicitly enabled.

Based on the Forge Neo fork by abzaloff and the original project by Physton.

---

# sd-webui-prompt-all-in-one

[![GitHub stars](https://img.shields.io/github/stars/Physton/sd-webui-prompt-all-in-one?style=flat-square)](https://github.com/Physton/sd-webui-prompt-all-in-one/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Physton/sd-webui-prompt-all-in-one?style=flat-square)](https://github.com/Physton/sd-webui-prompt-all-in-one/network/members)
[![GitHub issues](https://img.shields.io/github/issues/Physton/sd-webui-prompt-all-in-one?style=flat-square)](https://github.com/Physton/sd-webui-prompt-all-in-one/issues)
[![GitHub issues closed](https://img.shields.io/github/issues-closed/Physton/sd-webui-prompt-all-in-one?style=flat-square)](https://github.com/Physton/sd-webui-prompt-all-in-one/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub license](https://img.shields.io/github/license/Physton/sd-webui-prompt-all-in-one?style=flat-square)](https://github.com/Physton/sd-webui-prompt-all-in-one/blob/master/LICENSE.md)
[![GitHub commits](https://img.shields.io/github/last-commit/Physton/sd-webui-prompt-all-in-one?style=flat-square)](https://github.com/Physton/sd-webui-prompt-all-in-one/commits/main)
[![Netlify Status](https://api.netlify.com/api/v1/badges/1441a696-a1a4-4ad7-b520-4abfd96acc76/deploy-status)](https://app.netlify.com/sites/aiodoc/deploys)

<div align="center">

### [🇺🇸 English](README.MD) | [🇷🇺 Русский](README_RU.MD) | [🇨🇳 简体中文](README_CN.MD) | [🇯🇵 日本語](README_JP.MD) | [🇰🇷 한국어](README_KR.MD) | [🇨🇳 繁體中文](README_TW.MD)

</div>

sd-webui-prompt-all-in-one is an extension based on [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) that aims to improve the user experience of the prompt/negative prompt input box. It has a more intuitive and powerful input interface, provides automatic translation, history and collection functions, and supports multiple languages to meet the needs of different users.

---

**📮📮📮 I am very sorry, due to limited personal energy, this project will no longer be maintained. However, if anyone improves the code, feel free to submit a Pull Request, and I will find time to merge it into the main branch.**

---

<div align="center">

### Installation tutorial, detailed feature introduction, usage instructions, frequently asked questions, and more can be found in the [Wiki](https://aiodoc.physton.com/).

</div>

----

**📢📢📢 This project has developed an independent standalone version that can run without relying on stable-diffusion-webui. It is lightweight and compact, focusing on editing and organizing prompt words. Visit [Physton/sd-webui-prompt-all-in-one-app](https://github.com/Physton/sd-webui-prompt-all-in-one-app) for the tutorial on how to use it.**

----

> If you find this extension helpful, please give me a star on Github!
> You could also buy me a coffee: [donate](#donate)

----

## Translation API Description

1. `API Key Not Required`: They are highly unstable and not every API can be used on your computer. If the translation fails, please try switching to another API. ⚠️⚠️⚠️ **Do not submit an issue!**
2. `API KEY Required`: You need to apply for an API KEY on your own. The application methods for different interfaces will appear after switching to the corresponding interface. ⚠️⚠️⚠️ **Most of them are `free`!**
3. `Offline Translation`: During initialization, automatic download of language models is required. If your network environment is poor, it may not be able to complete the automatic download and initialization.

## [Wiki](https://aiodoc.physton.com/)

- [Installation](https://aiodoc.physton.com/Installation.html)
- [Extension update description](https://aiodoc.physton.com/ExtensionUpdateDescription.html)
- [Translation API Description](https://aiodoc.physton.com/TranslationApiConfiguration.html#translation-api-description)
- [Contributing](https://aiodoc.physton.com/Contributing.html)
- [Custom Theme](https://aiodoc.physton.com/Contributing.html#custom-theme)
- [FAQ](https://aiodoc.physton.com/FAQ.html)
- [Buy me a coffee](#buy-me-a-coffee)

## Language support

Translation supports almost all national languages, but the UI interface of most countries will be displayed in English. If you need localized language display, you can translate and submit a PR.

<details>
<summary>UI Supported languages</summary>

`简体中文` `繁體中文` `English` ` Русский` `日本語` `한국어` ` Français` `Deutsch` ` Español` `Português` `Italiano` `العربية`
</details>

<details>
<summary>Translation Supported languages</summary>

`简体中文 (中国)` `繁體中文 (中國香港)` `繁体中文 (中國台灣)` `English (US)` `Afrikaans (South Africa)` `Shqip (Shqipëria)` `አማርኛ (ኢትዮጵያ)` `العربية (السعودية)` `Հայերեն (Հայաստան)` `অসমীয়া (ভাৰত)` `Azərbaycan dili (Latın, Azərbaycan)` `বাংলা (বাংলাদেশ)` `Башҡорт (Россия)` `Euskara (Espainia)` `Bosanski (Latinski, Bosna i Hercegovina)` `Български (България)` `Català (Espanya)` `Hrvatski (Hrvatska)` `Čeština (Česká republika)` `Dansk (Danmark)` `درى (افغانستان)` `ދިވެހިބަސް (ދިވެހިރާއްޖެ)` `Nederlands (Nederland)` `Eesti (Eesti)` `Føroyskt (Føroyar)` `vosa Vakaviti (Viti)` `Filipino (Pilipinas)` `Suomi (Suomi)` `Français (France)` `Français (Canada)` `Galego (España)` `ქართული (საქართველო)` `Deutsch (Deutschland)` `Ελληνικά (Ελλάδα)` `ગુજરાતી (ભારત)` `Kreyòl ayisyen (Ayiti)` `עברית (ישראל)` `हिन्दी (भारत)` `Hmong Daw (Latn, United States)` `Magyar (Magyarország)` `Íslenska (Ísland)` `Bahasa Indonesia (Indonesia)` `Inuktitut (Kanatami)` `Inuktitut (Latin, Canada)` `ᐃᓄᒃᑎᑐᑦ (ᑲᓇᑕᒥ)` `Gaeilge (Éire)` `Italiano (Italia)` `日本語 (日本)` `ಕನ್ನಡ (ಭಾರತ)` `Қазақ (Қазақстан)` `ភាសាខ្មែរ (កម្ពុជា)` `Klingon (Latn)` `Klingon (plqaD)` `한국어 (대한민국)` `کوردی (عێراق)` `Kurmancî (Latînî, Tirkiye)` `Кыргызча (Кыргызстан)` `ລາວ (ລາວ)` `Latviešu (Latvija)` `Lietuvių (Lietuva)` `Македонски (Северна Македонија)` `Malagasy (Madagasikara)` `Bahasa Melayu (Latin, Malaysia)` `മലയാളം (ഇന്ത്യ)` `Malti (Malta)` `Māori (Aotearoa)` `मराठी (भारत)` `Монгол (Кирилл, Монгол улс)` `ᠮᠣᠩᠭᠣᠯ ᠤᠯᠤᠰ (ᠨᠢᠭᠡᠳᠦᠯ ᠤᠨᠤᠭ᠎ᠠ)` `မြန်မာ (မြန်မာ)` `नेपाली (नेपाल)` `Norsk bokmål (Norge)` `ଓଡ଼ିଆ (ଭାରତ)` `پښتو (افغانستان)` `فارسی (ایران)` `Polski (Polska)` `Português (Brasil)` `Português (Portugal)` `ਪੰਜਾਬੀ (ਗੁਰਮੁਖੀ, ਭਾਰਤ)` `Querétaro Otomi (Latn, México)` `Română (România)` `Русский (Россия)` `Samoan (Latn, Samoa)` `Српски (ћирилица, Србија)` `Srpski (latinica, Srbija)` `Slovenčina (Slovensko)` `Slovenščina (Slovenija)` `Soomaali (Soomaaliya)` `Español (España)` `Kiswahili (Kenya)` `Svenska (Sverige)` `Reo Tahiti (Polynésie française)` `தமிழ் (இந்தியா)` `Татарча (латин, Россия)` `తెలుగు (భారత)` `ไทย (ไทย)` `བོད་ཡིག (རྒྱ་གར།)` `ትግርኛ (ኢትዮጵያ)` `lea fakatonga (Tonga)` `Türkçe (Türkiye)` `Українська (Україна)` `اردو (پاکستان)` `ئۇيغۇرچە (ئۇيغۇرچە، جۇڭگو)` `O'zbekcha (Lotin, O'zbekiston)` `Tiếng Việt (Việt Nam)` `Cymraeg (Y Deyrnas Unedig)` `Yucatec Maya (México)` `isiZulu (iNingizimu Afrika)`
</details>

## Features

- `Intuitive input interface` provides a more intuitive and powerful input interface, displaying bilingual prompt word comparisons for easy understanding.
- `Automatic translation` automatically translates prompt words/reverse prompt words, supporting multiple languages.
- `Dozens of translation services` with dozens of online translations and offline translation models.
- `Multilingual support` supports translation for most languages spoken in the world, allowing you to input prompt words in any language.
- `History records` automatically records when prompt words/reverse prompt words change.
- `Favorites` allows you to quickly bookmark and batch bookmark your favorite prompt words/reverse prompt words.
- `Quick adjustments` drag and adjust the position of prompt words, one-click increase or decrease the weight of prompt words, one-click delete, disable, translate, or bookmark, and more.
- `Batch operations` select multiple prompt words/reverse prompt words in a box, one-click delete, translate, or bookmark, and more.
- `ChatGPT` generates prompt words intelligently through ChatGPT.
- `Prompt word blacklist` allows you to set a blacklist to automatically filter prompt words.
- `One-click adding of prompt words` thousands of prompt words available, just a click away.
- `Keyword highlighting` Lora, LyCORIS, Textual Inversion highlighting and detection.
- `Customizable keyword colors` different types of keywords can be displayed in different custom colors.
- `Custom themes` customize themes and extend styles.
- `...` More features waiting for you to discover.

## Demo

- [Switch language](https://aiodoc.physton.com/LanguageSelection.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.switch_language.gif)

- [Translation API settings](https://aiodoc.physton.com/TranslationApiConfiguration.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.translate_setting.gif)

- [Show/Hide content](https://aiodoc.physton.com/OtherFeatures.html#show-collapse-the-extension-panel)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.fold.gif)

- [Show/Hide the WebUI input box](https://aiodoc.physton.com/OtherFeatures.html#show-hide-the-webui-input-box)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.show_input.gif)

- [Automatic translation](https://aiodoc.physton.com/AutomaticTranslation.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.auto_translate.gif)

- [One-click translation](https://aiodoc.physton.com/BatchTranslation.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.translate.gif)

- [Elegant input](https://aiodoc.physton.com/KeywordInputBox.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.elegant_input.gif)

- [Quick adjustment](https://aiodoc.physton.com/ListOfKeywords.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.quick_adjust.gif)

- [Favorite and History](https://aiodoc.physton.com/History.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.history_favorite.gif)

- [Use ChatGPT to Generate Prompts](https://aiodoc.physton.com/UsingChatgptToGeneratePrompts.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.chatgpt.gif)

- [Writing in WebUI input box](https://aiodoc.physton.com/WritingInWebUIInputBox.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.writing_webui.gif)

- Support for [a1111-sd-webui-tagcomplete](https://github.com/DominikDoom/a1111-sd-webui-tagcomplete)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.tagcomplete.gif)

- [Highlighting and detection of Lora, LyCORIS, and Textual Inversion](https://aiodoc.physton.com/ListOfKeywords.html#highlight-keyword)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.keyword_detection.gif)

- [Format of Prompt](https://aiodoc.physton.com/FormatOfPrompts.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.prompt_format.gif)

- [Batch operation](https://aiodoc.physton.com/BatchTranslation.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.batch_operation.gif)

- [Custom Theme / Extension styles](https://aiodoc.physton.com/ThemeStyle.html)

  ![](https://s1.imagehub.cc/images/2023/06/06/demo.custom_theme.gif)

- [One-Click Keyword Addition](https://aiodoc.physton.com/GroupTags.html)

  ![](https://s1.imagehub.cc/images/2023/08/15/demo.group_tags.gif)

## Donate

[Donation list](https://aiodoc.physton.com/Donate.html)

### Buy me a coffee

| ko-fi (EN) | [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/physton) |
|:-----------:| :----: |
| Paypal (EN) | [https://paypal.me/physton](https://paypal.me/physton) |
| 爱发电 (CN) | [https://afdian.net/a/physton/thank](https://afdian.net/a/physton/thank) |
| 支付宝 (CN) | ![](https://s1.imagehub.cc/images/2023/07/05/alipay.jpeg) |
| 微信赞赏 (CN) | ![](https://s1.imagehub.cc/images/2023/07/05/wechat.jpeg) |
