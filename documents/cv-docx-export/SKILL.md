---
name: cv-docx-export
description: "Turn a finished CV into a parsing-safe Word file ready to upload: one column, real heading styles, no tables, headers or images, the right paper size, and correct fonts for Chinese, Japanese or Korean text. Use when asked to give me my CV as a Word file, export my CV to docx, make an ATS-safe CV file, or produce my 简历 as a Word document."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cv-docx-export

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

Produces the .docx file, a text read-back proving it parses, and the upload file name.
