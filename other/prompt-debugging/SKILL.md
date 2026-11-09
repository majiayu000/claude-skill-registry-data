---
name: prompt-debugging
description: "Figure out why a prompt isn't working and fix it — diagnose the actual failure (ambiguity, missing context, wrong format, conflicting instructions) instead of randomly rewording. Use when asked why isn't my prompt working, the AI keeps ignoring my instructions, my prompt gives inconsistent results, or how do I fix this prompt."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# prompt-debugging

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

Produces a diagnosis of the specific failure mode, the targeted fix for it (not a vibes rewrite), a corrected prompt, a check that it generalizes rather than fixing one case, and the principle behind the fix so you stop hitting it — turning prompt frustration into a debuggable, repeatable process.
