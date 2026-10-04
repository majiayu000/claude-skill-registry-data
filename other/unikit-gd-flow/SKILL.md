---
name: unikit-gd-flow
description: >-
  Author and own one flow's design document (the FLOW.md objective flow) at
  .unikit/gamedesign/flows/FLOW-<slug>.md — the dynamics layer of the GDD (what the player
  does over time). Create the skeleton and walk the collaborative section-cycle to write its
  objectives, pacing, dependencies, and funnel events ("design the first-session flow", "map
  the onboarding sequence", "write the FLOW for the boss encounter"), AND revise it after
  approval under the delta discipline ("retune the pacing", "add a branch", "change a GOAL",
  "rework the onboarding") — a cue/number change is Tuning, a small step change a Tweak,
  restructuring a Rework; each bumps the version and logs the delta. Selects the wiring
  mode (linear | conditional | emergent) and re-renders the ## Flow Map [gen] / ## Funnel
  [gen] blocks in GAME.md. To add or detail a system use /unikit-gd-system; to edit GAME.md
  content use /unikit-gd-spec; to apply a multi-zone edit use /unikit-gd-apply; for a new
  game concept use /unikit-gd-brainstorm.
argument-hint: "<flow name | FLOW-slug> [\"<what to change>\"]  (mode inferred from doc state + intent; no flags)"
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

# Game Design — Per-Flow GDD (Authoring & Revision)

Own **one flow's design document** at `.unikit/gamedesign/flows/FLOW-<slug>.md` —
the **dynamics** axis of the GDD (what the player does over time), alongside the
system GDDs (the rules) and `GAME.md` (the whole). This skill owns the **flow zone**
(`gd-principles` → Zone Ownership): the **full lifecycle** of a `FLOW.md` lives here
— **create** the skeleton, **fill** its placeholders, and **revise** approved
content (Tuning / Tweak / Rework) under the delta discipline. There is no separate
editor skill.

A flow registers **itself**: this skill writes the flow's own `GD-IDS.yaml` `flows:`
and `events:` entries and re-renders the `## Flow Map [gen]` / `## Funnel [gen]`
blocks in `GAME.md` — there is **no add-flow in `unikit-gd-spec`**. It never authors
a system, never edits the `GAME.md` one-pager content, and never adds a system to the
roster — those are `unikit-gd-system` and `unikit-gd-spec`.

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
   **`gd-lifecycle.md`** (the lifecycle & status spine), **`gd-flow-axis.md`** (the
   **Flow Axis** contract — the `AC · GOAL · event` grammar, flow lifecycle, wiring
   mode, cross-axis staleness, Win/Lose ↔ terminal GOAL), and **`gd-provenance.md`**
   (the explore-seed / import provenance markers). This skill **applies** that
   contract; it does not restate the mechanics. If missing, warn (`unikit-ai update`)
   and fall back to the protocol as summarized in this file.
2. **`.unikit/gamedesign/GAME.md`** — pillars, loops, target aesthetics, win/lose
   intent, and non-goals the flow must serve; its `## System Map [gen]` is the system
   roster the flow's `GOAL`s depend on. If it does not exist, **stop** — there is no
   master spec yet. Read `.unikit/gamedesign/concepts/INDEX.md` (if it exists) to route
   precisely: a `drafted`/`approved` concept present → recommend `/unikit-gd-spec`
   (build the master spec from it); no concept — or no `concepts/INDEX.md` (or no
   `concepts/` dir) at all → recommend `/unikit-gd-brainstorm` first, then
   `/unikit-gd-spec`.
3. **`.unikit/gamedesign/GD-IDS.yaml`** — find the target flow's entry under `flows`.
   If there is **no entry**, this is a new flow: a flow registers itself, so author it
   here (Create — Phase 3 writes the `flows:` row). The `GOAL`s a new flow needs may
   reference systems that are **not yet on the map**; that crossing into the *system*
   roster routes back to `/unikit-gd-spec` add-system (see the re-entry seam in
   Phase 4) — never write a `systems:` row here.
4. **`.unikit/memory/gamedesign/RULES_INDEX.md`** — load the **core** domain rules
   for this flow's **purpose**, on demand by `Load When`, plus any studio `library`
   rule on the same topic. Read the purpose from the flow's name and Overview (the
   dynamics it shapes), **not** from a coarse label; when the purpose is ambiguous,
   confirm the domain with one `AskUserQuestion` rather than guessing. Domains are
   opt-in and combinable — a flow may match more than one. Every flow shapes
   **pacing + guidance**, so `core-loops` is always relevant; `ux-onboarding` rides
   along whenever the flow teaches or guides:

   | Flow purpose | Core rules to load |
   |--------------|--------------------|
   | onboarding / first session | `ux-onboarding`, `core-loops` |
   | core loop / session arc | `core-loops`, `player-motivation` |
   | progression / mastery arc | `progression`, `core-loops` |
   | combat / encounter | `balance`, `frameworks` |
   | economy / shop funnel | `economy`, `monetization-ethics` |
   | narrative / quest | `narrative` |
   | level / mission | `level-design` |
   | liveops / event | `liveops`, `player-motivation` |
   | meta / retention | `player-motivation`, `liveops` |

   Obey the index's **Rule-Loading Discipline**: load by `Load When`, load a reference
   only from its parent rule's `> **References**:`, and **never glob the memory tree**
   (`.unikit/memory/gamedesign/**`) to discover rules.

5. **`.unikit/RULES.md`** (if present) — project overrides, highest priority. **Rule topics:** load the topic files listed under its `## Topics` whose `Load when` matches the design work at hand — the concept, system, flow or content type; when unsure, load.
6. **Schema guard (clean break — no automatic migration).** `GD-IDS.yaml` MUST be
   `version: 2`. If it is still `version: 1`, **STOP** and report: the design
   workspace is on the pre-v2 layout — v2 dropped the standalone markdown
   system-index and now renders the system, flow, and funnel maps into `GAME.md`
   (`## System Map [gen]` / `## Flow Map [gen]` / `## Funnel [gen]`); there is no
   automatic migration. Tell the user to bump `GD-IDS.yaml` to `version: 2` and fold
   the legacy index rows into GAME.md's `[gen]` maps before re-running.

**One-way boundary:** never read `.unikit/code/`, project source, or build
artifacts. Flow is a *read target* for the code side, never a writeback surface — a
flow's "realized" state is **derived**, never written here.

## Phase 1 — Context

Gather the facts the flow must stay consistent with (read-only):

- **Known facts** from `GD-IDS.yaml` — pillars (the flow serves them), the systems
  in `systems` (a `GOAL` exercises a system through `GOAL → SYS`, refined to
  `GOAL → AC`), and terms already locked. These are constraints, not suggestions.
- **Exercised system GDDs** — for each system this flow's `GOAL`s touch, read its
  header and sections **C (Detailed Design)**, **H (Acceptance Criteria)**, and
  **B (Player Fantasy)** so each `GOAL` lands on a real rule/AC and the promised
  feeling is grounded. A `GOAL` aimed at a missing or deprecated system is a
  registry gap (route it through `unikit-gd-spec` add-system — Phase 4).
- **Recent `unikit-gd-verify` reports** for this flow, if any
  (`.unikit/gamedesign/reviews/`).
- **Explore research (internal design lens)** — if this flow was seeded from a
  `unikit-gd-explore` brief, discover the research **deterministically** (survives a
  `/clear`): read the flow's `GD-IDS` `flows[].research:` pointer (authoritative),
  falling back to the `researches/INDEX.md` entry whose `Target:` is this
  `FLOW-<slug>`. Read that research's `RESEARCH_BRIEF.md` → **`## Flow Feature Plan`**
  block and use its objective/pacing/dependency **seeds** as the *starting drafts* —
  a **seeded** section is **drafted silently** in Generation (Phase 4) and confirmed
  in the group review (Phase 5); a seed is a draft, not an approved write. For a
  **revision** (Edit), the matching block is
  **`## Flow Improvement Plan`** — its ready-to-apply delta lines, expected scale,
  touched `GOAL`s/systems, and any `RF-<date>-n` it closes pre-fill the change set
  (the user still approves every edit). These explore-seeded drafts are **untagged
  normal authored content** (`gd-provenance` → Provenance) — the import-only
  `extracted` / `generated` markers do not apply to flows.

## Phase 2 — Resolve Mode + Depth (no flags)

Check `.unikit/gamedesign/flows/FLOW-<slug>.md` and read the intent in the prompt:

1. **Does not exist** → **Create**: build the skeleton (Phase 3), then run the
   Decision-First flow — the **wiring mode** is the first decision in Phase 4 (it
   shapes sections B and C).
2. **Exists** and the prompt describes a **change to approved content** (a goal,
   pacing beat, dependency, event, or the wiring mode: "retune the pacing", "add a
   branch", "change a GOAL", "rework the onboarding") → **Edit**: classify the scale
   and apply the delta (Revision below). Approved text is changed **only** through
   this path.
3. **Exists with `[To be designed]` placeholders** and the intent is to continue /
   fill (or no change is described) → **Fill**: resume from the remaining placeholders.
   Approved text is **never overwritten** — only placeholders are filled. Skip the
   skeleton sub-step (Phase 3.1); still fork-scan and run Phases 4–5 over the
   placeholders.
4. **Exists, complete, no change described** → authoring is done; nothing to write.
   Offer review / verify (Handoff) and stop.

If the flow name is ambiguous (matches several entries, or none) → `AskUserQuestion`
listing candidates. Never guess the target. Print the candidates to the screen as plain
markdown first — the question mechanism carries the options and nothing else.

**Depth gate (Create / Fill only).** Once the mode is Create or Fill, present **one**
depth picker — the named tiers `core/standard/full`, each with what it adds, not bare
letters:

```
AskUserQuestion: How deep should this pass go?
Options:
1. core (recommended) — the floor that gets the flow to a solid, usable base: Overview,
   Objective Flow (the run of objectives the player works through).
2. standard — core + Pacing, Dependencies, Events (the funnel).
3. full — every section, fully tuned.
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
| **Create / Fill** | `{{skills_dir}}/{{self_name}}/references/mode-author.md` — the Decision-First section-cycle: the A–F section map + core-set, Phase 3 (Skeleton + Fork-Scan), Phase 4 (Decision Interview + Generation, incl. the wiring-mode decision + the re-entry seam), Phase 5 (Group Review). |
| **Edit** | `{{skills_dir}}/{{self_name}}/references/mode-revise.md` — classify the scale (Tuning / Tweak / Rework / Structural-redirect), apply the change, then the mandatory delta tail. |

## Phase 6 — Registry & State (write `flows:` / `events:`, then re-render the maps)

After the sections are authored and accepted:

1. **Write the `GD-IDS.yaml` `flows[]` entry** (the flow's machine truth — the flow
   registers itself): `id: FLOW-<slug>`, `name`, `status: active`, `mode`,
   `doc_status`, `version`, `depends_on` (the `SYS` ids from section D), `goals:` (one
   `GOAL-<flow>-<n>` per row — `id`, `summary`, `targets:` the `SYS`/`AC` it
   exercises), `research:` (the explore-research folder if seeded — a non-id path;
   owned here, not by `unikit-gd-spec`), `source: flows/FLOW-<slug>.md`, `added`. Write
   each funnel event under `events[]` (`id`, `name`, `status`, `source`, `flow:`).
   Get approval before the write; existing values are never changed silently; every
   fact carries its `source` (`gd-principles` → Facts Registry).
2. **Status (inferred — `gd-lifecycle`).** Set the flow's status in the **two places
   that must agree** — the `FLOW.md` header `> Status:` token and the `GD-IDS.yaml`
   `doc_status`: `detailed` once the whole **core-set (A/B)** is authored; **held at
   `skeleton`** while a **core** section carries `<!-- deferred -->` (the soft floor
   guard; the WARN in Phase 4); `detailed · partial (n/m)` (rendered, inferred from the
   markers) when the core is complete but ≥1 **non-core** section is deferred. Set
   `version: 1` (header + `GD-IDS`). Write the initial changelog block to section F
   (`#### v1 — <date> — initial design` with the `GOAL: + GOAL-<slug>-1 … N (new)`
   line and `Affected (gd-verify): —`) — the single current block (K1).
3. **Regen-on-write — re-render the maps (B1).** As the last step, re-render
   `GAME.md`'s `## Flow Map [gen]` and `## Funnel [gen]` blocks from `GD-IDS`
   (the `RULES_INDEX` render model): replace **only** the content between
   `<!-- gen:flow-map -->` / `<!-- /gen:flow-map -->` and between
   `<!-- gen:funnel -->` / `<!-- /gen:funnel -->` — **never** touch the authored
   one-pager above, and **never** the `## System Map [gen]` block (that is
   `unikit-gd-spec`'s render).
   - **Flow Map** — one row per `flows[]` entry, grouped by wiring-mode
     (Linear/Conditional, Emergent): `ID | Flow | Mode | Status | Ver | Depends (SYS) |
     Realized | Doc`. `Status` mirrors `doc_status` (plus `deprecated` from the
     `status` field), with the **`· partial (n/m)` suffix** appended when the `FLOW.md`
     carries ≥1 `<!-- deferred -->` (the canonical render format from `gd-lifecycle` —
     the same suffix verify and the System Map use); `Ver` is `—` until `skeleton`.
   - **`Realized` is DERIVED, never written:** `yes` once **every** system in the
     flow's `depends_on` carries a non-empty `implemented_version` in `GD-IDS`
     (the code-set field), else `no`. It is computed from the systems' state on each
     render — there is no `implemented` field on flows.
   - **Funnel** — one row per `events[]` entry: `Order | Event | Flow | Measures`,
     ordered by funnel position.

---

## Handoff & Next Steps

Recommend the next steps (do not auto-invoke):

- ✅ Verify consistency & impact — /unikit-gd-verify FLOW-<slug>
- 🔍 Qualitative review (fresh session) — /unikit-gd-review flows/FLOW-<slug>.md
- 🧩 Detail an exercised system — /unikit-gd-system <SYS-slug>

A review is most independent in a **fresh session** (the reviewer should not have
authored the doc). `unikit-gd-verify` is read-only — it checks the flow against the
registry and **prints** dependent flows on cross-axis staleness; the `## Flow Map [gen]`
/ `## Funnel [gen]` were already re-rendered on this skill's write (B1).

## Final: Compact Report

The terminal plaque (TIER A — `gd-principles` → Language: name leads, ids are
parenthetical copy-paste tags, status is a plain phrase):

```
Flow: <name>  (FLOW-<slug>)
Mode: <linear | conditional | emergent>   ·   Depth: <core | standard | full>  (create/fill)
Action: <create | fill | edit (tuning|tweak|rework)>
Doc: .unikit/gamedesign/flows/FLOW-<slug>.md — <ready | ready, a couple of optional blocks left | skeleton, main blocks not filled yet>, vN
Registry: +<G> goals, +<E> events, depends_on [<name> (SYS-<slug>), …]  (GD-IDS.yaml)
Goals: GOAL-<slug>-1 … GOAL-<slug>-N   [GOAL delta on an edit: +<n> / changed <n> / removed <n>]
Maps: ## Flow Map [gen] + ## Funnel [gen] re-rendered
```

No summary document, no report file.

## Ownership Boundaries

- **Owns:** the **full lifecycle** of `flows/FLOW-<slug>.md` — creating the skeleton,
  filling placeholders, **and revising approved content** (Tuning / Tweak / Rework,
  with the version bump + changelog; the status stays `detailed`); the flow's `GD-IDS.yaml`
  facts (`flows[]` incl. `goals`, `mode`, `depends_on`, `research:`, and the flow's
  `events`) and its `doc_status` / `version`; the wiring-mode selection; and the
  **re-render** of the `## Flow Map [gen]` and `## Funnel [gen]` blocks in `GAME.md`
  (the `[gen]` regions only).
- **Not this skill:** systems → `unikit-gd-system`; the system roster, the `GAME.md`
  one-pager content (pillars, win/lose intent, monetization stance) **and** its
  `## System Map [gen]` render → `unikit-gd-spec`; quality verdicts →
  `unikit-gd-review`; consistency & cross-axis impact → `unikit-gd-verify`.
- **Never:** write, fill, or edit without approval; overwrite approved text outside
  the delta discipline; skip the version bump or changelog on an edit (unrecorded
  delta); change a `GD-IDS.yaml` value silently; delete or renumber an ID; write the
  `systems:` roster or the `GAME.md` one-pager content; touch the `## System Map
  [gen]` block; read the code workspace or project source.

## Quick Reference

```
/unikit-gd-flow FLOW-first-session                      → select mode + create skeleton + author A–F (if no doc yet)
/unikit-gd-flow first-session                           → resolve to the FLOW-slug; same flow
/unikit-gd-flow FLOW-first-session                      → resume filling placeholders (partial doc)
/unikit-gd-flow FLOW-first-session "retune the pacing"  → Tuning: edit C/B, one approval
/unikit-gd-flow first-session "add a stealth branch"    → Rework: section-cycle old-vs-new
/unikit-gd-flow FLOW-onboarding "switch to conditional" → Rework: mode change (B + C restructured)
```
