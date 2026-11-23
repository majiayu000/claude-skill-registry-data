---
name: write-a-skill
description: Create new agent skills with proper structure, progressive disclosure,
  and bundled resources. Use when user wants to create, write, build, or author a
  new skill.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# write-a-skill

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- В исходном наборе не разрешён ресурс references/topic.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
