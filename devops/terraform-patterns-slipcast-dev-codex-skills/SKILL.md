---
name: terraform-patterns
description: 'Terraform infrastructure-as-code agent skill and plugin for Claude Code,
  Codex, Gemini CLI, Cursor, OpenClaw. Covers module design patterns, state management
  strategies, provider configuration, security hardening, policy-as-code with Sentinel/OPA,
  and CI/CD plan/apply workflows. Use when: user wants to design Terraform modules,
  manage state backends, review Terraform security, implement multi-region deployments,
  or follow IaC best practices.'
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# terraform-patterns

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
