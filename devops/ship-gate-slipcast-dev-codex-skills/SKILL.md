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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

