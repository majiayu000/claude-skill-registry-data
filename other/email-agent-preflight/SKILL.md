---
name: email-agent-preflight
description: "Run the pre-flight checklist before an agent touches an inbox — the read-vs-send permission line, the injection-in-email-body threat, the send-guard rules, and the blast-radius limits that keep a compromised agent from mailing the company. Use when asked let my agent read/send email safely, set up guardrails before the agent touches my inbox, is it safe to give the agent email access, or review my email agent's permissions."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# email-agent-preflight

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

Produces the permission tier, the injection defenses, the send-gate rules, and the incident kill-switch.
