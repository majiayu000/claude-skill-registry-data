---
name: code-review-checklist
description: Code review methodology with severity levels. P0/P1/P2 classification, security checks, and deviation tracking — each with reasoning.
user-invocable: false
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


# Code Review Checklist

Методология code review с приоритизацией по влиянию. Фокус на том, что реально влияет на пользователей и систему.

## Severity Levels

### P0 — Critical (блокирует деплой)
Проблемы, которые напрямую вредят пользователям или данным:
- **SQL injection, XSS, secrets в коде** — потому что это эксплуатируемые уязвимости
- **Потеря/повреждение данных** — потому что это необратимо
- **Сломанная бизнес-логика** — потому что пользователь получает неправильный результат
- **Бесконечные циклы, утечки памяти** — потому что это роняет production
- **must_haves truth = FALSE** — потому что основная цель задачи не достигнута

### P1 — Warning (стоит исправить)
Проблемы, которые ухудшают поддерживаемость и устойчивость:
- **Отсутствие error handling** — потому что unhandled errors приводят к непонятным ошибкам у пользователей
- **Дублирование кода** — потому что баг в одном месте придётся искать во всех копиях
- **Нарушение паттернов проекта** — потому что непоследовательный код замедляет всю команду
- **Файл превышает лимит** — потому что большие файлы сложнее ревьюить и поддерживать
- **must_haves truth = PARTIAL** — потому что часть цели не реализована

### P2 — Info (для справки)
Наблюдения, которые можно учесть в будущем:
- Стилистические несоответствия
- Возможные улучшения

## Процесс ревью

1. **Что изменилось**: `git status --short`, changed-file list, `git log --oneline -10` — общая картина
2. **Безопасность**: SQL injection, XSS, exposed secrets, unsafe inputs — потому что это самый критичный вектор
3. **Цель задачи**: код делает то, что задумано? Сравни с описанием задачи
4. **Edge cases**: обработаны ли граничные случаи? Особенно null/undefined, пустые массивы, сетевые ошибки
5. **Deviation tracking**: кодер применил auto-fix правильно? Исправления в scope текущей задачи?
6. **Размер файлов**: проверь по `file-size-limits` skill
7. **Verdict**: `approved: true/false`

## Claude Companion для второго ревью

Если изменение широкое, рискованное или затрагивает security/data/billing/release readiness, запусти Claude Companion как независимое advisory-review, если он доступен. Не используй его для мелких one-file fixes и чисто стилистических правок.

Типовые Codex plugin prompts:

```text
$claude:code-review Review the completed implementation. Plan: <plan-path or none>. Changed files: <enumerate files>. Verification: <commands and results>. Check bugs, regressions, missing tests, unsafe assumptions, and scope drift.

$claude:security-review Review the completed implementation. Plan: <plan-path or none>. Changed files: <enumerate files>. Verification: <commands and results>. Check security risk, unsafe inputs, secrets exposure, and auth/permission regressions.

$claude:data-consistency-review Review the completed implementation. Plan: <plan-path or none>. Changed files: <enumerate files>. Verification: <commands and results>. Check data consistency, identity mapping, migration, and query/filter regressions.
```

Review pack должен содержать plan path, changed-file list, worker/stage scope, verification commands/results, known risks и точные вопросы для Claude. Не передавай secrets, `.env`, customer data, production dumps или unrelated files.

После ответа Claude:

1. Прочитай `outbox_path`.
2. Раздели findings на `accept`, `partially_accept`, `reject`, `needs_user_decision`.
3. Не принимай рекомендации автоматически. Проверяй их по коду, задаче и AGENTS.md.
4. Исправь принятые P0/P1 findings и заново запусти релевантные проверки.
5. В финальном ответе упомяни отклонённые существенные findings только если они влияют на риск.

## Принципы оценки

- Фокусируйся на реальном влиянии: безопасность → достижение цели → корректность → стиль, потому что этот порядок отражает приоритет для пользователей
- Если код работает и build зелёный — ищи реальные проблемы, а не стилистические придирки, потому что nitpicking замедляет pipeline без пользы
- P0 findings → automatic reject. P1 findings → reject если их больше 2. P2 — информационно
- must_haves FALSE = automatic reject, потому что цель задачи — первичный критерий успеха
