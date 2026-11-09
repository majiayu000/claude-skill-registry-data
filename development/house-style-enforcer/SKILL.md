---
name: house-style-enforcer
description: "Apply a team's writing style consistently — extract the house style from exemplar documents into a checkable rule card, run the conformance pass on new drafts, and fix violations without flattening the author's voice. Use when asked make this match our style, why do our docs all sound different, build a style guide from our best docs, or check this draft against house style."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# house-style-enforcer

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

Produces the extracted rule card, the conformance pass with per-fix reasons, and the voice-preservation line.
