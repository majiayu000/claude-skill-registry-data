---
name: medical-bill-decoder
description: "Decode an itemized medical bill or EOB into plain English and find the charges worth disputing. Use when someone asks 'why is my medical bill so high', 'decode my hospital bill', 'what is this EOB saying', or 'can I negotiate this bill'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# medical-bill-decoder

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

Produces a line-by-line decode, duplicate and unbundling flags, balance-billing red flags, and ready-to-read scripts for requesting an itemized bill, financial assistance, and a negotiation call.
