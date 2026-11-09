---
name: package-health
description: "Check a package's health before you depend on it — npm and PyPI registry APIs via keyless curl: downloads, release recency, maintenance signals, and the dependency-decision read. Use when asked is this npm package maintained, check this PyPI library before we adopt it, compare these two packages, or is this dependency abandoned."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# package-health

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

Produces the health read with the signals interpreted (not just listed), the numbers with their commands, and the adopt/avoid/vendor recommendation framing.
