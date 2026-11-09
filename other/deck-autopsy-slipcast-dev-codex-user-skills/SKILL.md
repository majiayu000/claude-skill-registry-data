---
name: deck-autopsy
description: "Autopsy a slide deck from photos or screenshots of its slides — the narrative arc, the numbers, and what each slide is hiding. Use when given slide images (a competitor's pitch, a conference talk, your own deck before a big meeting) and asked what the deck argues, whether it holds up, or how to counter or improve it. Requires image input."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# deck-autopsy

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

Produces a slide-by-slide read, the reconstructed argument chain, weak links, and the questions the deck is engineered to avoid.
