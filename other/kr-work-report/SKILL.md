---
name: kr-work-report
description: "Use when asked 보고서 써 줘, 주간보고 작성해 줘, 개조식으로 정리해 줘, 팀장님께 보고할 내용 정리, 1페이지 보고서, 업무 보고서 양식, or write a Korean business report or weekly report."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# kr-work-report

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

Produces a Korean workplace report in 개조식 and 두괄식 style: a one-line conclusion, then 현황, 문제점, 대안 비교, 건의사항 and 향후 계획 for a 보고서, or 금주 실적, 차주 계획 and 이슈 및 협조 요청 for a 주간보고, with consistent noun-form endings, numbers and owners, plus a short verbal briefing version.
