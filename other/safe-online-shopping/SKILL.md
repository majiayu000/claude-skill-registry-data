---
name: safe-online-shopping
description: "Check whether an online store or seller is legit before you pay — and pay in a way you can get your money back if it isn't. Use when asked is this website legit, is this online store a scam, should I buy from this site, or how to shop safely online."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# safe-online-shopping

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

Produces a trust assessment from the store's signals (too-good pricing, contact/policy gaps, domain and review red flags), safe-payment guidance that preserves buyer protection, what to check before checkout, and what to do if you've already paid a scam site.
