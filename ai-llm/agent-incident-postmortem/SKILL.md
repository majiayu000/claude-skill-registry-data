---
name: agent-incident-postmortem
description: "Run a blameless postmortem for an incident caused by an AI agent or LLM feature — hallucinated facts shipped to users, runaway tool use, prompt injection, cost blowouts, or wrong actions taken autonomously. Use when asked to write up an AI incident, analyse why an agent did something wrong, or produce corrective actions after an LLM failure. For non-AI production incidents use incident-postmortem."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# agent-incident-postmortem

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

Produces a structured postmortem with trace reconstruction, a root-cause layer analysis, and corrective actions including a permanent regression case.
