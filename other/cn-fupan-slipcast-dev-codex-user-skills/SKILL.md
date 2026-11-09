---
name: cn-fupan
description: "Run a 复盘 (fupan), the structured project review widely used in Chinese companies: review the goal, assess the result, analyse why, and draw rules for next time, with a blame-free tone and owned actions. Use when asked 帮我做复盘, 项目复盘, 活动复盘, 复盘会怎么开, or a fupan or retrospective in Chinese."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-fupan

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

Produces the 复盘 document in Chinese with goal versus result, root causes split into controllable and uncontrollable, lessons stated as reusable rules, and an action list with owners and dates, plus a meeting agenda.
