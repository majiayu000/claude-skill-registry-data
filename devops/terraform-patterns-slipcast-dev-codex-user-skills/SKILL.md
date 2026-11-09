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
