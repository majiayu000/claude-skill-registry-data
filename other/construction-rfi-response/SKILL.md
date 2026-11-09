---
name: construction-rfi-response
description: "Answer a construction request for information so the site can act on it — a direct answer, the drawing or specification reference that supports it, and an explicit statement of whether it changes cost or programme. Use when asked to respond to an RFI, answer a contractor query, or handle a request for information on site, or when RFIs keep coming back for clarification."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# construction-rfi-response

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

Produces the answer with its reference, the cost and time implication stated, the instruction status, the distribution list, and the register entry.
