---
name: cn-extracurricular-plan
description: "Use when asked 兴趣班怎么选, 孩子报几个兴趣班合适, 课外班规划, 双减后还能报什么班, 寒暑假怎么安排, 预付费培训退费, or plan a child's out-of-school activities in mainland China."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-extracurricular-plan

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

Produces a weekly timetable that protects sleep, homework and free play, a choice framework (the child's interest, purpose, cost, travel), a term budget, a check of each class against the 双减 rules on academic training and prepaid fees, contract questions to ask a provider, and a review point to drop what is not working, with rules marked to confirm locally.
