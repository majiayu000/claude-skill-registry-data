---
name: infra-as-code-review
description: "Write an infrastructure-as-code review checklist and conduct a structured review of Terraform, CloudFormation, Pulumi, or Ansible code. Use when asked to review IaC code, audit infrastructure configurations, check cloud security posture, or produce a reusable IaC review checklist."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# infra-as-code-review

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

Produces a structured review report with severity-categorized findings, remediation guidance, and a reusable checklist.
