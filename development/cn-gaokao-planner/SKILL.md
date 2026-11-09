---
name: cn-gaokao-planner
description: "Help a student and family plan university applications after the 高考 (gaokao): use the student's provincial rank rather than raw score, build a 冲 / 稳 / 保 (reach, match, safe) list from official historical admission data, check subject requirements under the new gaokao, and weigh major against university. Use when asked 帮我填高考志愿, 志愿怎么填, 冲稳保怎么排, 这个分数能上什么学校, or plan gaokao applications. Never guarantees admission."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-gaokao-planner

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

Produces a structured application list with the reasoning for each choice, a risk check of the whole list, and the questions to settle as a family.
