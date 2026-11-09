---
name: prior-authorization-letter
description: "Write a persuasive prior-authorization / medical-necessity letter to an insurer. Use when asked to write a prior authorization letter, a letter of medical necessity, or to appeal a denied treatment/medication/procedure."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# prior-authorization-letter

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

Produces a structured letter — patient and request, clinical justification tied to guidelines, treatments tried, and the specific approval asked for — ready for clinician review and signature.
