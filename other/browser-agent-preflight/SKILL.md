---
name: browser-agent-preflight
description: "Run the pre-flight checklist before an agent drives a browser — the untrusted-web-content threat (every page is attacker-controllable), the credential and session-cookie exposure, the action-confirmation gates for purchases and posts, and the sandboxing that limits the damage. Use when asked let my agent browse safely, is it safe to give the agent computer/browser use, guardrails before the agent uses my browser, or review my browser agent's setup."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# browser-agent-preflight

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

Produces the sandbox decision, the content-injection defenses, the action gates, and the credential-isolation rules.
