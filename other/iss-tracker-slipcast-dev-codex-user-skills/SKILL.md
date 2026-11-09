---
name: iss-tracker
description: "Track the International Space Station live with keyless curl — where it is right now, what it's over, and when to look up, with the orbital math translated into human terms. Use when asked where is the ISS right now, is the space station overhead, when can I see the ISS tonight, or track the station for the kids."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# iss-tracker

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

Produces the live position translated to a place name, the overhead-math explained, the visibility rules of thumb, and the rerunnable command — the library's proof that live data can also just be delightful.
