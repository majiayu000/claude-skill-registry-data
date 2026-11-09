---
name: follow-up-chaser
description: "Chase unanswered emails without being annoying — the escalating-gently sequence with timing rules, the re-ask that makes replying easy, and the close-the-loop discipline that ends zombie threads. Use when asked they haven't replied what do I send, write a follow-up that isn't pushy, how long do I wait before chasing, or manage my waiting-on list."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# follow-up-chaser

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

Produces the follow-up sequence with dates, drafts per rung, and the give-up-gracefully exit.
