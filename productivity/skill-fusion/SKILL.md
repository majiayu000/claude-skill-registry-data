---
name: skill-fusion
description: "Fuse two skills from this library into one hybrid brief for a task that sits between them — the meta-skill. Use when a task straddles two skills (a PRD that's also a pitch; a postmortem that must double as a board update) and running them separately would produce two documents where one is needed."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# skill-fusion

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

Produces the fused operating brief: combined structure, merged quality bar, precedence rules for where the parents disagree, and the fused output itself if input was provided.
