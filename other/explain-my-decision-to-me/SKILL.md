---
name: explain-my-decision-to-me
description: "Talk through a decision out loud with a patient thinking partner that reflects your reasoning back, so the answer you already half-know becomes clear. Use when asked help me think this through, I need to talk this out, be my sounding board, or I don't know what I actually think."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# explain-my-decision-to-me

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

Produces a structured reflection of your own reasoning — what you've actually said, the values driving it, the contradictions and gaps, and the question that would clarify it — acting as a rubber-duck / sounding board rather than handing you an answer you didn't reach yourself.
