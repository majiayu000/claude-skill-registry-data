---
name: prescription-cost-navigator
description: "Work down the cost of a prescription systematically — the generic and therapeutic-alternative conversation, discount programs vs insurance math, pharmacy price variance, and manufacturer/assistance programs, in the order that saves the most first. Use when asked my prescription is too expensive, how do I save on my meds, is there a cheaper version of this drug, or I can't afford my medication."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# prescription-cost-navigator

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

Produces the cost-reduction ladder for the specific prescription, the scripts for pharmacist and prescriber conversations, and the never-do list (skipping doses is not a savings plan).
