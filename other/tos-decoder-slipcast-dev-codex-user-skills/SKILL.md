---
name: tos-decoder
description: "Decode a terms of service or privacy policy into what you're actually agreeing to, ranked by real-world impact. Use when someone asks 'what am I agreeing to', 'decode this privacy policy', 'is this ToS bad', or 'should I click accept'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# tos-decoder

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

Produces a ranked findings table with a 'should I care?' verdict per finding, covering data resale, arbitration and class-action waivers, unilateral changes, content licenses, and what deletion really means.
