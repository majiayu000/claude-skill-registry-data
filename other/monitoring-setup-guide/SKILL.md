---
name: monitoring-setup-guide
description: "Write a monitoring setup guide for a service — defining what to measure, how to alert on it, and how to build the observability stack covering the four golden signals, business metrics, log strategy, distributed tracing, alerting rules, dashboard layout, and observability debt. Use when asked to set up monitoring for a service, define alerting strategy, write an observability plan, create a dashboard specification, or document logging standards for a team."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# monitoring-setup-guide

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

Produces a metric definitions table, alert rules specification, dashboard layout wireframe, log schema, tracing setup checklist, and monitoring gap analysis.
