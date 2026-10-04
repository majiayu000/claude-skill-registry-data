---
name: dev-cycle
version: 1.1.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-06-13
description: "8-фазный цикл разработки: запросы функций, текущее состояние, функциональное планирование, фронтенд, планирование бэкенда, код бэкенда, тесты, юзкейсы. Итеративный фреймворк для систематической разработки ПО."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [development, dev-cycle, phases, workflow, systematic, iterative]
language: ru
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/dev-zyklus.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="dev-cycle banner">

> **Русский** — Официальная русская версия `dev-cycle`.


# Цикл разработки (Dev Cycle) (Русский)

> **Цель:** Структурированный процесс от запроса функции до валидированной системы.
> Любая разработка проходит через эти 8 фаз.

---

## Обзор и назначение

```
  +--------------------------------------------------------------+
  |                    DEVELOPMENT CYCLE                         |
  +--------------------------------------------------------------+
  |                                                              |
  |  Phase 1   Feature Requests (functional requirements)        |
  |     |                                                        |
  |     v                                                        |
  |  Phase 2   Check Current State (What already exists?)        |
  |     |                                                        |
  |     v                                                        |
  |  Phase 3   Functional Planning                               |
  |            (Workflows, Agents, Experts, Skills, Services)    |
  |     |                                                        |
  |     v                                                        |
  |  Phase 4   Implement Functional Frontend                     |
  |            (Skill files, workflow markdown, agent profiles)   |
  |     |                                                        |
  |     v                                                        |
  |  Phase 5   Plan and Align Backend                            |
  |            (CLI handlers, DB schema, API endpoints)          |
  |     |                                                        |
  |     v                                                        |
  |  Phase 6   Implement Backend Tasks                           |
  |            (Python code, tools, DB migrations)               |
  |     |                                                        |
  |     v                                                        |
  |  Phase 7   Technical Tests and Bugfixes                      |
  |            (B/O/E tests, bugfix protocol)                    |
  |     |                                                        |
  |     v                                                        |
  |  Phase 8   Functional and Feature Test: USE CASES            |
  |            (End-to-end validation from user perspective)      |
  |                                                              |
  +--------------------------------------------------------------+

  Core principles throughout:
  - Functional description first (before code)
  - CLI First (everything controllable via terminal)
  - Clear separation of user data and system data
```

---

## Фаза 1: Запросы функций (Функциональные требования)

**Что:** Сбор и формулирование функциональных требований.

**Входные данные:**
- Пожелания, идеи и проблемы пользователей
- Предложения партнеров (LLM-ассистентов)
- Инсайты из юзкейсов (петля обратной связи!)

**Выходные данные:**
- Задачи в системе задач (например, в виде issue, тикета или списка TODO)
- Требования описывают ЧТО требуется, а не КАК

**Правила:**
- Всегда формулировать требования функционально («Пользователь может делать X»)
- Не технически («Реализовать REST эндпоинт для X»)
- Использовать юзкейсы как источник требований (Фаза 8 -> Фаза 1)

---

## Фаза 2: Проверка текущего состояния

**Что:** Инвентаризация существующего функционала.

**Чек-лист:**
```
  [ ] Search existing tools/scripts
  [ ] Check documentation/help on the topic
  [ ] Check existing skills/agents/services
  [ ] Check DB schema (if relevant)
  [ ] Check use cases - has something similar been tested?
```

**Выходные данные:**
- Документация того, что есть, чего не хватает, что требует расширения
- Предотвращение дублирования

---

## Фаза 3: Функциональное планирование

**Что:** Планирование на функциональном уровне — НЕ писать код сразу.

**Уровни планирования:**

| Уровень | Вопрос | Артефакт |
|-------|----------|----------|
| Workflow | КОГДА/КАК происходит координация? | workflows/*.md |
| Agent | КТО исполняет? | agents/*.txt |
| Expert | КТО обладает предметными знаниями? | experts/*/ |
| Skill | ЧТО делается? | skills/*.md |
| Service | КАК это делается технически? | services/*/ |

**Правила:**
- Сначала мыслить функционально, затем технически
- Workflows описывают процессы, а не детали реализации
- Каждому агенту нужен четкий профиль
- Сервисы должны работать без пользовательских данных

---

## Фаза 4: Реализация функционального фронтенда

**Что:** Создание файлов skill, workflow markdown, профилей агентов.

«Фронтенд» здесь — это слой функционального описания:
- Файлы workflow (.md)
- Профили агентов (.txt)
- Экспертные знания
- Описания сервисов
- Файлы справки

**Выходные данные:**
- Все функциональные описания существуют
- LLM-партнер может прочитать и понять workflow
- Функциональный слой полностью задокументирован

---

## Фаза 5: Планирование и согласование бэкенда

**Что:** Согласование технической архитектуры с функциональным фронтендом.

**Области планирования:**

| Область | Вопрос | Расположение |
|------|----------|----------|
| CLI Handlers | Какие команды? | handlers/*.py |
| DB Schema | Какие таблицы/колонки? | schema/*.sql |
| API Endpoints | Какие GUI эндпоинты? | server.py |
| Tools | Какие Python-скрипты? | tools/*.py |

**Выходные данные:**
- Технический план, согласованный с функциональным фронтендом
- Проект схемы базы данных (DB schema)
- Структура CLI-команд

---

## Фаза 6: Реализация задач бэкенда

**Что:** Написание кода Python, миграций БД, обработчиков CLI.

**Чек-лист (для каждой задачи):**
```
  [ ] Works without user data (empty DB)?
  [ ] CLI command available?
  [ ] Input can come from files/folders?
  [ ] Output goes to structured DB?
  [ ] Scan/import is repeatable (idempotent)?
  [ ] No hardcoded path?
  [ ] Tool registered and documented?
  [ ] Help file created?
```

---

## Фаза 7: Технические тесты и исправление ошибок (Bugfixes)

**Что:** Обеспечение технической корректности.

**Типы тестов (B/O/E):**

| Тип | Перспектива | Описание |
|------|-------------|-------------|
| B-Tests | Внешняя/Автоматизированная | Автоматизированные тесты, CI/CD |
| O-Tests | Функциональная (Вход->Выход) | Ручная функциональная проверка |
| E-Tests | Субъективная/Опыт | UX-оценка, эргономика |

**При багах:**
- Применять протокол исправления багов (bugfix protocol)
- Соблюдать правило 20 минут (сменить подход через 20 минут)
- Документировать извлеченные уроки (lessons learned)

---

## Фаза 8: Функциональный тест и тест фичей — ЮЗКЕЙСЫ (USE CASES)

**Что:** Сквозная (End-to-end) валидация с точки зрения пользователя.

**Юзкейсы служат ДВУМ целям:**
1. **Индикаторы фичей** — Что требуется? Что должно быть возможно?
2. **Тестовые сценарии** — Работает ли это на самом деле от А до Я?

**Формат юзкейса:**
```
  USECASE_NNN: Short Title

  PRECONDITION: What must be in place?
  INPUT:        What does the user enter / what data?
  EXPECTED:     What should the result be?
  TESTS:        Which components are tested?
```

**Петля обратной связи (Feedback Loop):**
- Непрошедшие юзкейсы -> новые задачи на Фазе 1
- Успешные юзкейсы -> валидированные фичи
- Новые идеи юзкейсов -> фиксация в качестве задач

---

## Резюме: Цикл (The Cycle)

```
  Phase 8 (Use Cases)
       |
       | New requirements / bugs
       v
  Phase 1 (Feature Requests)  -->  Phase 2 (Current State)
       ^                                    |
       |                                    v
  Phase 7 (Tests/Bugs)         Phase 3 (Functional Planning)
       ^                                    |
       |                                    v
  Phase 6 (Backend Code)       Phase 4 (Functional Frontend)
       ^                                    |
       |                                    v
       +──────────────────── Phase 5 (Backend Planning)
```

Цикл закольцован: юзкейсы валидируют фичи и одновременно создают новые требования.

---

## Специфичные для фаз скиллы

| Фаза | Специализированный скилл | Триггер |
|-------|-------------------|---------|
| Фазы 1-3 | Project bootstrapper (при наличии) | Создание нового проекта (с нуля / greenfield) |
| Фаза 2 | [project-onboarding](../../project-onboarding/SKILL.en.md) | Принятие существующего проекта |
| Фазы 2-3 | [docs-analysis](../../docs-analysis/SKILL.en.md) | Сверка документов требований с кодом |
| Фазы 5-6 | [pipeline-optimizer](../../pipeline-optimizer/SKILL.en.md) | Реконструкция существующей структуры |
| Фаза 7 | [bugfix-protocol](../../bugfix-protocol/SKILL.en.md) | Систематический 6-фазный дебаг |
| Фазы 7-8 | [bugsweep](../../bugsweep/SKILL.en.md) | Сходящаяся зачистка багов (Bug Sweep) перед релизом |

Если в вашей коллекции скиллов есть индекс скиллов, поищите в нем дополнительные скиллы, специфичные для фаз.

---

## История изменений

### 1.1.0 (2026-06-13)
- Новая таблица «Специфичные для фаз скиллы» со ссылками на project-onboarding, docs-analysis, pipeline-optimizer, bugfix-protocol и bugsweep

### 1.0.0 (2026-03-12)
- Перенесено из BACH (dev-zyklus v1.0.0)

---

*Создано: 2026-01-28 | Перенесено: 2026-03-12*
