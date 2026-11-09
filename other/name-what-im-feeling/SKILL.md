---
name: name-what-im-feeling
description: "Turn a vague bad mood or 'off' feeling into a precisely-named emotion and its likely cause — because naming it is what starts to defuse it. Use when asked I feel off and don't know why, help me figure out what I'm feeling, I'm in a weird mood, or why am I upset."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# name-what-im-feeling

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

Produces a short, gentle inquiry that distinguishes the actual emotion from the fog (anxious vs frustrated vs lonely vs overwhelmed), its most likely trigger, what the feeling might be pointing at, and one small thing that tends to help that specific state — never diagnosing, just helping you locate yourself.
