---
name: disagreeing-experts
description: "Put one situation in front of three professionals chosen to disagree — the lawyer, the accountant, and the therapist read the same divorce — each ruling independently, with the conflicts surfaced in a disagreement table instead of blended into mush. Use when asked for different professional perspectives, what would a lawyer versus an accountant say, I keep getting one-sided advice, or pressure-test this from multiple angles. The anti-consensus skill: it never averages."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# disagreeing-experts

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

Produces three independent readings, the disagreement table with why the frames diverge, and the decision map of which expert to weight for which sub-decision.
