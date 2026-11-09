---
name: ransomware-first-response
description: "Handle the first hour of a suspected ransomware or malware infection calmly and correctly — contain it, preserve options, and avoid the moves that make it worse. Use when asked what to do about ransomware, my files are encrypted with a ransom note, I think I have malware, or my computer's been hacked."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ransomware-first-response

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

Produces an immediate containment checklist, a preserve-evidence-and-options step, a recovery path (backups, known decryptors, professional help), guidance on the ransom-payment decision, and reporting steps — for personal/small-setup use, not a substitute for professional incident response.
