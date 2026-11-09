---
name: cn-lesson-plan
description: "Use when asked 帮我写教案, 写一份新课标教案, 教学设计, 单元教学设计, 大单元教案, or a lesson plan in the format Chinese schools expect."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-lesson-plan

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

Produces a complete 教案 in Chinese with 教材分析, 学情分析, 教学目标 tied to the subject's 核心素养, 教学重难点, 教学方法, a timed 教学过程 with teacher and student activity, 板书设计, layered 作业设计 within the 双减 time limits, and 教学反思 prompts, with curriculum references marked to confirm against the current 课程标准.
