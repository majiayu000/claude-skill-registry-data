---
name: vuln-triage
description: "Triage a vulnerability or scanner finding — assess real severity, exploitability, and how urgently to fix. Use when asked to triage a CVE, prioritize scanner/pentest findings, assess a vuln's risk, or decide what to patch first."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# vuln-triage

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

Produces a triage verdict: CVSS-informed severity adjusted for your context, exploitability, real risk, a fix/mitigation, and an SLA — so you fix what matters, not just what's red.
