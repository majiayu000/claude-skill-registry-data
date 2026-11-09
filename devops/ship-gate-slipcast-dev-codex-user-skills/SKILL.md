---
name: ship-gate
description: Pre-production audit that scans a codebase for security, database, deployment,
  code quality, AI/LLM, dependency, frontend, and observability issues. Intercepts
  deploy commands and blocks until critical items pass. Stack-agnostic. Use for "run
  ship gate", "am I ready to ship", "pre-launch audit", "can I deploy", "push to production",
  "go live checklist", "preflight check". Not for CI/CD setup or infra provisioning.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# ship-gate

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

