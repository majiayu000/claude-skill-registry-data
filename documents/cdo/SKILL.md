---
name: cdo
description: >
  CDO v2 — опциональный оркестратор. Используй только когда пользователь явно просит оркестрацию, делегирование или параллельную агентную работу, и только если текущая среда разрешает запуск субагентов.

  Triggers: "CDO", "оркестратор", "запусти агентов", "разбей на субагентов", "параллельно агентами", "делегируй".
---

# CDO v2 — Optional Agent Orchestrator

> **Safety override:** Не автозапускай CDO как дефолтный режим. Не запускай субагентов, если пользователь явно не попросил делегирование/параллельную агентную работу или если текущие системные/developer-инструкции это запрещают.

## Как это работает

```
Пользователь: "хочу добавить систему гильдий"
    ↓ (0 вопросов)
CDO: классификация → Feature, XL, systems: social+backend+iOS+DB+economy
    ↓
CDO: pipeline → architect ∥ conductor → nexus → server+fortress → screen → guardian+oracle → gatekeeper → herald
    ↓
CDO: запускает Agent 1, передаёт результат → Agent 2 → ... → Agent N
    ↓
Пользователь: получает готовый execution plan / готовый код / готовый ревью
```

---

## Phase 1: INSTANT CLASSIFICATION (без вопросов к пользователю)

Определи за 1 секунду:

| Что определить | Как |
|---------------|-----|
| **Домен(ы)** | По карте доменов ниже |
| **Тип задачи** | feature / enhancement / bugfix / audit / refactor / balance / deploy / research / docs |
| **Размер** | S (1 агент) / M (2-3) / L (4-6) / XL (7+) |
| **Режим** | sequential / parallel / hybrid |
| **Pipeline** | Конкретный список агентов в порядке запуска |

### Карта доменов (ВСЯ экосистема)

| Сигналы в запросе | Домен | Агенты |
|------------------|-------|--------|
| Hexbound, iOS, SwiftUI, баланс, комбат, арена, данжен, прогрессия, лор, экран, экономика игры | **Hexbound Studio** | `hexbound-studio:*` (30+ агентов) |
| Amazon, FBA, ниша, листинг, PPC, поставщик, бренд Амазон | **Amazon Team** | `amazon-product-research`, `amazon-ops` |
| Портфель, бюджет, рынки, крипто, налоги, кредиты, прогнозы | **Finance Office** | `finance-office:*` (15+ агентов) |
| Дизайн, UX, ревью экрана, accessibility, wireframe, прототип | **Design** | `full-design-review`, `design:*`, `design-department:*` |
| Данные, SQL, дашборд, график, статистика, анализ | **Data** | `data:*` |
| Код, архитектура, дебаг, деплой, тесты, CI/CD | **Engineering** | `engineering:*` |
| Контент, SEO, email, кампания, бренд (не Amazon) | **Marketing** | `marketing:*` |
| Спека, роадмап, спринт, метрики, стейкхолдеры | **Product** | `product-management:*` |
| Outreach, pipeline продаж, звонок, прогноз | **Sales** | `sales:*` |
| Word, Excel, PowerPoint, PDF | **Документы** | `docx` / `xlsx` / `pptx` / `pdf` |

### Приоритет при конфликтах
1. Hexbound-специфичное → всегда `hexbound-studio:*`
2. Amazon-специфичное → всегда `amazon-*`
3. Личные финансы → `finance-office:*` (не `finance:*` — это корпоративный учёт)

---

## Phase 2: PIPELINE CONSTRUCTION

### Режим SEQUENTIAL (цепочка)
Результат Agent A → передаётся как контекст → Agent B → ... → Agent N.

```
Agent A ──результат──→ Agent B ──результат A+B──→ Agent C ──→ финал
```
**Когда:** каждый следующий агент нужен результат предыдущего.

### Режим PARALLEL (одновременно)
Запуск нескольких Agent tool в ОДНОМ сообщении. Результаты собираются вместе.

```
         ┌→ Agent A → результат A ─┐
Задача ──┤→ Agent B → результат B ─├→ CDO синтезирует
         └→ Agent C → результат C ─┘
```
**Когда:** агенты работают независимо.

### Режим HYBRID (комбо)
```
Phase 1 (parallel): architect ∥ conductor
Phase 2 (sequential): nexus получает результаты обоих → bladework
Phase 3 (parallel): guardian ∥ oracle
Phase 4: gatekeeper → herald
```

---

## Phase 3: AGENT BUS — Прямая коммуникация между агентами

### Как агенты общаются

Агенты общаются через **файловую шину** `.claude/agent-bus/`. Каждый агент читает результаты других и пишет свои. CDO НЕ передаёт контекст вручную — агенты сами забирают нужное.

**Полный протокол:** `.claude/agent-bus/PROTOCOL.md`

### Lifecycle одного pipeline

```
1. CDO очищает bus:
   find .claude/agent-bus -maxdepth 1 -type f -name '*.md' ! -name 'PROTOCOL.md' ! -name 'AGENT_HEADER.md' -delete

2. CDO запускает Wave 1 — НЕСКОЛЬКО Agent tool вызовов в ОДНОМ сообщении:
   Agent tool (guardian) ─┐
   Agent tool (oracle)  ─┼─ параллельно
   Agent tool (scales)  ─┘

3. Каждый Agent:
   a) Читает .claude/agent-bus/ — что уже есть от других
   b) Делает свою работу
   c) Пишет результат в .claude/agent-bus/{name}.md
   d) В секции ## Alerts пишет @mentions для других агентов

4. CDO запускает Wave 2 — агенты ЧИТАЮТ bus и видят результаты Wave 1:
   Agent tool (screen) ──→ читает guardian.md, oracle.md → работает → пишет screen.md
   Agent tool (nexus)  ──→ читает все файлы → пишет nexus.md

5. CDO читает ВСЕ .md в bus → синтезирует финальный ответ
```

### Контекст при запуске агента (MANDATORY)

Каждый вызов Agent tool ОБЯЗАН содержать:

```
## CDO PIPELINE CONTEXT
Задача: {оригинальный запрос пользователя}
Wave: {1 из 3}
Агенты в этой волне: {guardian, oracle, scales}

## AGENT BUS PROTOCOL
После завершения работы — ОБЯЗАТЕЛЬНО запиши результат:
  Write tool → .claude/agent-bus/{твоё-имя}.md
Перед началом работы — прочитай bus:
  Bash: ls .claude/agent-bus/  → Read каждый .md файл (кроме PROTOCOL.md)
Если нашёл проблему для другого агента — добавь в ## Alerts:
  @{agent-name}: описание проблемы

Формат результата в bus-файле:
# {Name} — Result
timestamp: {now}
status: OK | WARNING | BLOCKED
## Findings
## Decisions
## Alerts
## Files Changed
```

### Динамическая маршрутизация (ESCALATION)

Если агент находит проблему ВНЕ своей компетенции — он пишет @mention в bus:

```
# Guardian — Result
## Alerts
- @oracle: endpoint /api/foo возвращает неправильный тип — проверь async
- @fortress: нужна миграция для нового поля lastLoginAt
```

CDO видит алерты при синтезе. Если адресат ещё не запускался — CDO добавляет его в следующую волну. Если уже отработал — CDO запускает его повторно с контекстом алерта.

Пользователь видит только финальный результат.

---

## Phase 4: PIPELINE TEMPLATES (готовые цепочки)

### HEXBOUND — Новая фича (Template A: Full Pipeline)
```
1. [PARALLEL] architect (vision) + conductor (scope)
   ↓ GO/NO-GO gate — если architect BLOCKED → стоп
2. nexus (cross-system impact) — получает context от обоих
3. [PARALLEL] профильные агенты по домену:
   - bladework (если бой) / vault (если экономика) / arena (если PvP) / depths (если PvE) / ascent (если прогрессия)
   - scales (если баланс) + heartbeat (если core loop)
4. [PARALLEL] UX/UI:
   - flow (UX) + canvas (visual) + blueprint (tokens)
5. [SEQUENTIAL по зависимостям] Engineering:
   - fortress (DB) → server (API) → console (admin) → screen (iOS) → engine (gameplay)
6. [PARALLEL] QA:
   - shield (test plan) + gauntlet (gameplay QA) + ledger (economy QA)
   ↓ QA gate — если shield BLOCKED → стоп
7. gatekeeper (pre-commit check)
8. herald (deploy)
9. [PARALLEL] Post-deploy:
   - lens (analytics) + scroll (docs) + context-auditor (CLAUDE.md update)
```

### HEXBOUND — Код-ревью (Template B)
```
1. [PARALLEL] guardian (iOS) + oracle (backend) — если оба затронуты
2. blueprint (design system) — если UI изменения
3. signal (security) — если auth/payment
4. gatekeeper (pre-commit)
```

### HEXBOUND — UX Ревью экрана (Template C)
```
1. mirror (полный UX аудит) — основной отчёт
2. [PARALLEL] flow (friction) + canvas (visual) + pulse (animation)
3. blueprint (tokens) — если нарушения найдены
4. psyche (motivation) — если экран влияет на retention
```

### HEXBOUND — Баланс (Template D)
```
1. [PARALLEL] scales (формулы) + vault (экономика)
2. gauntlet (playtesting) — на основе результатов обоих
3. ledger (abuse/exploit test)
4. strategist (retention impact)
5. architect (final approval)
```

### HEXBOUND — Деплой (Template E)
```
1. gatekeeper — если FAIL → стоп, показать что фиксить
2. blacksmith (build verify) — если FAIL → стоп
3. herald (deploy all products)
4. gate (release verification) — если прод
```

### HEXBOUND — Hotfix (Template F)
```
1. server/engine (diagnose + fix)
2. fortress (data integrity check)
3. shield (regression)
4. gate (rollback plan)
5. herald (emergency deploy)
```

### AMAZON — Product Research (Template G)
```
1. [PARALLEL] Scout (product) + Pulse (trends)
2. Shadow (competitors) — получает нишу от Scout
3. Vault (financial model) — получает данные от Shadow
4. [PARALLEL] Shield (risks) + Architect (brand strategy)
5. Commander (final verdict) — синтез всего
```

### FINANCE — Полный обзор (Template H)
```
1. [PARALLEL] market-intelligence + financial-news-analyst + macro-economist
2. portfolio-analyst — с учётом рыночного контекста
3. risk-manager — на основе портфеля + макро
4. chief-financial-strategist — финальный синтез
```

### УТРЕННИЙ БРИФ (Template I)
```
[ALL PARALLEL]:
  - finance-office:cdo-orchestrator (финансовый обзор)
  - Hexbound: git log + открытые задачи
  - Проверка памяти (текущие проекты, дедлайны)
CDO: синтезирует → краткий бриф с приоритетами дня
```

---

## Phase 5: SYNTHESIS + BUS SUMMARY — Сборка результатов

После получения ответов от всех агентов:

1. **Прочитай ВСЕ файлы в `.claude/agent-bus/`** (кроме PROTOCOL.md, AGENT_HEADER.md)
2. **Объединить findings** — дедупликация, группировка по теме
3. **Разрешить конфликты** — если агенты спорят, выбрать позицию (или эскалировать architect)
4. **Приоритизировать** — Critical → High → Medium → Low
5. **Проверить @mentions** — если есть нерешённые алерты, запустить дополнительную волну
6. **Записать самари в bus** — сжатый итог всего pipeline
7. **Очистить индивидуальные файлы** — оставить только самари

### Bus Summary (ОБЯЗАТЕЛЬНО после каждого pipeline)

После синтеза CDO ОБЯЗАН:

```bash
# 1. Записать самари
Write tool → .claude/agent-bus/_summary.md

# 2. Удалить индивидуальные файлы агентов (чтобы bus не рос)
rm -f .claude/agent-bus/guardian.md .claude/agent-bus/oracle.md ... (все кроме PROTOCOL.md, AGENT_HEADER.md, _summary.md)
```

**Формат `_summary.md`:**
```markdown
# Pipeline Summary
date: {YYYY-MM-DD HH:MM}
task: {краткое описание задачи}
agents: guardian, oracle, scales, screen (кто участвовал)
status: OK | WARNING | BLOCKED

## Key Findings
- finding 1 (source: guardian)
- finding 2 (source: oracle)

## Actions Taken
- файл X изменён (agent)
- миграция создана (fortress)

## Unresolved
- @oracle алерт от guardian — не обработан (если остались)

## Files Changed (all agents combined)
- path/to/file1.swift
- path/to/file2.ts
```

**Правило:** `_summary.md` всегда перезаписывается (не аппендится). Это снэпшот ПОСЛЕДНЕГО pipeline. Предыдущие самари не хранятся — они не нужны, результат в коде.

### Формат финального ответа пользователю

```
[Прямой ответ — 1-3 предложения]

[Детали от агентов — только то, что нужно пользователю, не внутренняя кухня]

[Action items — если есть, конкретные следующие шаги]

[Предупреждения — если были блокеры или escalations]
```

**НЕ показывать:** internal pipeline details, "Agent X said Y", промежуточные артефакты. Пользователь видит РЕЗУЛЬТАТ, не процесс.

---

## Phase 6: VERIFY — Post-Task Checklist (CDO ALWAYS RUNS)

### Backend
- [ ] TypeScript compiles (`npx next build`)
- [ ] Prisma schema synced (`backend/prisma/` = `admin/prisma/`)
- [ ] No PII in logs
- [ ] try/catch on all routes
- [ ] async/await correct
- [ ] No N+1 queries

### iOS
- [ ] New .swift files in pbxproj (4 sections)
- [ ] No force unwraps
- [ ] DarkFantasyTheme tokens (no hardcoded colors)
- [ ] ButtonStyles.swift styles
- [ ] LayoutConstants for radius/spacing
- [ ] Ornamental pattern on panels
- [ ] `.compositingGroup()` after ornamental stacks
- [ ] `.transaction { $0.animation = nil }` for optional VM

### Design System
- [ ] All tokens verified in source files
- [ ] CurrencyDisplay used (not SF Symbols)
- [ ] ItemCardView for items, UnifiedHeroWidget for character

### Deploy
- [ ] `git push origin main`
- [ ] `git subtree push` if admin changed
- [ ] No merge conflict markers

### Docs
- [ ] Relevant docs updated in `/docs/`
- [ ] CLAUDE.md updated if new rules
- [ ] Schema/API reference updated if changed

---

## БЛОКЕРЫ — Стоп-сигналы

Эти агенты могут **остановить pipeline**:

| Агент | Блокирует | Override |
|-------|----------|---------|
| architect | Любую фичу (vision mismatch) | Только Артём |
| gatekeeper | Деплой (pre-commit fail) | Fix → re-run |
| blacksmith | Деплой (build fail) | Fix → re-run |
| shield | Релиз (QA fail) | Только Артём |
| risk-manager | Финансовое решение | Только Артём |

Если блокер → СТОП → сообщить пользователю ЧТО не так и КАК починить.

---

## Правила CDO

### ДЕЛАЙ
- Используй Agent tool только когда пользователь явно попросил агентную делегацию и текущая среда это разрешает
- Если субагенты запрещены или не нужны, выполняй работу локально обычным пошаговым планом
- **Очищай bus перед каждым pipeline:** `find .claude/agent-bus -maxdepth 1 -type f -name '*.md' ! -name 'PROTOCOL.md' ! -name 'AGENT_HEADER.md' -delete`
- В prompt каждого Agent tool включай: задачу + bus protocol + путь к SKILL.md агента
- Используй Escalation через @mentions в bus
- Адаптируй templates — они база, не догма
- Для S-задач (1 агент) — вызывай напрямую без pipeline overhead
- **Читай bus после каждой волны** — проверяй @mentions и статусы

### НЕ ДЕЛАЙ
- Не делай CDO дефолтным режимом для любого запроса
- Не запускай субагентов без явной просьбы пользователя
- Не запускай больше 5 агентов в одной волне
- Не показывай пользователю pipeline internals — показывай результат
- Не дублируй работу — если guardian проверил tokens, blueprint не нужен для того же
- Не пропускай Phase 6 (verify) — даже для "маленьких" задач
- **Не передавай контекст вручную** — агенты читают bus сами

### CDO Maxim

> **"Пользователь описывает ЧТО. CDO решает КТО, КАК, и В КАКОМ ПОРЯДКЕ. Агенты делают РАБОТУ. Пользователь получает РЕЗУЛЬТАТ."**

---

## Agent Bus (Team Communication)

> CDO — оркестратор bus. Он очищает, запускает волны, читает результаты, пишет самари, чистит за собой.

### CDO Bus Lifecycle

```
1. find .claude/agent-bus -maxdepth 1 -type f -name '*.md' ! -name 'PROTOCOL.md' ! -name 'AGENT_HEADER.md' -delete
2. Launch Wave 1 (parallel Agent tools)
3. Wait for completion
4. Read all .claude/agent-bus/*.md — check @mentions, statuses
5. If unresolved @mentions → Launch Wave 2 with targeted agents
6. Repeat until all waves done
7. Write .claude/agent-bus/_summary.md (compressed summary)
8. rm -f .claude/agent-bus/{agent-name}.md (cleanup individual files)
9. Present result to user (no internals)
```

### При старте pipeline
```bash
# Очистка bus (сохраняем только протокол и хедер)
rm -f .claude/agent-bus/_summary.md
# Индивидуальные файлы агентов удалятся автоматически в конце
```

### При завершении pipeline
Записать `_summary.md` и удалить все `{agent-name}.md` — bus должен быть чистым между pipeline'ами.
