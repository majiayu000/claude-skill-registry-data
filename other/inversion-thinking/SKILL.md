---
name: inversion-thinking
description: "Solve a problem backwards — ask how to guarantee the worst outcome, then avoid all of it. Use when asked to help me not fail at, what could go wrong with, how do I avoid messing up, or think about this in reverse."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# inversion-thinking

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

Produces the inverted question (how to guarantee failure), the specific ways you'd cause the disaster, and then the plan that is simply the avoidance of each — often clearer and more actionable than trying to plan success directly, because failure modes are more concrete than success factors.
