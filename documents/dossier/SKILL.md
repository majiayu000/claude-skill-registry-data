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

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

