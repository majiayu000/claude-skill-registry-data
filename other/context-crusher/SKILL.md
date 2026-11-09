---
name: context-crusher
description: "Compress tool outputs, logs, and JSON before they enter the context window — structural compression via a deterministic stdlib script (schema + samples + stats instead of 300 raw rows), no API, no summarization loss. Use when asked shrink this tool output, my context is full of JSON, compress these logs before analysis, or stop wasting tokens on raw data."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# context-crusher

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

Produces the crushed artifact with its token math shown, the crush-or-keep decision rules, and the fetch-the-original escape hatch.
