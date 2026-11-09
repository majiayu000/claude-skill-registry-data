---
name: vet-estimate-decoder
description: "Decode a veterinary treatment estimate — what each line is for, which items are core vs precautionary, and how to have the options conversation nobody offers you. Use when someone asks 'is this vet estimate reasonable', 'decode my vet's treatment plan', 'do we need all these tests', or 'I can't afford this vet bill what are my options'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# vet-estimate-decoder

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

Produces a line-by-line decode with core/precautionary/comfort triage, the questions that surface the tiered options vets keep in reserve, and the payment and assistance paths.
