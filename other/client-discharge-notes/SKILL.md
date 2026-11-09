---
name: client-discharge-notes
description: "Write clear at-home care instructions for a pet owner after a veterinary visit, procedure, or hospitalization. Use when asked to write discharge instructions, go-home notes, post-op care, or medication instructions for a pet owner."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# client-discharge-notes

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

Produces plain-language home-care instructions: medications (what/how much/when/how), activity restrictions, what to watch for, warning signs that mean call-now, the recheck plan, and emergency contacts — written so a worried owner can actually follow them.
