---
name: tool-permission-review
description: "Review what an agent is actually allowed to do before you turn it loose — the tool-by-tool audit (each capability's blast radius), the least-privilege pass that removes what the task doesn't need, the dangerous-combination check, and the allow/ask/deny tiering. Use when asked review my agent's permissions, what can this agent actually do, lock down my agent's tools, or is this MCP/tool set safe to grant."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# tool-permission-review

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

Produces the permission inventory with blast radius, the least-privilege cuts, the dangerous-combo flags, and the allow/ask/deny assignments.
