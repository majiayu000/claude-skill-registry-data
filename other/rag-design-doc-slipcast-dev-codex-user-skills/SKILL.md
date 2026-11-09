---
name: rag-design-doc
description: "Design a Retrieval-Augmented Generation system end to end. Use when asked to design a RAG pipeline, a 'chat with your docs' feature, a knowledge assistant, or to debug why a RAG system gives wrong/ungrounded answers."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# rag-design-doc

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

Produces a RAG design doc — ingestion & chunking, embeddings & index, retrieval & reranking, the generation prompt, grounding/citations, evaluation, and failure modes with mitigations.
