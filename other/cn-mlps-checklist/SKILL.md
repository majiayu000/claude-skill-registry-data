---
name: cn-mlps-checklist
description: "Use when asked 等保怎么做, 等保 2.0 定级, 等保备案和测评流程, 等保三级要求, 我们的系统需要过等保吗, or prepare an information system for China's Multi-Level Protection Scheme (MLPS 2.0, 网络安全等级保护)."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-mlps-checklist

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

Produces a grading recommendation (定级) with the reasoning for the expert review, the filing (备案) and assessment (测评) steps and their usual timing, a gap checklist across the ten control areas of GB/T 22239-2019, and a remediation plan, marked as preparation for a licensed assessor.
