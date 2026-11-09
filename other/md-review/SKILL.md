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

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

