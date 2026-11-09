---
name: cn-parent-meeting
description: "Use when asked 帮我写家长会发言稿, 家长会PPT大纲, 班主任家长会讲话, 期中家长会, 新生家长会, 毕业班家长会, or prepare a parent meeting as a Chinese teacher."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-parent-meeting

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

Produces a parent-meeting pack in Chinese: an agenda, a timed speech for the 班主任 or subject teacher with class data presented without ranking individual students, a slide outline, specific requests to parents, a one-page handout, answers to likely questions, and a follow-up message for the parents' WeChat group.
