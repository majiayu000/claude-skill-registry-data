---
name: cn-homework-helper-parent
description: "Use when asked 孩子这道题不会怎么教, 辅导作业总发火, 怎么给孩子讲应用题, 陪写作业, 作业太多写到很晚, or help a parent guide (not do) a child's homework in China."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-homework-helper-parent

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

Produces, for the specific question, an age-appropriate way to explain it with guiding questions in order, a hint ladder that stops before the answer, a similar practice item, what to do if the child is stuck or upset, and a homework routine, written for the parent in Chinese; it never hands over a finished answer for the child to copy.
