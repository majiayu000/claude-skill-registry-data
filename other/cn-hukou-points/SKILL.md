---
name: cn-hukou-points
description: "Use when asked 积分落户怎么算, 我能不能落户上海 / 北京 / 深圳, 居转户条件, 落户积分差多少, 人才引进落户, or check eligibility for a city household registration (户口) in China."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-hukou-points

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

Produces the routes available in the person's city (积分落户, 居转户, 人才引进, 应届生落户 and others), a score estimate built only from the city's current official scoring table, the gap and how to close it, a document checklist and a timeline, each marked to confirm with the city's official notice.
