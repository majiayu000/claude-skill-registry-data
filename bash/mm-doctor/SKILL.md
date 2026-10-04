---
name: mm-doctor
version: 0.6.0
description: Самопроверка mm-системы — junction'ы, конфиг, vault, паспорта, bridge-архив, GSD-консистентность (passport vs PROJECT.md), наличие сторонних плагинов (karpathy, context-mode). Auto-fix очевидного. Use when user says "проверь систему", "почему не работает", "/mm-doctor", "mm-status", "что-то сломалось", "проверь mm", "mm health". Запускать перед началом работы на новой машине ИЛИ когда что-то странно себя ведёт.
---

# mm-doctor — System Health Check & Auto-Fix

Прогон диагностики всей mm-системы. Не пишет ничего без подтверждения.

## Конфиг

Загрузи `mm-config.json` по алгоритму из `<repo>/docs/CONFIG-LOADING.md`. Поддержка `mm-config.local.json` overlay обязательна. Loader должен инжектировать `_repo_root`.

Если loader падает — это уже первая ошибка, выведи её и предложи фикс из CONFIG-LOADING.md.

## Чек-лист (выполнять по порядку, помечать ✅ / ⚠️ / ❌)

### 1. Конфиг

- ✅ `mm-config.json` найден (откуда: env / junction / fallback)
- ✅ Валидный JSON
- ⚠️ Если использован legacy fallback (см. `docs/CONFIG-LOADING.md`) — предложи `[Environment]::SetEnvironmentVariable("MM_REPO_ROOT", "<repo>", "User")`
- ✅ `mm-config.local.json` (если есть) валидный, deep-merged
- ✅ Ключевые пути присутствуют: `obsidian_*`, `_repo_root`

### 2. Repo integrity

- ✅ `<repo>/templates/passport.md` существует
- ✅ `<repo>/templates/project-instructions.md` существует
- ✅ `<repo>/skills/mm-bridge/SKILL.md`, `mm-init-project`, `mm-setup`, `mm-resume`, `mm-handoff`, `mm-save-session`, `mm-instructions`, `mm-projects`, `mm-doctor`, `mm` существуют (10 skills)
- ✅ `<repo>/scripts/register-skills.py` существует

### 3. Симлинки / Junction'ы (`~/.claude/skills/mm-*`)

Для каждого `mm-*` в `<repo>/skills/` и `<repo>/vendor/`:
- ✅ Ссылка `~/.claude/skills/mm-<name>` существует
- ✅ Является reparse-point/symlink (симлинк на Mac/Linux, junction на Windows)
- ✅ Target указывает на `<repo>/skills/mm-<name>` (или `vendor/mm-<name>`)

Проверка на macOS/Linux:
```bash
ls -la ~/.claude/skills/
readlink ~/.claude/skills/mm-bridge  # должно вести на <repo>/skills/mm-bridge
```

PowerShell-проверка (Windows):
```powershell
$item = Get-Item "$env:USERPROFILE\.claude\skills\mm-bridge" -Force
$item.Attributes -band [System.IO.FileAttributes]::ReparsePoint  # должно быть != 0
$item.Target  # должно совпадать с <repo>/skills/mm-bridge
```

При ошибках предложи: `Запустить scripts/register-skills.py для пере-создания ссылок? (y/n)`. Если y — запусти.

### 4. Obsidian vault (Базовая настройка)

Если проект не открыт, проверь глобальные пути из конфига `paths.obsidian_*`:
- ✅ `obsidian_vault` существует
- ✅ `obsidian_claude_root` существует
- ✅ `obsidian_bridge` существует (создай если нет — это безопасно)
- ✅ `obsidian_bridge_archive` существует (создай если нет)
- ✅ `obsidian_sessions` существует (создай если нет)
- ✅ `obsidian_projects` существует (создай если нет)
- ⚠️ `obsidian_index` файл есть; если нет — предупреди но не падай

### 5. Bridge state

- ✅ `<obsidian_bridge>/next-prompt.md` — info: есть/нет, дата
- ⚠️ Если есть и старше 7 дней — намекни: `Старый бридж-промпт от <date>. Уже использован?`
- ⚠️ Архив старше 30 дней: посчитай файлы в `<obsidian_bridge_archive>` старше 30 дней. Если > 0:
  ```
  В архиве bridge-промптов: <N> файлов, <M> старше 30 дней.
  Удалить старые? (y/n)
  ```

### 6. Текущий проект и База Знаний (если cwd внутри проекта)

Если в `cwd` или родителях есть `passport.md`:
- ✅ Frontmatter паспорта валидный YAML
- ✅ Все 11 секций присутствуют в `passport.md`
- ✅ Frontmatter содержит `gsd_version: <none|v1|v2|core>`
- ⚠️ `updated:` в паспорте старше 30 дней → предложи `/mm-init-project --update`
- ⚠️ Секция 8 «Контекст для промптов» содержит маркер `<!-- TODO: заполни секцию 8 -->` → намекни завить
- ✅ Определение пути базы знаний `<vault_root>` (локальная папка `.vault/` в корне или глобальная `<obsidian_projects>/<name>/` из конфига)
- ✅ Папки базы знаний существуют:
  - `00-home/`
  - `atlas/`
  - `knowledge/` (и ее подпапки: `integrations/`, `decisions/`, `debugging/`, `patterns/`, `business/`)
  - `sessions/`
  - `inbox/`
- ✅ Ключевые файлы базы знаний существуют:
  - `00-home/index.md`
  - `00-home/текущие приоритеты.md`
  - `project-instructions.md` (в корне хранилища — туда пишут и `/mm rules`, и `/mm new`)
  - `handoff.md` (скелет или полный)
  - `passport.md` (копия, в корне хранилища — её читают `/mm projects` и `clear-gate.py`)
  - ⚠️ Если рядом лежит `atlas/passport.md` — это дубль от старой раскладки, который никто не читает: `⚠️ atlas/passport.md — дубль паспорта, удали его вручную, источник это <vault>/passport.md.`
- ✅ В `CLAUDE.md` присутствует секция `## Obsidian Knowledge Vault` с правильным путем к базе знаний.
- ✅ Sync с копией паспорта в базе знаний (sha256): совпадают?
- ⚠️ handoff.md существует. Если нет → `⚠️ handoff.md отсутствует — запусти /mm save (или /mm next) чтобы создать; он нужен для Project Knowledge claude.ai.`

### 6.1. GSD ↔ passport консистентность (если есть GSD)

Если passport `gsd_version` ≠ none, прогони cross-check:

**Проверка 1: версия в passport совпадает с реальностью**
- Если в passport `gsd_version: v1` или `core`, проверь что `<project_root>/.planning/` существует. (Для `core` проверь также наличие `.planning/config.json`).
- Если `gsd_version: v2` — проверь `<project_root>/.gsd/`.
- Если расходится → `❌ passport говорит gsd_version: <v1|core>, но .planning/ не найдена. Запусти /mm-init-project --update.` (или аналогично для v2).

**Проверка 2: scope не разъехался**
- Если есть `.planning/PROJECT.md` (v1/core):
  - Прочитай первые 30 строк и сравни с секцией 1 («Назначение») паспорта.
  - Если **ключевые слова не пересекаются** (jaccard < 0.3 на нормализованных tokens) → `⚠️ passport.md секция 1 и .planning/PROJECT.md описывают разное. Возможно scope изменился. Обнови passport через /mm-init-project --update.`
- Если есть `.gsd/STATE.md` или AGENTS.md → аналогично.

**Проверка 3: текущая фаза не устарела в паспорте**
- В passport секция 9 строка `Текущий milestone / phase: <X>`.
- В `.planning/STATE.md` или `.gsd/STATE.md` — фактический current.
- Если расходятся → `⚠️ passport.md секция 9 говорит фаза «X», STATE.md показывает «Y». Обнови.`

**Проверка 4: source-of-truth direction**
- В passport секция 9 строка `Source-of-truth для scope/requirements: <X>`.
- Должна быть `.planning/PROJECT.md` (если GSD есть) или `passport.md` (если GSD нет).
- Иначе → `⚠️ Source-of-truth не указан явно — две системы могут разъехаться. Заполни секцию 9.`

**Проверка 5: mm не пишет в .planning/**
- Если git log показывает что любой mm-skill коммитил файлы в `.planning/*` за последние 30 дней → `❌ mm писал в .planning/ — это нарушение контракта. Откатить вручную.`
- (это защита от будущих багов; mm-skills не должны это делать)

**Проверка 6: GSD-директива есть в CLAUDE.md** (ретро-детектор)
- Если `gsd_version != none`, проверь что `<project_root>/CLAUDE.md` содержит подблок `### GSD в этом проекте` (его добавляет `/mm-init-project` с версии 0.5.0).
- Если блока нет → `⚠️ В проекте есть GSD, но в CLAUDE.md нет GSD-директивы (проект инициализирован старой версией mm). Запусти /mm-init-project (update) — добавит правило маршрутизации работы через GSD.`
- Это закрывает вопрос «какие старые проекты надо обновить под новую GSD-интеграцию» — doctor находит их сам.

### 6.2. Валидация кода Telethon (если `telethon` обнаружен в проекте)

Если в проекте используется библиотека `telethon` (в зависимости от флага `telethon_project` в паспорте или наличия `telethon` в манифестах):
- ✅ Наличие инструкции по сессиям: файл `knowledge/integrations/telethon-sessions.md` присутствует в Obsidian Vault проекта. Если нет → `⚠️ Рекомендуется скопировать инструкцию по сессиям в базу знаний — запусти /mm new.`
- ✅ Проверка кода инициализации: просканируй `*.py` файлы на наличие создания `TelegramClient`.
  - Для каждого `TelegramClient(...)` проверь:
    - Присутствует ли аргумент `proxy` (или `proxy=...`). Если отсутствует → `⚠️ Обнаружена инициализация TelegramClient без прокси (риск моментального бана).`
    - Передаются ли параметры фингерпринта (`device_model`, `system_version`, `app_version`, `lang_code`, `system_lang_code`). Если они опущены или захардкожены (строковые литералы вместо переменных из загруженного `.json`) → `⚠️ Параметры устройства (fingerprint) не передаются или захардкожены. Рекомендуется загружать их динамически из .json.`
    - Проверяется ли статус `frozen` аккаунта. Ищи вызов `get_dialogs(limit=...)` или `get_me()` в цепочке инициализации. Если нет → `⚠️ Отсутствует дешевая проверка аккаунта на freeze после входа.`
    - Присутствуют ли обработчики исключений `FloodWaitError` и `AuthKeyDuplicatedError`. Если нет → `⚠️ Не найдены обработчики критических ошибок Telethon (FloodWaitError, AuthKeyDuplicatedError).`

### 6.3. Валидация UI/UX Telegram-ботов (если `tg_bot_project` обнаружен в проекте)

**Пропуск валидации:** Если в frontmatter файла `passport.md` проекта параметр `telegram_ui_ux` установлен в `false`, **полностью пропусти эту фазу** (не проводи проверки и не выводи предупреждения). Это позволяет разработчику использовать собственный дизайн интерфейса без предупреждений от системы.

Если в проекте разрабатывается Telegram-бот (в зависимости от флага `tg_bot_project` в паспорте или наличия бота в зависимостях) **и** параметр `telegram_ui_ux` в frontmatter `passport.md` **не** равен `false`:
- ✅ Наличие стандартов UI/UX: файл `knowledge/patterns/tg-bot-ui-ux.md` присутствует в Obsidian Vault проекта. Если нет → `⚠️ Рекомендуется скопировать стандарт UI/UX в базу знаний — запусти /mm new.`
- ✅ Проверка Reply-клавиатур: просканируй `*.py` файлы на создание `ReplyKeyboardMarkup`.
  - Проверь, передан ли аргумент `resize_keyboard=True`. Если нет → `⚠️ Обнаружена Reply-клавиатура без resize_keyboard=True (будет занимать слишком много места на мобильных).`
- ✅ Проверка разметки сообщений (Parse Mode):
  - Просканируй вызовы `send_message(...)`, `reply(...)`, `edit_text(...)` и др.
  - Если используется `parse_mode="MarkdownV2"` или аналогичный Markdown без явного экранирования динамических переменных, предупреди → `⚠️ Обнаружен вывод динамических данных с parse_mode=MarkdownV2. Рекомендуется использовать HTML + html.escape для предотвращения ошибок 400 Bad Request.`
- ✅ Одноклик-копирование:
  - Проверь, обернуты ли длинные ID, токены, ключи и пути к файлам в текстах сообщений в тег `<code>...</code>` или `<pre>...</pre>`. Если нет → `⚠️ Технические данные (ID, токены, пути) выводятся как обычный текст. Оберни в тег <code>, чтобы пользователь мог копировать их в один тап.`
- ✅ Диалоги подтверждения:
  - Изучи inline-клавиатуры подтверждения. Если кнопка подтверждения (Да/Удалить) находится справа, а отмена — слева, предупреди → `⚠️ Рекомендуется располагать кнопки в диалоге подтверждения в порядке [✅ Да] [❌ Отмена] (подтверждение слева, отмена справа).`

### 7. Версии

**Единый источник версии mm-системы — `config.version`** в `mm-config.json` (repo-wide release). Per-skill `version:` в каждом `SKILL.md` — гранулярная история конкретного скилла; **разные per-skill версии это норма, не рассинхрон.**

Для каждого `mm-*/SKILL.md`:
- ✅ Имеет `version:` в frontmatter
- ✅ `name:` совпадает с папкой

Версионная консистентность:
- ✅ `config.version` присутствует и валиден (semver).
- ⚠️ Если у текущего проекта `passport.mm_version` **старше** `config.version` → `⚠️ Паспорт проштампован mm <passport.mm_version>, актуальная <config.version>. Прогони /mm-init-project (update) для refresh.`
- ⚠️ Проверка обновлений: запусти `python3 <repo>/scripts/auto-update.py` (или проверь командой `git fetch && git status`) для сверки с репозиторием GitHub. Если локальный репо отстает от origin/main → `⚠️ Доступно обновление системы. Запусти /mm update или npx markdown-memory для обновления.`
- (Файл `.mm-versions.json` больше не используется — игнорируй, если встретишь.)

### 8. Глобальный CLAUDE.md (опционально)

Прочитай `~/.claude/CLAUDE.md` если есть:
- ⚠️ Если содержит дублирующие правила Sessions/Projects/INDEX (старая ручная инструкция) — намекни упростить через ссылку на `/mm-save-session`
- ✅ Иначе — ok

### 9. Сторонние интеграции (плагины, MCP)

Проверь установлены ли рекомендованные плагины:

- **karpathy-skills** (`~/.claude/plugins/marketplaces/karpathy-skills/`) — 4 принципа кодинга
  - ✅ установлен / ⚠️ нет — `claude plugin marketplace add forrestchang/andrej-karpathy-skills && claude plugin install andrej-karpathy-skills@karpathy-skills`
  - ✅ В `~/.claude/CLAUDE.md` есть секция Karpathy Guidelines (4 принципа продублированы текстом для всех проектов)

- **context-mode** (`~/.claude/plugins/marketplaces/context-mode/`) — MCP-сервер экономии контекста
  - ✅ установлен / ⚠️ нет — `claude plugin marketplace add mksglu/context-mode && claude plugin install context-mode@context-mode`
  - Если установлен:
    - ✅ Каталог сессий `~/.claude/context-mode/sessions/` существует и есть `.db` файлы
    - ⚠️ База старше 90 дней без cleanup → намекни `/ctx-purge`
    - ⚠️ Хуки контекст-мода работают параллельно с GSD-хуками — это норм, оба независимы. Если видишь медленный PostToolUse — это сумма обоих, не баг.
    - 💡 Для расширенной диагностики используй `/ctx-doctor` (skill самого context-mode)
  - 📊 Опционально показать накопленную статистику: `~/.context-mode/stats.json` (если есть)

- **GSD hooks** в `~/.claude/hooks/` — должны быть в `settings.json` SessionStart/PreToolUse/PostToolUse. Уже проверено в этих секциях выше.

- **Telegram bridge** (claude-code-telegram, опционально):
  - Если в `mm-config.local.json` `tg_bridge.enabled = true`:
    - ✅ `<repo>/external/claude-code-telegram/` существует
    - ✅ `<repo>/external/claude-code-telegram/.env` существует
    - ✅ В `.env` заполнены `TELEGRAM_BOT_TOKEN`, `ALLOWED_USERS`, `APPROVED_DIRECTORY` (НЕ читай значения — только проверь не пустые)
    - ⚠️ Если `CLAUDE_MAX_COST_PER_USER` не задан — предупреди (риск runaway costs)
    - ⚠️ Если `APPROVED_DIRECTORY = C:\` или другой слишком широкий путь — предупреди про безопасность
    - 💡 Проверка процесса: `Get-Process python` (Windows) или `pgrep -f python` (macOS/Linux) — если ни одного Python-процесса бота нет, бот может быть не запущен. Это просто намёк, не ошибка.
  - Если `tg_bridge.enabled = false` or нет — пропусти. Это опциональная фича.

## Финальный отчёт

```
🩺 mm-doctor отчёт

✅ Конфиг: загружен через <env|junction|fallback>, valid
✅ Repo integrity: все templates и SKILL.md на месте
✅ Симлинки/Junction'ы: <N>/<N> OK
⚠️ Obsidian: vault найден, bridge_archive не было — создал
✅ Bridge state: next-prompt.md от <date> (свежий)
⚠️ Bridge archive: 47 файлов старше 30 дней — предложил удалить
✅ Текущий проект: <name>, passport валидный (gsd_version: <none|v1|v2|core>), sync OK
✅ handoff.md: на месте <или ⚠️ отсутствует — /mm save>
✅ GSD-директива в CLAUDE.md: есть <или ⚠️ нет — /mm new для retrofit; или n/a если GSD нет>
⚠️ Секция 8 паспорта: TODO-маркер не убран
✅ Skills frontmatter: <N>/<N> имеют version и name
✅ Версии: config.version <X.Y.Z>, passport.mm_version <X.Y.Z> <совпадают | паспорт старше — /mm new>
✅ Обновление mm-системы: <✅ актуально | ⚠️ доступно обновление — /mm update>
✅ karpathy-skills plugin: установлен
✅ context-mode plugin: установлен, sessions/ есть
⚠️ Telethon codebase: <✅ OK | ⚠️ обнаружены ban-риски в коде / отсутствует telethon-sessions.md | n/a если Telethon не используется>
⚠️ TG Bot UI/UX: <✅ OK | ⚠️ обнаружены отклонения от стандартов / отсутствует tg-bot-ui-ux.md | n/a если бот не разрабатывается | 🚫 отключено (telegram_ui_ux: false в passport.md)>
⚠️ Telegram bridge: не установлен (опционально — см. docs/TG-BRIDGE.md)

Итого: 3 предупреждения, 0 ошибок.

Что предлагаю сделать сейчас:
1. Удалить 47 старых bridge-архивов (одна команда)
2. Заполнить секцию 8 в <path>/passport.md
3. (опционально) упростить ~/.claude/CLAUDE.md через ссылку на /mm-save-session
4. (опционально) обновить mm-систему через /mm update (если доступно обновление)

Согласовать каждое отдельно? (y / только 1 / только 2 / skip)
```

## Auto-fixes (требуют подтверждения)

С разрешения юзера:
- Создать недостающие папки в Obsidian (`bridge`, `archive`, `sessions`, `projects`)
- Пере-запустить `register-skills.py` при битых симлинках/junction'ах
- Удалить bridge-архивы старше N дней
- Установить `MM_REPO_ROOT` env var
- Сгенерировать безопасный модуль-хелпер для Telethon (например, `telegram_builder.py` на основе шаблона `telethon-sessions.md`) и отрефакторить небезопасную инициализацию клиента (с подтверждением изменений)
- Сгенерировать безопасный модуль-хелпер для ботов `tg_bot_ui_helper.py` (на основе стандартов `tg-bot-ui-ux.md`), содержащий стандартные элементы разметки и Middleware, а также вывести разработчику пошаговые инструкции по рефакторингу (с подтверждением изменений)

**Никогда без подтверждения:**
- Удаление файлов в Obsidian (кроме архивов с явным yes)
- Правка `~/.claude/CLAUDE.md` (это вне репо, чувствительный файл)
- Правка чужих passport.md
- `git` операции (за исключением /mm update, выполняющего git pull)

## Edge cases

- **Запуск без интернета**: всё локально, должно работать.
- **Запуск из worktree**: используй ту же worktree-detection логику что и mm-init-project (resolve до main repo).
- **Несколько mm-config.json в разных папках** (по ошибке клонировали репо дважды): обнаружь и предупреди.
- **Junction указывает на старый репо** (после переезда): предложи запустить register-skills.ps1 в новой локации.

## Что НЕ делать

- Не молчать при ошибках — всегда показывай конкретную команду фикса.
- Не «чинить» вещи без подтверждения юзера.
- Не отчитываться победно если есть ⚠️/❌ — отчёт должен быть честным.
