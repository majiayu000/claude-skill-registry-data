---
name: cn-letter-of-credit-check
description: "Use when asked 信用证审证, 信用证审单, 审核信用证条款, 单证不符点, L/C 软条款, 交单前检查, or check a letter of credit or a set of export documents against it for a Chinese exporter. Not legal or banking advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-letter-of-credit-check

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

Produces an L/C term review (dates, amounts, shipment, documents, soft clauses) with what to ask the buyer to amend, and a document-by-document discrepancy checklist (invoice, bill of lading, packing list, insurance, certificate of origin, inspection) with the relevant UCP 600 articles, all marked to confirm with the bank's documentary credit team.
