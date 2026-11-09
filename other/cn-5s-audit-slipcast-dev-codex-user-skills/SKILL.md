---
name: cn-5s-audit
description: "Use when asked 5S 检查表, 6S 管理, 现场管理检查, 5S 评分标准, 车间 6S 稽核, 做一份 5S 推行计划, or design a 5S or 6S audit for a workshop, warehouse or office in a Chinese factory."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-5s-audit

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

Produces an audit checklist for the area with scored criteria for 整理, 整顿, 清扫, 清洁, 素养 (and 安全 for 6S), a scoring guide with photo evidence rules, a results summary and red-tag list, a corrective-action tracker with owners and dates, and an audit rota, in Chinese.
