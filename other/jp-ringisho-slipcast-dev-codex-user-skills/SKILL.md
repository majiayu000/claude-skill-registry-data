---
name: jp-ringisho
description: "Use when asked 稟議書の書き方, write a ringi approval request in Japanese, 稟議書を作って, how to get a purchase or project approved in a Japanese company, or 帮我写一份日本公司的稟議書."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# jp-ringisho

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

Produces a finished 稟議書 in standard Japanese corporate structure and polite register: purpose, background, proposal, cost and its basis, alternatives compared, expected effect, risks, approval route, and attachments, plus the questions approvers are likely to ask.
