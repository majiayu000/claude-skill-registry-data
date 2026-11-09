---
name: dns-lookup
description: "Query DNS records and domain registration data with zero API keys — DNS-over-HTTPS via dns.google and domain registration via RDAP, through plain curl. Use when asked what does this domain resolve to, check the MX or TXT records, who registered this domain, when does it expire, or has DNS propagated."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# dns-lookup

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

Produces the records decoded (SPF/DKIM/DMARC read, not just dumped), the registration facts from RDAP, and the rerunnable commands.
