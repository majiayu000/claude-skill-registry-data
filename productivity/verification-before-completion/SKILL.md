---
name: verification-before-completion
description: "Verify work actually meets its brief BEFORE declaring it done — a structured self-review pass that catches the gaps, unmet requirements, and untested claims that 'looks finished' hides. Use when about to hand over any deliverable (document, code, analysis, plan), when past work kept coming back with 'you missed…', or as the standing final step of any multi-step task."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# verification-before-completion

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

Produces the verified deliverable plus a short verification record: what was checked, what was found and fixed, what remains open.
