---
name: cn-8d-report
description: "Use when asked 写8D报告, 客户投诉8D, 质量问题8D, 客诉回复报告, 8D 怎么写, 根本原因分析报告, or write an 8D problem-solving report for a customer complaint or internal quality issue in a Chinese factory."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-8d-report

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

Produces a bilingual (Chinese and English) 8D report from D0 to D8 with the problem described by 5W2H, dated containment actions and suspect-stock quantities, root cause for both occurrence and escape (流出) with 5 Why and fishbone evidence, verified corrective actions, prevention through updated PFMEA, control plan and SOP, and closure criteria, in the format customers expect.
