---
name: interview-synthesis
description: "Turn a pile of interview notes into findings that survive scrutiny — the code-then-theme pass, the counting discipline (how many actually said it), the quote selection that illustrates instead of cherry-picks, and the confidence lines a small sample earns. Use when asked synthesize these user/customer/exit interviews, what did we actually learn from the calls, turn 12 transcripts into insights, or are these themes real."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# interview-synthesis

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

Produces the coded themes with counts, the divergences preserved, the illustrative quotes, and the claims sized to the sample.
