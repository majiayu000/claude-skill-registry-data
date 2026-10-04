---
name: booster-feature-add
description: |
  Безопасное добавление новой фичи в существующую архитектуру через паттерны уже написанного кода.
---

# booster Feature Add

## Цель

Перед реализацией найти правильное место, стиль и аналог существующей фичи.

## Алгоритм

```text
project_memory("get", "architecture_overview", repo="<repo>")
project_memory_recall(query="<feature description>", repo="<repo>")
preflight_analysis(task="<feature description>", target="<suspected symbol>", repo="<repo>")
semantic_search("<feature description>")
find_symbol("<related class or service>")
impact_analysis(target="<related class or service>", repo="<repo>", max_depth=3)
read_with_context("<analog file>", line=<line>, context=60)
call_graph("<neighbor symbol>")
import_graph("<target file>")
git_intelligence(symbol="<related class or service>", repo="<repo>", limit=8)
external_deps("<neighbor symbol>")
find_duplicates(min_lines=3)
```

## До написания кода выясни

- куда добавлять реализацию
- есть ли аналог или шаблон
- какие зависимости уже используются
- нужен ли тест и конфиг
- какие diagnostics уже есть в затронутых файлах
- какой blast radius у основного символа

## После реализации

```text
find_symbol("<new symbol>")
collect_diagnostics(paths=["<changed file>"], repo="<repo>")
validation_loop_plan(task="<feature description>", changed_paths=["<changed file>"], repo="<repo>")
run_validation_checks(commands=["<project tests>"], paths=["<changed file>"], repo="<repo>")
booster.task_complete(task_id="<task-id>", repo_paths=["<repo>"])
project_memory("set", "feature_<name>", "...", repo="<repo>")
remember_project_fact(category="feature", fact="<what changed and why>", repo="<repo>")
```

`booster.task_complete()` is the lifecycle boundary for the agent task. It
queues a final bounded reindex and preserves the generated artifacts in an
immutable snapshot keyed by the current git commit and artifact digest.
