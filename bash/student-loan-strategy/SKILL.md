---
name: student-loan-strategy
description: "Decide what the extra money does about student loans — attack them, invest alongside them, or ride a forgiveness track — with the three paths simulated on your actual loans and the guaranteed-vs-assumed framing kept honest. Use when asked should I pay off my student loans faster, pay loans or invest, is my forgiveness track worth it, or model my student debt."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# student-loan-strategy

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

Produces the three-path comparison from the script, the guaranteed-return framing, the forgiveness-track math with its warnings, and the decision sheet.
