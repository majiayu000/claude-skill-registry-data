---
name: ha:architecture-process
description: "Author ADRs and run the breaking-change process for Home Assistant core public APIs — when the architecture repo is required, the 22-ADR reference table, the C3 custom-integration-search + deprecation + dev-blog workflow, and the PR3 integration breaking-change checklist. Use when a core diff touches the entity model, device classes, YAML config structure, or any symbol a custom integration can import."
audience: framework-development
effort: medium
user-invocable: false
paths:
  - "homeassistant/helpers/**"
  - "homeassistant/components/*/__init__.py"
  - "homeassistant/const.py"
  - "homeassistant/config_entries.py"
---

# Architecture Process — ADRs & Breaking Core Public APIs

The HOW-TO for two framework-development gates that **hard-stop review** until you clear
them:

1. **Architecture-repo approval** — before you change the entity model, add a device
   class, or change YAML config structure (PR4).
2. **Breaking a core public API** — the custom-integration search, deprecation window,
   `report_usage` log, and dev-blog post that a custom-integration-visible change requires
   (C3, extending PR3).

Both are process, not code. The `iron-law-judge` can detect that you *tripped* a gate
(diff touches a base-entity class ⇒ architecture discussion required); it cannot clear
the gate for you. This skill is the procedure.

**Roster tags** carry through from the law files: `[OHF]` = verified Open Home
Foundation employee; `[UNVERIFIED]` = active reviewer, employment unconfirmed.
`[UNVERIFIED]` enforcers are guidance ("some maintainers ask for…"), never a sole hard
block — a rule reaches IRON tier only with OHF co-enforcers.

Every directive below carries ≥1 citation (ADR / PR discussion / dev-blog URL). Do not
improvise around a missing citation.

---

## 1. When the Architecture Repo Is REQUIRED (PR4)

Three change classes **cannot be reviewed on their own** — open a discussion in
`home-assistant/architecture` first and **stop until it is approved**:

| Trigger | Example |
|---|---|
| Entity-model change | new base-entity attribute/property, changing a base class in `homeassistant/helpers/entity.py` or a platform base (e.g. `sensor/__init__.py`) |
| New device class | adding a member to a `*DeviceClass` enum |
| YAML config structure change | changing the schema shape integrations declare their config in (ADR-0007) |

**The gate, verbatim:**
- "there needs to be approval in a discussion in our architecture repository" —
  MartinHjelmare[OHF], https://github.com/home-assistant/core/pull/163136#discussion_r2811436602
- Doc-backed by the *changing-the-entity-model* developer docs and enforced as a hard
  gate by MartinHjelmare[OHF], frenck[OHF] (ADR hard gates), jbouwh[OHF] — PR4,
  `docs/iron-laws.md`.

**What "STOP" means:** review does not continue on the PR while the discussion is open.
Open exactly one architecture discussion; **do not** pre-write the resolution, ADR text,
migration, or code beyond the minimum needed to describe the proposal. The discussion
decides whether the pattern is accepted, and often *how* — you implement to that
outcome, not ahead of it.

**How to open it:**
1. File a discussion at `home-assistant/architecture` describing the new pattern, the
   problem it solves, and the alternatives you rejected. Genuinely-new patterns
   (not covered by an existing ADR) are the target — established patterns don't need one.
2. Link the discussion from the PR so review can resume once it resolves.
3. If the decision is broad and durable, it becomes an ADR (see §3) — that write-up is a
   follow-up to the *approved* discussion, not a substitute for it.

Cross-ref: the detection half (diff touches base-entity classes / adds a device class /
changes YAML config structure ⇒ require a linked architecture discussion) is the
mechanical PR4 check in `docs/iron-laws.md`.

---

## 2. ADR Awareness — the Gates That Hard-Stop PRs

ADRs are accepted architecture decisions. Several are **merge-blocking gates**: a diff
that violates one is rejected regardless of code quality. Know these before you write,
not at review time.

**Gate ADRs you will hit on integration/framework work:**

- **ADR-0010 (config entries)** — config entries are the canonical configuration
  mechanism; YAML platform configuration is deprecated. New integrations set up via
  config flow, not YAML.
  https://github.com/home-assistant/architecture/blob/master/adr/0010-integration-configuration.md
- **ADR-0011 (discovery requires unique ID)** — discovery-based integrations must set
  `unique_id` in the config flow and call `_abort_if_unique_id_configured()`. This is the
  doc backing for P7 (stable unique IDs).
  https://github.com/home-assistant/architecture/blob/master/adr/0011-discovery-requires-unique-id.md
- **ADR-0007 (integration config YAML structure)** — the YAML schema shape is itself an
  architecture decision; changing it is a PR4 trigger (§1).
  https://github.com/home-assistant/architecture/blob/master/adr/0007-integration-config-yaml-structure.md
- **ADR-0021 (YAML deprecation policy)** — legacy YAML platform config is removed over a
  multi-year window; config entries preferred. This is the timeline authority behind any
  YAML-removal PR.
  https://github.com/home-assistant/architecture/blob/master/adr/0021-YAML-integration-configuration-deprecation-policy.md
- **ADR-0022 (integration quality scale)** — the Bronze/Silver/Gold/Platinum framework
  and its rulebook; the 56-rule quality scale that gates new integrations (PR2) derives
  from here.
  https://github.com/home-assistant/architecture/blob/master/adr/0022-integration-quality-scale.md
- **ADR-0009 (translations 2.0)** — decentralized JSON translations in `strings.json`;
  doc backing for P9 / F1.
  https://github.com/home-assistant/architecture/blob/master/adr/0009-translations-2.0.md
- **ADR-0008 (code owners)** — a `codeowners` entry in `manifest.json` is required.
  https://github.com/home-assistant/architecture/blob/master/adr/0008-code-owners.md

**Watch the status column.** An ADR can be **Rejected** (the decision is "don't do
this") or **Superseded** (a newer ADR governs):

- **ADR-0004 (webscraping) — Rejected.** Do not add HTML-scraping integrations; prefer
  official APIs, document limitations where none exists.
  https://github.com/home-assistant/architecture/blob/master/adr/0004-webscraping.md
- **ADR-0002 → superseded by ADR-0020** (minimum supported Python version). Cite 0020,
  not 0002.
  https://github.com/home-assistant/architecture/blob/master/adr/0020-minimum-supported-python-version.md

### 22-ADR Reference Table

Source: `.claude/plans/ha-plugin-conversion/research/adrs.md` (mined 2026-07-12).
Full text: `https://github.com/home-assistant/architecture/tree/master/adr`.

| # | Title | Status |
|---|-------|--------|
| 0001 | Record architecture decisions | Accepted |
| 0002 | Minimum supported Python version | Superseded by 0020 |
| 0003 | Monitor condition and data selectors | Accepted |
| 0004 | Webscraping | **Rejected** |
| 0005 | Code formatting | Accepted |
| 0006 | Docker images | Accepted |
| 0007 | Integration config YAML structure | Accepted |
| 0008 | Code owners | Accepted |
| 0009 | Translations 2.0 | Accepted |
| 0010 | Integration configuration (config entries) | Accepted |
| 0011 | Discovery requires unique ID | Accepted |
| 0012 | Define supported installation method | Accepted |
| 0013 | Home Assistant container | Accepted |
| 0014 | Home Assistant Supervised | Accepted |
| 0015 | Home Assistant OS | Accepted |
| 0016 | Home Assistant Core | Accepted |
| 0017 | Hardware screening OS | Accepted |
| 0018 | Supported databases | Accepted |
| 0019 | GPIO | Accepted |
| 0020 | Minimum supported Python version (update) | Accepted |
| 0021 | YAML integration config deprecation | Accepted |
| 0022 | Integration quality scale | Accepted |

---

## 3. Authoring an ADR

An ADR records a decision that outlives one PR. You write one when an architecture-repo
discussion (§1) resolves in favor of a durable, repo-wide rule — ADR-0001 established the
process itself: decisions live as Markdown files in the `adr/` directory.
https://github.com/home-assistant/architecture/blob/master/adr/0001-record-architecture-decisions.md

**Structure** (follow the existing files in the `adr/` directory):

1. **Number & title** — next sequential number, short imperative title.
2. **Status** — `Proposed` → `Accepted`; later `Rejected` or `Superseded by NNNN`. When
   you supersede an ADR, edit the old one's status to point forward (as 0002 → 0020) and
   the new one back.
3. **Context** — the problem and the forces at play. Cite prior ADRs and the discussion.
4. **Decision** — the rule, stated so a reviewer can mechanically check a PR against it.
5. **Consequences** — what becomes easier, what becomes harder, and the migration cost
   for existing integrations (this is where a deprecation timeline belongs — §5).

**Rules for the write-up:**
- The ADR follows the *approved* discussion; it does not replace §1's approval step.
- If the decision breaks or deprecates anything custom integrations can see, the ADR's
  Consequences section must reference the breaking-change process in §4 (deprecation
  window, dev-blog).
- Translate/document nothing user-facing here — an ADR is a developer artifact; user
  docs are the separate merge-gate PR (PR5).

---

## 4. Breaking a Core Public API — Step by Step (C3)

Any change visible to a custom integration — a changed signature, a removal, a behavior
change, or a moved import path — is a breaking change and runs this full process. C3
extends PR3 from the framework side by adding the **pre-merge custom-integration search**
and the **`report_usage` single-log** mechanism.

Enforced by MartinHjelmare[OHF], emontnemery[OHF], bdraco[OHF], joostlek[OHF],
arturpragacz[UNVERIFIED] (~19 PRs) — C3, `docs/framework-dev-laws.md`.

### Step 1 — Search custom integrations for usage, BEFORE the PR

Establish who breaks. This is a **precondition**, not a post-merge report.
- "This is not backwards compatible, have we searched for custom components" —
  emontnemery[OHF], https://github.com/home-assistant/core/pull/152772#discussion_r2390927018
- "Changing the signature of async_extract_referenced_entity_ids is a breaking change." —
  bdraco[OHF], https://github.com/home-assistant/core/pull/148087#discussion_r2183907209

### Step 2 — Add a deprecation shim, logged once via `report_usage`

Keep the old symbol working; emit a deprecation notice through the `report_usage` helper
— not an ad-hoc `_LOGGER.warning`. `report_usage` logs once and points the author at the
fix, and it respects P2 (don't log-and-raise; the helper decides).
- "I think we can simply use the `report_usage` helper." — MartinHjelmare[OHF],
  https://github.com/home-assistant/core/pull/153167#discussion_r2686569571

### Step 3 — Calibrate the deprecation window: 6 months vs 12 months

| Who has to change | Window |
|---|---|
| Users edit their own **configuration** to self-fix | **6 months** |
| Integrations must change **code** | **12 months** (about a year) |

- "For changes which only require users to change their configuration: 6 months" —
  emontnemery[OHF], https://github.com/home-assistant/core/pull/155689#discussion_r2485514877
- "I think we generally deprecate technical things up to a year" — joostlek[OHF],
  https://github.com/home-assistant/core/pull/162425#discussion_r2774340545

Removal "cannot be included in a patch release" — it's a breaking change tied to a
release with a breaking-change section (PR3):
- "Removing a previously available entity is a breaking change and cannot be included in
  a patch release." — edenhaus[OHF],
  https://github.com/home-assistant/core/pull/154137#discussion_r2419783773

### Step 4 — Write a developer-blog post

Anything a custom integration can see needs a `developers.home-assistant.io/blog` post
announcing the deprecation, the replacement, and the removal date (C3 / PR3). The blog
history in §5 is your template and precedent set.

### Step 5 — Remove in a SEPARATE PR, after the window elapses

Deprecation and removal are **two PRs**, in that order — never one (PR1):
- "It either does a deprecation or a removal (and in that order)... Not both." —
  frenck[OHF], https://github.com/home-assistant/core/pull/173953#discussion_r3418436259

The removal PR also cleans up docs and brands repos (PR5):
- "We need a link before we can merge here." — MartinHjelmare[OHF],
  https://github.com/home-assistant/core/pull/161936#discussion_r2848311597

### The C3 flow, condensed

```
custom-integration search  →  deprecation shim + report_usage (single log)
   →  6mo (user-fixable) / 12mo (integration-fixable) window
   →  dev-blog post  →  [window elapses]  →  SEPARATE removal PR (+ docs/brands cleanup)
```

---

## 5. Precedent — the Deprecation Timeline

Source: `.claude/plans/ha-plugin-conversion/research/blog-standards-changes.md`
(mined 2026-07-12). Use these as the shape and cadence your own deprecation should
follow — announced version, removal version, and the blog post that carried it.

| Item | Deprecated in | Removal | Window | Blog |
|---|---|---|---|---|
| `@bind_hass`, `hass.components` | 2024.9 | 2025.3 | 6mo | https://developers.home-assistant.io/blog/2024/09/11/extending-deprecation-hass-components/ |
| `hass.helpers` | 2024.11 | 2025.5 | 6mo | https://developers.home-assistant.io/blog/2024/10/09/extend-deprecation-hass-helpers/ |
| Media Player `SUPPORT_*` constants → `MediaPlayerEntityFeature` | 2024.10 | 2025.10 | 12mo | https://developers.home-assistant.io/blog/2024/09/23/constants-media-player-deprecation/ |
| Camera API methods (`async_handle_web_rtc_offer`, …) | 2024.12 | 2025.6 | 6mo | https://developers.home-assistant.io/blog/2024/11/26/camera-deprecations/ |
| `async_run_job()` / `async_add_job()` → `async_create_task` | 2024.3 | TBD | — | https://developers.home-assistant.io/blog/2024/03/13/deprecate_add_run_job/ |
| `async_add_hass_job()` | 2024.4 | TBD | — | https://developers.home-assistant.io/blog/2024/04/07/deprecate_add_hass_job/ |
| `hass` arg in service helpers | 2025.9 | TBD | — | https://developers.home-assistant.io/blog/2025/09/22/deprecate-hass-argument-service-helpers/ |
| Legacy device-tracker platform API | 2026-04 | 2027.5 | 12mo | https://developers.home-assistant.io/blog/2026/04/20/legacy-device-tracker-deprecation/ |
| `show_advanced_options` (advanced-mode config flow) | 2026-05 | 2027.6 | 12mo | https://developers.home-assistant.io/blog/2026/05/26/advanced-mode-config-flow-deprecation/ |
| Condition / script APIs | 2026-05 | through 2027.1 | — | https://developers.home-assistant.io/blog/2026/05/13/condition-script-api-changes/ |

**Reading the precedent:** the 12-month windows (`SUPPORT_*` constants, device tracker,
advanced mode) are the integration-code-fixable changes from Step 3; the 6-month windows
(`hass.components`, `hass.helpers`, camera) are closer to config/usage swaps. When your
change resembles a row here, cite that row's window and blog as precedent in your PR.

The **Quality Scale overhaul (2024-11-20)** is the one immediate, non-windowed standards
reset in the set — a rulebook change under ADR-0022, not an API deprecation:
https://developers.home-assistant.io/blog/2024/11/20/integration-quality-scale/

---

## 6. Breaking-Change Checklist for Integrations (PR3)

For integration-authoring diffs (not core framework symbols), a user-visible breaking
change — removing an entity, changing a `unique_id`, dropping a service parameter —
requires all of:

- [ ] **Breaking-change section** in the PR description.
- [ ] **Migration**: a config-entry **minor-version bump** with `async_migrate_entry`
      handling the old shape.
- [ ] **Deprecation period** — a year if users can't self-fix (mirrors §4 Step 3 for the
      integration layer).
- [ ] **Dev-blog post** for any API change that custom integrations can see.
- [ ] **Removal not in a patch release** — breaking changes ship with a minor/major.
- [ ] **Linked documentation PR** (PR5) — a home-assistant.io PR link is a merge gate
      when user-facing behavior changes; removals clean up docs & brands too.

Enforced by edenhaus[OHF], frenck[OHF], joostlek[OHF], MartinHjelmare[OHF],
emontnemery[OHF] (5/7) — PR3, `docs/iron-laws.md`.
- "Removing a previously available entity is a breaking change and cannot be included in
  a patch release." — edenhaus[OHF],
  https://github.com/home-assistant/core/pull/154137#discussion_r2419783773

Mechanical detection (PR3): diffs removing entities/unique_ids/service params without a
version bump + `async_migrate_entry` are flagged for this checklist.

---

## Decision Pointer — Which Path Am I On?

| Your change | Path |
|---|---|
| New base-entity attribute, new device class, YAML config structure change | §1 architecture-repo approval **first** (PR4), then possibly an ADR (§3) |
| Changing/removing a symbol a custom integration imports | §4 the C3 breaking-API process |
| User-visible break inside one integration (entity/unique_id/service param) | §6 the PR3 integration checklist |
| Recording a durable, repo-wide decision | §3 author an ADR (after §1 approval) |

## References

| File | Content |
|---|---|
| `docs/framework-dev-laws.md` | C3 full text (custom-integration search + 6/12mo window + `report_usage` + dev-blog), tiers, rosters |
| `docs/iron-laws.md` | PR1 (deprecation OR removal, never both), PR3 (integration breaking-change process), PR4 (architecture-repo gate), PR5 (docs/brands merge gate), P7 (unique IDs / ADR-0011) |
| `.claude/plans/ha-plugin-conversion/research/adrs.md` | The 22-ADR index with statuses and per-ADR summaries |
| `.claude/plans/ha-plugin-conversion/research/blog-standards-changes.md` | The full deprecation timeline with removal dates and blog URLs |
| `ha:core-internals` skill | The framework-layer review criteria that route breaking changes here |
