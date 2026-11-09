---
name: benefits-decoder
description: "Decode an employment benefits package into what it's actually worth and where the fine print bites. Use when someone asks 'is this offer good', 'decode my benefits package', 'what does my equity actually mean', or 'what should I ask HR before signing'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# benefits-decoder

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

Produces a benefit-by-benefit decode with real dollar values, ranked red flags (vesting cliffs, clawbacks, 'discretionary' bonuses, unlimited-PTO economics), and the questions to ask HR before signing.
