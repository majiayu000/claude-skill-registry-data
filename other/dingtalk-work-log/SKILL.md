---
name: dingtalk-work-log
description: "Write a DingTalk work log (钉钉日志): the daily report (日报), weekly report (周报) or monthly report (月报) in the fields DingTalk's built-in log templates use, so it can be filled in directly. Use when asked 帮我写钉钉日报, 钉钉日志怎么写, 今日完成工作, 写日报, fill in my DingTalk daily report, or turn today's notes into a 日报."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# dingtalk-work-log

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

Produces the log field by field (今日完成工作, 未完成工作, 需协调工作, 备注 or the weekly and monthly equivalents), each short enough for the mobile form, plus a one-line version for the team group.
