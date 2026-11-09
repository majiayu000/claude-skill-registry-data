---
name: prescription-refusal-to-fill
description: "Handle a prescription you are not going to dispense — the professional judgement recorded, the patient conversation, the prescriber contact, and the continuity of care that stops a refusal becoming abandonment. Use when asked how to refuse to fill a prescription, decline to dispense, handle a suspected forgery or early refill, or document a corresponding-responsibility decision. Legal obligations vary by jurisdiction; verify yours."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# prescription-refusal-to-fill

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

Produces the decision record, the conversation script, the prescriber contact, the continuity step, and the escalation path.
