---
name: skill-tester
description: 'Validate, test, and score the quality of skills within the claude-skills
  ecosystem. Comprehensive meta-skill: structure validation, Python script testing
  (syntax + imports + runtime + output format), multi-dimensional quality scoring
  with letter grades and tier classification (BASIC/STANDARD/POWERFUL). Use when authoring
  a new skill, auditing existing skills for tier promotion, setting up pre-commit
  hooks for skill quality, or integrating skill QA into CI.'
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# skill-tester

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

