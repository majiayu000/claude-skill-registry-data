---
name: booster-review
description: |
  Глубокий code review с проверкой безопасности, архитектуры, производительности и качества.
---

# booster Review

## Цель

Найти реальные риски, а не просто стилистические замечания.

## Алгоритм

```text
git_diff("<path>")
git_intelligence(path="<path>", limit=5)
project_memory_recall(query="review <path>")
read_with_context("<file>", line=1, context=200)
find_symbol("<main changed symbol>")
impact_analysis(target="<main changed symbol>", max_depth=3)
call_graph("<main changed symbol>")
import_graph("<file>")
external_deps(file="<file>")
collect_diagnostics(paths=["<file>"], include_security=true)
code_grep("TODO|FIXME|HACK|password|secret|eval|exec")
run_validation_checks(commands=["<tests>"], paths=["<file>"])
```

## Проверяй явно

- инъекции
- секреты в коде
- нарушения слоёв
- ломаную обратную совместимость
- синхронный I/O на горячих путях
- новые или скрытые diagnostics
- security findings из bandit/semgrep/cargo audit, если инструменты доступны

## Формат вывода

1. критичные риски
2. важные замечания
3. остаточные риски и пробелы тестов
