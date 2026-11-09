---
name: self-host-packager
description: "Use when asked to make a project self-hostable, package an app for Docker, write a docker-compose setup, document self-hosting, or let users run my app on their own server."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# self-host-packager

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

Produces a one-command self-host for a project: docker-compose.yml, a .env.example with a table explaining every variable, SELF_HOSTING.md covering HTTPS, backups and upgrades, and a back-up-this-folder section that tells users exactly what holds all their data.
