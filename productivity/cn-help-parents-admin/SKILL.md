---
name: cn-help-parents-admin
description: "Use when asked 帮爸妈办医保, 帮父母办养老金认证, 爸妈异地就医备案, 帮老人办银行业务, 父母被诈骗了怎么办, 教爸妈用手机办事, 代办委托书, or help an adult child handle 医保, 社保, 养老金, banking or scam protection for ageing parents in mainland China."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-help-parents-admin

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

Produces a task list for this errand, what the adult child can do remotely versus what needs the parent in person, the documents and authorisation needed, a step list for the parent in very plain large-step language (长辈版) with a call-for-help line, and an anti-scam card, with every local rule marked to confirm.
