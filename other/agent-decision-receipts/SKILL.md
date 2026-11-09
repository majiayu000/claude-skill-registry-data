---
name: agent-decision-receipts
description: 'Mint a tamper-evident, post-quantum-signed receipt for a consequential
  agent action (deploy, delete, pay, grant-access, model decision) so it can be verified
  later from the certificate alone. Use when an autonomous agent takes a side-effecting
  action that may need to be proven later, or when satisfying EU AI Act Article 12
  record-keeping. Three decisions: whether an action needs a receipt, minting it,
  verifying it. Signing is delegated to the open-source OpenAgentOntology package.
  Not after-the-fact log analysis; not a hosted notary; not a legal opinion.'
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# agent-decision-receipts

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

