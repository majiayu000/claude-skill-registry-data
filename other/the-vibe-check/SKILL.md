---
name: the-vibe-check
description: "Harden a vibe-coded app before strangers use it — the audit for prototypes built fast with AI: exposed secrets, missing auth checks, unvalidated input, data with no deletion path, and the five embarrassing holes every weekend build has. Use when someone says 'Claude built my app, is it safe to launch', 'harden my prototype', 'vibe check my project', or before putting real users on a hackathon build. Defensive review of YOUR OWN app."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# the-vibe-check

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

Produces a ranked findings list with fixes, a launch-blocker line, and a 'what I'd break first' attacker's tour.
