---
name: stage-launch
description: Phase 2 of building a Claude Managed Agent — turn a validated build sheet
  into exact API payloads and a resumable BYOK curl launch script, then launch (environment
  → agent → session → kickoff) using the founder's OWN Anthropic key. Use when the
  user says "launch it", "deploy the agent", "create the agent now", or when the orchestrator
  routes phase=stage-launch. payload_generator.py emits the four ordered payloads;
  launch_script_writer.py writes launch.sh that reads $ANTHROPIC_API_KEY at runtime
  and never embeds it; payload_validator.py runs a pre-launch check including an API-key-leak
  scan. No tool in this skill makes network calls — the user runs launch.sh themselves.
  Distinct from interview (planning) and grade-iterate (the outcome loop).
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# stage-launch

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

