---
name: tw-labour-standards
description: "Use when asked 加班費怎麼算, 特休有幾天, 被資遣可以拿多少, 預告期間是多久, 勞退 6% 雇主有沒有提繳, 這樣合法嗎 勞基法, or check work terms against Taiwan's Labor Standards Act (勞動基準法)."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# tw-labour-standards

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

Produces a check of the person's situation against the Act (wages and the minimum wage, working hours and overtime pay, annual leave, notice and severance under the new pension system, pension contributions), worked calculations from their own figures, what to ask the employer, and where to complain (地方勞工局 and 1955), each figure marked to confirm.
