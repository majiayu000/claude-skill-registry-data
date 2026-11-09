---
name: capital-allocation
description: "Allocate a finite budget or headcount across competing initiatives by return and strategic fit. Use when asked to allocate budget, decide where to invest, build a funding/portfolio plan, or make trade-offs across initiatives under a cap."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# capital-allocation

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

Produces a capital-allocation plan — initiatives scored by expected return × strategic fit per dollar, a funded/unfunded split against the cap, the cut line, and the reasoning.
