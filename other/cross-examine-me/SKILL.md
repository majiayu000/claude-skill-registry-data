---
name: cross-examine-me
description: "Stress-test a decision or claim through a sharp, fair Q&A — the questions a good lawyer or skeptical friend would ask before you commit. Use when asked to cross-examine me, ask me hard questions about this, interrogate my plan, or make me defend this."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cross-examine-me

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

Produces a sequenced line of probing questions (from clarifying to challenging to the killer question), space to answer, and a debrief on where your answers were strong, evasive, or exposed a gap — so weaknesses surface in private before they surface in public.
