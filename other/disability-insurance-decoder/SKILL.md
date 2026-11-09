---
name: disability-insurance-decoder
description: "Decode a disability insurance policy or employer LTD plan — own-occupation vs any-occupation, the benefit math after offsets and taxes, and the definitions that decide whether it pays. Use when someone asks 'is my disability insurance any good', 'decode my LTD policy', 'what does own-occupation mean', or 'how much would I actually get'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# disability-insurance-decoder

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

Produces a definition decode of the clauses that decide claims, the real benefit math after offsets, ranked red flags, and the questions to ask before relying on the coverage.
