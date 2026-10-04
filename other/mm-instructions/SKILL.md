---
name: mm-instructions
version: 0.5.1
description: Генерирует текст для claude.ai → Project → Instructions из шаблона + персонализирует под текущий проект. Кладёт результат в Obsidian для копипаста. Use when user says "сделай инструкции для проекта", "обнови project instructions", "/mm-instructions", "перегенери инструкции", "что вставить в Project Instructions". Без аргументов = универсальная версия; с проектом = подставляет имя.
---

# mm-instructions — claude.ai Project Instructions Generator

Создаёт ready-to-paste текст для **Project Instructions** в claude.ai. Это «инструкция» для веб-Клода: как работать в паре с PowerShell-Клодом и mm-системой. Раз сгенерировал — копипастишь в Project, оно живёт там вечно.

## Конфиг

Загрузи `mm-config.json` по алгоритму из `<repo>/docs/CONFIG-LOADING.md`. Поддержка `mm-config.local.json` overlay обязательна. `<repo>` берётся из `_repo_root` инжектированного в конфиг loader'ом.

Понадобятся:
- `paths.obsidian_projects`
- `paths.obsidian_bridge` (универсальная версия идёт сюда)
- `default_language`
- `_repo_root` (для шаблона `templates/project-instructions.md`)

## Режимы

### A. Для конкретного проекта

Запуск из папки с `passport.md`. Скилл:
1. Читает `passport.md` → берёт `project` из frontmatter, тип, стек, `gsd_version` из frontmatter, секцию 8 «Контекст для промптов», секцию 9 (текущий milestone/phase, если GSD).
2. Берёт шаблон `<skills_repo>/templates/project-instructions.md`.
3. Подставляет:
   - `<PROJECT_NAME>` → имя проекта.
   - **GSD-блок** (между `GSD-BLOCK-START`/`GSD-BLOCK-END`): если `gsd_version != none` — заполняет `<GSD_VERSION>` и `<GSD_CURRENT_PHASE>`; иначе **удаляет блок целиком**.
   - В конец добавляет секцию **«Особенности этого проекта»** с топ-3 строками из секции 8 паспорта (как напоминание Клоду в каждом промпте).
4. Сохраняет в `<obsidian_projects>/<project>/project-instructions.md` (перезапись).

### B. Универсальная версия

Запуск без `passport.md` или с флагом «универсальная» / «общая». Скилл:
1. Берёт шаблон as-is.
2. `<PROJECT_NAME>` заменяет на `<универсальный — определяется в чате>`; `<USER_NAME>` — на `config.user.name`.
3. Удаляет секцию «Особенности этого проекта» **и GSD-блок** (универсальной комнате конкретный GSD неизвестен).
4. Сохраняет в `<obsidian_bridge>/project-instructions-universal.md`.

Эту версию вставляешь в Project, который ты используешь как **«комната для идей»** — где ещё нет конкретного проекта, или где обсуждаешь общие задачи.

## Процесс

### Шаг 1. Определи режим

- В cwd есть `passport.md` → режим A, имя из frontmatter.
- Нет → спроси: `Универсальная версия (1) или укажи путь к passport.md (2)?`

### Шаг 2. Прочитай шаблон

`<skills_repo>/templates/project-instructions.md`. Скопируй в память как строку.

### Шаг 3. Подстановки (режим A)

Замени все вхождения `<PROJECT_NAME>` на реальное имя.

Замени все вхождения `<USER_NAME>` на `config.user.name` (из mm-config, с учётом local-оверлея). Если поля нет — оставь нейтральное «разработчика».

**GSD-блок** (между `<!-- GSD-BLOCK-START ... -->` и `<!-- GSD-BLOCK-END -->`):
- Если `gsd_version != none`: замени `<GSD_VERSION>` на `v1 (.planning/)`, `v2 (.gsd/)` или `core (.planning/ config.json)`, `<GSD_CURRENT_PHASE>` — на текущую фазу из секции 9 паспорта (или `см. STATE.md`, если не указана). Сами маркеры-комментарии удали.
- Если `gsd_version == none` (или поля нет): **удали весь блок целиком** вместе с маркерами — у проекта нет GSD, незачем путать веб-Клода.

В конец файла, перед последней секцией «Доступные команды», вставь:

```markdown
# Особенности этого проекта (топ-правила из паспорта)

> Сверяй каждый сгенерированный промпт с этими правилами. Они жёсткие.

<до 5 пунктов из секции 8 паспорта, точная копия — без перефразирования>
```

### Шаг 4. Сохрани

- A: `<obsidian_projects>/<project>/project-instructions.md`
- B: `<obsidian_bridge>/project-instructions-universal.md`

Если файл уже был — не архивируй, перезаписывай (это деривативный артефакт, оригинал всегда можно перегенерить).

### Шаг 5. Подтверди

```
✅ Project Instructions готовы

Режим: <A для проекта <name> | B универсальная>
Файл: <abs_path>
Длина: ~<N> строк

Что делать:
1. Открой файл, скопируй ВСЁ содержимое
2. claude.ai → Project «<name>» → Settings → Instructions
3. Удали старое, вставь новое, Save
4. Проверь: New Chat → "Что ты делаешь?" — должен ответить про режимы A/B/C
```

## Edge cases

- **Шаблон отсутствует** (`templates/project-instructions.md` нет): скажи `Не найден шаблон: <_repo_root>/templates/project-instructions.md. Возможно, markdown-memory не до конца установлен — проверь git pull в репо (см. $env:MM_REPO_ROOT).`
- **Секция 8 паспорта пустая** (только TODO-маркер): пропусти секцию «Особенности этого проекта», предложи `Заполни сначала секцию 8 в passport.md, потом перегенери.`
- **Имя проекта с пробелами** (плохая практика): пройдёт, но в файле проекта в Obsidian используй slug.

## Что НЕ делать

- Не вставляй в инструкции живые секреты, ENV-значения, токены.
- Не делай инструкции длиннее 1.5 страниц — Claude.ai всё равно ужмёт восприятие.
- Не выдумывай правила «от себя» — только то, что в шаблоне или явно в паспорте.
