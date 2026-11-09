---
name: claim-denial-decoder
description: "Decode an insurance claim denial letter — what the cited reason actually means, whether it's commonly overturnable, and the appeal letter that answers it point by point. Use when someone asks 'my insurance claim was denied what do I do', 'decode this denial letter', 'can I appeal this denial', or 'write my insurance appeal'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# claim-denial-decoder

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

Produces the denial decode with overturn-likelihood framing, the evidence checklist, the point-by-point appeal letter, and the escalation ladder past the insurer.
