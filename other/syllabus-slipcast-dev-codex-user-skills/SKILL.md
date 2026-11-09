---
name: syllabus
description: Generates a curated supplementary reading list from any course syllabus
  using Consensus academic search. Grill-me intake (syllabus input format + course
  audience + year range) plus a grouping forcing-options checkpoint before any search
  runs — so the reading list matches the course's level and recency need. Parses the
  syllabus to extract topics and learning outcomes, searches Consensus for recent
  peer-reviewed papers per topic, and produces a professionally formatted .docx with
  clickable Consensus links, plain-language summaries calibrated to audience level,
  and Bloom-higher-order discussion questions tied to course learning goals. Use when
  the user uploads a syllabus, course outline, or curriculum document and wants supplementary
  readings (e.g., 'create a reading list from this syllabus', 'find recent papers
  for my course') — even casual mentions with a syllabus attached should trigger this
  skill.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# syllabus

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

