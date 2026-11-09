---
name: lease-decoder
description: "Decode a residential lease into plain English and rank the clauses that can hurt you. Use when someone asks 'what am I signing', 'decode my lease', 'is this rental agreement normal', or 'can my landlord really do this'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# lease-decoder

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

Produces a clause-by-clause decode table, ranked red flags, break-clause and deposit math, questions to ask before signing, and what's actually negotiable.
