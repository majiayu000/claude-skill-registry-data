---
name: cn-shuzhi-deck
description: "Use when asked 帮我做述职 PPT, 述职 PPT 大纲, 年终述职怎么讲, 10 分钟述职讲稿, 述职 PPT 每页写什么, or turn a written year-end review into a 述职 presentation. For writing the review itself use cn-year-end-review; for a promotion to the next level use cn-promotion-defence."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-shuzhi-deck

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

Produces a slide-by-slide 述职 PPT outline with a conclusion-first headline per slide (结论先行), the chart or visual for each, a timed speaking script (讲稿) that fits the slot, a one-slide version for a short slot, and a rehearsal and Q&A checklist.
