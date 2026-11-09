---
name: medication-therapy-review
description: "Structure a pharmacist's medication therapy review so it finds the problems worth escalating and documents them in a form a prescriber will act on. Use when asked to conduct a medication review, run an MTM or MUR, deprescribing review, or polypharmacy assessment, or to prepare a review for a patient on many medicines. A documentation and reasoning framework for a licensed pharmacist; it makes no clinical determination and recommends no specific drug or dose."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# medication-therapy-review

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

Produces the medication list reconciled, the drug-therapy-problem list classified and prioritised, the patient-goal alignment, the prescriber recommendations with rationale, and the follow-up plan.
