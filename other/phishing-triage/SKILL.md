---
name: phishing-triage
description: "Decide fast whether a suspicious message is a phishing scam — and what to do next — without clicking anything. Use when asked is this email/text a scam, is this message legit, I got a suspicious message, or did I just get phished."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# phishing-triage

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

Produces a quick verdict with the specific red (and green) flags in the message, a safe way to verify through official channels, exactly what to do next (delete/report, or act if genuine), and recovery steps if you already clicked or entered details.
