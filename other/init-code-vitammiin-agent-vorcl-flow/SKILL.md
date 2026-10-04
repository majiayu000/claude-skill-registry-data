---
name: init-code
description: "Статически исследует репозиторий и создаёт evidence-based PROJECT_DESCRIPTION.md с назначением, запуском, стеком, структурой, data flow, тестами, конфигурацией и unknowns. Use для onboarding или инициализации описания существующего кода; не создаёт AGENTS.md и не исполняет target code."
---

# Init Code

Создай описание через canonical `$init-code` workflow:

1. Запусти `node <skill-root>/scripts/inspect.mjs --root <repo> --format json`.
2. Статически проверь найденные manifests, entrypoints, routes, schemas, CI и test configs. Не запускай код, hooks или package scripts целевого проекта.
3. Запиши `PROJECT_DESCRIPTION.md` с разделами `Purpose`, `How to Run`, `Technology`, `Structure`, `Runtime and Data Flow`, `Testing`, `Configuration and Integrations`, `Evidence and Unknowns`.
4. Подкрепляй каждый факт относительным путём в бэктиках; помечай inference и unknowns. Не раскрывай значения `.env`/секретов.
5. Если файл существует, без `--update` не перезаписывай его: создай timestamped sibling. Проверь `node <skill-root>/scripts/validate-description.mjs <file>`.

Работай в `report-only`: разрешён только явно запрошенный Markdown-артефакт, без Task Master и production/config/data mutations.

После создания `PROJECT_DESCRIPTION.md` поддерживается общим `$workflow`: любая изменяющая роль читает его до работы, запускает `scripts/check-impact.mjs` по своим changed paths и обновляет только разделы, контекст которых действительно изменился. После обновления повторно запускается `validate-description.mjs`.
