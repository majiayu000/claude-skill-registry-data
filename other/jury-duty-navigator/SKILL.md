---
name: jury-duty-navigator
description: "Handle a jury summons calmly — confirm it's real, understand what's actually required, request a deferral or excusal the right way if you genuinely need one, arrange work and pay, and know what to expect at selection and on the day. Use when someone says I got a jury summons, can I get out of jury duty, how do I defer jury service, or what happens at jury duty. Not legal advice; routes to the court for anything binding and never coaches dodging a legal obligation."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# jury-duty-navigator

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

Produces a response plan, a deferral/excusal request if warranted, and a what-to-expect brief, with a clear warning that ignoring a summons has consequences.
