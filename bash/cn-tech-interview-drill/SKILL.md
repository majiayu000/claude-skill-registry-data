---
name: cn-tech-interview-drill
description: "Use when asked 帮我准备大厂技术面试, 八股文怎么背, 模拟一面二面, 系统设计面试题, 项目深挖怎么答, 手撕算法, or run a mock technical interview for a Chinese internet company."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-tech-interview-drill

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

Produces a preparation plan for the interview rounds Chinese tech companies run (笔试, 技术一面二面, 交叉面, HR 面), a 八股 question bank by stack with answer points, a system design walkthrough, a project deep-dive script, and a mock round asked one question at a time with follow-ups (追问) and scores.
