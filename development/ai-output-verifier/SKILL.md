---
name: ai-output-verifier
description: "Check AI output before you trust or use it — where it's likely wrong, what to verify, and how to catch confident-sounding errors. Use when asked can I trust this AI answer, how do I verify what AI told me, fact-check this AI output, or is this AI response reliable."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ai-output-verifier

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

Produces a risk read on the specific output (the claims most likely to be wrong or made up), the parts that need independent verification vs the parts that are low-risk, how to actually verify each, the tells of AI hallucination and overconfidence, and a habit for building verification into your AI use — because AI is confidently wrong often enough that unchecked trust is a real risk.
