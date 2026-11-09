---
name: source-triangulation
description: "Verify a claim before repeating it — the independent-sources test (three citations of one press release is one source), the provenance trace to the original, and the confidence grading that separates established from echoed. Use when asked is this claim actually true, verify this stat before the deck, everyone cites this number where's it from, or how solid is this source."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# source-triangulation

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

Produces the provenance trace, the independence assessment, the confidence grade with its reasoning, and the repeat-it-as phrasing.
