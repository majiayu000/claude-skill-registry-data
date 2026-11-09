---
name: opposing-counsel
description: "Read a contract the way the counterparty's lawyer will — hunting for leverage, not fairness. Use when someone says 'read this like opposing counsel', 'how would the other side attack this agreement', 'find the weaknesses before they do', or before sending or signing any contract."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# opposing-counsel

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

Produces the demand/position letter opposing counsel would actually send, plus an out-of-character debrief with the clause fixes that defang each attack.
