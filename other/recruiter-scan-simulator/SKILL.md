---
name: recruiter-scan-simulator
description: "Simulate a busy recruiter's first scan of a CV for a specific role: what they read in the first seconds, what they decide, and why, then step out of character to say what would change the decision. Use when asked would a recruiter shortlist my CV, review my CV like a recruiter, what does a screener see first, or why am I not getting interviews."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# recruiter-scan-simulator

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

Produces the in-character scan with the reading order and a shortlist, maybe or reject decision, then a debrief with the three changes most likely to flip it.
