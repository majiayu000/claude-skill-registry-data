---
name: scam-message-decoder
description: "Decode a suspicious message — text, email, call transcript, or DM — against the anatomy of known scam families, with a 🔴🟡🟢 read and the safe next move. Use when someone asks is this a scam, decode this suspicious text, my 'bank' just called me, this job offer seems off, or my parent got a weird message."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# scam-message-decoder

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

Produces the verdict with the specific scam-family match, the tells quoted from the message itself, the safe-verification path (never the message's own links or numbers), and the if-you-already-clicked triage.
