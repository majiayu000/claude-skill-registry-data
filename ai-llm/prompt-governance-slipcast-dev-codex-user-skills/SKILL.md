---
name: prompt-governance
description: 'Use when managing prompts in production at scale: versioning prompts,
  running A/B tests on prompts, building prompt registries, preventing prompt regressions,
  or creating eval pipelines for production AI features. Triggers: ''manage prompts
  in production'', ''prompt versioning'', ''prompt regression'', ''prompt A/B test'',
  ''prompt registry'', ''eval pipeline''. NOT for writing or improving individual
  prompts (use senior-prompt-engineer). NOT for RAG pipeline design (use rag-architect).
  NOT for LLM cost reduction (use llm-cost-optimizer).'
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# prompt-governance

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

