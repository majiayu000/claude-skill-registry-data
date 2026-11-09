---
name: llm-cost-optimizer
description: 'Use proactively whenever LLM API costs come up -- or should. Triggers
  include: ''my AI costs are too high'', ''optimize token usage'', ''which model should
  I use'', ''LLM spend is out of control'', ''implement prompt caching'', ''we''re
  about to launch an AI feature'', ''build me an AI endpoint''. Don''t wait for an
  explicit cost complaint -- if someone is building an AI feature, designing an LLM
  endpoint, or choosing between models, cost architecture belongs in the conversation.
  Apply immediately when any of these are true: a system prompt appears that exceeds
  a few hundred tokens, all requests are hitting the same model, max_tokens is not
  set, or no per-feature cost logging exists. NOT for RAG pipeline design (use rag-architect).
  NOT for improving prompt quality or effectiveness (use senior-prompt-engineer).'
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# llm-cost-optimizer

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

