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

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.



## Особенности переноса

- В исходном наборе не разрешён ресурс ./pages/01-home.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
- В исходном наборе не разрешён ресурс ./pages/02-dashboard.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
- В исходном наборе не разрешён ресурс ./pages/03-user-list.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
- В исходном наборе не разрешён ресурс ./pages/04-user-detail.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
- В исходном наборе не разрешён ресурс ./pages/05-settings.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
