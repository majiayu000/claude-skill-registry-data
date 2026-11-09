---
name: raise-vs-jump
description: "Model staying for annual raises vs job-hopping for bigger bumps — cumulative earnings trajectories, the crossover year, and the costs the salary math hides (vesting resets, promotion paths, search risk). Use when asked should I switch jobs for more money, is job hopping worth it, model my salary if I stay vs leave, or raise versus new offer."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# raise-vs-jump

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

Produces the year-by-year salary and cumulative-earnings table, the crossover year, and the not-in-the-model checklist that usually decides it.
