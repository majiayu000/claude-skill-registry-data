---
name: code-to-prd
description: 'Reverse-engineer any codebase into a complete Product Requirements Document
  (PRD). Analyzes routes, components, state management, API integrations, and user
  interactions to produce business-readable documentation detailed enough for engineers
  or AI agents to fully reconstruct every page and endpoint. Works with frontend frameworks
  (React, Vue, Angular, Svelte, Next.js, Nuxt), backend frameworks (NestJS, Django,
  Express, FastAPI), and fullstack applications. Use when users mention: generate
  PRD, reverse-engineer requirements, code to documentation, extract product specs
  from code, document page logic, analyze page fields and interactions, create a functional
  inventory, write requirements from an existing codebase, document API endpoints,
  or analyze backend routes.'
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# code-to-prd

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- В исходном наборе не разрешён ресурс ./pages/01-home.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
- В исходном наборе не разрешён ресурс ./pages/02-dashboard.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
- В исходном наборе не разрешён ресурс ./pages/03-user-list.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
- В исходном наборе не разрешён ресурс ./pages/04-user-detail.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
- В исходном наборе не разрешён ресурс ./pages/05-settings.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
