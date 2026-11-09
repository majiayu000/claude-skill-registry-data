---
name: wecom-announcement
description: "Write an internal announcement for WeCom (企业微信) or a company group chat: policy changes, office notices, system outages, holiday arrangements and organisational updates, in the clear, polite register Chinese staff expect. Use when asked 写一则企业微信公告, 帮我写内部通知, 放假通知, 系统维护通知, 组织架构调整公告, or write a staff announcement in Chinese."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# wecom-announcement

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

Produces the announcement with a 标题, the one-line 要点, details by audience, actions and deadlines, a contact, plus a short version for group chats and a pinned-message version.
