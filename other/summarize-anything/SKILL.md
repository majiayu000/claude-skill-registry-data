---
name: summarize-anything
description: "Turn a long article, email thread, document, or transcript into a tight summary you can act on — the gist, the key points, and what it means for you. Use when asked for a TL;DR, to summarize this, give me the gist, or the key takeaways."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# summarize-anything

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

Produces a one-line TL;DR, the key points as scannable bullets, any decisions/action items with owners, and open questions — faithful to the source, with nothing invented and important caveats kept.
