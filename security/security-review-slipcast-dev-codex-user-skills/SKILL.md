---
name: security-review
description: "Review a design, PR, or feature for security issues before it ships. Use when asked to do a security review, security-review a change/PR, or check a feature for vulnerabilities. For code and systems you own or are authorized to review."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# security-review

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

Produces a structured review across the common risk areas (authn/authz, input handling, secrets, data exposure, dependencies), findings ranked by severity with concrete fixes, and a ship / fix-first verdict.
