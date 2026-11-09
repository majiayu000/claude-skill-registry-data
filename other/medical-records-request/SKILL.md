---
name: medical-records-request
description: "Request your medical records and actually get them — what to ask for, the request letter that can't be shuffled aside, the timelines and fee rules to cite (jurisdiction-flagged), and the escalation path for stonewalls. Use when asked how do I get my medical records, write a records request, my doctor's office won't send my records, or what records should I collect."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# medical-records-request

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

Produces the itemized request letter, the delivery and format choices decoded, the follow-up ladder, and the personal health-file structure for keeping them.
