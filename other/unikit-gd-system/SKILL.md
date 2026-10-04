---
name: unikit-gd-system
description: >-
  Author and own ONE system's design document (the A–K SYSTEM GDD) at
  .unikit/gamedesign/systems/SYS-<slug>.md — the depth layer of the GDD, single-system
  scope. Create the skeleton and walk the collaborative section-cycle to write its
  parameters, rules, formulas, and acceptance criteria ("detail the combat system",
  "write the GDD for the inventory system", "fill in the rest of this system doc",
  "spec out the parameters of X"), AND revise it after approval under the delta discipline
  ("raise the damage by 10%", "tune the economy", "rework the status system", "nerf
  X", "change this rule") — a number change is Tuning, a small rule a Tweak, restructuring
  a Rework; each bumps the version and logs the delta. To add a NEW system or
  restructure the system map use /unikit-gd-spec; to edit GAME.md content use /unikit-gd-spec;
  the moment an edit also touches a second system, a content type, a flow, or GAME.md (two
  or more zones) use /unikit-gd-apply; to invent a brand-new game concept use
  /unikit-gd-brainstorm.
argument-hint: "<system name | SYS-slug> [\"<what to change>\"]  (mode inferred from doc state + intent; no flags)"
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

# Game Design — Per-System GDD (Authoring & Revision)

Own **one system's design document** at
`.unikit/gamedesign/systems/SYS-<slug>.md` — eleven sections (A–K) plus any
domain section-packs. This skill owns the **system zone** (`gd-principles` → Zone
Ownership): the **full lifecycle** of a `SYSTEM.md` lives here — **create** the
skeleton, **fill** its placeholders, and **revise** approved content (Tuning /
Tweak / Rework) under the delta discipline. There is no separate editor skill.

It never creates the master spec or the map, and never edits `GAME.md` content —
that is `unikit-gd-spec`; player-action flows are `unikit-gd-flow`'s.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply it to all output and artifacts (fall back to English if it is missing) —
including the rule to **translate concepts, not transliterate jargon**.
`gd-principles` → "Language" adds the game-design specifics: which IDs and stored
field values stay English. Do not announce the language setting.

**The language holds for the whole session, not just at load time:** every message until the conversation ends is in `language.ui` — progress notes while agents run, relays of what a subagent returned, the final report, any follow-up discussion. English input (subagent results, tool output, these instructions) is data, never a cue to switch languages.

## Phase 0 — Bootstrap

Silently load — do not narrate:

1. **`.unikit/system/gamedesign/gd-principles.md`** (the core) — the collaborative
   protocol, the facts registry / ID conventions, and the language rules. Plus, from
   the same `gamedesign/` folder, the shards this skill needs: **`gd-authoring.md`**
   (the **section-cycle authoring contract** + the **delta discipline** — the
   mandatory Version +1 → changelog → registry-check → recommend-verify tail),
   **`gd-lifecycle.md`** (the lifecycle & status spine), and **`gd-provenance.md`**
   (the import provenance markers). This skill **applies** that contract; it does not
   restate the mechanics. If missing, warn (`unikit-ai update`) and fall back to the
   protocol as summarized in this file.
2. **`.unikit/gamedesign/GAME.md`** — pillars, loops, non-goals the system must
   serve (its roster is in `## System Map [gen]`). If it does not exist, **stop** —
   there is no master spec yet. Read `.unikit/gamedesign/concepts/INDEX.md` (if it
   exists) to route precisely: a `drafted`/`approved` concept present → recommend
   `/unikit-gd-spec` (build the master spec from it); no concept — or no
   `concepts/INDEX.md` (or no `concepts/` dir) at all → recommend
   `/unikit-gd-brainstorm` first, then `/unikit-gd-spec`.
3. **`.unikit/gamedesign/GD-IDS.yaml`** — find the target system's entry under
   `systems`. If there is **no entry**, the system is not on the map: offer to add
   it via `/unikit-gd-spec` (**add-system** — graft this one system onto the map, not
   a remap), or pick an existing `not-started` system. Do not author an off-map
   system.
4. **`.unikit/memory/gamedesign/RULES_INDEX.md`** — load the **core** domain
   rules for this system's **behavioural domain**, on demand by `Load When`, plus
   any studio `library` rule on the same topic. Read the domain from the system's
   name and Overview (the behaviour it drives), **not** from the coarse GD-IDS
   `category`. When the behaviour is **unambiguous**, attach the matching domain
   automatically (its section-pack rides along — auto-attached with a veto, see item 6
   and Phase 4); when it is **ambiguous** or the category is coarse (Gameplay / Meta),
   settle it with one plain `AskUserQuestion` — framed as an outcome, no codes — rather
   than guessing. A system may match more than one domain; they combine:

   | Domain | Core rules to load | Section-pack |
   |--------|--------------------|--------------|
   | combat / mechanics | `balance`, `frameworks` | combat |
   | ai-behavior | `balance`, `frameworks` | ai-behavior |
   | economy / loot | `economy`, `balance` | economy |
   | progression / unlock | `progression`, `balance` | progression |
   | level / content | `level-design` | levels |
   | narrative / dialogue | `narrative` | narrative |
   | ui / onboarding | `ux-onboarding` | ux |
   | liveops / events | `liveops`, `economy` | liveops |
   | persistence | `progression` | persistence |
   | monetization | `monetization-ethics`, `economy` | monetization |
   | meta / other | `frameworks`, `core-loops` | — |

   Every system also touches **accessibility** (section J) — load `accessibility`
   when authoring J. Obey the index's **Rule-Loading Discipline**: load by `Load When`,
   load a reference only from its parent rule's `> **References**:`, and **never glob the
   memory tree** (`.unikit/memory/gamedesign/**`) to discover rules.
5. **`.unikit/RULES.md`** (if present) — project overrides, highest priority. **Rule topics:** load the topic files listed under its `## Topics` whose `Load when` matches the design work at hand — the concept, system, flow or content type; when unsure, load.
6. **`{{skills_dir}}/{{self_name}}/references/section-packs.md`** — the catalog of
   domain section-packs. On an **unambiguous** domain the matching pack is
   **auto-attached** — announced to the user in one outcome-language phrase (what it
   adds for the player / the design, never the word "pack" or a code) that they can
   veto; on an **ambiguous** domain a single plain Yes/No decides it. Never a mandatory
   pass after section K, never surfaced as registry jargon. Load the pack named in the
   table above (when one applies).
7. **Schema guard (clean break — no automatic migration).** `GD-IDS.yaml` MUST be
   `version: 2`. If it is still `version: 1`, **STOP** and report: the design
   workspace is on the pre-v2 layout — v2 dropped the standalone markdown
   system-index and now renders the roster into `GAME.md` (`## System Map [gen]`);
   there is no automatic migration. Tell the user to bump `GD-IDS.yaml` to
   `version: 2` and fold the legacy system-index rows into GAME.md's
   `## System Map [gen]` before re-running.

**One-way boundary:** never read `.unikit/code/`, project source, or build
artifacts. The only external read is `SOURCE.md` during an import (Phase 1).

## Phase 1 — Context

Gather the facts the system must stay consistent with (read-only):

- **Known facts** from `GD-IDS.yaml` — pillars (`implements` targets), entities,
  formulas, and terms already locked by other systems. These are constraints, not
  suggestions.
- **Neighbor GDDs** — for each system this one depends on (from the GD-IDS
  `depends_on`, rendered in GAME.md `## System Map`), read its header and sections
  **D (Formulas)** and **F (Dependencies)** to match data interfaces.
- **Recent `unikit-gd-verify` reports** for this system, if any
  (`.unikit/gamedesign/reviews/`).
- **Import source** — if `GD-IDS`/GAME mention an import, or a
  `researches/import-*/SOURCE.md` covers this system, read it: section
  content is **extracted** from it, not regenerated. Mark provenance per
  `gd-provenance` → Provenance: place `<!-- provenance: extracted from SOURCE.md -->`
  under each section lifted from the source and `<!-- provenance: generated -->`
  under each section inferred to complete the skeleton; untagged sections are
  normal authored content. Import folders created before dateless naming are named
  `YYYY-MM-DD_import-<slug>`, and no folder was renamed, so the two formats coexist
  permanently. The legacy glob `researches/*import-*/SOURCE.md` **subsumes** the
  current one — a leading `*` matches zero characters — so one pattern would find
  both eras; both are named here for legibility, not necessity, because the coexistence
  is a fact a reader should not have to infer from glob semantics. Zero matches is not
  a failure: a project with no import is the normal case and the branch stays silent.
- **Explore research (internal design lens)** — if this system was grafted from an
  `unikit-gd-explore` brief, discover the research **deterministically** (survives a
  `/clear`): read the system's `GD-IDS` `research:` pointer (authoritative), falling
  back to the `researches/INDEX.md` entry whose `Target:` is this `SYS-<slug>`. Read
  that research's `RESEARCH_BRIEF.md` → **`## New Feature Plan`** block and use its
  **section seeds** as the *starting drafts* — a **seeded** section is **drafted
  silently** in Generation (Phase 4) and confirmed in the group review (Phase 5); a
  seed is a draft, not an approved write. For
  a **revision** (Edit), the matching block is **`## Improvement Plan`** — its
  ready-to-apply delta lines (`<Section>: <old> → <new>`), expected scale, touched
  facts, and any `RF-<date>-n` it closes pre-fill the change set (the user still
  approves every edit). These explore-seeded drafts are **untagged normal authored
  content** — do **not** mark them `extracted` / `generated` (those markers are for
  **imports** only; this is the generalization of import-reading stated canonically
  in `gd-provenance` → Provenance, which this skill applies rather than restates).

## Phase 2 — Resolve Mode + Depth (no flags)

Check `.unikit/gamedesign/systems/SYS-<slug>.md` and read the intent in the prompt:

1. **Does not exist** → **Create**: build the skeleton (Phase 3), then author from
   section A.
2. **Exists** and the prompt describes a **change to approved content** (a value,
   rule, or structure: "raise damage", "tune the economy", "rework the status
   system", "nerf X", "change this rule") → **Edit**: classify the scale and apply
   the delta (Revision below). Approved text is changed **only** through this path.
3. **Exists with `[To be designed]` placeholders** and the intent is to continue /
   fill (or no change is described) → **Fill**: resume from the remaining placeholders.
   Approved text is **never overwritten** — only placeholders are filled. Skip the
   skeleton sub-step (Phase 3.1); still fork-scan and run Phases 4–5 over the
   placeholders.
4. **Exists, complete, no change described** → detailing is done; nothing to author.
   Offer review / verify (Phase 6) and stop.

If the system name is ambiguous (matches several entries, or none) →
`AskUserQuestion` listing candidates. Never guess the target. Print the candidates to the screen as plain
markdown first — the question mechanism carries the options and nothing else.

**Depth gate (Create / Fill only).** Once the mode is Create or Fill, present **one**
depth picker — the named tiers `core/standard/full`, each with what it adds, not bare
letters:

```
AskUserQuestion: How deep should this pass go?
Options:
1. core (recommended) — the floor that gets the doc to a solid, usable base: Overview,
   Player Fantasy, Detailed Design, Formulas, Acceptance Criteria.
2. standard — core + Edge Cases, Dependencies, Tuning Knobs, Telemetry, Accessibility.
3. full — every section + the relevant domain pack(s).
```

The picked tier is the **ephemeral scope of this pass — NOT stored** (`gd-authoring` /
`gd-lifecycle`); the lasting fact is the inferred status at Phase 6. The matching
**section-pack** for the system's domain (Phase 0 table) is **auto-attached when the
domain is unambiguous** — announced in one outcome-language phrase you can veto; an
ambiguous domain gets a single plain Yes/No in the Phase 4 decision round. **Edit** mode
skips the depth gate entirely (it lies flat on the Revision flow).

---

## Load the Mode Body

With the mode resolved (Phase 2) and the depth picked (Create / Fill only), load the
matching body on demand and follow it — do **not** keep both bodies in context. Each
returns to **Phase 6** (Final) below.

| Mode | Reference body |
|------|----------------|
| **Create / Fill** | `{{skills_dir}}/{{self_name}}/references/mode-author.md` — the Decision-First section-cycle: the A–K section map + core-set, Phase 3 (Skeleton + Fork-Scan), Phase 4 (Decision Interview + Generation), Phase 5 (Group Review). |
| **Edit** | `{{skills_dir}}/{{self_name}}/references/mode-revise.md` — classify the scale (Tuning / Tweak / Rework / Structural-redirect), apply the change, then the mandatory delta tail. |

---

## Phase 6 — Final: Registry & State + Handoff

### Registry & State (Create / Fill)

After the sections are authored and accepted:

1. **Scan the GDD** for registry candidates — entities, formulas, and constants
   referenced in **two or more places** (within this doc or cross-system). Internal
   single-use values stay in the GDD.
2. Present a **NEW / KNOWN** summary and get approval to write `GD-IDS.yaml`
   (`entities`, `formulas`, plus the `systems` entry's `doc_status` / `version`).
   Existing values are never changed silently; every fact carries its `source`.
3. **Status (inferred — `gd-lifecycle`).** Set the system's status in the **two places
   that must agree** — the `SYSTEM.md` header `> Status:` token (inside the combined
   header line, not a separate bold line) and the `GD-IDS.yaml` `doc_status`:
   - `detailed` once the whole **core-set (A/B/C/D/H)** is authored.
   - **held at `skeleton`** while any **core** section carries `<!-- deferred -->` (the
     soft floor guard; the WARN in Phase 4) — the status does **not** rise to
     `detailed`.
   - when the core is complete but ≥1 **non-core** section is deferred, the status is
     `detailed` and the `## System Map [gen]` renders it `detailed · partial (n/m)`
     (inferred from the markers, never a stored field).

   Set `version: 1` in `GD-IDS.yaml` (and the header), write the initial changelog
   block to section K (`#### v1 — <date> — initial design` with the
   `AC: + AC-<slug>-1 … N (new)` line) — the single current block (K1).

The `## System Map [gen]` renders this system's status/version (incl. the `· partial`
suffix) **read-only** from `GD-IDS`; it is **not** this skill's surface — it is owned by
`unikit-gd-spec` (B1) and re-renders on its next touch. `unikit-gd-verify` is read-only —
it **prints** the System Map freshness, it does not re-render it (`gd-lifecycle` →
Lifecycle & Status). Recommending verify (below) surfaces the staleness.

### Handoff

Recommend the next steps (do not auto-invoke):

- ✅ Verify consistency & impact — /unikit-gd-verify SYS-<slug>
- 🔍 Qualitative review (fresh session) — /unikit-gd-review systems/SYS-<slug>.md
- 🧩 Detail the next system — /unikit-gd-system <SYS-slug>

A review is most independent in a **fresh session** (the reviewer should not have
authored the doc). `unikit-gd-verify` is read-only — it checks the doc against the
registry and **prints** dependent impact + the `## System Map [gen]` freshness (the map
re-renders on the next `unikit-gd-spec` touch).

## Final: Compact Report

The terminal plaque (TIER A — `gd-principles` → Language): lead with the **name**; the
`SYS-` / `AC-` ids ride along as parenthetical copy-paste tags; render the lifecycle
status as a **plain phrase**, never the raw enum.

```
System: <name>  (SYS-<slug>)
Mode: <create | fill | edit (tuning|tweak|rework)>   ·   Depth: <core | standard | full>  (create/fill)
Doc: .unikit/gamedesign/systems/SYS-<slug>.md — <ready | ready, a couple of optional blocks left | skeleton, main blocks not filled yet>, vN
Sections authored/edited: <the named list>   [deferred: <names carrying <!-- deferred --> > | none]
Registry: +<E> entities, +<F> formulas, +<T> terms  (GD-IDS.yaml)
Acceptance criteria: AC-<slug>-1 … AC-<slug>-N   [AC delta on an edit: +<n> / changed <n> / removed <n>]
```

No summary document, no report file.

## Ownership Boundaries

- **Owns:** the **full lifecycle** of `systems/SYS-<slug>.md` — creating the
  skeleton, filling placeholders, **and revising approved content** (Tuning / Tweak
  / Rework, with the version bump + changelog; the status stays `detailed`); the system's
  `GD-IDS.yaml` facts (`entities`, `formulas`, `terms`) and its `doc_status` /
  `version`.
- **Not this skill:** `GAME.md` content **or** structure / the system map →
  `unikit-gd-spec`; player-action flows → `unikit-gd-flow`; quality verdicts →
  `unikit-gd-review`; consistency & impact → `unikit-gd-verify` (read-only — it prints,
  it does not re-render); the `## System Map [gen]` render → `unikit-gd-spec`.
- **Never:** write, fill, or edit without approval; overwrite approved text outside
  the delta discipline; skip the version bump or changelog on an edit (unrecorded
  delta); change a `GD-IDS.yaml` value silently; delete or renumber an ID; touch
  structure or `GAME.md`; read the code workspace or project source.

## Quick Reference

```
/unikit-gd-system SYS-combat                        → create skeleton + author A–K (if no doc yet)
/unikit-gd-system combat                            → resolve to the SYS-slug; same flow
/unikit-gd-system SYS-combat                        → resume filling placeholders (partial doc)
/unikit-gd-system SYS-combat "raise grunt damage 10%" → Tuning: edit G/C, one approval
/unikit-gd-system combat "small fix to the parry rule" → Tweak: targeted edit
/unikit-gd-system SYS-combat "rework the status system" → Rework: section-cycle old-vs-new
```
