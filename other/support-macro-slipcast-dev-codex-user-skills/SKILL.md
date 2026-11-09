---
name: support-macro
description: "Write reusable support macros / canned responses that sound human, not robotic. Use when asked to write a support macro, a canned response, a saved reply, or a template for a common customer ticket."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# support-macro

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

Produces a macro — an empathetic opener, the clear answer/steps, placeholders for personalisation, and a warm close — plus variants (resolved / need-more-info / escalating), tuned to keep it human.
