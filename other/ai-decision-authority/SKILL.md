---
name: ai-decision-authority
description: Routes marketing and GTM decisions into three AI governance zones (AI-Primary,
  Collaborative, Human-Primary) by stakes and reversibility. Use when deciding which
  AI outputs need human review, whether an agent may act autonomously on a task, why
  AI adoption is collapsing under review requirements, or when auditing a list of
  workflows for safe autonomy. Triggers on 'should a human review this', 'can the
  agent just do this', 'AI governance policy', 'human in the loop'.
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# ai-decision-authority

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

