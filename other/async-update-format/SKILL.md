---
name: async-update-format
description: "Write status updates people actually read — the traffic-light-plus-narrative format (state first, story second), the blockers-are-asks rule, and the skimmable structure that respects a reader with thirty seconds. Use when asked write my weekly update, format our team's status posts, nobody reads my updates, or what goes in a good async check-in."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# async-update-format

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

Produces the update format with a filled example, the blockers-as-asks discipline, and the reader-time contract.
