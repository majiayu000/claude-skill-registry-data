---
name: prompt-library-builder
description: "Build a personal library of reusable prompts for the things you ask AI again and again — so you stop rewriting the same request from scratch. Use when asked help me build a prompt library, save my best prompts, I keep writing the same prompts, or organize my AI prompts."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# prompt-library-builder

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

Produces a captured set of your recurring AI tasks turned into reusable, parameterized prompt templates, an organization scheme so you can find them, guidance on what makes a prompt reusable (clear role, inputs, output format), and how to store and improve them — turning ad-hoc prompting into a personal toolkit that compounds.
