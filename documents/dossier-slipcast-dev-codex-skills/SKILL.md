---
name: dossier
description: Decision-grade entity research skill — produces a hypothesis-tested dossier
  on a specific company, person, nonprofit, or government org, not a generic profile.
  Forcing intake makes the user state their hypothesis upfront (what they already
  believe and want to verify or disprove) so the dossier tests it rather than confirms
  it. Output is an editable Word document (.docx) with verdict on the hypothesis,
  identity facts, 12-month activity timeline, network and reputation signals, red
  flags, conversation hooks tied to specific findings, and source-provenance audit
  log. Uses WebSearch + WebFetch + free APIs (SEC EDGAR, GitHub, ProPublica) as workhorses;
  optional BYOK MCPs enhance coverage. Use when the user asks for background research,
  diligence, or meeting prep on a specific entity (e.g., 'prep me for a meeting with
  [person/company]', 'due diligence on [company]'). Honors sensitivity exclusions
  for journalism + personal-vetting contexts.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# dossier

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

