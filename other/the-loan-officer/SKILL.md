---
name: the-loan-officer
description: "Simulate the mortgage or business-loan underwriting conversation before you have it for real — the deposit-source probe, the any-other-debts completeness test, the casual question about your job plans that can sink the file — run against your actual numbers, with a debrief on every answer that raised a flag. Use when asked to practice a mortgage interview, prep for a loan application meeting, why might the bank decline us, or what will the underwriter ask. Not financial advice; never coaches concealment."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# the-loan-officer

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

Produces the interview transcript with the officer's file notes, the flag list by severity, and a debrief with the document that answers each flag.
