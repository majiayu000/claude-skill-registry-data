---
name: thread-to-decision
description: "Land a sprawling chat thread on an actual decision — the summarize-and-fork move (positions restated, the question isolated), the decider-and-deadline injection, and the recorded close that ends the forty-message orbit. Use when asked this thread is going in circles, get a decision out of this discussion, summarize where we landed, or why do our threads never conclude."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# thread-to-decision

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

Produces the thread summary with positions attributed, the isolated decision question, the closure message, and the decision record.
