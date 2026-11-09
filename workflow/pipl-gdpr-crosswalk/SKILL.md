---
name: pipl-gdpr-crosswalk
description: "Compare China's Personal Information Protection Law (PIPL) with the EU GDPR for a specific data flow, and produce the gap list and cross-border transfer path for a company operating in both. Use when asked PIPL vs GDPR, 个人信息保护法和 GDPR 的区别, how do we transfer personal data out of China, our app serves users in China and Europe, or 数据出境 compliance. Not legal advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# pipl-gdpr-crosswalk

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

Produces a requirement crosswalk for the described processing, the transfer mechanism that likely applies in each direction, a prioritised gap list, and the questions to take to counsel.
