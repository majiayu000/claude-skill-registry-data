---
name: md-review
description: Converts a markdown PR writeup or code review (one with ```diff fenced
  blocks and severity-tagged GFM callouts [!BLOCKER]/[!MAJOR]/[!MINOR]/[!NIT] callouts)
  into a single-file 2-column HTML review — unified-diff on the left, severity-tagged
  annotation cards on the right, top jump-nav listing every finding, mandatory named
  reviewer footer. Triggers when the markdown-html-orchestrator classifies an input
  as REVIEW, or when invoked directly via /cs-md-review. Refuses without explicit
  --reviewer (a code review must name a human), refuses if no diff hunks present (route
  to md-document instead), and refuses to encode severity in color only (every badge
  ships color + icon + aria-label per WCAG 1.4.1). Use after orchestrator routing.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# md-review

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

