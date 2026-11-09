---
name: interview-mapper
description: Maps a single interview transcript into a verbatim-grounded, lens-coded
  structure and checks whether analytic conclusions hold across independent re-runs.
  Use when the user wants to code, map, interpret, or make sense of an interview transcript,
  depth interview, custdev/JTBD/expert/usability/exit/win-loss/focus-group session,
  or wants cross-interview synthesis (insight cards, patterns) built up from coded
  transcripts — even if they don't name a method. Every conclusion must carry a verbatim
  quote verified against the source text; unstable conclusions are flagged for a human,
  never resolved by a single silent pass. Not for generating new interviews, not for
  plain audio transcription, and not for research-method or sample-size planning above
  the transcript (see product-research).
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# interview-mapper

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

