---
name: form-explainer
description: "Explain an official form field by field (tax, benefits, immigration, employment, school, health, vehicle or court forms) from a photo, PDF, pasted text or just its name and number: what it is for, what each field means and what to put, the documents needed, the deadline, and where to send it. Use when someone says 'what is this form', 'help me understand form P45 / W-4 / Form 16', 'what do I write in this box', or 'I got this form in the post'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# form-explainer

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

Produces a one-line purpose, a field-by-field guide, a documents checklist, common mistakes, and what happens next.
