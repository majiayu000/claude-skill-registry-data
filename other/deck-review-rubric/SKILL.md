---
name: deck-review-rubric
description: "Review a deck against a rubric instead of taste — the five dimensions (argument, evidence, density, arc, honesty), the severity-sorted feedback that separates broken from suboptimal, and the review conversation that improves the deck without rewriting it in the reviewer's voice. Use when asked review my deck, give feedback on this presentation, is this ready for the board, or our deck reviews are just font opinions."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# deck-review-rubric

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

Produces the rubric scores with evidence, the severity-sorted feedback, the two-fixes-that-matter-most call, and the reviewer discipline notes.
