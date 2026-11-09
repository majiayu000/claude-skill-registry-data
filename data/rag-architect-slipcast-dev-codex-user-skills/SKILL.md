---
name: rag-architect
description: 'Use when the user asks to design a RAG pipeline, choose a chunking strategy
  or embedding model, pick a vector database, or evaluate retrieval quality (precision@k,
  recall@k, NDCG). Examples: ''design a RAG system for our docs'', ''what chunk size
  should I use for this corpus'', ''evaluate my retriever against ground truth''.
  NOT for general LLM cost tuning (use llm-cost-optimizer) or agent loops over retrieval
  (use agenthub).'
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# rag-architect

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

