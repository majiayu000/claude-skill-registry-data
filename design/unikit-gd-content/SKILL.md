---
name: unikit-gd-content
description: >-
  Author and own ONE content type's typed schema (the CONTENT-TYPE.md) at
  .unikit/gamedesign/content-types/CT-<slug>.md — the content / catalog layer of the GDD
  (cards, items, weapons, enemies, levels, quests, loot). Use whenever the user wants to ADD
  a new kind of content or UPDATE its schema, e.g. "add a new content type", "design the
  loot content", "define the card schema", "add an enemies content type", "add a rarity
  field to items", "switch this catalog to curated". Create the skeleton, fill its typed
  field schema (CT.fields), scale, relationships, and validation, AND revise the schema under
  the delta discipline (a schema change bumps the version + changelog). Selects the scale
  (bulk | curated) and self-registers content_types/content. This owns the content SCHEMA,
  not the catalog of values — adding individual entries/units is data handled in the editor,
  not a schema edit. To add or detail a system use /unikit-gd-system; to add a flow use
  /unikit-gd-flow; to apply a multi-zone edit use /unikit-gd-apply.
argument-hint: "<content type name | CT-slug> [\"<what to change>\"]  (scale inferred from doc state + intent; no flags)"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(ls *)
  - Bash(find *)
  - Bash(wc *)
  - Bash(date *)
  - AskUserQuestion
disable-model-invocation: false
user-invocable: true
metadata:
  author: unikit
  version: "1.0"
  category: game-design
---

# Game Design — Per-Content-Type GDD (Authoring & Revision)

Own **one content type's design document** at
`.unikit/gamedesign/content-types/CT-<slug>.md` — the **content / catalog** axis of
the GDD (the data the game is made of: the cards, items, levels, enemies, quests),
alongside the system GDDs (the rules), the flow GDDs (the dynamics), and `GAME.md`
(the whole). This skill owns the **content zone** (`gd-principles` → Zone Ownership):
the **full lifecycle** of a `CONTENT-TYPE.md` lives here — **create** the skeleton,
**fill** its placeholders, and **revise** the approved **schema** (the typed
`CT.fields` + scale + relationships) under the delta discipline. There is no separate
editor skill.

A content type is a **schema + descriptor, never the catalog of values**. `GD-IDS.yaml`
carries the contract (the typed `CT.fields`, the `scale`, `belongs_to`); the bulk
instance values live in the editor, not the registry. That split is the heart of this
zone — see **Schema vs values** below.

A content type registers **itself**: this skill writes the type's own `GD-IDS.yaml`
`content_types:` and `content:` entries (and the `resources:` / `tracks:` / `knobs:`
facts it owns via a registry-check) and re-renders the `## Content Map [gen]` block in
`GAME.md` — there is **no add-content in `unikit-gd-spec`**. It never authors a system,
never authors a flow, never edits the `GAME.md` one-pager content, and never adds a
system to the roster — those are `unikit-gd-system`, `unikit-gd-flow`, and
`unikit-gd-spec`.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply it to all output and artifacts (fall back to English if it is missing) —
including the rule to **translate concepts, not transliterate jargon**.
`gd-principles` → "Language" adds the game-design specifics: which IDs and stored
field values stay English (IDs like `CT-*`, `CU-*`, `RES-*`, field `type`/`enum`
tokens, and `ref<>` targets are stable machine values — never translated). Do not
announce the language setting.

**The language holds for the whole session, not just at load time:** every message until the conversation ends is in `language.ui` — progress notes while agents run, relays of what a subagent returned, the final report, any follow-up discussion. English input (subagent results, tool output, these instructions) is data, never a cue to switch languages.

## Phase 0 — Bootstrap

Silently load — do not narrate:

1. **`.unikit/system/gamedesign/gd-principles.md`** (the core) — the collaborative
   protocol, the facts registry / ID conventions, and the language rules. Plus, from
   the same `gamedesign/` folder, the shards this skill needs: **`gd-authoring.md`**
   (the **section-cycle authoring contract** + the **delta discipline** — including
   the **content delta: schema vs values** rule that governs this zone),
   **`gd-lifecycle.md`** (the lifecycle & status spine + the **content axis** block:
   the `CT` `doc_status` spine, `belongs_to`, and display precedence), and
   **`gd-content-axis.md`** (the content-axis contract this zone authors against: the
   CT/CU schema model, `ref<>` resolution, `scale` ↔ structure, RES/TRACK/KNOB, and
   the code-reads-content boundary). This skill **applies** that contract; it does
   not restate the mechanics. If missing, warn (`unikit-ai update`) and fall back to
   the protocol as summarized in this file.
2. **`.unikit/gamedesign/GAME.md`** — pillars, loops, target aesthetics, and
   non-goals the content must serve; its `## System Map [gen]` is the system roster a
   content type's `belongs_to` (and any `ref<SYS>`) depend on. If it does not exist,
   **stop** — there is no master spec yet. Read `.unikit/gamedesign/concepts/INDEX.md`
   (if it exists) to route precisely: a `drafted`/`approved` concept present →
   recommend `/unikit-gd-spec` (build the master spec from it); no concept — or no
   `concepts/INDEX.md` (or no `concepts/` dir) at all → recommend
   `/unikit-gd-brainstorm` first, then `/unikit-gd-spec`.
3. **`.unikit/gamedesign/GD-IDS.yaml`** — find the target type's entry under
   `content_types`. If there is **no entry**, this is a new content type: a content
   type registers itself, so author it here (Create — Phase 5 writes the
   `content_types:` row). The `belongs_to` a new type needs may reference a system
   that is **not yet on the map**; that crossing into the *system* roster routes back
   to `/unikit-gd-spec` add-system (see the re-entry seam in Phase 4) — never write a
   `systems:` row here.
4. **`.unikit/memory/gamedesign/RULES_INDEX.md`** — load the **core** domain rules
   for this type's **purpose**, on demand by `Load When`, plus any studio `library`
   rule on the same topic. Read the purpose from the type's name and Overview (what
   the units are), **not** from a coarse label; when the purpose is ambiguous, confirm
   the domain with one `AskUserQuestion` rather than guessing. Domains are opt-in and
   combinable — a content type may match more than one:

   | Content purpose | Core rules to load |
   |-----------------|--------------------|
   | items / loot / gear | `economy`, `balance` |
   | currencies / shop wares | `economy`, `monetization-ethics` |
   | cards / units / abilities | `balance`, `frameworks` |
   | enemies / encounters | `balance` |
   | levels / missions / maps | `level-design` |
   | quests / dialogue / lore | `narrative` |
   | characters / NPCs | `narrative`, `player-motivation` |
   | cosmetics / battle-pass | `monetization-ethics`, `liveops` |
   | progression tracks / unlocks | `progression` |

   Obey the index's **Rule-Loading Discipline**: load by `Load When`, load a reference
   only from its parent rule's `> **References**:`, and **never glob the memory tree**
   (`.unikit/memory/gamedesign/**`) to discover rules.

5. **`.unikit/RULES.md`** (if present) — project overrides, highest priority. **Rule topics:** load the topic files listed under its `## Topics` whose `Load when` matches the design work at hand — the concept, system, flow or content type; when unsure, load.
6. **Schema guard (clean break — no automatic migration).** `GD-IDS.yaml` MUST be
   `version: 2`. If it is still `version: 1`, **STOP** and report: the design
   workspace is on the pre-v2 layout — v2 dropped the standalone markdown
   system-index and now renders the system, flow, funnel, and content maps into
   `GAME.md` (`## System Map [gen]` / `## Flow Map [gen]` / `## Funnel [gen]` /
   `## Content Map [gen]`); there is no automatic migration. Tell the user to bump
   `GD-IDS.yaml` to `version: 2` before re-running.

**One-way boundary:** never read `.unikit/code/`, project source, or build artifacts.
Content crosses to code as a **contract** (the schema + descriptor), never as data —
the bulk values stay in the editor (`gd-principles` → One-Way Boundary).

## Phase 1 — Context

Gather the facts the content type must stay consistent with (read-only):

- **Known facts** from `GD-IDS.yaml` — pillars (the content serves them), the
  `systems` (the `belongs_to` consuming system and any `ref<SYS>` targets), the
  `resources` / `tracks` already locked (a field may `ref<RES>` / reference a track),
  the `entities` / `formulas` a field may `ref<ENT>` / `ref<FORM>`, and the `terms`.
  These are constraints, not suggestions.
- **The consuming system's GDD** — read the `belongs_to` system's header and sections
  **A (Overview)**, **C (Detailed Design)**, and **G (Tuning Knobs)** so the schema
  serves a real consumer (the system that reads these units). A `belongs_to` aimed at
  a missing or deprecated system is a registry gap (route it through
  `unikit-gd-spec` add-system — Phase 4).
- **Recent `unikit-gd-verify` reports** for this content type, if any
  (`.unikit/gamedesign/reviews/`).
- **Explore research (internal design lens)** — if this type was seeded from a
  `unikit-gd-explore` brief, discover the research **deterministically** (survives a
  `/clear`): read the type's `GD-IDS` `content_types[].research:` pointer
  (authoritative), falling back to the `researches/INDEX.md` entry whose `Target:` is
  this `CT-<slug>`. Read that research's `RESEARCH_BRIEF.md` →
  **`## Content Feature Plan`** block and use its schema / scale / catalog **seeds**
  as the *starting drafts* — a **seeded** section is **drafted silently** in Generation
  (Phase 4) and confirmed in the group review (Phase 5); a seed is a draft, not an
  approved write. For a **revision** (Edit), the matching block is
  **`## Content Improvement Plan`**. These explore-seeded drafts are **untagged normal
  authored content**.

## Phase 2 — Resolve Scale + Depth (no flags)

Check `.unikit/gamedesign/content-types/CT-<slug>.md` and read the intent in the
prompt:

1. **Does not exist** → **Create**: build the skeleton (Phase 3), then run the
   Decision-First flow — the **scale** is the first decision in Phase 4 (it shapes
   section C and how the units register).
2. **Exists** and the prompt describes a **change to the approved schema** (a field, a
   type, the scale, `belongs_to`, a `ref<>`: "add a rarity field", "retype condition",
   "switch to curated") → **Edit**: classify the scale of change and apply the delta
   (Revision below). Approved schema is changed **only** through this path.
3. **Exists with `[To be designed]` placeholders** and the intent is to continue /
   fill (or no change is described) → **Fill**: resume from the remaining placeholders.
   Approved text is **never overwritten** — only placeholders are filled. Skip the
   skeleton sub-step (Phase 3.1); still fork-scan and run Phases 4–5 over the
   placeholders.
4. **Exists, complete, no change described** → authoring is done; nothing to write.
   Offer review / verify (Handoff) and stop.

If the type name is ambiguous (matches several entries, or none) → `AskUserQuestion`
listing candidates. Never guess the target. Print the candidates to the screen as plain
markdown first — the question mechanism carries the options and nothing else.

> **Catalog churn is not an Edit here.** Adding, removing, or editing the individual
> content **units** — a `curated` row's field values, a `bulk` type's `count` — is
> **data, not a schema edit** (`gd-authoring` → Content delta). It does not bump the
> version and needs no changelog. Only a **schema** change (Phase 2 case 2) runs the
> Revision delta tail. For a `bulk` type the instance values never enter `GD-IDS` at
> all — they live in the editor.

**Depth gate (Create / Fill only).** Once the mode is Create or Fill, present **one**
depth picker — the named tiers `core/standard/full`, each with what it adds, not bare
letters:

```
AskUserQuestion: How deep should this pass go?
Options:
1. core (recommended) — the floor that gets the type to a solid, usable base: Overview,
   Schema (CT.fields), Scale & Generation.
2. standard — core + Relationships & Dependencies, Validation & Edge Cases.
3. full — every section, fully specified.
```

The picked tier is the **ephemeral scope of this pass — NOT stored**
(`gd-authoring` / `gd-lifecycle`); the lasting fact is the inferred status at Phase 6.
**Edit** mode skips the depth gate entirely (it lies flat on the Revision flow).

---

## Load the Mode Body

With the mode resolved (Phase 2) and the depth picked (Create / Fill only), load the
matching body on demand and follow it — do **not** keep both bodies in context. Create
/ Fill returns to **Phase 6** (Registry & State) below; Edit returns to **Handoff**.

| Mode | Reference body |
|------|----------------|
| **Create / Fill** | `{{skills_dir}}/{{self_name}}/references/mode-author.md` — the Decision-First section-cycle: the A–F section map + core-set, Phase 3 (Skeleton + Fork-Scan), Phase 4 (Decision Interview + Generation, incl. the scale decision + the re-entry seam), Phase 5 (Group Review). |
| **Edit** | `{{skills_dir}}/{{self_name}}/references/mode-revise.md` — a **schema** change: classify the scale (Tuning / Tweak / Rework / Structural-redirect), apply it, then the mandatory delta tail (catalog churn is data — handled directly, not here). |

## Phase 6 — Registry & State (write `content_types:` / `content:`, then re-render the map)

After the sections are authored and accepted:

1. **Write the `GD-IDS.yaml` `content_types[]` entry** (the type's machine truth — the
   content type registers itself): `id: CT-<slug>`, `name`, `status: active`, `scale`,
   `belongs_to` (the `SYS` id from section D), `doc_status`, `version`, `fields:` (the
   typed schema from section B — for a `bulk` type this is the SPEC each instance
   follows; for `curated` it is the schema each `content` row subsets), `research:`
   (the explore-research folder if seeded — a non-id path; owned here),
   `source: content-types/CT-<slug>.md`, `added`. Then write the **units**:
   - **bulk →** one `content[]` row with `kind: set`, `count`, `spec` (the descriptor
     only; the values stay in the editor).
   - **curated →** one `content[]` row per unit with `kind: instance` and
     `fields:` ⊆ `CT.fields` (each value valid by the schema's name + type).

   Get approval before the write; existing values are never changed silently; every
   fact carries its `source` (`gd-principles` → Facts Registry).
2. **Register the facts this type introduces (`RES-` / `TRACK-` / `KNOB-`).** A field
   may reference a **resource** (`ref<RES>`), a **progression track**, or a global
   **tuning knob** that is not yet a registry fact. These are **facts, registered by
   the owning zone via a registry-check** — not a profile edit:
   - `RES-<slug>` → `GD-IDS.yaml` `resources` (a currency / consumable / material),
   - `TRACK-<slug>` → `tracks` (a season / battle-pass / mastery ladder),
   - `KNOB-<slug>` → `knobs` (a cross-system balance value; a per-system tuning value
     stays in that system's section G).

   Before adding one, **registry-check**: if the fact already exists, reference it;
   never duplicate or renumber. Get approval for each new fact; each carries its
   `source`.
3. **Status (inferred — `gd-lifecycle`).** Set the type's status in the **two places
   that must agree** — the `CONTENT-TYPE.md` header `> Status:` token and the
   `GD-IDS.yaml` `doc_status`: `detailed` once the whole **core-set (A/B/C)** is
   authored; **held at `skeleton`** while a **core** section carries `<!-- deferred -->`
   (the soft floor guard; the WARN in Phase 4); `detailed · partial (n/m)` (rendered,
   inferred from the markers) when the core is complete but ≥1 **non-core** section is
   deferred. Set `version: 1` (header + `GD-IDS`). Write the initial changelog block to
   section F (`#### v1 — <date> — initial schema` with the `Fields: + <field> … (new)`
   line and `Affected (gd-verify): —`) — the single current block (K1).
4. **Regen-on-write — re-render the map (B1).** As the last step, re-render `GAME.md`'s
   `## Content Map [gen]` block from `GD-IDS` (the `RULES_INDEX` render model):
   replace **only** the content between `<!-- gen:content-map -->` /
   `<!-- /gen:content-map -->` — **never** touch the authored one-pager above, and
   **never** the `## System Map [gen]` / `## Flow Map [gen]` / `## Funnel [gen]` blocks
   (those are `unikit-gd-spec` / `unikit-gd-flow` renders).
   - **Content Map** — one row per `content_types[]` entry, grouped by `scale` (Bulk,
     Curated): `ID | Content Type | Scale | Status | Ver | Belongs (SYS) | Units | Doc`.
     `Status` mirrors `doc_status` (plus `deprecated` from the `status` field), with the
     **`· partial (n/m)` suffix** appended when the `CONTENT-TYPE.md` carries ≥1
     `<!-- deferred -->` (the canonical render format from `gd-lifecycle` — the same
     suffix verify and the System/Flow maps use); `Ver` is `—` until `skeleton`; `Units`
     is the registered `count` for a `bulk` type or the number of `curated` rows.

---

## Handoff & Next Steps

Recommend the next steps (do not auto-invoke):

- ✅ Verify consistency & impact — /unikit-gd-verify CT-<slug>
- 🔍 Qualitative review (fresh session) — /unikit-gd-review content-types/CT-<slug>.md
- 🗺️ Add the consuming/another system — /unikit-gd-spec (add-system)

A review is most independent in a **fresh session** (the reviewer should not have
authored the doc). `unikit-gd-verify` is read-only — it checks the content type against
the registry and **prints** cross-axis staleness (a `belongs_to`/`ref<SYS>` system edit);
the `## Content Map [gen]` was already re-rendered on this skill's write (B1).

## Final: Compact Report

The terminal plaque (TIER A — `gd-principles` → Language: name leads, ids are
parenthetical copy-paste tags, status is a plain phrase):

```
Content type: <name>  (CT-<slug>)
Scale: <bulk | curated>   Belongs to: <system name> (SYS-<slug>)   ·   Depth: <core | standard | full>  (create/fill)
Action: <create | fill | edit (tuning|tweak|rework) | catalog churn>
Doc: .unikit/gamedesign/content-types/CT-<slug>.md — <ready | ready, a couple of optional blocks left | skeleton, main blocks not filled yet>, vN
Registry: <F> fields; <U> units (<count> bulk | <n> curated); +<R> resources/tracks/knobs  (GD-IDS.yaml)
Map: ## Content Map [gen] re-rendered
```

No summary document, no report file.

## Ownership Boundaries

- **Owns:** the **full lifecycle** of `content-types/CT-<slug>.md` — creating the
  skeleton, filling placeholders, **and revising the approved schema** (Tuning / Tweak
  / Rework, with the version bump + changelog; the status stays `detailed`); the type's
  `GD-IDS.yaml` facts (`content_types[]` incl. `fields`, `scale`, `belongs_to`,
  `research:`; the `content[]` units; and the `resources` / `tracks` / `knobs` facts it
  registers) and its `doc_status` / `version`; the scale selection; and the
  **re-render** of the `## Content Map [gen]` block in `GAME.md` (the `[gen]` region
  only).
- **Not this skill:** systems → `unikit-gd-system`; flows → `unikit-gd-flow`; the
  system roster, the `GAME.md` one-pager content (pillars, win/lose intent,
  monetization stance) **and** its `## System Map [gen]` render → `unikit-gd-spec`;
  quality verdicts → `unikit-gd-review`; consistency & cross-axis impact →
  `unikit-gd-verify`.
- **Never:** write, fill, or edit without approval; overwrite approved schema outside
  the delta discipline; run the delta tail for catalog churn (data, not a schema edit);
  skip the version bump or changelog on a **schema** edit (unrecorded delta); change a
  `GD-IDS.yaml` value silently; delete or renumber an ID; write the `systems:` roster
  or the `GAME.md` one-pager content; touch the `## System Map [gen]` / `## Flow Map
  [gen]` / `## Funnel [gen]` blocks; read the code workspace or project source.

## Quick Reference

```
/unikit-gd-content CT-item                        → select scale + create skeleton + author A–F (if no doc yet)
/unikit-gd-content item                           → resolve to the CT-slug; same type
/unikit-gd-content CT-item                        → resume filling placeholders (partial doc)
/unikit-gd-content CT-item "add a rarity field"   → Tweak: edit B Schema, one approval
/unikit-gd-content item "switch to curated"       → Rework: scale flip (C + header + GD-IDS)
/unikit-gd-content CT-card "retype cost to enum"  → Rework: type change + data migration
```
