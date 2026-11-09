---
name: tool-procurement-eval
description: "Evaluate a new tool before it joins the stack — the problem-first framing (tools answer needs, not demos), the trial designed with success criteria upfront, the stack-fit check (integration, overlap, the tool-sprawl tax), and the security/data review sized to the stakes. Use when asked should we buy this tool, evaluate this software for the team, we have three tools that do this already, or run a proper trial before committing."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# tool-procurement-eval

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

Produces the need statement, the trial design with pre-set criteria, the stack-fit audit, and the adopt/decline verdict with its reasoning.
