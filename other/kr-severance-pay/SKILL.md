---
name: kr-severance-pay
description: "Use when asked 퇴직금 계산해 줘, 퇴직금 얼마 받을 수 있어, 평균임금 어떻게 계산해, 퇴직연금 DB형 DC형 차이, IRP로 퇴직금 받아야 해, 퇴직금을 안 줘요, or how is severance pay calculated in Korea."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# kr-severance-pay

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

Produces an eligibility check, a step-by-step 퇴직금 calculation from the person's own figures (평균임금, 계속근로기간, bonuses and leave pay), how their 퇴직연금 type changes what they receive, the payment deadline and IRP rules, tax on leaving, and what to do if it is unpaid, every legal figure marked to confirm.
