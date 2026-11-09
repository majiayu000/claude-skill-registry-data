---
name: morning-brief-designer
description: "Design a proactive agent's morning brief: which connected sources it reads, what earns a line, the fixed section order and length cap, and the wording rules that keep it honest. Use when asked to design my morning brief, set up what Duet tells me each morning, make my daily brief shorter or more useful, or decide what belongs in a daily agent summary."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# morning-brief-designer

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

Produces a brief specification the agent follows every morning: sources, selection rules, an 8-line template with citations, and what to leave out.
