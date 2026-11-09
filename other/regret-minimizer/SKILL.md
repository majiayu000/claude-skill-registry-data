---
name: regret-minimizer
description: "Reframe a hard choice through the lens of future regret — which option will you regret less at 80? — to cut through short-term noise. Use when asked which will I regret less, help me decide with the long view, I don't want to look back and wish, or use the regret test on this."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# regret-minimizer

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

Produces each option projected forward to old age (the regret of doing it vs not), a distinction between action-regret and inaction-regret (people regret inactions more), the fear that's really driving the hesitation, and the choice that best minimizes lifelong regret — for the decisions that echo.
