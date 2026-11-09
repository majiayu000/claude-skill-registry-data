---
name: cn-jargon-translator
description: "Use when asked 把这段黑话翻译成人话, 这句话到底什么意思, 帮我把周报去黑话, 用大厂黑话改写这段, 互联网黑话词典, 对齐抓手闭环是什么意思, or translate Chinese internet-company jargon (互联网黑话) into plain words and back."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-jargon-translator

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

Produces a line-by-line translation of 黑话 into plain Chinese with what each sentence actually commits to (who, what, by when), a rewrite at the chosen tone (白话, 得体职场, or 满分大厂味 parody), a 40-plus term glossary with plain meanings, and a 周报去黑话 mode that turns a jargon-heavy weekly report into one a reader can act on.
