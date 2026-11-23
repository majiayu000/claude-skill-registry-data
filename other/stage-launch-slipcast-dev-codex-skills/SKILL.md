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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

