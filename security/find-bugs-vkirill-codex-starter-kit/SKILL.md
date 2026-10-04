---
name: find-bugs
description: Методология поиска багов и уязвимостей. Security checklist, STRIDE, attack surface mapping, верификация.
tags: [security, audit, bugs, vulnerabilities]
stacks: [security]
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


# Find Bugs — Методология поиска уязвимостей

## Главное правило

**Не исправляй — только находи и докладывай.** Каждая находка должна быть обоснована реальным кодом.

## Фаза 1: Attack Surface Mapping

Для каждого модуля определи:
- Все пользовательские входы (request params, headers, body, URL)
- Все database queries
- Все auth/authz проверки
- Все операции с состоянием/сессиями
- Все внешние вызовы (API, сервисы)
- Все криптографические операции

## Фаза 2: Security Checklist

Проверь КАЖДЫЙ пункт для КАЖДОГО модуля:

- [ ] **Injection**: SQL, command, template, header injection
- [ ] **XSS**: Все выходные данные в шаблонах корректно экранированы?
- [ ] **Authentication**: Auth проверки на всех защищённых операциях?
- [ ] **Authorization/IDOR**: Контроль доступа проверен, а не только аутентификация?
- [ ] **CSRF**: State-changing операции защищены?
- [ ] **Race conditions**: TOCTOU в паттернах read-then-write?
- [ ] **Session**: Fixation, expiration, secure flags?
- [ ] **Cryptography**: Secure random, правильные алгоритмы, нет секретов в логах?
- [ ] **Information disclosure**: Ошибки, логи, timing attacks?
- [ ] **DoS**: Unbounded операции, отсутствие rate limits, resource exhaustion?
- [ ] **Business logic**: Edge cases, нарушения state machine, numeric overflow?

## Фаза 3: STRIDE анализ

Для каждого компонента системы проверь:

| Угроза | Вопрос |
|--------|--------|
| **S**poofing | Можно ли подделать идентичность? Есть ли auth на всех endpoints? |
| **T**ampering | Можно ли изменить данные в transit/at rest? Есть ли integrity checks? |
| **R**epudiation | Есть ли audit log? Можно ли отрицать действие? |
| **I**nfo Disclosure | Утечки данных через логи, ошибки, API responses? |
| **D**enial of Service | Unbounded operations, missing timeouts, resource exhaustion? |
| **E**levation of Privilege | Можно ли получить повышенные права? Есть ли role checks? |

## Фаза 4: Верификация

Для каждой потенциальной проблемы:
- Проверь: не обработана ли она уже в другом месте кода?
- Поищи существующие тесты покрывающие сценарий
- Прочитай окружающий контекст для подтверждения
- Отметь что НЕ удалось проверить полностью и почему

## Приоритизация

**security vulnerabilities > bugs > code quality**

Пропускай: стилевые/форматные замечания

Для каждой находки:
- **Файл:Строка** — краткое описание
- **Severity**: Critical / High / Medium / Low
- **Problem**: Что не так
- **Evidence**: Почему это реальная проблема (не уже исправлено, нет теста)

Если ничего значительного не найдено — скажи об этом. Не выдумывай.
