---
name: deep-research
description: 'Run a disciplined, multi-source research investigation for a high-stakes
  question or decision — fan-out web search across many channels, parallel sub-agents,
  source triangulation (each claim backed by ≥3 independent sources), an adversarial
  review pass, and every source saved to its own file with verbatim quotes for reuse.
  Use when a low-quality answer is expensive: strategy work, comparing N products/methods/markets,
  validating a hypothesis with external data, or mapping how a field works. NOT for
  quick fact-checks (answer directly), structured 12-dimension competitor scoring
  (use competitive-teardown), or fast topic overviews where the decision risk is low
  (use the research router instead).'
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# deep-research

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

