---
name: dictionary-lookup
description: "Look up word definitions, pronunciation, etymology and synonyms with zero API keys — the Free Dictionary API via curl, with honest handling of words it doesn't know. Use when asked define a word, how do you pronounce this, what's the origin of a word, or synonyms for something."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# dictionary-lookup

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

Produces the definition set organized by part of speech, IPA pronunciation with audio link, and the rerunnable command — with the model's own knowledge clearly separated from the fetched source.
