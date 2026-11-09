---
name: cn-medical-insurance-claim
description: "Use when asked 医保怎么报销, 异地就医怎么备案, 住院能报多少, 门诊报销比例, 手工报销要什么材料, 惠民保值不值得买, or work out what China's basic medical insurance (医保) will pay for a treatment."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-medical-insurance-claim

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

Produces the person's scheme (职工医保 or 居民医保), how a claim works for this case (direct settlement or manual reimbursement), an out-of-pocket estimate built from the city's own deductible, rate and cap, the cross-region registration (异地就医备案) steps, and the documents to keep.
