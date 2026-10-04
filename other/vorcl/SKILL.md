---
name: vorcl
description: "Универсальный scoped Task Master orchestrator: фиксирует IDs текущей цели, атомарно claim-ит их и делегирует реализацию и независимую проверку. Use для нетривиальной tracked/remediation цели любого домена."
---

# Scoped goal orchestrator

Сначала выбери режим из `$workflow`: report-only пишет только явно запрошенный report artifact, но не `.taskmaster`/product state; track-only не меняет product code; remediation разрешает изменения в границах запроса.

До создания задач примени `$workspace-capability-routing`: сопоставь requested outcome с manifests/entrypoints/configs текущего workspace, выбери одного primary owner и только необходимые supporting roles/skills. Не маршрутизируй по incidental runtime.

Для persistent режима:

1. `add_task`/`parse_prd`; сохрани только возвращённые IDs.
2. Создай scoped run через `$workflow`; atomic claim каждого ID → `get_task` → `set_task_status in-progress`. Bare `next_task` запрещён.
3. Профильный Executor, выбранный по workspace evidence и capability catalog, работает только над claimed ID.
4. Отдельный Checker выполняет `testStrategy`, не редактируя implementation/acceptance tests.
5. Только Orchestrator ставит `done`; цикл ограничен IDs run.

Короткий router: architecture — `$architect`, `$principal-architect`, `$archmap`; implementation — `$backend`, `$frontend`, `$expo-mobile`; audits/contracts — `$analyzer`, `$integrity`, `$security`, `$resilience`, `$logging`, `$swagger`; data/platform — `$database`, `$render`, `$devops`; visual/source — `$screenshot`, `$design-studio`, `$visual-research`, `$pinpoint`; artifacts — `$drawio`, `$mermaid`, `$docs`; verification/release — `$testing`, `$gitflow`; research/operations — `$firecrawl`, `$liveboard`.

Targeted hardcode/mock → `$integrity`; broad code-quality audit → `$analyzer`. Полный multi-language architecture package → `$principal-architect`; лёгкая TS/JS dependency map → `$archmap`. Неочевидную междоменную архитектуру начинает `$architect`.
