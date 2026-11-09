---
name: credential-recognition
description: "Get foreign qualifications, degrees, or professional licenses recognised in a new country — figure out whether recognition is even needed, which body assesses it, what evidence they want, and the bridging route if there's a gap. Use when someone says 'get my degree recognised abroad', 'is my foreign license valid here', 'credential evaluation', or 'can I work as a [nurse/engineer/teacher] in [country] with my qualifications'. Routes to official assessment bodies; requirements are country- and profession-specific."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# credential-recognition

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

Produces a recognition roadmap, the assessing body, an evidence checklist, and the bridging options.
