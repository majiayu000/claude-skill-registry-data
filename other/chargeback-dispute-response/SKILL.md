---
name: chargeback-dispute-response
description: "Win a chargeback dispute — read the reason code, assemble the evidence packet, and write the rebuttal that actually persuades the bank. Use when asked to fight a chargeback, respond to a payment dispute, write a chargeback rebuttal, or contest a customer chargeback. For merchants."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# chargeback-dispute-response

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

Produces the reason-code decode, the required-evidence checklist for that code, the structured rebuttal letter, and an honest read on whether this one is winnable — so you fight the right disputes and concede the rest.
