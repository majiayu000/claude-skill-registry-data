---
name: assumption-audit
description: "Surface the hidden assumptions a plan or belief rests on, then test what happens when each one is wrong. Use when asked what am I assuming here, check my assumptions, what if I'm wrong about, or stress-test my thinking."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# assumption-audit

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

Produces the unstated assumptions your conclusion depends on (ranked by how load-bearing they are), a flip of each to see which one breaking would change everything, and the cheapest way to check the riskiest ones — because the assumption you didn't know you were making is what sinks plans.
