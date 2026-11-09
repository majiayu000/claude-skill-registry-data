---
name: ai-assisted-performance-review
description: "Evaluate performance fairly when output is AI-assisted — what still measures the human, what now measures the tooling, and how to run the review conversation. Use when reviewing someone whose work is heavily AI-assisted, when output volume stopped meaning anything, when calibrating a team with uneven AI adoption, or when writing review criteria for the AI era. For the general review document use performance-review; for redesigning the role itself use role-redesign-for-ai."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ai-assisted-performance-review

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

Produces review guidance: a what-measures-whom analysis, rewritten criteria, calibration rules for mixed-adoption teams, and conversation scripts.
