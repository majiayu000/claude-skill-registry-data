---
name: cn-inquiry-reply
description: "Use when asked 回复询盘, 外贸询盘怎么回, 帮我回客户邮件, 阿里国际站询盘回复, 客户只问价格怎么回, 跟进没回复的客户, or reply to a foreign-trade inquiry from a Chinese exporter."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-inquiry-reply

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

Produces a reply email in English (or the buyer's language) with a Chinese version for the sales team, a read of the inquiry's quality and the buyer's likely type, the questions to qualify the buyer, a price or quotation approach without underselling, and a follow-up sequence for no reply, with export-control and sanctions checks flagged.
