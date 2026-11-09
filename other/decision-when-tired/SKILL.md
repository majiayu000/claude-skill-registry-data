---
name: decision-when-tired
description: "Make a decent decision when you're too depleted to think well — a low-energy protocol that protects you from bad tired-brain choices. Use when asked I'm too tired to decide, help me choose I'm exhausted, I can't think straight right now, or should I even decide this now."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# decision-when-tired

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

Produces a first check on whether this decision can simply wait until you're rested, and if not, a minimal-effort path to a safe-enough choice (default to reversible, avoid the tired-brain traps, use a simple rule) — because decisions made depleted are predictably worse, and the best move is often not to make them now.
