---
name: tone-fixer
description: "Rewrite a message to the tone you actually want — less harsh, more confident, warmer, firmer, or shorter — without losing your point. Use when asked to make this sound less rude, soften this email, make me sound more confident, make this nicer/firmer, or fix the tone of a message."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# tone-fixer

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

Produces two or three rewrites at the target tone, a note on exactly what was changed and why, and a flag if the original's tone was fine as-is.
