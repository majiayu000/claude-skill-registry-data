---
name: cn-civil-exam-essay
description: "Practise the essay paper (申论) of the Chinese civil service examination (国考 / 省考): work a question from the given materials (给定资料), find the scoring points (要点), draft an answer in the expected format, and mark it the way examiners do. Use when asked 申论怎么写, 帮我批改申论, 归纳概括题怎么答, 申论大作文, 公文写作题, or practise the shenlun paper."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-civil-exam-essay

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

Produces a question-type diagnosis, the points extracted from the materials with their source paragraphs, a model answer within the word limit, a marking of the person's own answer against the points, and a practice plan.
