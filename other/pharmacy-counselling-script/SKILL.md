---
name: pharmacy-counselling-script
description: "Write the counselling a patient will actually follow when collecting a new or changed medicine — what it is for, how to take it, what to expect, and the one thing that would make them stop. Use when asked to write patient counselling, counsel on a new prescription, explain a medicine to a patient, or improve adherence at the counter. A communication framework for a licensed pharmacist; it makes no clinical determination and substitutes for no product-specific information."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# pharmacy-counselling-script

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

Produces the counselling script in plain language, the teach-back questions, the red-flag advice, the adherence anticipation, and the documentation line.
