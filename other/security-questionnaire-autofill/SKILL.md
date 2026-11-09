---
name: security-questionnaire-autofill
description: "Draft answers to a vendor security questionnaire (SIG, CAIQ, or a custom sheet) from your real controls — fast, consistent, and honest about gaps. Use when asked to fill out a security questionnaire, answer a SIG/CAIQ, respond to a customer's security review, or complete a vendor risk assessment."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# security-questionnaire-autofill

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

Produces drafted answers grounded in your stated controls, a gap list of questions you can't truthfully answer yet, and reusable answer snippets for next time — never fabricated compliance.
