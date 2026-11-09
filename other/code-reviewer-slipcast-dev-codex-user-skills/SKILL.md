---
name: code-reviewer
description: 'Use for any code review: a pull request, a diff, a commit, or a pasted
  function, handler or file in TypeScript, JavaScript, Python, Go, Swift, Kotlin,
  C#/.NET, Java, C, C++, Rust, Ruby, PHP or Dart/Flutter. Applies per-language rule
  packs (security such as SQL injection and missing auth, async and resource handling,
  error handling, performance) and scripts that score a PR''s risk and complexity,
  then gives a merge verdict with blocking and non-blocking findings. Use whenever
  the user asks to review, check or look over code, says ''code review'', ''review
  this PR'', ''review this diff'' or ''is this safe to merge'', or asks what is wrong
  with a snippet, even a single function.'
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# code-reviewer

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

