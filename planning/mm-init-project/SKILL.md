---
name: mm-init-project
version: 0.6.0
description: Инициализирует или обновляет проект для mm-системы — создаёт passport.md в корне, копию в Obsidian, dashboard.md, handoff.md (скелет), project-instructions.md для claude.ai. Use when user says "оформи проект", "сделай паспорт", "init project", "/mm-init", "/mm-init-project", "обнови паспорт", "регистрирую проект". Работает на пустой папке (новый проект) и на существующем коде с любыми .md файлами (auto-discovery + dry-run preview перед записью). Включает auto-detect стека (~150 фреймворков), dual-detection GSD v1 (.planning/) и v2 (.gsd/), import scope/requirements из GSD-артефактов, secret-grep, детектор рассинхрона между копиями паспорта.
---

# mm-init-project — Project Bootstrap & Refresh (safe edition)

Создаёт «паспорт» проекта — единый источник контекста для claude.ai Project Knowledge и для всех mm-* skills. **Всегда показывает план перед записью**, никогда не уничтожает чужие .md файлы.

## Контракт безопасности (это важно — соблюдай дословно)

**Skill ПИШЕТ только в эти файлы:**
- `<project_root>/passport.md` — создаёт или обновляет
- `<project_root>/CLAUDE.md` — **только** добавляет секции `## Obsidian Knowledge Vault` и `## mm-system` если их нет; **никогда** не редактирует существующие секции
- `<project_root>/.gitignore` — добавляет правила для игнорирования локальных настроек Obsidian (`.vault/.obsidian/`)
- Файлы Obsidian Vault (хранилище в `<project_root>/.vault/` при локальном режиме или `<obsidian_projects>/<name>/` при глобальном режиме):
  - `00-home/index.md` — карта всех заметок; **в режиме update не трогает, если файл есть и непустой**
  - `00-home/текущие приоритеты.md` — текущие приоритеты; **в режиме update не трогает, если файл есть и непустой**
  - `project-instructions.md` — инструкции для claude.ai (в корне хранилища, туда же пишет `/mm rules`)
  - `handoff.md` — создаёт **скелет** на старте (в корне хранилища)
  - `passport.md` — копия паспорта проекта (в корне хранилища; её читают `/mm projects`, `clear-gate.py` и sync-check фазы 1f)
  - `atlas/архитектура проекта.md` — описание архитектуры
  - `atlas/база данных.md` — схема БД
  - `atlas/деплой.md` — информация о деплое
  - Создает папки `knowledge/integrations/`, `knowledge/decisions/`, `knowledge/debugging/`, `knowledge/patterns/`, `knowledge/business/`, `sessions/`, `inbox/` if they don't exist.

**Skill ТОЛЬКО ЧИТАЕТ (никогда не редактирует):**
- README.md, ARCHITECTURE.md, NOTES.md, OVERVIEW.md, CONTEXT.md, DESIGN.md, ROADMAP.md, TODO.md, BUGS.md, DECISIONS.md, и любые другие *.md в проекте
- package.json, pyproject.toml, requirements.txt, go.mod, Cargo.toml, pom.xml
- .env.example (не .env!)
- Dockerfile, docker-compose.yml, railway.json, vercel.json
- .git/config, git log, git status

**Skill НЕ ТРОГАЕТ ВООБЩЕ:**
- `.env`, `*.key`, `*.pem`, `secrets/` — даже не читает значения
- node_modules/, .venv/, dist/, build/, target/
- Файлы вне `<project_root>` за исключением Obsidian-папки из конфига

**Перед любой записью** — обязательная фаза Preview (см. ниже). Без подтверждения `y` — ничего не пишется.

## Конфиг

Загрузи `mm-config.json` по алгоритму из `<repo>/docs/CONFIG-LOADING.md`. Поддержка `mm-config.local.json` overlay обязательна. `<repo>` берётся из `_repo_root` инжектированного loader'ом.

Понадобятся:
- `paths.obsidian_projects`
- `_repo_root` (для `templates/passport.md` и `templates/project-instructions.md`)
- `bot_defaults.*`
- `default_language`

## Фаза 0. Определи целевую папку (worktree-aware)

**Целевая папка** = «корень проекта», не «cwd как есть».

Алгоритм:
1. Возьми `cwd`.
2. Если в пути есть подстрока `\.claude\worktrees\` или `/.claude/worktrees/` — это worktree. Найди корневой репо:
   - Прочитай `<cwd>/.git` (это файл-указатель, не папка). Извлеки `gitdir: <path>`. Из него выведи main repo path.
   - Если не получилось — спроси: `Это git worktree. Какую папку считать корнем проекта? <предложи: ...>`.
3. Иначе — поднимись от `cwd` пока не найдёшь `.git/` (папку, не файл) или `package.json` / `pyproject.toml` / любой явный маркер корня. Если ничего нет — `cwd` и есть корень.

**Имя проекта** = basename целевой папки. Покажи: `Имя проекта: <name> (целевая папка: <path>). Ок? (y/n или новое имя)`.

## Фаза 1. Discovery (что уже есть в проекте)

Просканируй и **выведи отчёт пользователю** перед любыми действиями.

### 1a. Существующие паспорта (миграция)

Поищи (case-insensitive) в `<project_root>` и `<project_root>/docs/`:
- `passport.md`, `PASSPORT.md`, `Passport.md`, `passport.MD` — варианты case
- `PROJECT_PASSPORT.md`, `project_passport.md` — старая louise-система (`Claude Setup/`)
- `*_passport.md`, `passport_*.md`

Любой найденный — **кандидат на миграцию**, не конфликт-блокер.

### 1b. Документы которые могут содержать контекст

Просканируй `*.md` в:
- `<project_root>/` (корень)
- `<project_root>/docs/`, `<project_root>/notes/`, `<project_root>/_docs/`
- `<project_root>/.planning/` (GSD-документы)

Распознай семантически по имени (case-insensitive substring):
| В имени есть | Категория |
|---|---|
| `readme` | Описание / overview |
| `architecture`, `design`, `arch` | Архитектура |
| `overview`, `context`, `intro` | Контекст |
| `notes`, `ideas` | Заметки |
| `decisions`, `adr`, `rfc` | Решения |
| `roadmap`, `plan` | Планы |
| `todo`, `tasks`, `backlog` | Задачи |
| `bugs`, `issues`, `known-issues` | Проблемы |
| `changelog`, `history` | История |
| `claude` (CLAUDE.md, claude-rules.md) | Правила для AI |

Прочитай **первые 50 строк** каждого найденного файла — для понимания.

### 1c. Маркеры стека (auto-detection)

**Manifest-файлы** — прочитай если есть:
- `package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `composer.json`, `Gemfile`, `mix.exs`, `pubspec.yaml`
- `Dockerfile`, `docker-compose.yml`, `railway.json`, `vercel.json`, `fly.toml`, `Procfile`
- `.env.example`, `.env.template` (не `.env`!)
- `tsconfig.json`, `next.config.*`, `vite.config.*`, `astro.config.*`, `nuxt.config.*`, `svelte.config.*`, `remix.config.*`
- `.python-version`, `.nvmrc`, `.tool-versions`, `runtime.txt`

**Auto-detection: пакет → стек** (по подстроке в зависимостях):

| Если в зависимостях | Тип | Фреймворк | Категория |
|---|---|---|---|
| `aiogram`, `python-telegram-bot`, `telethon`, `pyrogram`, `telegraf`, `grammy` | bot | по имени | tg-bot |
| `discord.py`, `discord.js`, `discordeno` | bot | по имени | discord-bot |
| `fastapi`, `flask`, `django`, `starlette`, `litestar`, `quart`, `sanic`, `bottle`, `pyramid` | web | по имени | python-web |
| `express`, `koa`, `hapi`, `fastify`, `nest`, `polka`, `hono`, `elysia` | web | по имени | node-web |
| `next`, `nuxt`, `astro`, `remix`, `sveltekit`, `gatsby`, `solid-start`, `qwik` | web | по имени | meta-framework |
| `react`, `vue`, `svelte`, `solid-js`, `preact`, `lit`, `htmx` | web | по имени | spa-frontend |
| `gin`, `echo`, `fiber`, `chi`, `gorilla/mux`, `huma` | web | по имени | go-web |
| `actix-web`, `axum`, `rocket`, `warp`, `tide`, `salvo` | web | по имени | rust-web |
| `rails`, `sinatra`, `hanami`, `roda` | web | по имени | ruby-web |
| `phoenix`, `plug` | web | по имени | elixir-web |
| `laravel`, `symfony`, `slim` | web | по имени | php-web |
| `sqlalchemy`, `sqlmodel`, `alembic`, `tortoise-orm`, `peewee`, `pydantic` | — | — | python-db |
| `prisma`, `drizzle`, `kysely`, `typeorm`, `sequelize`, `mongoose`, `mikro-orm` | — | — | node-db |
| `gorm`, `ent`, `sqlx`, `bun`, `pgx` | — | — | go-db |
| `diesel`, `sea-orm`, `sqlx` (rust) | — | — | rust-db |
| `pytest`, `unittest`, `nose2`, `tox` | — | тесты Python | testing |
| `vitest`, `jest`, `mocha`, `playwright`, `cypress`, `ava`, `tap` | — | тесты JS | testing |
| `cargo test` (default), `nextest` | — | тесты Rust | testing |
| `loguru`, `structlog`, `winston`, `pino`, `zap`, `tracing`, `slog` | — | логирование | observability |
| `pydantic`, `zod`, `joi`, `yup`, `ajv`, `valibot`, `arktype` | — | валидация | validation |
| `openai`, `anthropic`, `litellm`, `langchain`, `llama-index`, `instructor` | — | — | ai-llm |
| `huggingface`, `transformers`, `torch`, `tensorflow`, `jax`, `keras` | — | — | ai-ml |
| `pandas`, `polars`, `numpy`, `scipy`, `dask` | — | — | data |
| `dlt`, `airflow`, `prefect`, `dagster`, `kafka-python`, `aiokafka` | — | — | pipelines |
| `redis`, `aioredis`, `kombu`, `celery`, `rq`, `bullmq` | — | — | queue/cache |
| `scrapy`, `playwright`, `puppeteer`, `selenium`, `httpx`, `aiohttp` | — | — | scraping/http |
| `tauri`, `electron`, `wails` | — | — | desktop |

**Файловые маркеры (если manifest неоднозначен):**
- `*.tsx` / `*.jsx` → React
- `*.vue` → Vue
- `*.svelte` → Svelte
- `*.astro` → Astro
- `app/page.tsx` → Next.js App Router
- `pages/*.tsx` → Next.js Pages Router
- `wrangler.toml` → Cloudflare Workers
- `serverless.yml` → Serverless Framework
- `terraform/`, `*.tf` → Terraform
- `helm/`, `Chart.yaml` → Kubernetes Helm

**Combo-recognition (комплекты):**
- React + TypeScript + Tailwind + shadcn → пометить «modern react stack»
- FastAPI + Pydantic + sqlmodel + pytest → пометить «modern python web»
- aiogram + sqlmodel + loguru → пометить «default bot stack» (из bot_defaults конфига)
- Наличие `telethon` в зависимостях → установить внутренний флаг `telethon_project: true`
- Наличие фреймворков категории `tg-bot` (`aiogram`, `python-telegram-bot`, `telegraf`, `grammy` и др.) в зависимостях → установить внутренний флаг `tg_bot_project: true`

**Приоритет определения типа** (когда несколько матчей):
1. tg-bot / discord-bot (если есть бот-фреймворк) — `bot`
2. meta-framework (Next/Nuxt/Astro/Remix) — `web`
3. python-web / node-web / go-web / rust-web — `web`
4. spa-frontend без backend — `web` (frontend-only)
5. ai-ml / ai-llm + entry point — `script` или `service`
6. data / pipelines — `script`
7. desktop — `desktop`
8. lib (если в `pyproject.toml` `[project]` без entry point ИЛИ в `package.json` `main` без `bin`) — `lib`
9. иначе — `script`

**Версии:**
- Питон: из `.python-version` или `pyproject.toml` `requires-python`
- Node: из `.nvmrc`, `engines.node` в package.json
- Go: из `go.mod` строка `go X.Y`
- Rust: из `rust-toolchain.toml` или edition в `Cargo.toml`

### 1d. Git-контекст

```bash
git rev-parse --show-toplevel
git remote -v
git branch --show-current
git log --oneline -10
```

### 1e. Системы которые могут конфликтовать (dual-detection GSD)

**GSD detection** (определи версию):
- `<project_root>/.planning/` существует:
  - Если `<project_root>/.planning/config.json` существует → **GSD Core**. В passport frontmatter `gsd_version: core`.
  - Иначе → **GSD v1**. В passport frontmatter `gsd_version: v1`.
- `<project_root>/.gsd/` существует → **GSD v2**. В passport frontmatter `gsd_version: v2`.
- Оба → **смешанный** (редкость, после миграции). Спроси: какой считать активным?
- Ни одного → `gsd_version: none`.

**Если GSD есть — попробуй импортировать scope/requirements** (чтобы не дублировать):

GSD v1 (`.planning/`):
- `PROJECT.md` → vision, audience, goals → секция 1 (Назначение) + секция 3 (Архитектура краткая)
- `REQUIREMENTS.md` → REQ-001..N → можно вытащить топ-5 в секцию 4 как «функциональные требования» (опционально)
- `ROADMAP.md` → phases, статусы → секция 9 паспорта строка `Текущий milestone / phase: <M1 / phase 03 — <title>>`
- `STATE.md` → current phase / position → секция 10 «В работе сейчас»
- `codebase/STACK.md`, `codebase/ARCHITECTURE.md`, `codebase/CONVENTIONS.md`, `codebase/CONCERNS.md` → если есть, переносим в секции 2, 3, 7, 10 паспорта (НЕ дублируя — кратко + ссылка `см. .planning/codebase/STACK.md`)

GSD v2 (`.gsd/`):
- `gsd.db` (SQLite) → если можешь прочитать через sqlite3 CLI/Python — извлеки текущий milestone/slice/task; иначе пропусти
- `STATE.md` (rendered dashboard) → парсинг как у v1
- `AGENTS.md` → preferences для агентов → ссылка в секции 7 паспорта

**Важное правило про дубликацию:**
- Если в `.planning/PROJECT.md` уже есть подробное описание проекта — в секции 1 паспорта пиши **краткое summary + ссылку** (`см. .planning/PROJECT.md`), не копируй целиком.
- В секции 9 явно укажи source-of-truth: `Source-of-truth для scope/requirements: .planning/PROJECT.md`. Это нужно чтобы будущий читатель не запутался какой документ актуальный.

**Никогда не пиши в `.planning/*` или `.gsd/*` напрямую** — там file-lock'и, hook'и-охранники GSD. Только читать.

**`CLAUDE.md`** → читай, оценивай размер: маленький (< 30 строк) — добавим секцию; большой — спросим перед добавлением.

**`passport.md`** (точное совпадение) → режим update, см. фазу 3.

### 1f. Sync-check между копиями паспорта

Копий паспорта ровно две: `<project_root>/passport.md` и `<vault_root>/passport.md`. Тот же путь пишет фаза 4.2 — второго места для паспорта в скилле нет.

Если есть и `<project_root>/passport.md` И `<vault_root>/passport.md`:
- Сравни sha256 содержимого (или хотя бы mtime + size).
- Если **расходятся** — это значит юзер редактировал одну из копий (например в Obsidian app). Покажи в Discovery:
  ```
  ⚠️ Рассинхрон: passport.md в проекте и в Obsidian отличаются.
     Проект:  updated <date>, sha <hex8>
     Obsidian: updated <date>, sha <hex8>

     Какую версию считать source-of-truth?
     [1] Проект (Obsidian перезапишется) — дефолт
     [2] Obsidian (проект перезапишется)
     [3] Show diff first
     [4] Cancel
  ```
- Запомни выбор для фазы 4 (write).

### 1g. Вывод фазы Discovery (покажи пользователю)

```
🔍 Discovery: <project_name>

Целевая папка: <abs_path>
Git: <branch>, <N> коммитов, remote: <url или local>

Найдено существующих паспортов:
  • PROJECT_PASSPORT.md  ← старая louise-система, можно мигрировать
  • passport.md          ← текущий формат, режим update
  (или: «не найдено»)

Найдено документов с контекстом:
  • README.md (описание)
  • docs/architecture.md (архитектура)
  • NOTES.md (заметки)
  (используются ТОЛЬКО для чтения — не будут изменены)

GSD detection:
  • Версия: <none | v1 (.planning/) | v2 (.gsd/) | core (.planning/ config.json)>
  • PROJECT.md: <есть, 240 строк — могу импортировать vision и audience в секции 1, 3>
  • REQUIREMENTS.md: <есть, REQ-001..REQ-014 — топ-5 в секцию 4?>
  • Текущий milestone: <M1 «MVP», phase 03/07 «add /stats command» (in-progress)>
  • codebase/: <STACK.md, ARCHITECTURE.md, CONVENTIONS.md — могу подсосать в секции 2, 3, 7>

Стек определён (auto-detection):
  • Язык: Python 3.12 (из .python-version)
  • Фреймворк: aiogram 3.x (из pyproject.toml)
  • DB: SQLite через sqlmodel
  • Тесты: pytest
  • Логирование: loguru
  • Тип: bot (combo: «default bot stack»)

Существующий CLAUDE.md: <нет / <N> строк, добавлю секцию mm-system / большой — спрошу>
```

## Фаза 2. Решения (если нужны)

Задай только реально неопределённые вопросы (максимум 3-4):

1. **Расположение Obsidian Vault (КРИТИЧНО):**
   Спроси пользователя, где хранить базу знаний (Obsidian Vault):
   ```
   Выберите расположение Obsidian Vault для проекта:
   [1] Локально в папке проекта (рекомендуется: <project_root>/.vault/, версионируется в git, синхронизируется с claude.ai автоматически) — дефолт
   [2] Глобально в папке Obsidian (из конфига: <obsidian_projects>/<name>/)
   ```

2. **Если найден PROJECT_PASSPORT.md** или другой кандидат миграции:
   `Найден старый паспорт <file>. Мигрировать его контент в новый passport.md? (y = мигрировать, переименую старый в .legacy / n = игнорировать)`

3. **Если есть passport.md И он явно устарел** (mtime старше 30 дней или git log показывает много коммитов после updated):
   Просто переходи в режим update без вопроса.

4. **Если CLAUDE.md > 30 строк**:
   `CLAUDE.md существует и непустой (<N> строк). Добавить правила базы знаний в конец? (y/n)`

5. **Если папка пустая** (новый проект):
   - Тип: bot / web / lib / script?
   - Язык / фреймворк? (для bot — дефолт `aiogram` из bot_defaults)
   - Назначение в одном предложении?

6. **Если в выбранной директории Vault уже есть файлы**:
   `В директории базы знаний уже есть файлы. Update (y) / Создать папку с суффиксом -2 (n) / Отмена (c)?`

7. **Если есть GSD (`.planning/PROJECT.md` или `.gsd/`) и режим init**:
   `Найден <PROJECT.md / .gsd/>. Импортировать описание/scope в секции 1, 3 паспорта (y) / только сослаться, не дублировать (n) / отмена (c)? Дефолт n — паспорт ссылается, не дублирует.`

Если пользователь говорит «решай сам» — выбирай разумный дефолт, отмечай в финальном отчёте `<assumed: ...>`.

## Фаза 3. План записи (Preview / Dry-run)

**Это обязательная фаза. Без подтверждения — НИЧЕГО не пишется.**

Покажи пользователю полный план в формате:

```
📋 План записи

Расположение Obsidian Vault: <локальное (.vault/) | глобальное (<path>)>

СОЗДАМ:
  + <project>/passport.md (новый файл, <N> секций)
    Источники: README.md, package.json, etc.
  + <vault_root>/00-home/index.md (карта всех заметок; в update — только если файла нет или он пуст)
  + <vault_root>/00-home/текущие приоритеты.md (активные приоритеты; в update — только если файла нет или он пуст)
  + <vault_root>/project-instructions.md (инструкции для claude.ai)
  + <vault_root>/handoff.md (скелет)
  + <vault_root>/passport.md (копия паспорта)
  + <vault_root>/atlas/архитектура проекта.md (архитектура)
  + <vault_root>/atlas/база данных.md (схемы БД)
  + <vault_root>/atlas/деплой.md (информация о деплое)
  + <vault_root>/knowledge/integrations/ (папка)
  + <vault_root>/knowledge/decisions/ (папка)
  + <vault_root>/knowledge/debugging/ (папка)
  + <vault_root>/knowledge/patterns/ (папка)
  + <vault_root>/knowledge/business/ (папка)
  + <vault_root>/sessions/ (папка для логов сессий)
  + <vault_root>/inbox/ (папка для входящего)

ИЗМЕНЮ:
  ~ <project>/CLAUDE.md (добавлю правила Obsidian Knowledge Vault, +18 строк)
  <если локальный режим:>
  ~ <project>/.gitignore (добавлю .vault/.obsidian/ в конец, +2 строки)

ПЕРЕИМЕНУЮ:
  → PROJECT_PASSPORT.md → PROJECT_PASSPORT.md.legacy

НЕ ТРОНУ:
  README.md, .planning/*, .env, src/

Continue? (y / n / edit)
```

`edit` → дай возможность изменить план: «Не переименовывай PROJECT_PASSPORT» / «Не трогай CLAUDE.md» / «Не создавай dashboard» — пользователь редактирует список через простой dialog, ты применяешь.

`n` → останови, ничего не пиши.

`y` → переходи к фазе 4.

## Фаза 4. Запись (atomic: всё или ничего)

Делай в этом порядке. Если хоть один шаг падает — **откати уже сделанное** (удали созданные файлы, восстанови переименованный):

### 4.1. Сгенерируй текст passport.md в памяти

Возьми шаблон `<skills_repo>/templates/passport.md`. Заполни:

- **Секции 1-7, 9** — из discovery (стек, архитектура, команды, конвенции из README, ENV из .env.example).
- **Секция 8 «Контекст для промптов»**:
  - Если миграция из PROJECT_PASSPORT.md и там есть аналогичный раздел — перенеси.
  - Иначе:
    - Если `telethon_project == true`, добавь следующие жесткие правила:
      * `При написании кода для Telethon-аккаунтов строго следуй правилам из [[telethon-sessions|инструкции по сессиям Telethon]].`
      * `Запрещены параллельные запуски сессий с одним файлом .session (риск AuthKeyDuplicatedError).`
      * `Все параметры устройства (fingerprint) бери строго из соответствующего .json файла.`
      * `Используй SOCKS5-прокси с rdns=True для всех подключений.`
    - Если `tg_bot_project == true`, добавь следующие жесткие правила:
      * `При проектировании интерфейса бота (текст, кнопки, эмодзи) строго следуй правилам из [[tg-bot-ui-ux|руководства по UI/UX ботов Telegram]].`
    - Иначе оставь шаблон + `<!-- TODO: заполни секцию 8 — критично, читается каждым промптом -->`.
- **Секция 10 «Текущее состояние»**:
  - Init: пустой шаблон.
  - Update (есть passport.md): сохрани существующий текст 1:1.
  - Migration: если в старом паспорте была секция «Текущее состояние / Status / Now» — перенеси.
- **Секция 11 «История»**:
  - Init: одна строка «<date> Initial».
  - Update: добавь строку «<date> Refresh: <что обновилось>».
  - Migration: «<date> Migrated from PROJECT_PASSPORT.md».

Frontmatter: `created` из существующего файла или сегодня; `updated` = сегодня; `mm_version` = `config.version` из mm-config.json (подставь значение, не оставляй плейсхолдер `<MM_VERSION>`); `telegram_ui_ux` = `true` (если `tg_bot_project == true`), иначе `false`.

### 4.2. Сгенерируй файлы Obsidian Vault в памяти

**Сгенерируй структуру и контент для файлов базы знаний:**
> **Guard режима update** (по образцу `handoff.md`): `00-home/index.md` и `00-home/текущие приоритеты.md` — живой курируемый контент, их владелец `/mm save`, а не инициализатор. В режиме **update** не трогай их, если файл существует и непустой; генерируй только в режиме **init** или когда файла нет/он пуст. Затирать накопленное содержимое нельзя.

1. **`00-home/index.md`**: Карта всех файлов в Vault. На старте содержит ссылки на `[[текущие приоритеты]]`, `[[project-instructions]]`, `[[handoff]]`, `[[atlas/passport|паспорт проекта]]`, `[[atlas/архитектура проекта]]`, `[[atlas/база данных]]`, `[[atlas/деплой.md]]` и заглушки для подразделов в `knowledge/` и `sessions/`. Если `telethon_project == true`, добавь также ссылку на `[[knowledge/integrations/telethon-sessions|инструкцию по сессиям Telethon]]`. Если `tg_bot_project == true`, добавь также ссылку на `[[knowledge/patterns/tg-bot-ui-ux|инструкцию по UI/UX ботов Telegram]]`.
2. **`00-home/текущие приоритеты.md`**: Содержит текущий milestone и приоритетные задачи, извлеченные из GSD или Discovery (на старте).
3. **`project-instructions.md`** (в корне Vault — туда же пишет `/mm rules`, второго места быть не должно): Возьми `<skills_repo>/templates/project-instructions.md`, подставь `<PROJECT_NAME>`, замени пути к файлам на новые пути в структуре базы (например, `00-home/index.md` вместо `dashboard.md`), добавь топ-3 пункта из секции 8 паспорта.
   - Если `telethon_project == true`, добавь в инструкции для ИИ блок:
     * `Этот проект использует Telethon. При написании кода по работе с сессиями/аккаунтами руководствуйся правилами из [[knowledge/integrations/telethon-sessions.md]].`
   - Если `tg_bot_project == true`, добавь в инструкции для ИИ блок:
     * `При создании диалогов, кнопок, FSM-сценариев и форматировании сообщений следуй правилам из [[knowledge/patterns/tg-bot-ui-ux.md]].`
4. **`handoff.md` (в корне Vault)**: Скелет handoff (шаблон см. в Appendix). В режиме **update** не трогай, если файл уже существует.
5. **`passport.md`** (в корне Vault): Копия сгенерированного `<project_root>/passport.md`. Именно эту копию читают `/mm projects`, `clear-gate.py` и sync-check фазы 1f — `atlas/passport.md` не создавай, иначе появится вторая копия, которую никто не читает и которая разъедется по датам.
6. **`atlas/архитектура проекта.md`**: Содержит описание архитектуры из секции 3 паспорта.
7. **`atlas/база данных.md`**: Содержит модели данных из секции 6 паспорта.
8. **`atlas/деплой.md`**: Содержит инструкции и команды деплоя из секции 5/2 паспорта.
9. **`knowledge/integrations/telethon-sessions.md`** (только если `telethon_project == true`): скопируй содержимое из `<skills_repo>/templates/telethon-sessions.md`.
10. **`knowledge/patterns/tg-bot-ui-ux.md`** (только если `tg_bot_project == true`): скопируй содержимое из `<skills_repo>/templates/tg-bot-ui-ux.md`.

### 4.3. Сгенерируй патч для CLAUDE.md (если нужен)

Если CLAUDE.md существует **и** в нём нет секции `## Obsidian Knowledge Vault` — добавь в конец:

```markdown

## Obsidian Knowledge Vault
Хранилище знаний: <vault_path>

### При старте сессии
Прочитай 00-home/index.md и текущие приоритеты.md.
Если задача касается модуля — прочитай заметку из knowledge/.

### При завершении (пользователь: "сохрани сессию")
1. Создай заметку в sessions/ с датой
2. Обнови текущие приоритеты.md
3. Если решение — создай в knowledge/decisions/
4. Если баг — создай в knowledge/debugging/
5. Обнови index.md если новые заметки

## Режимы работы (IDE vs CLI)
1. **Если ты запущен в чат-окне Antigravity IDE (Gemini)**:
   - Ты выступаешь **исключительно как Планировщик и Архитектор**.
   - Тебе **категорически запрещено** самостоятельно изменять файлы проекта, записывать код в файлы или запускать изменяющие состояние команды (типа `git commit`, `git push`).
   - Твоя задача — использовать инструменты чтения (файлы, логи) и поиска, анализировать код, планировать изменения и генерировать готовый промпт для CLI-агента.
2. **Если ты запущен в консоли/терминале как CLI-агент (Claude Code / CLI-клиент)**:
   - Ты выступаешь как **Исполнитель**.
   - Ты должен автоматически вносить изменения в файлы, запускать тестов, делать коммиты и пушить изменения без подтверждений (согласно Karpathy-style discipline) на основе промптов, полученных из IDE.

## mm-system
Этот проект подключён к mm-системе.
- Паспорт: `passport.md` (актуальный source-of-truth)
- База знаний: `<vault_path>`
- Skills: глобальные `mm-*` (см. `~/.claude/skills/`)
- Конец сессии: `/mm-save-session`
- Перед новым чатом claude.ai: `/mm-handoff`

### Интеграция с Antigravity (Gemini IDE)
- Агент Antigravity поддерживает те же команды mm-системы.
- При получении команды (например `/mm resume`, `/mm save`, `/mm setup`, `где мы`, `сохрани сессию`) агент должен найти соответствующий SKILL.md по пути `~/.claude/skills/mm-<name>/SKILL.md` или в каталоге репозитория `$MM_REPO_ROOT/skills/mm-<name>/SKILL.md`, прочесть его и выполнить указанные в нем инструкции.
```

Где `<vault_path>` — это `.vault/` (если выбран локальный режим) или `<obsidian_projects>/<name>/` (если глобальный).

### 4.4. Запиши всё

В строгом порядке (с откатом при падении):
1. Создай директорию Vault (`<project_root>/.vault/` или глобальную) и все подпапки: `00-home/`, `atlas/`, `knowledge/integrations/`, `knowledge/decisions/`, `knowledge/debugging/`, `knowledge/patterns/`, `knowledge/business/`, `sessions/`, `inbox/`.
2. Запиши `<project>/passport.md`.
3. Запиши файлы в Vault:
   - `<vault>/00-home/index.md` (в режиме update — только если не существует или пуст)
   - `<vault>/00-home/текущие приоритеты.md` (в режиме update — только если не существует или пуст)
   - `<vault>/project-instructions.md`
   - `<vault>/handoff.md` (только если не существует)
   - `<vault>/passport.md`
   - `<vault>/atlas/архитектура проекта.md`
   - `<vault>/atlas/база данных.md`
   - `<vault>/atlas/деплой.md`
   - `<vault>/knowledge/integrations/telethon-sessions.md` (только если `telethon_project == true`)
   - `<vault>/knowledge/patterns/tg-bot-ui-ux.md` (только если `tg_bot_project == true`)
4. Если выбран локальный режим, открой `<project>/.gitignore`, и если в нём нет строки `.vault/.obsidian/` — добавь в конец:
   ```
   # Local Obsidian UI state
   .vault/.obsidian/
   ```
5. Если есть PROJECT_PASSPORT.md и пользователь подтвердил миграцию — переименуй в `.legacy`.
6. Примени патч к CLAUDE.md.

При ошибке на шагах 1-6: удали созданные файлы и папки, верни переименованный паспорт.

### 4.5. Проверка инвариантов + secret-grep

После записи проверь:
- `passport.md` содержит все 11 секций.
- Frontmatter валидный (parse YAML).
- В Obsidian нет файлов с похожими именами (`passport.md` vs `passport_old.md`) — если есть, предупреди.

**Secret-grep (критично — passport едет в claude.ai):**

Прогони passport.md через regex-поиск потенциальных секретов. **Паттерны — в каноне `<repo>/config/secret-patterns.json`** (Класс A — высокоточные, Класс B — широкие/warn-only; пояснение — `<repo>/docs/SECRET-PATTERNS.md`). Не дублируй их здесь — source of truth именно json.

Если что-то нашёл — **не молчи, не удаляй сам**. Покажи:
```
⚠️ В passport.md найдено что выглядит как секрет:
   Строка 47: TELEGRAM_TOKEN=12345...
   Строка 53: api_key: sk-abc123...

   passport.md загружается в claude.ai Project Knowledge → попадёт во внешний сервис.

   Действия:
   [1] Удалю секреты сам, оставлю плейсхолдер `<REDACTED>` — рекомендуется
   [2] Покажу строки, я отредактирую вручную, перезапусти /mm-init-project
   [3] Игнорировать (например это пример из docs)
```

Только после ответа юзера продолжай.

## Фаза 5. Финальный отчёт

```
✅ mm-init-project завершён

Режим: <init | update | migration>
Проект: <name>
Тип: <type> | Язык: <lang> | Стек: <главное>

Записано:
  ✓ <project>/passport.md
  ✓ <vault>/00-home/index.md (карта всех заметок; в update пропущен, если был непустой)
  ✓ <vault>/00-home/текущие приоритеты.md (активные приоритеты; в update пропущен, если был непустой)
  ✓ <vault>/project-instructions.md (инструкции для claude.ai)
  ✓ <vault>/handoff.md (скелет)
  ✓ <vault>/passport.md (копия паспорта)
  ✓ <vault>/atlas/архитектура проекта.md
  ✓ <vault>/atlas/база данных.md
  ✓ <vault>/atlas/деплой.md
  ✓ <vault>/knowledge/integrations/telethon-sessions.md (только если `telethon_project == true`)
  ✓ <vault>/knowledge/patterns/tg-bot-ui-ux.md (только если `tg_bot_project == true`)
  ✓ <project>/CLAUDE.md (добавлены правила Obsidian Knowledge Vault)
  <если локальный режим:>
  ✓ <project>/.gitignore (добавлен игнор .vault/.obsidian/)

Перенесено из старого паспорта (если миграция):
  ✓ Секция «Контекст для промптов» (5 правил)
  ✓ Секция «Текущее состояние» (3 пункта)
  Старый файл переименован: PROJECT_PASSPORT.md.legacy

Не тронуто:
  README.md, docs/, NOTES.md, .planning/, .env

Следующие шаги:
  1. Открой passport.md, проверь секции 1-7 (заполнены автоматически — могут быть неточны)
  2. Заполни секцию 8 «Контекст для промптов» — это критично
  3. claude.ai → New Project «<name>»
  4. Knowledge → загрузи passport.md и dashboard.md из Obsidian
  5. Instructions → скопируй из project-instructions.md
```

## Edge cases

- **Папка пустая, но git initialized без коммитов**: спрашивай как новый проект.
- **Имя папки с пробелами / кириллицей**: используй для отображения как есть; для slug в Obsidian (имя папки) — транслит в kebab-case.
- **Несколько языков** (моно-репо): тип = `multi`, перечисляй через запятую.
- **Symlinks / junctions в проекте**: не следуй по ним (Get-Item Attributes & ReparsePoint).
- **Скрытые .md** (`.DS_Store.md` или подобное мусорное): игнорируй файлы начинающиеся с точки (кроме `.planning/`).
- **Очень большой проект** (> 1000 .md файлов): сканируй только корень + 1 уровень глубже + `docs/`. Не углубляйся.
- **Vault недоступен** (путь из конфига не существует): останови, скажи `Obsidian vault не найден: <path>. Проверь mm-config.json или создай папку.`
- **Существующий passport.md в Obsidian отличается от проекта** (рассинхрон): предупреди — какую версию считать source-of-truth? Дефолт: проектная версия выигрывает.

## Что НЕ делать

- Не делать `git init`, `git add`, `git commit`, `git push` — никаких git-операций.
- Не читать значения из `.env`, `*.key`, `*.pem`, `secrets/`.
- Не редактировать README.md, ARCHITECTURE.md и любые другие .md **в корне проекта** (только passport.md и CLAUDE.md). Файлы внутри Obsidian-папки проекта — passport.md/dashboard.md/project-instructions.md — это разрешённый scope (см. контракт безопасности в начале skill).
- Не удалять файлы (только переименование с суффиксом `.legacy` при миграции).
- Не пропускать фазу Preview — даже если кажется «и так всё ясно».
- Не задавать больше 3-4 вопросов; для остального — разумные дефолты с пометкой `<assumed: ...>`.

## Appendix: шаблон dashboard.md

```markdown
---
project: <name>
updated: <date>
---

# <name> — Dashboard

## Сейчас
<пусто на старте — обновляется через /mm-save-session>

## Последние сессии
- <будут появляться после /mm-save-session>

## Открытые вопросы
- [ ] см. passport.md секция 10

## Ссылки
- Код: `<абсолютный путь к проекту>`
- Паспорт: [[passport]]
- Sessions: [[sessions/]]
- Handoff (для нового чата claude.ai): [[handoff]]
```

## Appendix: шаблон handoff.md (скелет на init)

На init кладётся именно этот скелет. Полноценный handoff (15-категорийный snapshot, выжимка сессий, GSD-контекст) генерирует `/mm-handoff` — он вызывается автоматически из `/mm-save-session` и заменяет скелет при первом же сохранении сессии.

```markdown
---
project: <name>
generated: <date>
covers_period: <date> — <date>
sessions_summarized: 0
---

# Handoff: <name>

> Этот файл загружается в Project Knowledge чата claude.ai вместе с passport.md.
> Обновляется автоматически при `/mm-save-session` (или вручную через `/mm-handoff` / `/mm next`).

## Сейчас в работе
<свежий проект — наполнится после первой рабочей сессии>

## Что сделано за период
Свежий проект, истории сессий ещё нет — см. [[passport]].

## Открытые вопросы
- [ ] см. [[passport]] секция 10

## Следующий логичный шаг
<определится после первой сессии>

## Где смотреть подробности
- Паспорт: [[passport]]
- Dashboard: [[dashboard]]
- Sessions: [[sessions/]]
- Код: `<абсолютный путь к проекту>`
```
