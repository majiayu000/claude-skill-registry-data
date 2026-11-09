---
name: spaced-repetition-setup
description: "Set up a spaced-repetition system to actually remember what you learn — good cards, the right review rhythm, and the mistakes that make flashcards useless. Use when asked help me memorize, set up flashcards / Anki, how do I remember what I study, or spaced repetition for."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# spaced-repetition-setup

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

Produces card-writing guidance (atomic, one-fact, testable — not walls of text), a review cadence that leverages the forgetting curve, what's worth making cards for vs not, and the common failure modes that make people quit — turning cramming-and-forgetting into durable memory.
