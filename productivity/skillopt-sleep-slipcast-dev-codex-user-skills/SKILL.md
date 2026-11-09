---
name: skillopt-sleep
description: 'Use when the user wants their Claude agent to self-improve from past
  usage, asks about a nightly/offline ''sleep'' or ''dream'' cycle, memory/skill consolidation,
  or says things like ''make my agent better the more I use it'', ''review my past
  sessions'', ''learn my preferences'', ''consolidate what you learned'', ''run the
  sleep cycle'', or wants to schedule offline self-optimization. Drives the skillopt_sleep
  engine: harvest past sessions → mine recurring tasks → replay offline → consolidate
  validated AGENTS.md and SKILL.md behind a held-out gate.'
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# skillopt-sleep

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.



## Особенности переноса

- Runtime отсутствует в установленном наборе: scripts/sleep.sh и пакет skillopt_sleep не включены. Доступны только инструкции; запуск, adopt и schedule возвращают blocked до отдельной установки и проверки CLI.
