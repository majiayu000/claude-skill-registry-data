---
name: ip-lookup
description: "Look up IP addresses and your own public IP with zero API keys — geolocation, ISP/ASN, and hosting flags via ip-api.com and ipify through curl. Use when asked what's my public IP, where is this IP from, whose network is this address, or is this IP a VPN/datacenter."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ip-lookup

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

Produces the lookup with ISP, ASN, and location fields interpreted honestly (city-level accuracy caveats included), and the rerunnable command.
