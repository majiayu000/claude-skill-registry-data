---
name: reply-in-their-tone
description: "Draft email replies that match the sender's register — formality, length, directness, and emoji-tolerance read from their message, so the reply lands as native instead of off-key. Use when asked reply to this email, draft a response that doesn't sound stiff, match their tone, or answer this without sounding like a robot."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# reply-in-their-tone

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

Produces the tone read of the incoming message, the reply drafted in that register, and the adjustment knobs.
