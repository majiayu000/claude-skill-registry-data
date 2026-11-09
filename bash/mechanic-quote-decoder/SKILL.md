---
name: mechanic-quote-decoder
description: "Read a garage quote or invoice like someone who can't be padded — which line items connect to your actual symptom, which are while-we're-in-there additions, the questions that make soft lines disappear, when a second opinion pays for itself, and the scripts for declining work without souring the relationship. Use when someone says 'is this mechanic quote fair', 'the garage called and now it's £900', 'do I really need all this', or before authorizing repairs. Not a diagnosis — it's the interrogation of one."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# mechanic-quote-decoder

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

Produces a line-by-line decode, the callback questions, and the authorize/decline/second-opinion sort.
