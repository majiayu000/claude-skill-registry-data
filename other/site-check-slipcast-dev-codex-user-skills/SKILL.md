---
name: site-check
description: "Answer 'is this site down or is it just me' properly — curl status/timing diagnostics, DNS cross-check, and TLS certificate reads, assembled into a where-it's-broken diagnosis. Use when asked is this website down, why can't I reach this site, check if my site is up, or is the SSL certificate expired."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# site-check

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

Produces the layered diagnosis (DNS → TLS → HTTP → content), response timing, cert expiry, and the rerunnable commands.
