---
name: security-guidance
description: PreToolUse security-anti-pattern hook for Claude Code. Catches 12 common
  security risks (command injection, XSS, SQL injection, unsafe deserialization, GitHub
  Actions workflow injection, eval/new Function code injection) BEFORE the Edit/Write/MultiEdit
  operation completes. Session-state caching prevents duplicate warnings on the same
  file+rule combo. Stdlib only — no dependencies. Use when you want a safety net during
  Claude Code sessions that touch security-sensitive code (auth, payments, user input
  handling, IaC). Disable with ENABLE_SECURITY_REMINDER=0 if you need to perform a
  verified-safe operation that would otherwise trip a pattern. Triggers — "add security
  hook", "block unsafe code", "detect command injection before write", "prevent SQL
  injection patterns", "security warning hook".
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# security-guidance

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
