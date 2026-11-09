---
name: cn-labour-contract-decoder
description: "Decode a mainland China labour contract (劳动合同) before signing: probation, pay and its structure, working hours, social insurance, non-compete and confidentiality, termination terms and anything that conflicts with the Labour Contract Law. Use when asked 帮我看看劳动合同, 劳动合同有什么坑, 试用期合法吗, 竞业限制条款, or review my Chinese employment contract. Not legal advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-labour-contract-decoder

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

Produces a clause-by-clause decode with red, amber and green flags, the statutory limits each clause must respect, the questions to ask HR, and suggested wording for changes.
