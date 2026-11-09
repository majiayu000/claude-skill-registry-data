---
name: passive-deal-screener
description: "Screens private investment opportunities from the passive LP (limited-partner) perspective — equity syndications, preferred equity, hard money / bridge funds, and private credit — pasted from any source (an investment platform listing, a direct GP email, raw terms). Use whenever asked to analyze, evaluate, screen, or review a real-estate or private-market deal, syndication, offering, or investment opportunity — e.g. 'is this deal worth pursuing', 'what should I ask the GP', 'analyze this offering memo'. LP lens only; not operator-side underwriting (acquisition/development/asset-management). For corporate-finance DCF/ratio work use financial-analyst."
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# passive-deal-screener

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

Produces a deal snapshot, stress-tests returns against public benchmarks, deconstructs the fee stack to a gross-to-net drag, surfaces severity-ranked red flags and missing disclosures, assesses GP alignment, and generates prioritized GP questions with bad-answer signals.
