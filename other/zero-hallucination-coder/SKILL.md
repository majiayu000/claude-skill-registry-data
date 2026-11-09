---
name: zero-hallucination-coder
description: Runs a disciplined Discuss → Map → Decompose → Execute → Verify loop
  that grounds code in verified structure — no invented APIs, no assumed imports,
  no placeholder code — with a lazy-senior-dev YAGNI ladder that deletes unnecessary
  code before it is written. Use when a coding task is high-stakes, complex, or spans
  existing code (auth, databases, migrations, multi-file features), or when the user
  explicitly asks to plan carefully before coding, avoid hallucinated code, or work
  rigorously. Not for trivial edits, typos, or throwaway one-off scripts — those do
  not need the full loop.
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# zero-hallucination-coder

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

