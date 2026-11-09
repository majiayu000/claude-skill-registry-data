---
name: severance-agreement-decoder
description: "Decode a severance agreement before you sign it — what you're giving up, what's negotiable, and the deadlines that decide your leverage. Use when asked to decode my severance, is this severance offer normal, review my separation agreement, or should I sign this release."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# severance-agreement-decoder

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

Produces a clause-by-clause decode with ranked red flags, the money math (severance vs what you're releasing), the consideration-period clock, and the asks worth making.
