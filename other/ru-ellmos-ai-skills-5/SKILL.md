---
name: model-strategy
version: 2.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-06-13
description: Многомодельная оркестрация и стратегия переключения моделей. Выбор моделей на основе оценки (score), делегирование между агентами (Gemini, Codex, Ollama), связывание с advisor, триггеры эскалации, матрица разрешений и оптимизация затрат.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [model-switching, orchestration, multi-model, cost-optimization, routing, cross-agent, advisor]
language: ru
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/ing-strategie.md', 'origin_version': '2.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="model-strategy banner">

> **Русский** — Официальная русская версия `model-strategy`.


# Стратегия переключения моделей (Русский)

> Многомодельная оркестрация: выбор моделей на основе оценки, делегирование между агентами, связывание с advisor, триггеры эскалации и оптимизация затрат

---

## 1. Каталог моделей

### Claude (поддерживает субагентов через инструмент Agent)

```
Level 4 (Reviewer):   Opus 4.8  — advisor, math review     [user only: /model, /advisor]
Level 3 (Strategist): Opus 4.6  — architecture, concepts   [subagent: model:"opus"]
Level 3 (Creative):   Fable 5   — creative texts, stories  [subagent: model:"fable"]
Level 2 (Workhorse):  Sonnet 4.6— implementation, debug    [subagent: model:"sonnet"]
Level 1 (Fast):       Haiku 4.5 — boilerplate, formatting  [subagent: model:"haiku"]
```

### Внешние агенты (скрипты-компаньоны / SSH)

```
Level 2-3: Gemini 3.5 pro  — research, scientific databases [agy-companion CLI]
Level 2:   Gemini 3.5 flash— fast research                  [agy-companion CLI]
Level 2-3: Codex 5.5 (GPT) — code review, code generation   [codex-companion CLI]
Level 2:   Codex 4.5 (GPT) — simpler code tasks             [codex-companion CLI]
```

### Локальные модели (без расхода токенов, 24/7)

```
Level 1-2: Ollama (Qwen 3.5:35b-a3b) — Haiku-to-Sonnet level [<ollama-host>:11434]
           Invocation: SSH + curl http://<ollama-host>:11434/v1/chat/completions
           Or: delegation via an agent-system control API (if available)
```

### Матрица доступности

| Модель | Запускается из LLM | Путь вызова | Ограничения |
|-------|---------------|-----------------|-------------|
| Sonnet 4.6 | Да | `Agent(model:"sonnet")` | — |
| Opus 4.6 | Да | `Agent(model:"opus")` | — |
| Haiku 4.5 | Да | `Agent(model:"haiku")` | — |
| Fable 5 | Да | `Agent(model:"fable")` | — |
| Opus 4.8 | Только advisor | `advisor()` в сессии | пользователь должен установить `/advisor` |
| Gemini 3.5 | Да (Bash) | `companion-for-agy "prompt"` | Только Windows, обходной путь для stdout |
| Codex 5.5/4.5 | Да (Bash) | `node codex-companion.mjs task "prompt"` | требуется авторизация |
| Ollama | Да (SSH/curl) | SSH + curl к API хоста Ollama | VPN/Tailscale должен быть активен |
| Opus 4.8 как основная модель | Нет | пользователь: `/model opus 4.8` | только действие пользователя |
| Fable 5 как основная модель | Нет | пользователь: `/model fable` | только действие пользователя |

---

## 2. Расчет оценки (score)

```
Dimensions (0-10):
  CLARITY     : How unambiguous is the task?
  COMPLEXITY  : How many components?
  CREATIVITY  : New solutions needed?
  CONTEXT     : How much prior knowledge?
  CRITICALITY : How important is perfection?

SCORE = (10 - CLARITY) + COMPLEXITY + CREATIVITY + CONTEXT + CRITICALITY
```

### Пороги оценок

| Оценка | Модель | Примеры |
|-------|-------|----------|
| 0-8 | Ollama (локальный хост) | генерация промптов, summary, простые тексты |
| 9-12 | Haiku | `__init__.py`, форматирование, шаблонный код (boilerplate) |
| 13-22 | Sonnet | реализация, исправление ошибок, стандартный код |
| 13-22 | Gemini 3.5 | исследования, поиск литературы, научные базы данных |
| 13-22 | Codex 5.5 | генерация кода (Luau, Node.js), вычислительные скрипты |
| 23-28 | Sonnet + проверкой advisor | сложный код с контролем качества |
| 23-35 | Fable 5 | творческие тексты, маркетинг, сторителлинг |
| 29-40 | Opus 4.6 | архитектура, стратегия, написание статей |
| 35-50 | Opus 4.6 + advisor | доказательства, архитектурные решения, статистика |
| 40-50 | Opus 4.8 (рекомендация пользователю) | математические доказательства, максимальная строгость |

---

## 3. Делегирование между агентами

### Какой внешний агент для чего использовать?

| Задача | Лучший агент | Причина |
|------|-----------|--------|
| Поиск научной литературы | Gemini 3.5 pro | встроенные навыки OpenAlex/arXiv/PubMed |
| Ревью кода (второе мнение) | Codex 5.5 | независимая перспектива |
| Генерация простых текстов | Ollama (локальный хост) | без расхода токенов, 24/7 |
| Творческие тексты, маркетинг | Fable 5 | сильнейший генератор творческого контента |
| Математические доказательства | Opus 4.8 (advisor) | наивысшая аналитическая глубина |

### Исключения (задокументированные слабости)

- **Gemini:** НЕ использовать для математических ревью/доказательств (задокументирована ошибка в направлении доказательства от 07.06.2026)
- **Codex 4.5:** только если недоступен 5.5; в остальных случаях всегда 5.5

### Пути вызова

> Замените плейсхолдеры `<host>`, `<ollama-host>`, `<tailscale-ip>`, `<user>` и `~/.ssh/<key>` параметрами вашей инфраструктуры.

**Gemini (via companion-for-agy):**
```
companion-for-agy --researcher --json --timeout 120000 "research prompt"
```

**Codex (via codex-companion):**
```
node "~/.claude/plugins/cache/openai-codex/codex/1.0.4/scripts/codex-companion.mjs" task --effort high "code prompt"
```

**Ollama on a remote host (via SSH):**
```
ssh -i ~/.ssh/<key> <user>@<tailscale-ip> "curl -s http://localhost:11434/v1/chat/completions -d '{\"model\":\"qwen3.5:35b-a3b\",\"messages\":[{\"role\":\"user\",\"content\":\"Prompt\"}]}'"
```

**Delegation to an agent system with tools (example):**
```
curl -s -X POST http://<host>:8081/api/chat -H "Content-Type: application/json" -d '{"prompt": "...", "chat_id": "claude-delegate"}'
```

---

## 4. Связывание с advisor

### Механика

`advisor()` — это **инструмент уровня сессии**: модель advisor задается пользователем через `/advisor`, а не программно. Это дает следующие шаблоны связывания:

| Шаблон | Как работает | Когда использовать |
|---------|--------------|-------------|
| **Advisor сессии** | пользователь задает `/advisor opus 4.8`, агент вызывает `advisor()` | стандартно для доказательств/архитектуры |
| **Оркестратор как ревьюер** | основная модель Opus проверяет результат субагента Sonnet | оркестратор сильнее исполнителя |
| **Контр-агент** | агент A работает, агент B проверяет в режиме оппонента | независимая проверка, 2 точки зрения |
| **Рекомендация пользователю** | агент рекомендует: "выполните эту задачу с opus 4.8 + advisor" | когда текущая сессия недостаточно сильна |

### Когда рекомендовать advisor?

- Математические доказательства (оценка ≥ 35)
- Архитектурные решения с долгосрочными последствиями
- Статистическая методология / дизайн исследований
- Сложные баги после 2+ безуспешных циклов отладки

### Когда НЕ использовать advisor?

- Рутинный код, контент, форматирование (оценка < 23)
- Реализация простых функций
- Четко определенные некритичные задачи

---

## 5. Триггеры эскалации

### Ollama -> Haiku
- Требуется доступ к файлам
- Требуется анализ кода

### Haiku -> Sonnet
- Затронуто более 2 файлов
- Требуется выбор между альтернативами
- Возникла непредвиденная ошибка
- Запрошена операция удаления

### Sonnet -> Opus
- Требуется архитектурное решение
- Необходимо интегрировать 3+ системы
- Требования противоречивы/неясны
- Требуется стратегическое планирование

### Sonnet -> Gemini (горизонтальная)
- Требуются научные исследования
- Проверка библиографии

### Sonnet -> Codex (горизонтальная)
- Ревью кода как второе мнение
- Перегрузка advisor (резервный ревьюер)

### Opus -> Opus + advisor
- Требуется проверка доказательства
- Критическое архитектурное решение
- Статистическая методология

### Деэскалация
- Концепция определена -> Sonnet берет на себя реализацию
- Задача тривиальна/рутинна -> Haiku берет на себя выполнение
- Только текст, без доступа к инструментам -> Ollama берет на себя выполнение

---

## 6. Матрица разрешений

| Операция | Ollama | Haiku | Sonnet | Opus | Gemini | Codex |
|-----------|--------|-------|--------|------|--------|-------|
| Чтение файлов | - | Да | Да | Да | Да* | Да* |
| Запись файлов | - | Да | Да | Да | Да* | Да* |
| Удаление файлов | - | - | Да** | Да | - | - |
| Системные команды | - | - | Да** | Да | Да* | Да* |
| Архитектурные решения | - | - | - | Да | - | - |
| Веб-исследования | - | - | Да | Да | Да | - |
| Вызов advisor() | - | - | Да | Да | - | - |

*через скрипт-компаньон в собственном режиме песочницы
**с подтверждением пользователя

---

## 7. Эффективность затрат

### Экономия токенов за счет маршрутизации

| Тип задачи | Без маршрутизации | С маршрутизацией | Экономия |
|-----------|-----------------|--------------|---------|
| Тривиальная | Токены Opus | Ollama (бесплатно) | 100% |
| Шаблонный код | Токены Opus | Токены Haiku | ~80% |
| Стандартный код | Токены Opus | Токены Sonnet | ~50% |
| Исследования | Токены Claude | Токены Gemini | ~70% (другой бюджет) |
| Ревью кода | Токены advisor() | Токены Codex | ~60% (другой бюджет) |

---

## 8. Золотое правило

> "Opus думает, Sonnet строит, Haiku исполняет, Ollama экономит. Gemini исследует, Codex проверяет, Fable повествует."

---

## История изменений

### 2.0.0 (12.06.2026)
- Делегирование между агентами: Gemini, Codex, Ollama (локальный хост) как цели маршрутизации
- Связывание с advisor: 4 шаблона (advisor сессии, оркестратор как ревьюер, контр-агент, рекомендация пользователю)
- Матрица доступности: задокументированы запускаемые из LLM vs. доступные только пользователю
- Добавлена Ollama (Qwen 3.5:35b-a3b, уровень от Haiku до Sonnet) как Level 1-2
- Горизонтальная эскалация: Sonnet -> Gemini (исследования), Sonnet -> Codex (ревью)
- Задокументированы исключения (Gemini не подходит для математики)
- Пороги оценок (score) расширены для всех моделей

### 1.0.0 (15.03.2015)
- Перенесено из BACH v3.8.0 (ing-strategie v2.0.0)

---

*Перенесено из BACH v3.8.0 | Расширено: делегирование между агентами + advisor v2.0.0*
