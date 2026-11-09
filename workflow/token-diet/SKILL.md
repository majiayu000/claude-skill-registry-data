---
name: token-diet
description: "Cut LLM output tokens 40–70% by stripping grammatical scaffolding while preserving every fact — telegraphic output modes, when they pay (pipelines, long sessions) and when they don't (single shots, human-facing prose), with the mode lines to switch on demand. Use when asked make the model respond tersely, cut output token costs, caveman mode, or compress agent-to-agent messages."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# token-diet

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

Produces the diet-mode instruction block ready to paste, the three compression levels with examples, the economics of when each pays, and the never-diet list.
