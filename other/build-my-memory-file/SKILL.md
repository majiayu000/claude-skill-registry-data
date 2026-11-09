---
name: build-my-memory-file
description: "Interview you into a durable personal MEMORY.md — your decision rules, patterns, past failures, and preferences — that any AI can read to help you better, with privacy guardrails built in. Use when asked to build my memory file, help my AI remember me, create a MEMORY.md, or set up context about myself."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# build-my-memory-file

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

Produces a structured personal-context file drawn out through good questions (how you decide, what you keep repeating, what you don't want to repeat), organized for an AI to use — while explicitly refusing to store sensitive data like credentials, financial, health, or others' personal info.
