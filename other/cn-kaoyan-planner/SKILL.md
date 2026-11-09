---
name: cn-kaoyan-planner
description: "Plan preparation for the Chinese postgraduate entrance examination (考研): choosing target schools and programmes with realistic odds, a phased study plan for the national subjects and the specialist papers, and preparation for the re-examination (复试) and adjustment (调剂). Use when asked 考研怎么规划, 帮我做考研复习计划, 择校择专业, 考研时间线, 复试怎么准备, 调剂, or plan my kaoyan."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-kaoyan-planner

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

Produces a school-and-programme shortlist method with the data to collect, a month-by-month study plan by subject, weekly templates, the key-date checklist to confirm against official notices, and a 复试 and 调剂 preparation guide.
