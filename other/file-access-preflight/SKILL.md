---
name: file-access-preflight
description: "Run the pre-flight checklist before an agent gets filesystem access — the scope boundary (which directories, read vs write), the secrets-exposure sweep, the destructive-operation gates, and the path-traversal and untrusted-file defenses. Use when asked let my agent access my files safely, is it safe to give the agent file/computer access, guardrails before the agent touches my filesystem, or scope down my coding agent's reach."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# file-access-preflight

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

Produces the scope boundary, the secrets sweep, the write/delete gates, and the untrusted-content rules.
