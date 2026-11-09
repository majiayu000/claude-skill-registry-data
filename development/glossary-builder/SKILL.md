---
name: glossary-builder
description: "Build a translation/terminology glossary so a product's key terms render consistently everywhere. Use when asked to create a glossary, a termbase, a do-not-translate list, or to keep terminology consistent across translators/locales."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# glossary-builder

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

Produces a glossary — each source term with its approved translation per locale, part of speech, definition/context, and do-not-translate flags — ready for a CAT tool or style guide.
