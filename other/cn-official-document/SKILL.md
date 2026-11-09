---
name: cn-official-document
description: "Use when asked 帮我写公文, 写一份请示, 写通知 / 报告 / 函 / 纪要, 公文格式怎么排, check this document against GB/T 9704, or draft an official document for a Chinese government body, public institution or state-owned enterprise."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-official-document

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

Produces a 公文 in the right document type with every required element in the order GB/T 9704-2012 sets, heading levels and numbering, a layout specification for Word or WPS, and a check of the type-specific rules such as one matter per 请示.
