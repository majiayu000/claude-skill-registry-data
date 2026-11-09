---
name: medication-management-system
description: "Set up a system to manage medications safely — for yourself or someone you care for — so doses aren't missed, doubled, or dangerously combined. Use when asked help me manage medications, keep track of my parent's pills, set up a medication system, or I keep forgetting my meds. Not medical advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# medication-management-system

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

Produces an organized medication list (what, dose, when, why), a routine and reminder setup that fits the person, a refill-tracking method so nothing runs out, safety checks (interactions and duplications to raise with a pharmacist), and an emergency-ready summary — because medication errors are common and dangerous, and a system prevents most of them.
