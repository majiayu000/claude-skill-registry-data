---
name: dental-emergency-triage
description: "Triage a dental emergency call so the right patient is seen today and the rest are safely scheduled — the red flags that are medical rather than dental, the questions that sort urgency, and the interim advice a receptionist can safely give. Use when asked to triage a dental emergency, decide who to fit in today, write phone triage guidance for front desk, or when a patient calls with swelling, trauma, or severe pain. Triage support only; never a diagnosis, and airway or spreading-infection signs go to emergency care immediately."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# dental-emergency-triage

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

Produces the urgency banding, the question script, the red-flag escalation list, interim self-care within scope, and the documentation line.
