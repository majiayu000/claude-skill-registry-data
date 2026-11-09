---
name: market-stall-pricing
description: "Price goods for a market stall, street stall or small shop so every sale covers its costs, and hold your price when customers bargain. Use when someone says 'how much should I sell this for', 'customers always bargain me down', 'am I making any money at the market', or 'what price for my vegetables, crafts or snacks'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# market-stall-pricing

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

Produces a cost-per-item calculation, a floor price, a starting price with room to bargain, bargaining lines that keep the margin, and a quick end-of-day check.
