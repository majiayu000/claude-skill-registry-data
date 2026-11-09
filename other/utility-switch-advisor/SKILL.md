---
name: utility-switch-advisor
description: "Decide whether to switch energy, broadband, or mobile providers — compare the real total cost, dodge the traps, and time it right. Use when asked should I switch energy/broadband/mobile providers, compare utility deals, is this a good energy tariff, or help me switch and save."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# utility-switch-advisor

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

Produces an apples-to-apples comparison (total annual cost, not headline rate), the traps to check (intro-then-jump pricing, exit fees, contract length), a switch/stay recommendation, the switching steps, and reminders to verify current prices on a comparison source.
