---
name: ha:core-internals
description: "Develop homeassistant/ core itself — helpers/ API contracts, config_entries, websocket_api, bootstrap/setup/loader, auth, util. Framework-layer review criteria (C-laws + maintainer case law). Use when a core-checkout diff touches framework paths rather than components/<domain>/."
audience: framework-development
effort: medium
user-invocable: false
---

# Core Internals — Developing `homeassistant/` Itself

Review criteria and API guidance for changing the Home Assistant framework layer:
`homeassistant/helpers/`, `core.py`, `bootstrap.py`/`setup.py`/`loader.py`/`runner.py`,
`config_entries.py`, `components/websocket_api/`, `auth/`, `util/`, `script/` (incl.
hassfest), and shared test infrastructure (`tests/common.py`, conftest files).

Evidence base: `review-patterns-core-internals.md` (1,012 maintainer review rows /
283 PRs / 12 reviewers, window 2025-07..2026-07), `docs/framework-dev-laws.md` (C1–C8),
and the core developer-docs snapshot (API shapes in
`${CLAUDE_SKILL_DIR}/references/core-api-shapes.md`).

**Roster tags**: `[OHF]` = verified Open Home Foundation employee; `[UNVERIFIED]` =
active reviewer, employment unconfirmed. `[UNVERIFIED]` enforcers carry weight as
guidance ("some maintainers ask for…"), never as sole justification for a hard block.

**Rule encoding**: ESTABLISHED rules from the evidence file are stated as directives.
CANDIDATE rules (fewer PRs / fewer distinct reviewers) are stated as
"maintainers have asked for…" — follow them, but they are not blocking on their own.

## When This Applies

Both conditions must hold:

1. **Core checkout** — `homeassistant/__init__.py` exists AND `script/` directory
   exists (the same detection `/ha:init` uses for the framework-development profile).
2. **The diff touches framework paths**:

| Area | Paths |
|---|---|
| helpers | `homeassistant/helpers/**` |
| core objects | `homeassistant/core.py`, `homeassistant/exceptions.py` |
| boot chain | `homeassistant/bootstrap.py`, `setup.py`, `loader.py`, `runner.py`, `block_async_io.py` |
| config entries | `homeassistant/config_entries.py`, `data_entry_flow.py` |
| websocket_api | `homeassistant/components/websocket_api/**` (the framework carve-out inside components/) |
| auth | `homeassistant/auth/**` |
| util | `homeassistant/util/**` |
| dev tooling | `script/**` (hassfest, gen_requirements, Docker/build files) |
| test infra | `tests/common.py`, `tests/conftest.py`, `tests/components/conftest.py` |

This skill does **NOT** apply when the diff is confined to
`homeassistant/components/<domain>/` (integration work — use the integration-authoring
skills) or `custom_components/`. The A–E laws (`docs/iron-laws.md`,
`docs/strong-defaults.md`) still fully apply here; this skill adds the C tier on top
and elevates core-style criteria (see the review checklist below) from secondary
guidance to primary review criteria.

## The C-Law Tier (summary — full text in `docs/framework-dev-laws.md`)

Do not restate rosters or citations from the law file; cite laws by ID.

| Law | Tier | One-liner | Relationship to A–E laws |
|---|---|---|---|
| C1 | STRONG-DEFAULT | A public helper's name and signature are its contract | adjacent to PS17, scoped to public-API stability |
| C2 | PROCESS-LAW | One concern per PR | strengthens PR1; carve-out: a new library ships with its first use |
| C3 | PROCESS-LAW | Breaking a public API is gated on a custom-integration search + calibrated deprecation | extends PR3 |
| C4 | IRON-LAW ★ | Nothing blocks the event loop; hot paths stay cheap | reinforces P4 + adds hot-path frugality |
| C5 | STRONG-DEFAULT | Fail loud, never silent — but bad data must never crash boot | shares the "never silent" theme with P2; the boot-survival half is net-new |
| C6 | STRONG-DEFAULT | Directional layering (`util/` → helpers → components); no import cycles | net-new at this layer |
| C7 | STRONG-DEFAULT | Typed, extensible interfaces | shares the typing spine with P5/P6 |
| C8 | IRON-LAW | New/changed core logic ships with tests + coverage | restates P12/P13 at the framework layer |

---

## 1. helpers/ — Public-API Contract Discipline (C1, C7)

A helper module's exported names, signatures, and docstrings ARE the framework's public
API. Custom integrations import them directly; there is no stability boundary between
you and thousands of downstream consumers.

**The name is the contract — rename on drift, ambiguity, or misleading scope.**
Highest-volume rule in the corpus (30+ PRs; C1). Enforced by emontnemery[OHF],
MartinHjelmare[OHF], arturpragacz[UNVERIFIED], abmantis[OHF], bdraco[OHF].
- "descriptions is not very descriptive. can we name it better?" — emontnemery,
  https://github.com/home-assistant/core/pull/156778#discussion_r2548860826
- "These names are confusing I think." — MartinHjelmare,
  https://github.com/home-assistant/core/pull/151965#discussion_r2333161480

**Declare event-loop safety in the name and decorator.** Async-safe regular methods get
`@callback`; coroutines and loop-only functions get the `async_` prefix. (Cross-ref
PS19 for the "coroutine that never awaits" half.) Enforced by emontnemery[OHF],
justanotherariel[OHF], arturpragacz[UNVERIFIED].
- "This should be decorated with @callback" — emontnemery,
  https://github.com/home-assistant/core/pull/159659#discussion_r2672199781
- "it should be prefixed with `async_`." — justanotherariel,
  https://github.com/home-assistant/core/pull/162068#discussion_r2764306349

**Docstrings explain non-obvious intent; stale or wrong docstrings block merge**
(19 PRs). Enforced by emontnemery[OHF], MartinHjelmare[OHF], abmantis[OHF].
- "Please add a body to the docstring explaining the difference" — MartinHjelmare,
  https://github.com/home-assistant/core/pull/152772#discussion_r2412249455
- "Stale docstring" — emontnemery,
  https://github.com/home-assistant/core/pull/156778#discussion_r2548789043

**Public signatures are typed and extensible (C7)** — TypedDict with correct totality
(`total=False` when partial), kwargs or a dataclass so the signature can grow, a
sentinel when `None` is a valid value, enums over magic numbers/strings (16 PRs).
Enforced by arturpragacz[UNVERIFIED], emontnemery[OHF], MartinHjelmare[OHF].
- "Make parameters either kwargs or a dataclass to keep it extendable" — arturpragacz,
  https://github.com/home-assistant/core/pull/168815#discussion_r3126596471
- "None is a valid device class, let's add a sentinel" — emontnemery,
  https://github.com/home-assistant/core/pull/165392#discussion_r2926688572
- "Let's not use a magic number" — emontnemery,
  https://github.com/home-assistant/core/pull/157888#discussion_r2590440222

## 2. Public-API Stability & Deprecation (C3)

Before changing or removing any exported helper/symbol:

1. **Search custom integrations for usage — pre-merge, not post-report** (19 PRs).
   Enforced by bdraco[OHF], MartinHjelmare[OHF], emontnemery[OHF].
   - "Changing the signature of async_extract_referenced_entity_ids is a breaking change."
     — bdraco, https://github.com/home-assistant/core/pull/148087#discussion_r2183907209
   - "This is not backwards compatible, have we searched for custom components" —
     emontnemery, https://github.com/home-assistant/core/pull/152772#discussion_r2390927018
2. **Calibrate the deprecation period**: 6 months if users can self-fix their config;
   12 months if integrations must change code (9 PRs). Enforced by emontnemery[OHF],
   MartinHjelmare[OHF], joostlek[OHF], bdraco[OHF].
   - "For changes which only require users to change their configuration: 6 months" —
     emontnemery, https://github.com/home-assistant/core/pull/155689#discussion_r2485514877
   - "I think we generally deprecate technical things up to a year" — joostlek,
     https://github.com/home-assistant/core/pull/162425#discussion_r2774340545
3. **Log the deprecation once via the `report_usage` helper**, not ad-hoc warnings.
   - "I think we can simply use the `report_usage` helper." — MartinHjelmare,
     https://github.com/home-assistant/core/pull/153167#discussion_r2686569571
4. **Write a dev-blog post** for anything custom integrations can see (C3/PR3).

For the full process (architecture-repo approval, dev-blog workflow, breaking-change
sections), defer to **C3** and the `ha:architecture-process` skill — do not restate it.

## 3. Layering & Module Placement (C6)

Direction of knowledge: `util/` knows nothing about Home Assistant → `helpers/` may
know HA concepts → components sit on top. Domain/WS logic lives in its own module.

- **`util/` is HA-agnostic.** If it imports or reasons about HA concepts, it belongs in
  `helpers/`. Enforced by MartinHjelmare[OHF], abmantis[OHF], emontnemery[OHF].
  - "utils should not be aware of or be specific to Home Assistant" — MartinHjelmare,
    https://github.com/home-assistant/core/pull/149846#discussion_r2252438042
- **Shared trigger/condition logic goes in `helpers/automation.py`** — not in
  `trigger.py`/`condition.py`, and never in a component (≥3 PRs). Enforced by
  emontnemery[OHF], abmantis[OHF], arturpragacz[UNVERIFIED], balloob[OHF].
  - "Let's move it to helpers.automation" — emontnemery,
    https://github.com/home-assistant/core/pull/165208#discussion_r2976719488
  - "moving such integration specific logic to the condition.py platform" — balloob,
    https://github.com/home-assistant/core/pull/175421#discussion_r3541905683
- **Route constants through `const.py` to break import cycles**; import from the
  component root. Maintainers have asked for this in auth/ work (CANDIDATE, 11.1):
  - "can you move the constant to `homeassistant/const.py` to avoid circular import." —
    balloob[OHF], https://github.com/home-assistant/core/pull/157552#discussion_r2573334350
  - Type-widening (e.g. making a field `None`-able) must be verified at every usage:
    "verify that all can handle a `None` value" — edenhaus[OHF],
    https://github.com/home-assistant/core/pull/163907#discussion_r2986372402
- **Prefer composition and free functions over inheritance**; subclass behavior stays in
  the subclass; don't nest classes (≥4 PRs). Enforced by arturpragacz[UNVERIFIED],
  MartinHjelmare[OHF], abmantis[OHF].
  - "Using inheritance here brings completely unnecessary complexity, without any significant gain."
    — arturpragacz, https://github.com/home-assistant/core/pull/165392#discussion_r2930900983
  - "it prevents the subclass behavior from creeping to the base class." — abmantis,
    https://github.com/home-assistant/core/pull/146910#discussion_r2217301309
- Maintainers have asked that **constructors carry no side effects** — set up in
  `async_setup`, tear down symmetrically in `async_unload` (CANDIDATE, 3.4):
  - "We don't want these kind of side effects in a constructor" — emontnemery[OHF],
    https://github.com/home-assistant/core/pull/148086#discussion_r2204044690

## 4. Registries, Entity & Coordinator Framework

- **`DataUpdateCoordinator` is the exception funnel.** Framework code feeding it raises
  `ConfigEntryAuthFailed`/`ConfigEntryNotReady` and sets `last_exception` +
  `last_update_success`; retry belongs to the caller that initiated the request
  (≥3 PRs, DOC-BACKED). Enforced by MartinHjelmare[OHF], emontnemery[OHF], bdraco[OHF].
  - "Make sure to set `last_exception` and `last_update_success`." — MartinHjelmare,
    https://github.com/home-assistant/core/pull/153167#discussion_r2698447975
  - "Retry should be handled by the integration that initiated the token request." —
    MartinHjelmare, https://github.com/home-assistant/core/pull/153167#discussion_r2682691467
- Maintainers have asked that **registry plumbing be shared in the base class** rather
  than duplicated per registry, and that a plain dict check replace the `@singleton`
  decorator where it suffices (CANDIDATE, 4.2):
  - "It's a bit stupid this has to be duplicated in every registry." — emontnemery[OHF],
    https://github.com/home-assistant/core/pull/164340#discussion_r2865290917
  - "I don't think we should use a singleton decorator here" — MartinHjelmare[OHF],
    https://github.com/home-assistant/core/pull/167653#discussion_r3233853336

## 5. Event-Loop Safety & Failure Visibility (C4, C5)

- **No blocking I/O in the event loop — push syscalls and file writes into the
  executor** (7 PRs; C4 reinforcing P4; DOC-BACKED by `block_async_io.py`). Enforced by
  balloob[OHF], MartinHjelmare[OHF], emontnemery[OHF].
  - "I/O in event loop" — balloob,
    https://github.com/home-assistant/core/pull/158679#discussion_r2619754764
  - "Side note: This is also a syscall." — MartinHjelmare,
    https://github.com/home-assistant/core/pull/158679#discussion_r2620371936
- **Never fail silently — raise or log with intent** (16 PRs; C5). Enforced by
  MartinHjelmare[OHF], emontnemery[OHF], edenhaus[OHF], bdraco[OHF], balloob[OHF].
  - "why do we silently return?" — emontnemery,
    https://github.com/home-assistant/core/pull/155016#discussion_r3057585813
  - "It looks like it might be silently swallowed" — bdraco,
    https://github.com/home-assistant/core/pull/147882#discussion_r2182566248
- **…but bad data must never crash boot.** The inverse constraint is equally
  load-bearing: boot-time loaders degrade gracefully on corrupt entries/state.
  - "HA should start and not fail." — edenhaus,
    https://github.com/home-assistant/core/pull/153369#discussion_r2429599861

## 6. Hot-Path Discipline (C4 — the bdraco lens)

The state-write path runs at ~100k calls/minute on busy installs. Any diff touching
`core.py` state writes, `helpers/entity.py`, registries, or the recorder path gets the
performance review.

- **The state-write path stays cheap** — no new registry/device lookups or non-cached
  calls before the state de-dup check (≥3 PRs). Enforced by bdraco[OHF],
  emontnemery[OHF].
  - "Its definitely a lot more expensive code in a hot path." — bdraco,
    https://github.com/home-assistant/core/pull/161250#discussion_r2728714430
  - "We regularly seen 100000 calls a minute to write state" — bdraco,
    https://github.com/home-assistant/core/pull/161250#discussion_r2728820305
- Maintainers have asked that **the rare/cold path not be optimized at the expense of
  the common case** (CANDIDATE, 6.2):
  - "We shouldn't optimize for a rare case as it adds more overhead" — bdraco[OHF],
    https://github.com/home-assistant/core/pull/148344#discussion_r2330550005

Cross-ref: the blocking-I/O half of C4 is mechanically checkable via P4's machinery;
hot-path frugality is a reviewer call — profile or diff-inspect the write path.

## 7. config_entries Lifecycle

- **Validate as early as possible, and explicitly.** A *new* entry with bad data
  raises; but loading *existing* entries at boot must survive bad data (≥3 PRs — this
  is C5 applied to config_entries). Enforced by edenhaus[OHF], MartinHjelmare[OHF],
  emontnemery[OHF].
  - "As this is a new config entry, I would expect that we raise" — edenhaus,
    https://github.com/home-assistant/core/pull/153369#discussion_r2494922110
  - "we validate as early as possible." — MartinHjelmare,
    https://github.com/home-assistant/core/pull/155016#discussion_r2486962762
- Maintainers have asked that **flow-type transitions be constrained** — repairs must
  not jump straight into options/subentry flows; model supported flows as an enum;
  treat config-entry replacement as legacy (CANDIDATE, 7.2):
  - "Add a flow type enum in the repairs integration instead." — MartinHjelmare[OHF],
    https://github.com/home-assistant/core/pull/165091#discussion_r2901581079
  - "Config entry replacement is legacy." — MartinHjelmare[OHF],
    https://github.com/home-assistant/core/pull/155016#discussion_r3084962526

API shapes (entry states, lifecycle hooks, subentries, flow manager classes):
see `${CLAUDE_SKILL_DIR}/references/core-api-shapes.md`.

## 8. websocket_api

Registration mechanics (`@websocket_command` + `@async_response` + `@require_admin`,
wired via `async_register_command`) are in the references file.

- **Cache expensive description/lookup results with an identity check** (or a
  `hass.data` setdefault at handler-setup time) — never rebuild per call (≥3 PRs).
  Enforced by emontnemery[OHF], MartinHjelmare[OHF].
  - "This should be cached" — emontnemery,
    https://github.com/home-assistant/core/pull/157334#discussion_r2564690926
  - "why don't we just create the cache when setting up the websocket handlers" —
    emontnemery, https://github.com/home-assistant/core/pull/157888#discussion_r2590457022
- Maintainers have asked that **target-selector filter semantics be preserved
  exactly** — each entity filter stands alone (no bunching into one AND), and WS
  commands support every filter the target selector documents (CANDIDATE, 8.2):
  - "We can't bunch together the entity filters like this" — emontnemery[OHF],
    https://github.com/home-assistant/core/pull/156778#discussion_r2548826109
- Maintainers have asked for **sets for membership tests, and modern set operators**
  (`|` over `set.union`) (CANDIDATE, 8.3):
  - "it's much faster to use sets for that than lists." — MartinHjelmare[OHF],
    https://github.com/home-assistant/core/pull/156778#discussion_r2545459693

## 9. bootstrap / setup / loader — Boot Resilience (C5)

Staged-startup facts (STAGE 0 substages: labs → logging → frontend → recorder →
zeroconf; timeouts per stage) are in the references file.

- **Startup-stage placement is deliberate.** `CORE_INTEGRATIONS` stays minimal; logging
  loads first; new features get their own late substage; wait for consumers to exist
  before adding a domain to an early stage (≥3 PRs, DOC-BACKED). Enforced by
  arturpragacz[UNVERIFIED], MartinHjelmare[OHF].
  - "we really want to keep the list here as lean as possible." — arturpragacz,
    https://github.com/home-assistant/core/pull/156840#discussion_r2540835107
  - "I would prefer we load logging first, as it can be crucial" — arturpragacz,
    https://github.com/home-assistant/core/pull/156840#discussion_r2540967804
- **File operations use try/except, not check-then-act** — the state can change between
  the check and the write (≥3 PRs). Enforced by MartinHjelmare[OHF].
  - "Checking before writing isn't sufficient since the state can change" —
    MartinHjelmare, https://github.com/home-assistant/core/pull/146675#discussion_r2241948575
  - "I'd try to read and catch `FileNotFoundError` instead." — MartinHjelmare,
    https://github.com/home-assistant/core/pull/171466#discussion_r3274085955
- Maintainers have asked that **boot-time gathers collect and return exceptions**
  rather than let one failure propagate, and that failure handling be encapsulated in
  the loader that owns it (CANDIDATE, 9.2):
  - "Should we not change this gather to collect and return exceptions?" —
    emontnemery[OHF], https://github.com/home-assistant/core/pull/164340#discussion_r2865251665

## 10. util/

- **`unit_conversion`/`unit_system` rigor**: keys sorted, constants exact against the
  base unit, superscript symbols, physical assumptions documented (≥3 PRs). Enforced by
  MartinHjelmare[OHF], abmantis[OHF], emontnemery[OHF].
  - "This conversion requires an assumption that the ppm is a mass ratio" —
    MartinHjelmare, https://github.com/home-assistant/core/pull/153187#discussion_r2387702293
- Maintainers have asked that util code **not consume internal/private third-party
  APIs**, and prefer a proven library over a hand-rolled reimplementation
  (CANDIDATE, 10.2):
  - "Internal pip APIs are not part of pip's public API" — frenck[OHF],
    https://github.com/home-assistant/core/pull/155684#discussion_r2558721516
  - "Do we really want to implement this ourselves, or would be better to use some library"
    — emontnemery[OHF], https://github.com/home-assistant/core/pull/145926#discussion_r2341202269

## 11. script/ & hassfest

- **Quality-scale level and record changes go in their own PRs**, separate from the
  feature; new integrations require Bronze (12 PRs, DOC-BACKED). Enforced by
  MartinHjelmare[OHF].
  - "Please update the quality scale in a separate PR." — MartinHjelmare,
    https://github.com/home-assistant/core/pull/148104#discussion_r2184380462
- Maintainers have asked that **hassfest validation not require a change per
  integration feature** — integrations own their own strings/schemas (CANDIDATE, 12.2):
  - "having to update hassfest for every preview feature seems like an antipattern" —
    MartinHjelmare[OHF], https://github.com/home-assistant/core/pull/156840#discussion_r2548976558
- Maintainers have asked that **build tooling never set wrong architecture-dependent
  defaults** — fail loud if a required build arg is missing, default only what is safe
  locally (CANDIDATE, 12.3):
  - "We should not set default wrong values. Leaving them empty is better" —
    edenhaus[OHF], https://github.com/home-assistant/core/pull/164756#discussion_r2889278949
- Maintainers have asked that **dangerous developer scripts be rejected** — no
  `git reset --hard`/stashing in shared tooling (CANDIDATE, 12.4):
  - "resetting hard is not something we should merge here" — frenck[OHF],
    https://github.com/home-assistant/core/pull/160782#discussion_r2683510972

## 12. Tests & Coverage (C8)

- **New/changed core logic ships with tests that assert real behavior** — uncovered
  lines and untested edge cases block merge; even deprecated code keeps basic coverage
  (14 PRs; C8 restating P12/P13 at the framework layer — framework paths sit outside
  the integration quality scale, so nothing else gates them). Enforced by bdraco[OHF],
  emontnemery[OHF], abmantis[OHF], frenck[OHF], MartinHjelmare[OHF].
  - "missing test coverage here" — bdraco,
    https://github.com/home-assistant/core/pull/162941#discussion_r2805187680
  - "can we add some really basic tests for the deprecated classes" — emontnemery,
    https://github.com/home-assistant/core/pull/148087#discussion_r2189093528
- **Mechanical gate — run coverage on the touched module** before claiming done:

  ```bash
  # helpers module
  python3 -m pytest tests/helpers/test_<module>.py \
      --cov=homeassistant.helpers.<module> --cov-report=term-missing
  # framework top-level module (config_entries, loader, setup, bootstrap, core)
  python3 -m pytest tests/test_<module>.py \
      --cov=homeassistant.<module> --cov-report=term-missing
  ```

  Every line your diff adds or changes must be exercised; behavior-assertion quality
  (does the test assert observable behavior, not implementation?) is a review call.
- Maintainers have asked for **no hidden magic in shared fixtures** — follow the
  pytest-asyncio migration guide; keep fixtures readable, no clever lambdas
  (CANDIDATE, 13.1):
  - "I don't think we should do magic here." — abmantis[OHF],
    https://github.com/home-assistant/core/pull/147814#discussion_r2318692456
  - "These lambdas are hard to read." — MartinHjelmare[OHF],
    https://github.com/home-assistant/core/pull/165603#discussion_r3066514871

## 13. Cross-Cutting PR Hygiene (C2)

- **One concern per PR** — split refactors, renames, and unrelated changes; revert
  accidental edits; merge `dev` rather than reformatting (34 PRs; C2 strengthening
  PR1). Enforced by MartinHjelmare[OHF], emontnemery[OHF], abmantis[OHF],
  arturpragacz[UNVERIFIED].
  - "Please break out the refactor to a separate PR." — MartinHjelmare,
    https://github.com/home-assistant/core/pull/169773#discussion_r3196561153
  - "Clean up accidental changes like that." — arturpragacz,
    https://github.com/home-assistant/core/pull/157661#discussion_r2646155740
- The deliberate carve-out: maintainers have asked that **a new dependency ship in the
  same PR that uses it**, not a separate one (CANDIDATE, 14.3):
  - "We don't need a separate PR for adding a new library" — emontnemery[OHF],
    https://github.com/home-assistant/core/pull/145926#discussion_r2344011236
- Maintainers have asked that **lists/keys stay alphabetically sorted**
  (CANDIDATE, 14.4; cross-ref PS20):
  - "Please sort 🔡." — MartinHjelmare[OHF],
    https://github.com/home-assistant/core/pull/162270#discussion_r2773031977

---

## Core-Style Review Checklist (elevated from integration guidance)

**Why this section exists**: for integration authors, these criteria are shared
Python/HA hygiene — they live in the strong defaults (notably PS20) and are inherited,
not headline review criteria. For core contributors they are **primary**: the
framework-review corpus (emontnemery's PART-B rules on scope, comments, tests, typing,
and idioms) shows maintainers enforcing them as first-class, merge-relevant findings on
framework diffs. Run this checklist on every framework-path diff before review:

- [ ] **Scope**: the PR does one thing; unrelated formatting/renames/bumps reverted or
  split out. ("please don't mix adding new features with unrelated changes like this" —
  emontnemery[OHF], https://github.com/home-assistant/core/pull/145005#discussion_r3380516012)
- [ ] **Comments earn their place**: they explain the non-obvious *why*; useless,
  stale, and LLM-filler comments deleted. ("Let's drop these Claude-comments, they are
  just annoying" — emontnemery[OHF],
  https://github.com/home-assistant/core/pull/165208#discussion_r2976812242)
- [ ] **No branching in tests**: expected values/calls arrive via parametrization;
  duplicated test bodies become shared helpers. (Cross-ref P12. "Don't branch in tests,
  instead pass in the expected value … via the parametrization" — emontnemery[OHF],
  https://github.com/home-assistant/core/pull/169989#discussion_r3435202711)
- [ ] **Mocking discipline**: fixtures patch-and-revert; freezegun for time; no import
  side-effects in libraries. ("mock libraries by using a fixture which patches when
  test starts and is reverted" — emontnemery[OHF],
  https://github.com/home-assistant/core/pull/153287#discussion_r2697317934)
- [ ] **Test through the real interface**: drive the public entry point (coordinator
  refresh, config entry, WS command), not internals. (Cross-ref P13.
  https://github.com/home-assistant/core/pull/155786#discussion_r3201002470)
- [ ] **Typing is precise**: correct/narrow annotations, `TYPE_CHECKING` guards for
  type-only imports, kwarg-only for ambiguous args. (Feeds C7. "If we bother to add
  type annotations, let's at least make them correct" — emontnemery[OHF],
  https://github.com/home-assistant/core/pull/160352#discussion_r2671116382)
- [ ] **No dead code**: single-use functions/variables inlined, unused strings and
  not-yet-called methods removed. (Cross-ref P10. "Don't add dead code." —
  emontnemery[OHF], https://github.com/home-assistant/core/pull/151509#discussion_r2428784085)
- [ ] **Constants and schemas live where used**: single-module constants stay local;
  per-call invariants hoist to module level. ("It's wasteful to recreate the schemas
  every time this runs" — emontnemery[OHF],
  https://github.com/home-assistant/core/pull/172796#discussion_r3593702127)
- [ ] **Idiomatic constructs**: `try`/`else` over post-`try` code, `itertools.chain`
  over list concatenation, the assignment operator, dict comprehensions.
  ("we do generally favor using the assignment operator" — emontnemery[OHF],
  https://github.com/home-assistant/core/pull/156778#discussion_r2555635243)
- [ ] **Project formatting** (cross-ref PS20 — do not restate): 88-char lines, PEP 257
  single-sentence docstring headers, snake_case, sorted lists, modules read
  top-to-bottom, standard interfaces keep standard parameter names.

## Breaking a Public API — Decision Pointer

Any change visible to a custom integration (signature, removal, behavior, import path)
routes through **C3** (`docs/framework-dev-laws.md`) and the `ha:architecture-process`
skill. Short form: custom-integration search → deprecation shim with `report_usage` →
6/12-month window → dev-blog post. Do not improvise the process here.

## Recorded Tension (current behavior prevails)

MartinHjelmare[OHF] has argued that `helpers/target.py` using the entity **"hidden"
flag to influence target selection was a design mistake** and should be inverted —
"hidden ... should not matter for how the entity is used in automations"
(https://github.com/home-assistant/core/pull/168860#discussion_r3128531028). This is a
reviewer self-critique of existing framework behavior, not a documented rule change.
**Until the framework changes, preserve the current `target.py` semantics** — do not
"fix" this in passing.

## Maintainer Review Map (who you will meet on a framework PR)

| Reviewer | Expect scrutiny on |
|---|---|
| MartinHjelmare [OHF] | process (one concern per PR), backwards compat, try/except over check-then-act, tests for every branch |
| emontnemery [OHF] | API design: naming, typed/total TypedDicts, sentinels, docstrings, caching, deprecation windows |
| arturpragacz [UNVERIFIED] | composition over inheritance, kwargs/dataclasses, bootstrap-substage placement |
| abmantis [OHF] | readability, circular imports, misplaced constants, monolith methods |
| bdraco [OHF] | hot paths, state-write cost, recorder, cache scoping, breaking-change flags |
| edenhaus [OHF] | boot resilience, validation placement, Docker/build-arg discipline |
| balloob [OHF] | event-loop blocking, layering vetoes, circular-import routing |
| frenck [OHF] | tooling safety, no internal third-party APIs, dangerous dev scripts |

## References

| File | Content |
|---|---|
| `${CLAUDE_SKILL_DIR}/references/core-api-shapes.md` | Docs/code-observed API shapes: core.py objects, helpers/ map, config_entries classes, bootstrap stages, WS registration, auth model, recorder boundary |
| `docs/framework-dev-laws.md` | C1–C8 full text with tiers, rosters, and relationship notes |
| `docs/iron-laws.md`, `docs/strong-defaults.md` | The A–E base laws this skill layers on (P4, P10, P12/P13, PR1, PR3, PS17, PS19, PS20) |
