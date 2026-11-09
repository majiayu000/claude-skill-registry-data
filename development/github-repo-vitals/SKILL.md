---
name: github-repo-vitals
description: "Read a GitHub repository's vital signs with keyless curl — commit recency, release cadence, issue/PR responsiveness, and bus factor — interpreted into an is-this-project-alive verdict. Use when asked is this repo maintained, check this project before we build on it, how active is this library's development, or compare these repos' health."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# github-repo-vitals

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

Produces the vitals with their reads, the responsiveness sampling, the rate-limit-aware command set, and the alive/coasting/abandoned verdict.
