---
name: senior-security
description: Use when the user asks for STRIDE threat modeling, DREAD risk scoring,
  data-flow-diagram threat analysis, or a quick secret scan — or when a security request
  needs routing to the right specialist skill (pen-testing, incident response, cloud
  posture, red team, AI security, threat hunting, secure code review). This skill
  owns threat modeling; everything else routes to a sibling.
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# senior-security

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

