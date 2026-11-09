---
name: prompt-optimizer
description: "Diagnose and rewrite an underperforming LLM prompt so it produces reliable, well-structured output. Use when asked to improve a prompt, fix a prompt that gives inconsistent or wrong results, reduce hallucination/refusals, or make output follow a format."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# prompt-optimizer

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

Produces a rewritten prompt with a diagnosis of what was failing, the specific changes and why, and a small test set to verify the fix.
