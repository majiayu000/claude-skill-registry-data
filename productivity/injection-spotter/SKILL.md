---
name: injection-spotter
description: "Spot prompt-injection in untrusted content before an agent acts on it — the anatomy of injected instructions across the channels attackers use (email, web, files, tool outputs, documents), the tell-list, and the safe-handling response. Use when asked is this content trying to hijack my agent, check this page or email or file for prompt injection, spot the injection, or why did my agent go off-task."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# injection-spotter

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

Produces the injection verdict with quoted tells, the channel-specific patterns, and the safe-handling protocol.
