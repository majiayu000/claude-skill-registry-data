---
name: vendor-security-review
description: "Run a third-party / vendor security review and assign a risk tier with required controls. Use when asked to assess a vendor's security, run a third-party risk assessment, complete a security questionnaire about a vendor, or decide what due diligence a new tool needs."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# vendor-security-review

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

Produces a vendor risk assessment — a data/access-driven risk tier, the questionnaire focus, required evidence (SOC 2, pen test, DPA), residual risk, and an approve/conditional/reject recommendation.
