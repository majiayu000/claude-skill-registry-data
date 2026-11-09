---
name: crm-hygiene-sweep
description: "Have a proactive agent sweep a CRM (HubSpot, Salesforce, Pipedrive) on a schedule for the things that quietly rot a pipeline: deals with no next step, close dates in the past, deals untouched for weeks, contacts with no owner, and duplicate records, reported per owner with suggested fixes a human approves. Use when asked to clean up my CRM, find stale deals, have Duet check HubSpot every week, which deals have no next step, or pipeline hygiene check."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# crm-hygiene-sweep

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

Produces the sweep rules, the per-owner list of issues with the evidence, the suggested fix per line, and the weekly summary numbers; it never edits, merges or deletes records itself.
