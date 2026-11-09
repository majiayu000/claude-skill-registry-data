---
name: cn-customs-docs
description: "Use when asked 出口报关需要什么单证, 报关资料清单, 申报要素怎么填, 报关单和发票对不上, 出口退税需要的单证, 进口清关资料, or prepare customs documents for an export or import shipment in mainland China."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-customs-docs

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

Produces a document checklist for this shipment (报关单 data, 商业发票, 装箱单, 合同, 委托书, licences and certificates), a cross-document consistency check, the 申报要素 to prepare for the HS code, inspection and licence flags, the timeline with the customs broker, and the records to keep for the export rebate, all marked to confirm with the broker and customs.
