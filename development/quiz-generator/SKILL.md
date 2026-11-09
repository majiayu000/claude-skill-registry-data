---
name: quiz-generator
description: "Generate a quiz or test on any topic with a balanced mix of question types and difficulty, plus a complete answer key with explanations. Use when asked to create a quiz, write a test, make practice questions, or build an assessment."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# quiz-generator

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

Produces well-formed questions aligned to learning objectives, tagged by difficulty and cognitive level, with an answer key and (for MCQs) plausible distractors and rationale.
