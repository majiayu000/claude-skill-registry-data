---
name: loan-decoder
description: "Decode a personal, auto, or mortgage loan offer into what it really costs and where the traps are. Use when someone asks 'is this loan a good deal', 'decode my loan offer', 'what am I signing', or 'what will this mortgage actually cost me'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# loan-decoder

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

Produces a total-cost-of-loan number, APR vs advertised-rate reconciliation, ranked red flags (prepayment penalties, junk fees, rate-reset exposure), and the three questions that most change the deal.
