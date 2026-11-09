---
name: cn-home-school-comms
description: "Use when asked 怎么给老师发消息, 跟班主任沟通, 孩子在学校被欺负怎么跟老师说, 对老师的做法有意见, 请假怎么写, 家长群里怎么说话, or write a message from a parent to a teacher in China."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-home-school-comms

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

Produces a ready-to-send WeChat or note message in Chinese, polite and specific, for the situation (asking, leave, a concern, a disagreement, bullying, thanks), a calmer version if the parent is upset, what to say if the teacher calls back, the escalation path if it is not resolved, and 家长群 etiquette.
