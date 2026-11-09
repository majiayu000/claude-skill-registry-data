---
name: from-first-principles
description: "Strip a problem down to what's actually true — the physics, economics, and human basics — and rebuild the answer from there, ignoring 'how it's normally done'. Use when asked to think from first principles, why is this done this way, challenge the assumptions here, or rebuild this from scratch."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# from-first-principles

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

Produces the problem reduced to its fundamental truths, the inherited assumptions and conventions named and questioned, and a solution reasoned up from the basics — which often looks nothing like the default because the default was just copied.
