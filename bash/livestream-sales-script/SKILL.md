---
name: livestream-sales-script
description: "Plan and script a live-commerce session (直播带货): the run of show, the script for each product segment, interaction prompts, offer timing, and a compliance check of every claim and price statement. Use when asked 帮我写直播带货脚本, 直播间话术, 直播流程, 直播排品, or write a livestream sales script."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# livestream-sales-script

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

Produces the session run of show by minute, a per-product script with selling points and objection answers, interaction and retention prompts, the offer schedule, a host and assistant split, and a compliance check against false advertising and price rules.
