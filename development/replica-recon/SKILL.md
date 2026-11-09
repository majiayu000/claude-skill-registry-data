---
name: replica-recon
description: 'Reverse-engineers any app into a recon map: screen inventory, user flows,
  component list, inferred data model and a feature matrix, from public pages, screenshots,
  app store listings, help docs and the user''s own account. The first step of the
  Replica pack. Use when the user says "clone this app", "reverse engineer X", "how
  does X work", "map out X", "what screens does X have", "I want to build my own version
  of X", "copy this app", or pastes an app''s URL or App Store link and wants to rebuild
  it.'
metadata:
  source-package: replica-skill-main
  adapted-for: Codex
---

# replica-recon

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

