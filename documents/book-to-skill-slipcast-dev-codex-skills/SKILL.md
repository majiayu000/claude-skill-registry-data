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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
- В исходном наборе не разрешён ресурс chapters/ch01-<slug>.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
- В исходном наборе не разрешён ресурс chapters/ch02-<slug>.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
- В исходном наборе не разрешён ресурс glossary.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
- В исходном наборе не разрешён ресурс patterns.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
- В исходном наборе не разрешён ресурс cheatsheet.md. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
