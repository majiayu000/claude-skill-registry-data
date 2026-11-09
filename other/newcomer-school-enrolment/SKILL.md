---
name: newcomer-school-enrolment
description: "Get a child into school after moving to a new country: who to contact, the documents schools ask for, what to do when papers are missing, language support, and the right to a place. Use when someone says 'we just moved, how do I enrol my child in school', 'the school wants documents we don't have', 'my child doesn't speak the language yet', or 'which school can my kid go to here'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# newcomer-school-enrolment

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

Produces an enrolment plan in order, a document checklist with fallbacks for missing papers, questions to ask the school, and a first-weeks support plan.
