---
name: arrival-setup
description: "Set up the essentials in the right order after moving to a new country — the ID/registration, bank account, phone, address, and social/tax number that unlock each other — so you don't get stuck in the chicken-and-egg loops that trap newcomers. Use when someone says 'I just moved to a new country', 'what do I do first after arriving', 'set up my life in [country]', or 'I can't open a bank account without an address but can't rent without a bank'. Routes to official sources; rules are local."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# arrival-setup

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

Produces a sequenced arrival checklist with dependencies and the official offices for each.
