---
name: fable-goal
description: Convert a rambling description of a desired outcome into one polished,
  autonomous /goal prompt ready to paste into a fresh session. Use when the user says
  "/fable-goal", "turn this into a goal prompt", "write me a fable prompt", "write
  the prompt that builds X", or rambles about something they want made and asks for
  the prompt that makes it happen. The output is a single copy-paste prompt, never
  the build itself. Do NOT use when the user wants the thing built right now in this
  session — only when they want the PROMPT that will make it happen in a fresh session.
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# fable-goal

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

- Исходные команды или настройки требуют проверки совместимости.
