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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

