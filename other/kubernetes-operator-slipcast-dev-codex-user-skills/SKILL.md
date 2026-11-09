---
name: kubernetes-operator
description: Use when building a Kubernetes Operator — custom controllers that reconcile
  CRD state. Triggers on "build an operator", "CRD design", "reconcile loop", "controller-runtime",
  "kubebuilder", "operator-sdk", "metacontroller", "KOPF", "operator capability levels",
  or "custom resource". Ships CRD validator, reconcile-loop linter, and OperatorHub
  capability auditor (all stdlib Python), 4 references on the operator pattern + CRD
  design + reconcile patterns + tooling landscape, and a /operator-audit slash command.
  NOT a generic k8s skill — specifically the Operator pattern.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# kubernetes-operator

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

