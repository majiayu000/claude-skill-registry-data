---
name: security-incident-response
description: "Run or document a security incident response — contain, eradicate, recover, and learn. Use when responding to a breach/compromise/security incident, writing an IR plan or runbook, or producing a post-incident report. For incidents on systems you own or defend."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# security-incident-response

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

Produces a phase-by-phase response (triage, contain, eradicate, recover, post-incident) with the immediate actions, comms, evidence-handling, and a blameless review.
