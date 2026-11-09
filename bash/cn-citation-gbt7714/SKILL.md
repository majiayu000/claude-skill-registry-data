---
name: cn-citation-gbt7714
description: "Use when asked 参考文献格式怎么写, 按 GB/T 7714 排参考文献, 帮我改参考文献格式, 顺序编码制还是著者-出版年制, 文献类型标识 J M D 是什么, or format references to the Chinese national standard."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-citation-gbt7714

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

Produces references formatted to GB/T 7714 in the numeric (顺序编码制) or author-year (著者-出版年制) system, with the right document type codes, a check of each entry, and a deterministic formatter script for long lists.
