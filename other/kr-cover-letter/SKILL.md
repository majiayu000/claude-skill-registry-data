---
name: kr-cover-letter
description: "Use when asked 자기소개서 써 줘, 자소서 첨삭해 줘, 지원동기 어떻게 써, 입사 후 포부 항목, 대기업 공채 자소서, 공기업 NCS 자기소개서, or write a Korean self-introduction essay for a job application."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# kr-cover-letter

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

Produces a 항목별 자기소개서 for a Korean employer: one answer per question within the character limit (공백 포함 or 제외 as specified), each with a 소제목, a 두괄식 opening and a concrete experience told as situation, action and result, tied to the job and company, plus a character count and the interview questions each answer invites.
