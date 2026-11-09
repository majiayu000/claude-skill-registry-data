---
name: voice-agent-design
description: "Design a voice AI agent for phone or in-app conversations — call flows, interruption handling, escalation to humans, and the metrics that catch a bad voice experience. Use when asked to design a voice agent, automate a phone line, spec an IVR replacement, or review why callers hate an existing voice bot."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# voice-agent-design

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

Produces a voice agent spec: persona and disclosure policy, conversation architecture, barge-in and repair behaviour, human-handoff rules, and a launch scorecard.
