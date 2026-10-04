---
name: booster-refactor
description: |
  Безопасный рефакторинг с анализом области влияния и обязательной верификацией после изменений.
---

# booster Refactor

## Цель

Менять структуру кода без изменения поведения.

## Алгоритм

```text
code_grep("<symbol>")
project_memory_recall(query="refactor <symbol>")
impact_analysis(target="<symbol>", max_depth=4)
call_graph("<symbol>")
import_graph("<file>")
read_with_context("<file>", line=<line>, context=80)
git_intelligence(path="<file>", symbol="<symbol>", limit=15)
find_duplicates(min_lines=4)
collect_diagnostics(paths=["<file>"])
run_validation_checks(commands=["<tests before>"], paths=["<file>"])
run_validation_checks(commands=["<tests after>"], paths=["<file>"])
git_diff("<repo or file>")
```

## Правила

- сначала определить все usages
- сначала получить blast radius через impact_analysis
- не смешивать рефакторинг и новую фичу
- при переносе символа оставлять совместимый импорт, если нужно
- проверять diagnostics и тесты до и после

## Когда остановиться

- если зона влияния неожиданно выросла
- если нет тестов и меняется критичный путь
