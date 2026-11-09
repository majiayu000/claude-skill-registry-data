---
name: panel-of-experts
description: "Get the take of the specific experts a situation actually needs — a lawyer, a therapist, an accountant, a doctor-minded thinker, whoever fits — each in their own voice. Use when asked what would a [profession] say, get expert perspectives on this, who should I be thinking like here, or what am I missing that a pro would catch."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# panel-of-experts

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

Produces a panel of the right domain experts for your situation, each flagging what a layperson would miss, where they'd disagree, and what to verify with a real professional — never a substitute for licensed advice on serious matters.
