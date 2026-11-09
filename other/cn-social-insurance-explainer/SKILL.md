---
name: cn-social-insurance-explainer
description: "Explain China's social insurance and housing fund (五险一金) for a specific person and city: what each part covers, what they and their employer pay, how the contribution base works, and what happens when they change job, city or leave work. Use when asked 五险一金是什么, 社保怎么交, 公积金怎么提取, 换工作社保断了怎么办, 社保基数, or explain Chinese social insurance. Not financial advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-social-insurance-explainer

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

Produces a plain explanation for their situation, a contribution calculation using their city's current rates, and a checklist for job changes, moving city, unemployment or freelancing.
