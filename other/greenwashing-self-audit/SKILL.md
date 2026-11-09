---
name: greenwashing-self-audit
description: "Audit your own marketing and report claims for greenwashing risk before a regulator, journalist, or competitor does. Use when asked to review sustainability claims, check marketing copy for greenwash, audit environmental claims on a website or report, or pressure-test green messaging."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# greenwashing-self-audit

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

Produces a claim inventory with substantiation status per claim, vague-term and omission flags, and a fix-or-drop recommendation for every claim.
