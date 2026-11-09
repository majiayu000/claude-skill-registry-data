---
name: rag-architecture-review
description: "Review an existing Retrieval-Augmented Generation system and find why it underperforms. Use when asked to review or audit a RAG pipeline, diagnose wrong/ungrounded answers from a 'chat with your docs' feature, or improve an already-built knowledge assistant."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# rag-architecture-review

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

Produces a staged review — ingestion, chunking, retrieval, reranking, generation, evaluation — with prioritised findings, root causes, and concrete fixes.
