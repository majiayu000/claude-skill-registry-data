---
name: cn-small-business-tax
description: "Use when asked 个体户怎么报税, 小规模纳税人增值税怎么算, 小微企业所得税优惠, 经营所得汇算, 开票超过免税额怎么办, or plan taxes for a sole trader (个体工商户) or small company in China."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-small-business-tax

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

Produces the taxes that apply (增值税, 附加税费, 个人所得税经营所得 or 企业所得税), the relief that may apply with the announcement to check, a worked estimate from the person's own figures, a filing calendar, and the questions for the local tax office or 12366.
