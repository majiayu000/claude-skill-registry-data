---
name: decision-panel
description: "Run a decision past a panel of clashing advisors — an optimist, a pessimist, a numbers person, an ethicist, and future-you — then get a chair's verdict. Use when asked to help me decide, weigh this decision, what should I do about, or run this by different advisors."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# decision-panel

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

Produces each advisor's honest take on the decision (each committed to their lens), where they disagree most, the question that would break the tie, and a chair's recommendation that weighs the panel — turning a lonely choice into a structured board meeting.
