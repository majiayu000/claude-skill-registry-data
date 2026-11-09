---
name: should-i-send-this
description: "Gut-check a message before you send it — is it going to land the way you intend, or will you regret it in an hour? Use when asked should I send this, is this message okay to send, check this before I hit send, or will I regret this text/email."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# should-i-send-this

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

Produces a read on how the message will actually land for its recipient, the parts that could be misread or that you're sending from emotion, whether now is the right time to send it at all, and a calmer rewrite if needed — catching the hot, snippy, or oversharing message before it does damage you can't undo.
