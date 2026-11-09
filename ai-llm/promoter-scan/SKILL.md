---
name: promoter-scan
description: "Find the requests you keep making to your AI assistant by scanning Claude Code transcripts and claude.ai exports, clustering them by intent, and ranking each recurring pattern by how promotable it is into a reusable skill. Use when asked what do I keep asking for, scan my transcripts, find repeated prompts, which of my prompts should become skills, or to start the promote loop."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# promoter-scan

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.

## Требования к результату

Produces a ranked report of recurring patterns with frequency, redacted example prompts, the variation between them, and a promotability score.
