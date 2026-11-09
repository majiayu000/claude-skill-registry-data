---
name: llm-guardrails-spec
description: "Specify the safety and reliability guardrails for an LLM feature before it ships. Use when asked to define LLM guardrails, add safety controls to an AI feature, prevent prompt injection or jailbreaks, or harden a chatbot/agent against misuse."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# llm-guardrails-spec

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

Produces a guardrails spec — threats, input/output controls, refusal and escalation policy, logging, and a red-team test set — mapped to where each control runs.
