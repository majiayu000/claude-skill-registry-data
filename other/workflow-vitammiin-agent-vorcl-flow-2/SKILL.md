---
name: workflow
description: "Безопасный scoped Task Master workflow: captured task IDs, atomic claim, независимый Checker и явные report-only/track-only/remediation режимы. Use для нетривиальной реализации или persistent task tracking."
---

# Workflow

## Режим

- **report-only** — только ответ или явно запрошенный audit/report artifact; без `.taskmaster`, product/config/data writes.
- **track-only** — разрешены task metadata, но не product code.
- **remediation** — задачи и код в пределах запроса пользователя.

Не повышай режим автоматически. Нетривиальная реализация идёт через `$task-master`; report-only — через эфемерный план.

## Scoped run

1. Создай задачи через `add_task`/`parse_prd` и сохрани IDs прямо из результата write-операции. Bare `next_task` по общему backlog запрещён.
2. Создай run: `node <workflow-skill>/scripts/vorcl-run.mjs create --run <run-id> --tasks <id,id> --owner <agent> --root <project>`.
3. Для каждого allowlisted ID: `claim --run <run-id> --task <id>` → `get_task <id>` → проверь статус → `set_task_status in-progress`. Долгая работа обновляет lease через `renew`; истёкший claim забирается только явным `reclaim --from-run <expected-old-run>`. Crashed operation-lock снимается после указанного expiry командой `unlock --expected-lock <id>`.
4. Executor реализует только claimed task. `update_subtask` допустим лишь для существующего subtask; top-level progress фиксируй в доступном task note/evidence, не выдумывай subtask ID.
5. Checker в отдельном контексте запускает `testStrategy`, не меняет implementation и acceptance tests, возвращает `ГОТОВО`/`НЕ ГОТОВО` с выводом.
6. Только Orchestrator ставит `done`. Цикл заканчивается по allowlist run, а не по всему repository backlog.

## PROJECT_DESCRIPTION maintenance

Это общий Definition of Done для любой изменяющей роли.

1. До реализации проверь `<scope-root>/PROJECT_DESCRIPTION.md`. Если файл существует, прочитай его до изменения кода; если отсутствует — не создавай автоматически.
2. После реализации перед Checker собери только changed paths текущей задачи и запусти, если доступен:

   ```bash
   node <init-code-skill>/scripts/check-impact.mjs --root <scope-root> --changed <path> [--changed <path> ...] [--external <kind[:detail]> ...]
   ```

3. Передавай `--external` для выполненных вне worktree мутаций (`render-deploy`, `environment`, `integration`, `database-schema`, `runtime`), даже если changed paths пусты. При `review-required` сравни файловый diff и external mutations с утверждениями документа. Material impact есть, когда изменились назначение/возможности, команды запуска/build/test, стек/runtime, packages/modules/boundaries/entrypoints/routes, data flow/schema, integrations, env names, testing/CI/deploy context.
4. Если material impact подтверждён, в той же задаче обнови только затронутые разделы `PROJECT_DESCRIPTION.md`, сохрани корректные пользовательские пояснения, замени stale evidence paths и запусти `validate-description.mjs` из `$init-code`.
5. Если material impact отсутствует, документ не редактируй; передай Checker краткое evidence-based объяснение `description impact: none`.
6. Изменение контекста при оставшемся stale `PROJECT_DESCRIPTION.md` означает **НЕ ГОТОВО**. Report-only роли и Checker сами этот файл не исправляют.

Роли для маршрутизации: `architect`, `principal-architect`, `backend`, `frontend`, `expo-mobile`, `analyzer`, `integrity`, `swagger`, `firecrawl`, `render`, `database`, `resilience`, `logging`, `screenshot`, `design-studio`, `visual-research`, `pinpoint`, `drawio`, `archmap`, `mermaid`, `testing`, `gitflow`, `security`, `docs`, `devops`, `liveboard`. Канонические ownership/negative criteria находятся в registry пакета.

## Запреты

- Не брать ID, не созданный текущим run.
- Не работать без успешного atomic claim и `in-progress`.
- Не закрывать без независимого verdict и evidence.
- Не закрывать modifying task с подтверждённым дрейфом существующего `PROJECT_DESCRIPTION.md`.
- Не писать Task Master или product state в report-only.
