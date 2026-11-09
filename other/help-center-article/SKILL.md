---
name: help-center-article
description: "Write a help-center / knowledge-base article that actually resolves the issue and deflects tickets. Use when asked to write a help doc, KB article, FAQ entry, how-to, or support documentation."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# help-center-article

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

Produces a findable, skimmable article — task-based title, the answer up front, numbered steps, screenshots-to-add markers, troubleshooting, and related links — written so users self-serve instead of contacting support.
