---
name: i18n-readiness-review
description: "Review a product/codebase for internationalization readiness before you localize. Use when asked if a product is ready to localize, to review i18n readiness, find hard-coded strings/locale bugs, or prep for going multilingual."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# i18n-readiness-review

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

Produces a readiness audit — externalized strings, locale-aware formatting, layout/expansion, encoding/RTL, and a prioritised list of i18n fixes to make before translation starts.
