---
name: moving-company-estimate-decoder
description: "Decode a moving company estimate — binding vs non-binding, the weight and cubic-feet games, valuation vs insurance, and the red flags that precede hostage-load stories. Use when someone asks 'is this moving quote legit', 'decode my moving estimate', 'binding vs non-binding estimate', or 'how do I avoid moving scams'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# moving-company-estimate-decoder

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

Produces an estimate-type decode with what-you'll-actually-pay scenarios, ranked red flags, the valuation decode, and the questions that separate real movers from brokers.
