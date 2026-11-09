---
name: cn-pipl-pia
description: "Use when asked 个人信息保护影响评估怎么做, 写一份 PIA, 处理敏感个人信息要评估吗, 自动化决策评估, PIPL 第五十五条, or assess a processing activity under China's Personal Information Protection Law."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-pipl-pia

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

Produces a personal information protection impact assessment (个人信息保护影响评估) covering the PIPL Article 55 triggers, the Article 56 questions (lawful, legitimate and necessary; impact and risk; adequacy of protection), a risk register with mitigations and owners, and a record kept for at least three years.
