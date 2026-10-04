---
name: booster-cognitive-runtime
description: |
  Cognitive Runtime для coding agents: AST impact graph, git intelligence,
  долгосрочная project memory, diagnostics и validation loop.
---

# Booster Cognitive Runtime

## Цель

Дать агенту восприятие уровня IDE + Git + архитектурной памяти перед тем, как
он меняет код, и после изменения прогнать инженерную петлю проверки.

## Preflight перед изменением

```text
project_memory_recall(query="<task>", repo="<repo>")
preflight_analysis(task="<task>", target="<symbol>", paths=["<file>"], repo="<repo>")
impact_analysis(target="<symbol>", repo="<repo>", max_depth=3)
git_intelligence(path="<file>", symbol="<symbol>", repo="<repo>", limit=8)
collect_diagnostics(paths=["<file>"], repo="<repo>", include_security=true)
```

Diagnostics включает внутреннюю Python syntax-проверку без subprocess, Ruff,
Pyright, TypeScript, Rust и security scanners, если соответствующие инструменты
доступны. Любой timeout или crash анализатора считается ошибкой проверки.

## Validation Loop после patch

```text
validation_loop_plan(task="<task>", changed_paths=["<file>"], repo="<repo>")
run_validation_checks(commands=["<focused test>"], paths=["<file>"], repo="<repo>")
```

## Что возвращать пользователю

- область влияния и риск
- существующие diagnostics до изменения
- git-причину исторического кода, если она есть
- какие проверки запущены
- что осталось непроверенным

## Правила

- Не полагайся только на embeddings, если есть символ и граф.
- Не игнорируй красные diagnostics в затронутых файлах.
- Не считай validation успешной, если diagnostic tool упал, завис или вернул
  непарсимый вывод.
- Не исправляй чужие старые ошибки вне задачи без явной необходимости.
- Сохраняй устойчивые выводы через `remember_project_fact`.
