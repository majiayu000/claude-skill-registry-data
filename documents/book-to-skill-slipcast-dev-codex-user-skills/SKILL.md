---
name: book-to-skill
description: Converts books, documentation folders, and source collections (PDF, EPUB,
  DOCX, HTML, Markdown, RST, AsciiDoc, RTF, MOBI/AZW) into structured agent skills
  — extracting named frameworks, principles, techniques, and anti-patterns into a
  master SKILL.md plus on-demand chapter files, a glossary, a patterns file, and a
  decision cheatsheet. Use when the user wants to study a document with an agent,
  apply an author's frameworks while working, turn internal docs or standards into
  a reusable knowledge base, or package a compiled book skill as a claude-skills plugin.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# book-to-skill

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
- В исходном наборе не разрешён ресурс chapters/ch01-<slug>.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
- В исходном наборе не разрешён ресурс chapters/ch02-<slug>.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
- В исходном наборе не разрешён ресурс glossary.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
- В исходном наборе не разрешён ресурс patterns.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
- В исходном наборе не разрешён ресурс cheatsheet.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
