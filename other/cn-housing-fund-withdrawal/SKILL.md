---
name: cn-housing-fund-withdrawal
description: "Use when asked 公积金怎么提取, 租房能提公积金吗, 离职后公积金怎么办, 公积金贷款能贷多少, 异地提取公积金, or plan how to use a Chinese housing provident fund (住房公积金)."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-housing-fund-withdrawal

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

Produces the withdrawal routes the person qualifies for (购房, 还贷, 租房, 离职或离开城市, 退休, 重大疾病 and others), the documents and channels for each, a comparison of withdrawing versus keeping the balance for a 公积金贷款, and the city-specific limits to confirm.
