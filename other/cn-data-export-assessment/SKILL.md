---
name: cn-data-export-assessment
description: "Use when asked 数据出境要申报吗, 数据出境安全评估还是标准合同, 个人信息出境标准合同怎么备案, 我们把数据传到海外总部合规吗, or decide how to transfer data out of mainland China lawfully."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-data-export-assessment

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

Produces a data map of what leaves China, the route that applies (an exemption, the personal information export standard contract, certification, or a CAC security assessment) with the thresholds to confirm, the filing steps, and the documents to prepare, including the personal information protection impact assessment.
