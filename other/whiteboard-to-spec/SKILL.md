---
name: whiteboard-to-spec
description: "Turn photos of a whiteboard, sticky-note wall, or napkin sketch into a structured spec the team can execute. Use when given whiteboard photos after a workshop, sketch images of a flow or architecture, or asked to 'write up what we drew'. Requires image input."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# whiteboard-to-spec

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

Produces a structured write-up — decisions, flows, open questions, owners — that preserves everything on the board and flags what was ambiguous.
