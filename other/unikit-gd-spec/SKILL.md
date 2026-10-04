---
name: unikit-gd-spec
description: >-
  Create and own the master game design document (GAME.md — the authored one-pager plus the
  generated [gen] system/flow maps) and the GD-IDS.yaml facts registry — the top-level,
  big-picture layer of the GDD and the machine interface the code side reads. Use it to write
  the master spec from a concept or dialogue, import an existing GDD (a file path or URL), edit
  GAME.md content ("change a pillar", "rework the monetization stance", "tweak the loop stack"),
  pitch the game ("pitch" → PITCH.md), re-decompose the systems ("remap"), and — importantly — to
  add a new system to the design map ("let's add a new system", "add a crafting system to the
  game design", "add this to the GDD"). This is the structural, map-level layer plus GAME.md
  content edits. To write or fill in the detailed parameters of one existing system, use
  /unikit-gd-system; to apply one edit spanning several zones at once use /unikit-gd-apply;
  to invent a brand-new game concept use /unikit-gd-brainstorm.
argument-hint: "[path-to-existing-GDD | URL | free-form description]  (mode inferred; no flags)"
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
  - WebFetch
  - AskUserQuestion
disable-model-invocation: false
user-invocable: true
metadata:
  author: unikit
  version: "1.0"
  category: game-design
---

# Game Design — Master Spec & System Map

Author the **whole-game truth** and the **map of every system**. This skill owns the
**spec / map zone** in `.unikit/gamedesign/` (`gd-principles` → Zone Ownership):

- **`GAME.md`** — the one-page master GDD. This skill owns **both halves**: the
  **authored one-pager** (premise, pillars, loop stack, win/lose intent, monetization
  stance, non-goals) and the **generated `[gen]` maps** at the bottom (`## System Map
  [gen]` / `## Flow Map [gen]` / `## Funnel [gen]`), which are mechanical read-only
  re-renders of `GD-IDS.yaml`. Both **content edits** to its sections and **structure**
  edits (which systems exist, remap) live here — there is no separate editor skill.
- **`GD-IDS.yaml`** — the machine-truth registry of pillars, systems, flows, and facts,
  **and the interface the code side reads** (`unikit-plan` / `unikit-verify` /
  `unikit-explore`).

Optionally it produces **`PITCH.md`**. Per-system detail (`systems/<slug>.md`) is
**not** this skill's job — that is `unikit-gd-system`; player-action flows
(`flows/<slug>.md`) are `unikit-gd-flow`'s; content types
(`content-types/CT-<slug>.md`) are `unikit-gd-content`'s. This skill remains the
**single writer of the system roster**: a flow's `GOAL → SYS` or a content type's
`belongs_to` that needs a missing system routes back here for add-system.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply it to all output and artifacts (fall back to English if it is missing) —
including the rule to **translate concepts, not transliterate jargon**.
`gd-principles` → "Language" adds the game-design specifics: which IDs and stored
field values stay English. Do not announce or mention the language setting.

**The language holds for the whole session, not just at load time:** every message until the conversation ends is in `language.ui` — progress notes while agents run, relays of what a subagent returned, the final report, any follow-up discussion. English input (subagent results, tool output, these instructions) is data, never a cue to switch languages.

## Bootstrap — Working Contract & Domain Knowledge (MANDATORY)

Before any authoring, silently load — do NOT narrate the loading:

1. **`.unikit/system/gamedesign/gd-principles.md`** — the cross-skill core: the
   zone-ownership model and routing rule, the collaborative protocol
   (Question → Options → Decision → Draft → Approval, Explain → Capture), the
   one-way design→code boundary, the facts-registry / ID conventions, the language
   rules, and the anti-patterns. Plus, from the same `gamedesign/` folder, the
   shards this skill needs: **`gd-authoring.md`** (the section-cycle authoring
   contract + the delta discipline, incl. the **GAME.md carve-out** this skill
   implements) and **`gd-lifecycle.md`** (the lifecycle & status spine).
   **This skill never re-specifies those mechanics — it applies them.**
   If the core file is missing, warn the user that `gd-principles` is not installed
   (`unikit-ai update`) and continue with the protocol summarized above as a fallback.
2. **`.unikit/memory/gamedesign/RULES_INDEX.md`** — the domain knowledge index.
   Load the core rules relevant to master-spec work **on demand** by their
   `Load When` column — most often `frameworks` (MDA, SDT/PENS, Flow),
   `player-motivation` (Quantic Foundry), `core-loops`, and `monetization-ethics`
   (for the Monetization Stance). Re-read at skill start; never rely on a prior
   conversation's cache. Obey the index's **Rule-Loading Discipline**: load by
   `Load When`, load a reference only from its parent rule's `> **References**:`, and
   **never glob the memory tree** (`.unikit/memory/gamedesign/**`) to discover rules.
3. **`.unikit/RULES.md`** (if present) — project overrides, highest priority. **Rule topics:** load the topic files listed under its `## Topics` whose `Load when` matches the design work at hand — the concept, system, flow or content type; when unsure, load.
4. **`.unikit/DESCRIPTION.md`** and **`.unikit/ROADMAP.md`** (optional) — project
   constraints and milestones; routing context only.
5. **Schema guard (clean break — no automatic migration).** When `GD-IDS.yaml`
   already exists it MUST be `version: 2`. If it is still `version: 1`, **STOP** and
   report: the design workspace is on the pre-v2 layout — v2 dropped the standalone
   markdown system-index that v1 kept beside the registry and now renders the maps
   read-only into `GAME.md` (`## System Map [gen]` / `## Flow Map [gen]` / `## Funnel
   [gen]`); there is no automatic migration. Tell the user to bump `GD-IDS.yaml` to
   `version: 2`, fold any rows from the legacy system-index into GAME.md's
   `## System Map [gen]`, and delete that legacy index file before re-running. Create
   mode (no `GD-IDS.yaml` yet) skips this check.

**One-way boundary:** this skill never reads `.unikit/code/`, project source, or
build artifacts. Importing a GDD reads only the document the user points at.

## Input

`$ARGUMENTS` — a single positional value, free-form, in any language. It may be a
**file path** or **URL** to an existing GDD, or a **description / intent**. There
are **no flags**: the mode is inferred (see Step 0). Ambiguity is always resolved
by asking — never by guessing.

## Workflow

### Step 0: Resolve Mode (no flags)

Mode is a function of the **artifact state on disk** and the **intent in the
prompt** (`gd-principles` "never guess" rule). Resolve in this order:

1. **The argument is a file path or URL** (contains `/`, ends in `.md`/`.markdown`,
   exists on disk, or starts with `http`) → **Import** mode. Confirm the target
   with the user if the path is uncertain.
2. The prompt asks for a **pitch** ("pitch", "питч", "one-pager to sell it") →
   **Pitch** mode.
3. The prompt asks to **rebuild / re-derive the system map** ("remap", "rebuild
   the map", "пересобери карту", "re-decompose systems") **and `GAME.md` exists**
   → **Remap** mode.
4. The prompt asks to **add one system** ("add a/new system", "let's add a crafting
   system", "add this to the GDD", "добавь систему", or it names a system **absent
   from the roster**) **and `GAME.md` exists** → **Add-System** mode. This is
   distinct from Remap: Remap re-derives the **whole** map, Add-System grafts **one**
   named system onto the existing map and **never touches the authored one-pager**.
   (It is the route the internal design lens hands a new mechanic to — see
   `references/mode-add-system.md`.)
5. The prompt asks to **change GAME.md content** ("change/rework/tune a pillar, the
   fantasy, a loop, the monetization stance, an anti-pillar, win/lose intent…") **and
   `GAME.md` exists** → **Edit** mode. This is the content-edit zone the spec owns
   (absorbed under zone-ownership: there is no separate `improve` skill). Editing
   GAME.md's *authored* sections is Edit; re-deriving the *roster* is Remap/Add-System.
6. **`GAME.md` does not exist** (check `.unikit/gamedesign/GAME.md`) and no import
   path → **Create** mode.
7. **`GAME.md` exists** and the intent is none of the above → **ambiguous**. Ask:

   ```
   AskUserQuestion: GAME.md already exists. What do you want to do?

   Options:
   1. Edit GAME.md content — change a pillar / fantasy / loop / stance
   2. Rebuild the system map — re-derive the roster from GAME.md
   3. Add one system to the map
   4. Create a pitch (PITCH.md)
   5. Import a different GDD — give me the path/URL
   ```

Announce the resolved mode in one line, then proceed to Step 2 (load the matching mode body).

### Step 1: Ensure the Workspace

Create `.unikit/gamedesign/` (and `systems/`, `flows/`, `concepts/`, `researches/`,
`reviews/` as needed) if missing. Get today's date in `YYYY-MM-DD` (`date +%F`).
If `GD-IDS.yaml` does not yet exist, you will create it from the canonical structure
described below (the `version: 2` registry); never overwrite an existing registry
value silently.

### Step 2: Load the Mode Body

With the mode resolved (Step 0) and the workspace ensured (Step 1), load the matching
mode body on demand and follow it — do **not** keep all six mode bodies in context:

| Mode | Reference body |
|------|----------------|
| **Create** | `{{skills_dir}}/{{self_name}}/references/mode-create.md` (also holds Phase A + Phase B, reused below) |
| **Import** | `{{skills_dir}}/{{self_name}}/references/mode-import.md` |
| **Edit** | `{{skills_dir}}/{{self_name}}/references/mode-edit.md` |
| **Remap** | `{{skills_dir}}/{{self_name}}/references/mode-remap.md` |
| **Add-System** | `{{skills_dir}}/{{self_name}}/references/mode-add-system.md` |
| **Pitch** | `{{skills_dir}}/{{self_name}}/references/mode-pitch.md` |

Import / Remap / Add-System reuse **Phase A / Phase B** from `mode-create.md` — load
that reference too when a body points to it. The shared **Regen-on-Write** contract
(below) and the **Final report** (below) stay here; every mode body returns to them.

---

## Genre Profile — Create Seed

In **Create** mode (and only Create — a fresh `GAME.md` from a concept/dialogue),
this skill **resolves and seeds a genre profile**. The user never types a `genres`
command — the spec drives the CLI (the skill-runs-CLI precedent: `/unikit` Step 9.2
`rules install`). Full mechanics live in `references/mode-create.md` → **Resolve the
genre profile (seed)**; in brief:

1. **Resolve (best-fit).** Read the descriptive `genre:` hint from the seed
   `CONCEPT.md` (a human intent, not a catalog id). Open the catalog with
   `unikit-ai genres list` (its output is authoritative — there is NO genre→id map
   in this skill), and **semantically best-fit** the hint to a profile by
   `name` / `aliases` / `summary` (e.g. «симулятор ломбарда» → `tycoon`). The hint
   may deliberately not equal any id.
2. **Install + record.** Run `unikit-ai genres install <id>` (idempotent — driven by
   this skill, not the user), then write the resolved id into the GAME.md header
   `> **genre_profile**: <id>` (distinct from the descriptive `genre:` intent in
   CONCEPT). Read the installed profile JSON
   (`.unikit/system/gamedesign/genres/<id>.json`).
3. **Seed interview.** Seeds (`seed_systems` / `seed_content_types` /
   `seed_entities` / `seed_resources`) are **proposals**, never auto-written — run a
   subtractive multi-select + add questions, with per-CT `scale`. `confidence` is the
   pre-fill knob (high → pre-check more, low → ask more). Kept seeds apply through the
   existing owner paths: systems → Phase B / spec Add-System; content → **route to
   `/unikit-gd-content` add-CT**; RES/TRACK/KNOB → their zone-owner.
4. **Universal baseline.** No `genre:` hint, no concept, or **no profile fits
   closely** → author WITHOUT a profile (treat as `confidence: low` — ask more,
   assume less), leave `genre_profile:` empty, install nothing.

**The profile is read-only.** Every divergence (a dropped seed, an added field, a
custom CT) lands in **GD-IDS** — the project's custom configuration is GD-IDS (import
from the profile + augment at spec), NEVER an edit to the profile JSON. The genre
layer dissolves into the registry, so **verify stays genre-blind** and only
`unikit-gd-review` reads the profile (its completeness lens).

---

## Regen-on-Write — `## System Map [gen]`

`GAME.md`'s `## System Map [gen]` block is a **mechanical re-render** of `GD-IDS.yaml`
`systems` (the `RULES_INDEX` model) — never hand-authored. `unikit-gd-spec` is its
primary writer: after **any** write that changes the roster or a system's registry
metadata (Create Phase B, Add-System, Remap, and a roster-affecting Edit), re-render
the block as the **last step**:

1. Read `GD-IDS.yaml` `systems`.
2. Group by `category` (omit empty categories); within a group sort by `tier`
   (MVP → Vertical Slice → Alpha → Full Vision) then design order.
3. One row per system: `ID | System | Tier | Status | Ver | Depends | Doc`.
   - `Status` mirrors `doc_status`, **overridden** by `deprecated` (from the
     `status` field) and by the code-set `implemented` (display-only — design never
     authors it; `gd-lifecycle` → Lifecycle & Status). Append the **`· partial (n/m)`
     suffix** when the system's `SYSTEM.md` carries ≥1 `<!-- deferred -->` (the
     canonical render format from `gd-lifecycle` — the **same** suffix
     `unikit-gd-verify` emits, so spec's regen-on-write never drops `· partial` before
     the next verify).
   - `Ver` is `—` until `skeleton`.
   - `Doc` is `systems/SYS-<slug>.md`.
4. Replace **only** the content between `<!-- gen:system-map -->` and
   `<!-- /gen:system-map -->`; never touch the authored one-pager above it. Full
   map (one row per system); collapse to a single grouped table only as an escape
   hatch for very large rosters (150+).

The `## Flow Map [gen]` / `## Funnel [gen]` blocks (rendered by `unikit-gd-flow`, the
Flow axis) and the `## Content Map [gen]` block (rendered by `unikit-gd-content`, the
Content axis) are **out of this skill's scope** — leave their template scaffold
untouched; this skill renders only `## System Map [gen]`. `unikit-gd-verify`
independently re-renders a stale `[gen]` block when its freshness check trips
(`gd-lifecycle` → Lifecycle & Status) — the render is deterministic, so all writers
always agree.

---

## Final: Compact Report & Next Steps

After artifacts are written, show a compact report (TIER A — `gd-principles` →
Language: names lead, ids are parenthetical copy-paste tags, status is a plain phrase;
no summary document, no report file):

```
Mode: <create | import | edit | remap | add-system | pitch>
Workspace: .unikit/gamedesign/
Written:
- GAME.md (vN — <still a draft | approved>) — incl. ## System Map [gen] re-rendered
- GD-IDS.yaml (<P> pillars, <N> systems)
- [SOURCE.md / PITCH.md when applicable]

System map: <N> systems — <M> MVP, … ; design order: <name> (SYS-<slug>), <name> (SYS-<slug>), …
```

Then recommend the next step (do not auto-invoke):

- 🧩 Detail the first MVP system — /unikit-gd-system <SYS-slug>
- 🔍 Review the master spec (fresh session) — /unikit-gd-review

## Ownership Boundaries

- **Owns:** all of `GAME.md` — the **authored one-pager** (its **content edits** under
  the GAME.md carve-out **and** its **structure**: which systems exist, remap) **and**
  its generated `## System Map [gen]` block (the primary regenerator). Owns the system
  roster (Create + Import Phase B, Add-System, Remap) and `GD-IDS.yaml`
  pillars + systems; optional `PITCH.md`; import `SOURCE.md`. Owns the `GD-IDS`
  `research:` pointer (written in Add-System when seeded from an explore brief) —
  `unikit-gd-explore` never writes it. Owns the **genre-profile resolve** (Create
  seed): best-fit the CONCEPT `genre:` hint to a profile, drive `unikit-ai genres
  install <id>`, and write the resolved `> **genre_profile**:` id into GAME.md (the
  user never types a `genres` command; the profile is read-only — divergence → GD-IDS).
- **Not this skill:** per-system GDDs (`systems/<slug>.md`) → `unikit-gd-system`;
  player-action flows (`flows/<slug>.md`) and the `## Flow Map [gen]` / `## Funnel
  [gen]` renders → `unikit-gd-flow`; content types (`content-types/CT-<slug>.md`) and
  the `## Content Map [gen]` render → `unikit-gd-content` (a content type registers
  itself — there is no add-content here); ideation / concepts →
  `unikit-gd-brainstorm`; research briefs → `unikit-gd-explore`.
- **Never:** write without explicit approval; change a `GD-IDS.yaml` value
  silently; delete or renumber an ID; read the code workspace or project source.

## Quick Reference

```
/unikit-gd-spec <description>            → create GAME.md (one-pager + maps) + GD-IDS.yaml
/unikit-gd-spec ./path/to/GDD.md         → import an existing GDD (extract, keep SOURCE.md)
/unikit-gd-spec https://…                → import from a URL
/unikit-gd-spec change PIL-2's design test → edit GAME.md content (GAME.md carve-out)
/unikit-gd-spec remap the systems        → re-derive the map (GAME.md must exist)
/unikit-gd-spec add a crafting system    → add-system: graft one system onto the map → seam to detail
/unikit-gd-spec pitch this game          → produce PITCH.md
```
