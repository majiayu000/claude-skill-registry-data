---
name: signature-pipeline-watch
description: "Have a proactive agent watch documents waiting for signature in DocuSign, Adobe Sign or PandaDoc: which are stuck, for how long, with whom, which have expiry dates coming, and which signed ones still need countersigning or filing, reported in the brief with drafted reminders a human sends. Use when asked to track contracts waiting for signature, chase unsigned DocuSign envelopes, have Duet watch my e-signatures, what contracts are stuck, or remind me about documents nobody has signed."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# signature-pipeline-watch

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

Produces the watch rules, the pipeline lines by stage and age, the drafted reminder per stuck envelope, and the interrupt rule for expiring envelopes.
