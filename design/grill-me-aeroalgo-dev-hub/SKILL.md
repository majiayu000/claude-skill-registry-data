---
name: grill-me
description: Hub CLARIFY Phase 0 for BACK|FRONT|INTEG PLAN/CLARIFY — framing grill + frontier interview via grilling primitive. Read at every clarify/plan Phase 0 start.
---

# Grill-me (hub — CLARIFY / PLAN Phase 0)

**Trigger:** `BACK|FRONT|INTEG CLARIFY` и `* PLAN` Phase 0 — **до** taxonomy Q и до написания plan.

**Не** тонкий upstream wrapper. Upstream `grill-me` = «вызови grilling»; здесь = **полный hub-контракт** + вызов primitive.

**Announce:** «Grill pass (Phase 0) — framing, затем frontier-опрос (grilling).»

---

## Skills chain (HARD)

1. **Read** `.agents/skills/grilling/SKILL.md` целиком — primitive (design tree · frontier · rounds).
2. **Brownfield / repo есть** → дополнительно Read `.agents/skills/grill-with-docs/SKILL.md` + `.agents/skills/domain-modeling/SKILL.md`. Docs пиши только если пользователь явно ок **или** термин/ADR уже зафиксирован в Q→A; path по умолчанию: `memory-bank/{role}/clarify/<slug>-glossary.md` (не обязательно root `CONTEXT.md`).
3. **Идея слишком большая на одну сессию** → предложи `.agents/skills/wayfinder/SKILL.md` (не автозапуск без согласия).
4. **Ответы у другого человека** → `.agents/skills/to-questionnaire/SKILL.md`.
5. **После shared understanding / Completion Report** (опционально) → `.agents/skills/to-prd/SKILL.md` (= alias `to-spec`) для синтеза без новых Q.
6. **Неясно какой skill** → `.agents/skills/ask-matt/SKILL.md`.

---

## Цель

Снять «угадывание по умолчанию» и **точно понять, что строим**, до Phase 1 PLAN:
- reframing + load-bearing premises;
- frontier-раунды по дереву решений (не dump всей очереди, не «один вопрос навсегда»);
- факты из codebase сам — решения только у пользователя.

---

## Шаг A — Grill pass (артефакт, mandatory)

Секция `## Grill pass` в `clarify-*.md` (шаблон `@.cursor/templates/clarify.md`). Пустая = **FAIL**.

| Поле | Содержание |
|------|------------|
| **Reframe** | 1–2 предложения: что строят *на самом деле* |
| **Premises** | 3–5 falsifiable · `accepted` / `challenged` / `rejected` / `deferred` |
| **Weakest link** | Одно допущение, ломающее scope |
| **Anti-scope** | Явный out-of-scope итерации |
| **Verdict** | `auto_resolved` · `needs_user_Q` |
| **Design tree (sketch)** | 3–8 узлов решений (коротко) до первого frontier-раунда |

### auto_resolved

Только если вход уже даёт personas, success criteria, out-of-scope и Evidence на каждый premise. Иначе `needs_user_Q`.

---

## Шаг B — Frontier interview (grilling, hub caps)

Канон механики: **grilling** (rounds + frontier). Hub-ограничения:

| Параметр | Значение |
|----------|----------|
| **Total Q** | **≤20** на CLARIFY-сессию (все раунды суммарно) |
| **Rounds** | **≤4** |
| **Per round** | только **независимые** Q (frontier); зависимые → следующий раунд |
| **Format** | numbered `❓ Qn` + MC/short + `➡️ Recommended` (как grilling) |
| **Chat UX** | один **раунд** за ход (весь frontier раунда); ждать ответы по номерам |
| **Facts** | grep/read/subagent — не спрашивать пользователя |
| **Stop** | frontier пуст · user `done`/`good` · квота 20 · нет material gaps |

### Приоритет узлов (impact)

1. Persona / value recipient (не «пользователи»)
2. Status quo / pain / demand reality
3. Narrowest shippable wedge
4. Anti-scope
5. Silent defaults (auth, tenant, stack, deploy, PII)
6. Failure / weakest link
7. Role: BACK data/NFR/integrations · FRONT first screen/empty/error · INTEG mock vs live / contract owner
8. Taxonomy Partial/Missing с material impact (scope→terminology)

### Grill bank (если нужна формулировка)

| ID | Когда |
|----|--------|
| G1 | persona размыта |
| G2 | status quo неясен |
| G3 | scope раздувается |
| G4 | anti-scope пуст |
| G5 | стек/auth «по умолчанию» |
| G6 | нет failure thinking |
| G7 FRONT | первый экран / empty / error |
| G8 INTEG | mock vs live / owner контракта |

После каждого раунда: дописать `## Q→A log` + `## Frontier rounds` в clarify-артефакт.

---

## Роль-акценты

- **BACK:** data, NFR, integrations, fail-closed — не выбирать стек вместо вопроса.
- **FRONT:** journeys, states, a11y-critical — не рисовать UI в CLARIFY.
- **INTEG:** method/path, authz, envelope, id mapping — не писать код.

---

## Completion / handoff

Строка в Completion Report:

`- **Grill:** done · verdict=… · rounds=N · grill_Q=M · mode=frontier`

При `* PLAN` Phase 0: после Completion Report → Phase 1 (не FINISH CLARIFY).

Опционально предложить `to-prd` / `to-spec` для синтеза WHAT до записи plan.md.

---

## FORBIDDEN

- Пропустить Grill pass или grilling Read «потому что ясно»
- >20 Q или >4 раунда без новой `continue * CLARIFY` сессии
- Параллельный dump **зависимых** вопросов в одном раунде
- Архитектурные решения вместо вопросов
- Писать полный plan до Completion Report Phase 0
- Заменять taxonomy/clarify shared-core этим skill целиком (taxonomy scan всё ещё обязателен)
- Auto-wayfinder / auto-CONTEXT.md в root без согласия
