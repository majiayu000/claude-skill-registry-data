---
name: teach-me-in-layers
description: "Learn a complex topic in progressive layers — a one-sentence version, then a paragraph, then the real depth — so you build a mental scaffold instead of drowning in detail. Use when asked explain this in layers, teach me X from simple to deep, I need to understand this progressively, or start simple then go deeper."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# teach-me-in-layers

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

Produces a topic explained at escalating depth (ELI5 → informed-adult → the real thing), each layer building on the last, checkpoints to make sure a layer landed before the next, and where to stop for your actual need — so you never get lost in detail without a frame to hang it on.
