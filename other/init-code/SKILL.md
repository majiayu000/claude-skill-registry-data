---
name: init-code
description: "Статически исследует существующий репозиторий и создаёт evidence-based PROJECT_DESCRIPTION.md: назначение, запуск, стек, структуру, runtime/data flow, тестирование, конфигурацию, интеграции и явно неизвестные области. Use при первом знакомстве с кодовой базой, onboarding, инициализации project context или обновлении устаревшего описания; не исполняет недоверенный код и не создаёт CLAUDE.md/AGENTS.md."
---

# Init Code

Создавай короткое описание фактического кода, а не инструкции агенту и не roadmap.

## Workflow

1. Определи root из аргумента, иначе используй текущий каталог. Не запускай package scripts, build, tests, hooks или код целевого проекта.
2. Запусти детерминированный inventory:

   ```bash
   node <skill-root>/scripts/inspect.mjs --root <repo> --format json
   ```

3. Проверь ключевые manifests, entrypoints, routes, schemas/migrations, CI, контейнеры и test configs, найденные inventory. Не считай имя каталога или README достаточным доказательством поведения.
4. Создай `PROJECT_DESCRIPTION.md`. Если он уже существует, без `--update` создай `PROJECT_DESCRIPTION-YYYYMMDD-HHMM.md`; никогда не затирай молча. С `--output <file>` используй явно заданный путь внутри scope.
5. Используй разделы строго в этом порядке:
   - `Purpose`
   - `How to Run`
   - `Technology`
   - `Structure`
   - `Runtime and Data Flow`
   - `Testing`
   - `Configuration and Integrations`
   - `Evidence and Unknowns`
6. Каждый фактический абзац или строку таблицы подкрепляй относительным путём в бэктиках. Если связь не подтверждена статически, пиши `Inference` с основанием; отсутствие доказательств переноси в unknowns.
7. Не копируй секреты и значения `.env`: разрешены только имена переменных из `.env.example` или кода. Не включай большие деревья файлов, полный dependency dump, рекламные формулировки, roadmap или советы по переписыванию.
8. Проверь результат:

   ```bash
   node <skill-root>/scripts/validate-description.mjs <description.md>
   ```

## Output contract

- Лид отвечает «что делает проект и для кого» в 2–4 предложениях.
- Команды приводятся только из manifest/Makefile/task config; если безопасная команда не найдена — `Not detected`.
- Data flow начинается с реального entrypoint/route и заканчивается подтверждённой границей; неподтверждённые звенья не дорисовываются.
- Unknowns включают coverage gaps, malformed manifests, symlinks и вопросы, которые нельзя решить чтением кода.
- Итог сообщает output path, detected systems, validator result и какие части остались inference.

## Maintenance contract

После создания файл становится частью Definition of Done `$workflow` для всех изменяющих ролей. Перед изменением агент читает существующий `PROJECT_DESCRIPTION.md`; после изменения запускает `scripts/check-impact.mjs` по changed paths и семантически сравнивает diff с документом. Обновляй только реально затронутые разделы и снова запускай `validate-description.mjs`. Не обновляй файл из-за форматирования, внутреннего рефакторинга без изменения описанного контекста или чужих изменений вне текущей задачи.
