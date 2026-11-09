---
name: referral-request
description: "Write a short message asking someone at a target company for a referral or a conversation, sized to how well the person knows them, with an easy way to say no. Use when asked how do I ask for a referral, message someone at Google about a job, ask a former colleague to refer me, or write a LinkedIn message to an employee. For general networking, see networking-outreach."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# referral-request

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

Produces the message for the right channel and relationship strength, a ready-to-forward blurb the referrer can paste, and a single follow-up.
