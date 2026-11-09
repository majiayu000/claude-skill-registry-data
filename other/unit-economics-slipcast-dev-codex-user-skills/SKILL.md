---
name: unit-economics
description: "Model the unit economics of a business — CAC, LTV, payback, contribution margin — from real inputs. Use when asked to calculate unit economics, work out LTV:CAC, find the payback period, or check whether a business model is viable per customer."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# unit-economics

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

Produces a computed unit-economics summary (LTV, CAC, ratio, payback, contribution margin) with a verdict and the levers that move it most.
