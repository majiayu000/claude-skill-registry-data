---
name: cn-school-entry
description: "Use when asked 幼升小怎么准备, 小升初流程, 入学信息采集, 学区房和多校划片, 公民同招, 民办摇号, 随迁子女入学, 居住证入学材料, or plan a child's entry to primary or junior high school in mainland China."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-school-entry

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

Produces a month-by-month timeline for the child's city, the documents to prepare (户籍, 房产 or 租房, 居住证, 社保), the questions to ask the 教育局 or school about 学区, 多校划片 and 派位, a public versus private comparison, and a checklist, with every local rule marked to confirm with the local education bureau.
