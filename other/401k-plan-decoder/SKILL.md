---
name: 401k-plan-decoder
description: "Decode a 401k or workplace retirement plan — the real cost of its funds, the match's fine print, vesting math, and the plan features worth using or avoiding. Use when someone asks 'is my 401k any good', 'decode my 401k plan', 'which funds should I look at', or 'what fees am I paying'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# 401k-plan-decoder

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

Produces a fee decode in dollars-over-time, match and vesting math, a fund-lineup triage by cost, and the questions for HR or the plan administrator.
