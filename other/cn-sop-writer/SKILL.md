---
name: cn-sop-writer
description: "Use when asked 写作业指导书, SOP 作业指导书, 工序作业标准, 标准作业书, 新员工看得懂的操作说明, WI 怎么写, or write a shop-floor work instruction for a production or inspection step in a Chinese factory."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-sop-writer

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

Produces a one-station 作业指导书 in Chinese with the header block (文件编号, 版本, 工序, 产品, 标准工时), materials and tools, numbered steps with key points (要点) and the reasons, quality checks and limits, safety notes and PPE, photo or diagram placeholders, abnormal-situation handling, and a revision record, written for a new operator.
