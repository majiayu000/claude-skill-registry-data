---
name: nt-translator
description: "Translate both directions across the neurodivergent↔neurotypical gap at work — decode what an indirect message actually meant ('let's circle back' = no), and rewrite your direct message so it lands without you having to sand off the point. Use when someone says 'what did my manager actually mean', 'my message came across wrong again', 'why do people think I'm blunt', or is ND navigating an NT workplace."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# nt-translator

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

Produces a decode of the received message and/or a rewrite of yours, with the reasoning shown so you learn the pattern.
