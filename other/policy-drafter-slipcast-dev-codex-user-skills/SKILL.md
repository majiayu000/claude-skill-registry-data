---
name: policy-drafter
description: "Draft an internal policy people can actually follow — the rule stated plainly with its reason, the bright lines separated from the judgment zones, the edge cases resolved by principle, and the enforcement reality stated honestly. Use when asked write our expense/remote-work/AI-use/security policy, turn this incident into a policy, our policy doc is unreadable, or people keep asking what's allowed."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# policy-drafter

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

Produces the policy with rules-plus-reasons, the bright-line/judgment split, the worked edge cases, and the honest enforcement section.
