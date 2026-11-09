---
name: style-fingerprint
description: "Study 3-5 documents the user actually shipped and distil a compact style card — so every skill writes in their voice, not the model's. Use when asked to learn my writing style, make outputs sound like me, build a voice profile, or when a user complains AI drafts don't sound like them."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# style-fingerprint

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

Produces a style card (rhythm, register, structure habits, pet phrases, banned moves) saved to the Brain where every other skill reads it.
