---
name: perimenopause-navigator
description: "Make sense of perimenopause symptoms nobody warned you about and prepare the GP conversation that actually helps — a symptom tracker mapped to what's likely hormonal, the prioritized list to raise, the HRT and treatment questions to ask, and how to push back on dismissal. Use when someone says 'is this perimenopause?', 'my doctor won't take my symptoms seriously', 'help me prepare for a menopause appointment', or is 40-55 and blindsided by symptoms. Not medical advice — it organizes your experience for the clinician who prescribes."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# perimenopause-navigator

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

Produces a symptom map, a GP-visit brief, and a treatment-questions list.
