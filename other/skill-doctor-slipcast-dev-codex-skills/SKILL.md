---
name: skill-doctor
description: Use when the user wants their agent setup graded from real conversation
  history, asks which installed skills are actually working, or wants evidence-backed
  skill edits — scores recent local Claude Code / Codex sessions against efficiency
  and code-quality rubrics, then drafts skill changes gated by a deterministic aggregator
  and renders one local shareable report.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# skill-doctor

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
