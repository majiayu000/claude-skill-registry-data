---
name: bilingual-cv-zh-en
description: "Produce a matched Chinese and English CV (中英文简历) from one set of facts: each version follows its own conventions rather than a literal translation, with names, titles, dates, education and company names rendered correctly in both. Use when asked for a Chinese and English resume, translate my CV into Chinese, 中英文简历, 英文简历, or apply to a foreign company in China or a Chinese company abroad."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# bilingual-cv-zh-en

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

Produces the Chinese CV, the English CV, a consistency table proving the facts match, and a glossary of the terms chosen.
