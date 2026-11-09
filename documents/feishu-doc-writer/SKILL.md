---
name: feishu-doc-writer
description: "Write a document for Feishu / Lark Docs (飞书文档) in the shape Feishu readers expect: a summary callout at the top, headed sections that work with the outline panel, task lists with @owners and dates, and tables that survive paste. Use when asked 写一份飞书文档, 帮我整理成飞书文档格式, 飞书方案文档, write this up for Feishu or Lark, or turn my notes into a Feishu doc."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# feishu-doc-writer

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

Produces paste-ready Markdown that Feishu converts on import, a 高亮块 summary, an owner-and-date task list, and a short message to share the doc in a Feishu group.
