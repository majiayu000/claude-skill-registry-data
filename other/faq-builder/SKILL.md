---
name: faq-builder
description: "Build an FAQ from the questions people actually ask — mined from tickets, chats, and repeated explanations, answered once and well, organized by the asker's words, and maintained by a capture loop instead of annual archaeology. Use when asked create an FAQ for this product/process/team, I answer the same questions weekly, turn our support threads into docs, or why does nobody find our answers."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# faq-builder

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

Produces the mined question list with frequencies, the answers in ask-language, the structure, and the capture loop.
