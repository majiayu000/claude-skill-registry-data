---
name: xiaohongshu-note
description: "Write a 小红书 (Xiaohongshu, RED) note that reads like a real person's experience: a scroll-stopping title, cover text, a body built on specific personal detail, tags, and a compliance check against restricted advertising words. Use when asked 帮我写小红书笔记, 小红书标题, 种草文案, 小红书怎么写才有流量, or write a Xiaohongshu post."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# xiaohongshu-note

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

Produces three title options, cover image text, the note body in the platform's style, tags, an engagement question, a check of restricted words and undisclosed advertising, and notes for the images.
