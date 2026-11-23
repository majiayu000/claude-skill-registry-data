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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

