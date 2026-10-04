---
name: mm-setup
version: 0.1.0
description: Онбординг/персонализация mm-системы под конкретного пользователя — спрашивает имя, чем занимается, стек, язык, путь к Obsidian vault, и записывает это в личный gitignored-оверлей config/mm-config.local.json + генерирует персональную копию claude.ai-скилла mm-web-bridge. Use when user says "/mm setup", "/mm onboard", "настрой под меня", "персонализируй", "первичная настройка", "сделай систему моей", "это не моё имя в скилле", "поменяй данные под меня". Запускать ОДИН раз после клонирования репо на новой машине.
---

# mm-setup — Персонализация mm-системы под пользователя

Делает систему «своей»: имя, домен, стек, пути — без правки committed-файлов (репо общий, расшарен на GitHub). Личное идёт в **gitignored** оверлей и в **генерируемую** персональную копию claude.ai-скилла.

## Контракт безопасности (соблюдай дословно)

**Skill ПИШЕТ только в:**
- `<repo>/config/mm-config.local.json` — создаёт или мёрджит (gitignored, личный оверлей)
- `<repo>/claude-ai-skills/_generated/mm-web-bridge/SKILL.md` — персональная копия для загрузки в claude.ai (gitignored)

**Skill НИКОГДА не трогает:**
- `config/mm-config.json` (committed — общие дефолты louise; их не перезаписываем)
- `claude-ai-skills/mm-web-bridge/SKILL.md` (committed шаблон — читаем как источник, не правим)
- любые `skills/*/SKILL.md`, `~/.claude/CLAUDE.md` (для глобального — только предложим сниппет)
- git-операции

## Конфиг

Загрузи `mm-config.json` по алгоритму из `<repo>/docs/CONFIG-LOADING.md` (нужен `_repo_root`). Если уже есть `mm-config.local.json` — прочитай его как текущие значения (режим повторной настройки).

## Шаг 1. Интервью

Задай **одним сообщением** (не по одному вопросу), с разумными дефолтами в скобках:

```
Настрою mm-систему под тебя. Ответь (можно коротко):
1. Имя — как тебя называть? <текущее из config, если есть>
2. Чем занимаешься / домен? (например: «Telegram-боты», «веб на React», «data-инженерия»)
3. Основной стек? (язык · фреймворк · БД · деплой — например «Python · aiogram 3.x · SQLite · Railway»)
4. Язык общения по умолчанию? (ru / en) <текущий default_language>
5. Путь к Obsidian vault? <текущий obsidian_vault, или предложи C:\Users\<user>\Documents\Obsidian Vault>
```

Дополнительно (не спрашивай, выведи сам):
- `<user>` для дефолтных путей возьми из `$env:USERPROFILE` / `~`.
- Если на п.5 дают только vault — остальные obsidian-пути (`Claude/`, `Bridge/`, `Sessions/`, `Projects/`, `INDEX.md`) выведи относительно него по той же структуре, что в committed `mm-config.json`.
- Если пользователь говорит «как у тебя в дефолте / пропусти» — оставь committed-значение (не дублируй его в local без нужды).

## Шаг 2. Покажи план (preview перед записью)

```
📋 Запишу в config/mm-config.local.json (личный, gitignored):
  user.name        = <name>
  user.domain      = <domain>
  user.stack       = <stack>
  default_language = <lang>
  paths.obsidian_* = <выведенные из vault пути>

📋 Сгенерирую claude.ai-скилл:
  claude-ai-skills/_generated/mm-web-bridge/SKILL.md
  (персональная копия — louise/Telegram заменены на <name>/<domain>/<stack>)

Committed-файлы НЕ трогаю. Продолжить? (y / n / правки)
```

Без `y` — ничего не пишется.

## Шаг 3. Запиши mm-config.local.json

Сформируй/обнови `<repo>/config/mm-config.local.json`. Только изменённые относительно дефолта ключи (deep-merge поверх committed). Минимум:

```json
{
  "default_language": "<lang>",
  "user": {
    "name": "<name>",
    "domain": "<domain>",
    "stack": "<stack>"
  },
  "paths": {
    "obsidian_vault": "<...>",
    "obsidian_claude_root": "<...>\\Claude",
    "obsidian_bridge": "<...>\\Claude\\Bridge",
    "obsidian_bridge_archive": "<...>\\Claude\\Bridge\\archive",
    "obsidian_sessions": "<...>\\Claude\\Sessions",
    "obsidian_projects": "<...>\\Claude\\Projects",
    "obsidian_index": "<...>\\Claude\\INDEX.md"
  }
}
```

Если файл уже есть — мёрджи, не затирай чужие ключи. Пути — в формате текущей ОС (Windows — `\\`).

## Шаг 4. Сгенерируй персональный mm-web-bridge

1. Прочитай committed-шаблон `<repo>/claude-ai-skills/mm-web-bridge/SKILL.md`.
2. Сделай **персональную копию**, заменив louise-специфику на данные пользователя:
   - имя «louise» → `<name>` (везде);
   - строку про стек/домен (абзац «louise работает на русском. Её типичный стек: …») → под `<domain>` и `<stack>` пользователя;
   - в **Принципе 1 (веб-проверка)** примеры «Telegram Bot API / aiogram» → под технологии из `<stack>` пользователя (если стек неизвестен/общий — оставь обобщённо «внешние API/библиотеки/фреймворки» без конкретики, но сам принцип сохрани — он универсален);
   - язык изложения — под `<lang>` (если en — можно перевести ключевые формулировки; если ru — оставь как есть).
   - `description` во frontmatter — тоже под пользователя (имя + домен + что следить за актуальностью именно его стека).
3. Сохрани в `<repo>/claude-ai-skills/_generated/mm-web-bridge/SKILL.md`.
4. **Не меняй смысл и структуру** скилла (три принципа, режимы A/B/C, GSD, конвенция «вариант N») — только идентичность/домен/стек.

## Шаг 5. Финальный отчёт + следующие шаги

```
✅ mm-system персонализирована под <name>

Записано:
  ✓ config/mm-config.local.json (личный оверлей)
  ✓ claude-ai-skills/_generated/mm-web-bridge/SKILL.md (для claude.ai)

Дальше:
  1. Загрузи claude.ai-скилл: заархивь _generated/mm-web-bridge/ → claude.ai → Customize → Skills → Upload a skill
     (или Write skill instructions и вставь содержимое SKILL.md)
  2. Прогони npx markdown-memory (или python3 scripts/register-skills.py) — регистрация скиллов mm-* в ~/.claude/skills/
  3. /mm check — проверь, что vault и пути на месте
  4. /mm new — оформи первый проект

Хочешь — выведу сниппет для ~/.claude/CLAUDE.md (глобальные правила под тебя)? Сам файл не трогаю (он вне репо).
```

Если пользователь просит сниппет CLAUDE.md — выведи готовый текст (имя, что mm подключён, ссылку на /mm), но **вставляет он сам**.

## Edge cases

- **Повторный запуск** (local уже есть): покажи текущие значения, спроси что менять, мёрджи.
- **Vault по указанному пути не существует**: предупреди, предложи создать папки (это безопасно) или поправить путь.
- **Пользователь = louise / её данные**: всё равно отработай — просто значения совпадут с committed-дефолтами (local будет минимальным).
- **Нет committed mm-web-bridge** (репо неполный): пропусти шаг 4 с предупреждением, config всё равно запиши.
- **Не Windows** (если когда-нибудь): пути в формате текущей ОС, `~` вместо `C:\Users\<user>`.

## Что НЕ делать

- Не писать личные данные в committed `mm-config.json` или committed `mm-web-bridge/SKILL.md` — только в local/_generated.
- Не делать git add/commit.
- Не править `~/.claude/CLAUDE.md` напрямую — только предложить сниппет.
- Не пропускать preview (шаг 2).
