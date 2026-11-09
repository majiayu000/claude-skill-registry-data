---
name: cn-prd-review
description: "Prepare for and run a product requirements review (需求评审 / PRD 评审会) the way Chinese internet teams do it: a pre-read the engineers, testers and designers can challenge, the questions each role will ask, the meeting run sheet and a written conclusion (通过 / 有条件通过 / 不通过). Use when asked 帮我准备需求评审, PRD 评审会怎么开, 评审前检查一下我的 PRD, 研发会问什么问题, or prepare my requirements review in Chinese."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-prd-review

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

Produces a readiness check of the PRD, a role-by-role question bank with answer points, a 60-minute run sheet, and the review minutes template with the conclusion and follow-ups.
