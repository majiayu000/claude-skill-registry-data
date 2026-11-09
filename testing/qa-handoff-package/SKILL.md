---
name: qa-handoff-package
description: "Turn a story and its change into a clean 'ready for QA' package — test scenarios, edge cases, the data and environment setup, and what's explicitly out of scope. Use when asked to prep a QA handoff, what should QA test here, write test scenarios for this story, or make this ready for QA."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# qa-handoff-package

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

## Требования к результату

Produces the scenarios mapped to acceptance criteria, the edge/negative cases devs forget, the exact data and environment setup to reproduce, the risk areas to probe, and the out-of-scope list so QA doesn't chase the wrong things.
