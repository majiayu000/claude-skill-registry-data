---
name: screenshot-teardown
description: "Tear down a competitor's product from screenshots of its actual UI — onboarding, pricing page, core flows. Use when given screenshots of a rival's app or website and asked what they're doing, how their flow works, or what to learn/steal/avoid. Requires image input. For a market-level teardown without screenshots use competitor-teardown."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# screenshot-teardown

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

Produces a UX-and-strategy teardown grounded in what is visibly on screen, with an inferences-vs-observations split.
