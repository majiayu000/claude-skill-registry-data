---
name: unikit-gd-verify
description: >-
  Mechanical consistency check for game design — answers "is the design consistent with
  itself?" — plus changed-scope impact analysis across all three GDD axes: systems, flows,
  and content types. Offline and deterministic: greps the facts registry against the
  documents (numbers, terms, IDs, duplicate & dangling references, roster↔disk, map
  freshness, Depends 3-way, status/version, AC presence, placeholder leaks, flow & content
  schema), and from a git diff computes which dependent systems, flows, and content a change
  affects. Scope is inferred: a named document checks that document; an unverified diff
  triggers a changed-scope pass; otherwise everything. Use when the user wants a consistency
  or impact check, e.g. "verify the design", "what did this change affect", "find broken
  references in the design". Conflicts triage into four tracks; the entailed fixes hand off
  to /unikit-gd-apply in one pass. This is the mechanical pass — for a subjective "is this
  design good" quality critique use /unikit-gd-review.
argument-hint: "[system name | SYS-slug | question]  (scope inferred; no flags)"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(ls *)
  - Bash(find *)
  - Bash(wc *)
  - Bash(date *)
  - Bash(git diff *)
  - Bash(git status *)
  - AskUserQuestion
disable-model-invocation: false
user-invocable: true
metadata:
  author: unikit
  version: "1.0"
  category: game-design
---

# Game Design — Consistency & Impact Verification

Answer **"is the design consistent with itself?"** — a mechanical, deterministic
check of every document against the facts registry, plus the **changed-scope
impact** of a recent edit. This is the design-side mirror of `unikit-verify` and a
CI-linter to `unikit-gd-review`'s senior reviewer: cheap, binary, run after every
edit. A **verify conflict cannot be declined** (unlike a review finding) — it is
resolved.

**`unikit-gd-verify` is fully read-only — it writes nothing** (no report file, no
changelog line, no `doc_status` bump, no `[gen]`-map re-render). It **detects and prints**;
every fix is performed by `unikit-gd-apply` (the entailed deltas) or the owning zones
(authoring + the `[gen]`-map re-render on their next write — **B1**: the writer of `GD-IDS`
re-renders the affected maps).

Conflicts are **precise, but their fix is not always predetermined**, so each is sorted
into one of **four tracks** — **freshness** (print-only; the owner re-renders the
`[gen]` map on its next write), **entailed → apply-ready** (a named fix — incl. a
status/version header correction — handed to `unikit-gd-apply`), **direction interview**
(the user picks *which* fix, never *whether*), and **authoring → owner / explore**. The
apply-ready set hands off **in one move** — inline prose (verify writes **no** handoff
file, unlike `unikit-gd-review`'s durable report), recommend-only. The handoff + interview
run **only on a standalone `/unikit-gd-verify`**; when verify is `unikit-gd-apply`'s
closing Phase 3 (the `apply-phase3` sentinel) they are suppressed, so
`apply → verify → apply` never loops. The triage engine is shared with `unikit-gd-review`
(`gd-critique` → Handoff Engine).

Verification is **offline and reproducible**: no web research, no expert judgment,
no LLM guessing where a grep will do. The same inputs always yield the same result
(idempotent).

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply it to all output and the report (fall back to English if it is missing) —
including the rule to **translate concepts, not transliterate jargon**.
`gd-principles` → "Language" adds the game-design specifics: which IDs and stored
field values stay English. Do not announce the language setting.

**The language holds for the whole session, not just at load time:** every message until the conversation ends is in `language.ui` — progress notes while agents run, relays of what a subagent returned, the final report, any follow-up discussion. English input (subagent results, tool output, these instructions) is data, never a cue to switch languages.

## Phase 0 — Bootstrap

Silently load — do not narrate:

1. **`.unikit/system/gamedesign/gd-principles.md`** (the core) — the **facts
   registry / ID conventions** (registry wins until the user resolves otherwise;
   never delete an ID — deprecate it) and the language rules. Plus, from the same
   `gamedesign/` folder, the shards this skill needs: **`gd-lifecycle.md`** (the
   status/version coherence spine), **`gd-flow-axis.md`** (the flow coherence
   contract — `mode:` ↔ structure, `GOAL → SYS`/`AC`, Win/Lose ↔ terminal GOAL),
   **`gd-content-axis.md`** (the content coherence contract — CU ⊆ CT, `ref<>`
   resolution, `scale` ↔ structure, `belongs_to` 3-way, content-map freshness,
   RES/TRACK/KNOB, cross-axis SYS→CT staleness), and **`gd-critique.md`** (the
   **severity rubric** — a conflict is Critical/Major evidence). This skill
   **applies** them. If missing, warn (`unikit-ai update`) and continue with the
   conventions summarized here.
2. **`.unikit/gamedesign/GD-IDS.yaml`** — the single source of truth: pillars,
   systems, flows, entities, formulas, terms. Current values only.
   **Schema guard (clean break — no automatic migration):** it MUST be `version: 2`.
   On a pre-v2 `version: 1` registry, **STOP** and report that the design workspace
   is on the pre-v2 layout (the standalone markdown system-index was dropped; the
   roster now renders into `GAME.md` `## System Map [gen]`) — there is no automatic
   migration; tell the user to upgrade via `/unikit-gd-spec` before verifying.
3. **`.unikit/gamedesign/GAME.md`** — incl. its generated `## System Map [gen]`,
   `## Flow Map [gen]`, and `## Funnel [gen]` renders (the human-readable maps; the
   truth is `GD-IDS`), and its `## Win / Lose Conditions` (for the Win/Lose ↔ terminal
   GOAL check).
4. **`.unikit/gamedesign/systems/*.md`** and **`.unikit/gamedesign/flows/*.md`** — the
   system and flow documents checked against the registry.

**One-way boundary:** never read `.unikit/code/`, project source, or build
artifacts. **Web research is forbidden here** (`gd-principles`) — verification must
stay deterministic. The only `git` use is reading the design-workspace diff.

## Phase 1 — Resolve Scope (no flags)

**Loop-guard sentinel (first).** If the argument is exactly **`apply-phase3`** — the
reserved loop-guard sentinel (`gd-critique` → Handoff Engine), passed by
`unikit-gd-apply` as its closing Phase 3 — this run is the **in-apply gate**, **not** a
scope. Treat it as a bare invocation for scope purposes (derive changed-scope from the
`git diff` exactly as below), but set the **in-apply flag**: the standalone handoff offer
and the direction interview (Phase 4 Track 3 / Phase 6) are **suppressed** this run, so
`apply → verify → apply` cannot loop. A standalone `/unikit-gd-verify` (no sentinel)
leaves the flag off — the handoff is active.

Scope is a function of context:

1. The argument names a system, flow **or content type** → check **that document** and
   its registry facts (a `FLOW-<slug>` runs the flow checks, a `CT-<slug>` the content
   checks below).
2. There is an **unverified diff** under `.unikit/gamedesign/` (`git diff` /
   `git status` shows changed design docs), or the prompt asks "what did this
   change affect" → **changed-scope** pass (Phase 3).
3. Otherwise → **full** check of every system, **every flow**, **every content type**,
   and the whole registry.

Announce the resolved scope in one line.

## Phase 2 — Mechanical Checks (grep-first)

Run every check deterministically; each mismatch is a **CONFLICT** with a citation:

| Check | Method | Conflict when |
|-------|--------|---------------|
| **Facts** | grep each `GD-IDS` entity/formula value across the docs — match the value on word boundaries, not as a bare substring | a document states a number/name that disagrees with the registry |
| **Terminology drift** | grep each term's `forbidden_aliases` **values** (the listed aliases, not the field name) across the docs | a forbidden alias is used in place of the canonical term |
| **ID validity** | scan every `SYS-`/`ENT-`/`FORM-`/`AC-`/`PIL-`/`FLOW-`/`GOAL-` id for shape (analytics `events` are `snake_case` tokens, not prefixed ids) | an id is malformed — wrong case, bad separator, or an unknown prefix |
| **Duplicate IDs** | group every declared id by value | the same id is declared for two different things |
| **Dangling references** | resolve every referenced id against `GD-IDS` | a referenced id does not exist, or a live (non-deprecated) section points at a `deprecated` entry |
| **Unregistered cross-doc fact** | grep `FORM-`/`ENT-` ids that surface in **two or more** documents | a fact crosses a document boundary yet has no `GD-IDS` entry |
| **Roster ↔ disk** | compare `GD-IDS` `systems` ids to the `systems/*.md` files on disk | a `skeleton`-or-later system has no file, or a `systems/*.md` file has no `GD-IDS` entry (→ route to `unikit-gd-spec` to register it — verify never writes the roster) |
| **Map freshness (3-surface)** | compare the `GAME.md` `## System Map [gen]` rows to `GD-IDS` `systems` — membership, `Status`, `Ver`, `Depends` | the render disagrees with `GD-IDS` — **not a conflict to resolve**: **print** a freshness notice; the owning zone re-renders the block on its next write (verify is read-only — B1); see *Map freshness* below |
| **Depends 3-way** | for each `A → B` edge, check it agrees across A's section F, A's `GD-IDS` `depends_on`, and A's `## System Map` Depends cell, and that B carries the reciprocal | the three sources disagree, or the reciprocal edge is missing or contradictory |
| **Status coherence** | a system's `doc_status` agrees across the **two places that must agree** — the header `> Status:` and `GD-IDS` `doc_status` (enum `not-started · skeleton · detailed`) | the two disagree for a system — system docs only; see the carve-outs below |
| **Version coherence** | the header `Version` and `GD-IDS` `version` agree; a `not-started` system carries **no** version, a `skeleton`-or-later system carries one | the two disagree, or a `skeleton`+ system is missing a version / a `not-started` system has one |
| **AC presence** | for a `detailed`-or-later system, section H is non-empty and every `AC-<sys>-N` id is unique | a `detailed`+ system has an empty H, or repeats an `AC-<sys>-N` — gaps in the numbering are **not** a conflict (numbering is stable after an AC is removed) |
| **Placeholder leak** | grep `[To be designed]` inside `detailed`-or-later documents (a `<!-- deferred -->` marker is **intentional** — never a leak) | a `detailed`+ document still carries a skeleton `[To be designed]` placeholder |
| **Core-floor coherence** | for a `detailed` document, check that **no core section carries `<!-- deferred -->`** — the core-set per zone (`gd-lifecycle`: system `A/B/C/D/H` · flow `A/B` · content `A/B/C`) | a `detailed`+ document defers a **core** section — the status was raised past the floor (the soft guard in `gd-authoring` was bypassed); route to the owning zone to author the core section or lower the status. A deferred **non-core** section is **not** a conflict (it is the inferred `detailed · partial` — see the render below) |

The registry is authoritative: when a document disagrees with `GD-IDS`, the
registry wins until the user resolves it the other way (`gd-principles`).

**Map freshness — print-only, not a conflict.** The `## System Map [gen]` block in
`GAME.md` is a deterministic **render** of `GD-IDS` `systems` (`gd-lifecycle` →
Lifecycle & Status), so a disagreement is a *freshness* issue, never a coherence
conflict to resolve. On any of —

- a `GD-IDS` system **missing from the map** (no row);
- a **phantom row** in the map with no matching `GD-IDS` system;
- a row whose **Status / Ver / Depends** differs from `GD-IDS`,

— **print** a freshness notice naming the stale rows (`## System Map [gen] stale —
<rows>; owner re-renders on next write`). verify is **read-only**: it does **not**
re-render the map. The owning zone re-renders on its next write — **B1**: the writer of
`GD-IDS` (`unikit-gd-spec` for the System Map, `unikit-gd-flow` / `unikit-gd-content` for
theirs) re-renders the affected `[gen]` block with the same deterministic render (group
by category, sort by tier then design order, display-precedence on
`deprecated`/`implemented`). A `systems/*.md` file with **no `GD-IDS` entry** (the
Roster ↔ disk check) is likewise **routed**: the roster is `unikit-gd-spec`'s to write,
so verify routes the user to `/unikit-gd-spec` to register the system.

**Deferred markers, the `· partial (n/m)` render, and the self-check (all three maps).**
A `<!-- deferred -->` marker is an **intentional** omission (`gd-lifecycle` — a section
the author chose to skip at this depth), **never** a placeholder leak. Its only
mechanical consequence at verify time is the **render**: a `detailed`+ document carrying
≥1 `<!-- deferred -->` should show **`· partial (n/m)`** appended to its row Status in the
relevant `## *Map [gen]`, where **n = the count of deferred non-core sections** (those
carrying the marker) and **m = the document's total deferrable (non-core) sections**
(`gd-lifecycle` → the canonical render format + per-zone core-set). This applies
identically to the **System, Flow, and Content** maps; like all freshness it is
**print-only, not a coherence conflict** — verify does **not** re-render (the owner
appends the suffix on its next re-render), and the status value itself stays the read-only
enum (`· partial` is a render annotation, not a `doc_status`, and is **not** part of the
two-place status/version coherence). **Self-check (marker ⟺ render):** every document with
≥1 `<!-- deferred -->` must render `· partial (n/m)` in its map row, **and** every
`· partial` suffix in a map must correspond to a document that actually carries the
marker — a mismatch in either direction is a **freshness** discrepancy, **printed** (the
owner fixes it on re-render). Annotate the freshness notice with the count, e.g.
`## System Map [gen] stale (partial 2/5 on SYS-combat); owner re-renders`.

**Scope & carve-outs (Status / Version / AC / Placeholder).** These four checks
read the **system** spine only — the header ↔ `GD-IDS` pair of a `systems/*.md`
document (the `## System Map [gen]` render is *not* a coherence surface — its
agreement is handled by *Map freshness* above):

- **Lifecycle-enum scope.** `GAME.md` (`drafted | approved`) and `CONCEPT.md`
  (`exploring | drafted | approved`) keep their **own** lifecycle enums — a
  `Status: approved` there is correct and is **never** a status conflict.
- **Display precedence.** A system with `status: deprecated` legitimately shows
  `deprecated` in the `## System Map [gen]` Status over its underlying `doc_status`;
  the read-only `implemented` value (a code-set display overlay) behaves the same.
  Both are display overlays in the **render** — never part of the two-place header ↔
  `GD-IDS` `doc_status` comparison. The companion **`GD-IDS` `implemented_version`**
  field (also code-set, by `unikit-verify` on all-AC-met) is a code-owned field —
  **not** a `doc_status` and **not** a `version` — so it never participates in Status
  or Version coherence and is never flagged as drift.
- **Non-id metadata (`research:`).** The `GD-IDS` `research:` field — a **path pointer**
  to the explore research that seeded an artifact (written by `unikit-gd-spec`
  add-system on a **system** row, by `unikit-gd-flow` on a **flow** `flows[]` row, and by
  `unikit-gd-content` on a **content type** `content_types[]` row) — is non-semantic
  metadata, **not** a registry id and **not** a `doc_status` / `version`. It is excluded
  from status/version coherence on all three axes, and the id-resolving checks pass it
  over **by construction**: **Dangling references** only resolves id tokens
  (`SYS-`/`ENT-`/`FORM-`/`AC-`/`PIL-`/`FLOW-`/`GOAL-`/`CT-`/`CU-`), and **Unregistered
  cross-doc fact** only greps `FORM-`/`ENT-` ids — a folder path matches neither — so no
  special-case logic is needed.

### Axis-aware checks — flow + content (load on demand)

Beyond the system checks above, the registry may carry **flows** and **content
types**, each with its own check family — the mirror of the system checks plus the
axis-specific ones. When `GD-IDS` `flows` and/or `content_types` is **non-empty**, load
the matching family from `{{skills_dir}}/{{self_name}}/references/axis-checks.md` and run
it; an empty `flows: []` / `content_types: []` (or no key) → **skip that family
silently** (not a conflict). The registry-wins rule and the freshness-vs-conflict
distinction apply exactly as above — freshness is **print-only** (the owner re-renders).

| Registry has | Family (in `references/axis-checks.md`) — coverage |
|--------------|----------------------------------------------------|
| `flows` non-empty | the **flow** family: GOAL-id validity, dangling goal-targets, flow status/version 2-place, flow Depends 3-way, wiring-mode-vs-structure, win/lose-vs-terminal-goal, funnel continuity, flow/funnel map freshness (`Realized` cross-axis derived) |
| `content_types` non-empty | the **content** family: CT/CU-id validity, CU-fields-subset-CT, ref-target resolution, scale-vs-structure, belongs-to 3-way, content status/version 2-place, content map freshness, RES/TRACK/KNOB fact coherence |

The **cross-axis impact** of a system edit on dependent flows / content types is the
reverse-edge walk in **Phase 3** (it stays here — it is impact analysis, not a per-axis
check).

## Phase 3 — Changed-Scope Impact (when a diff is unverified)

Compute the blast radius of a recent edit:

1. **Changed set** = `git diff HEAD` (and `git status`) restricted to
   `.unikit/gamedesign/` → the systems whose documents changed on disk. (There is no
   stored "pending re-verify" state to re-scan — status records readiness only; a change
   is carried by the git diff + version, not by a `doc_status`.)
2. Walk `GD-IDS` `depends_on` edges (rendered in the `## System Map` Depends column)
   to the **transitive closure** of systems that depend (directly or indirectly) on
   a changed one.
3. Classify each affected system into an **Affected** table:

   | System / Flow | Relation | Verdict |
   |---------------|----------|---------|
   | SYS-enemy-ai | depends on SYS-combat (changed) | **Needs Review** |
   | SYS-economy | soft dep, no touched interface | **Still Valid** |
   | SYS-loot | uses a removed AC | **Likely Stale** |
   | FLOW-first-session | exercises SYS-combat (changed) via GOAL→AC | **Needs Review** |

   Verdicts: **Still Valid** / **Needs Review** / **Likely Stale**.
4. **Print the impact** (verify writes nothing):
   - **Print the Affected table** to the console — the changed system + every dependent
     with its verdict. verify does **not** write the `Affected (gd-verify):` line into
     section K (it is read-only); the owner records that line on its next authoring touch
     if it acts on the impact (`gd-authoring` → Delta Discipline).
   - For each affected **dependent** with a `Needs Review` / `Likely Stale` verdict,
     **recommend** a re-author pass to its owner — verify does **not** bump any
     `doc_status` (status records readiness only; a re-author bumps `Ver`, not status).
   - **Idempotent:** re-running on the same diff yields the same Affected table — there is
     no state to mutate.

**Cross-axis impact (system → flow, one-way).** A system edit can stale a **flow** that
exercises it (through `GOAL → SYS` / `GOAL → AC`) — `gd-flow-axis` → Flow Axis. Extend
the pass across the axis (skip when `flows: []`):

- **Reverse-edge walk:** for each changed **system**, find every flow whose
  `flows[].depends_on` includes it, or whose `goals[].targets` reference it
  (`GOAL → SYS` / `GOAL → AC`). Those flows join the **Affected** table as **flow rows**
  (Relation: `exercises SYS-x (changed)`), with the same Still Valid / Needs Review /
  Likely Stale verdicts (a flow using a **removed** `AC` is Likely Stale). The reverse
  does **not** hold — editing a flow never stales a system.
- **Print impact (dependent flow):** list affected flows in the printed Affected table.
  For each `Needs Review` / `Likely Stale` dependent flow, **recommend** a re-author pass
  to `unikit-gd-flow` — verify writes **nothing** (no `doc_status` bump, no `FLOW.md`
  header write, no section-F note, no `## Flow Map [gen]` re-render). Acting on the
  recommendation (the `Ver+1` + changelog touch) is the owner's call.

**Cross-axis impact (system → content type, one-way).** A system edit can stale a
**content type** that feeds it (through `belongs_to` / a `ref<SYS>` field) —
`gd-content-axis` → Content Axis. Extend the pass across the axis (skip when
`content_types: []`):

- **Reverse-edge walk:** for each changed **system**, find every content type whose
  `content_types[].belongs_to` names it, or whose `CT.fields` carry a `ref<SYS>` to it.
  Those types join the **Affected** table as **content rows** (Relation: `feeds SYS-x
  (changed)`), with the same Still Valid / Needs Review / Likely Stale verdicts (a type
  whose consuming system removed a relied-on contract is Likely Stale). The reverse does
  **not** hold — editing a content type never stales a system.
- **Print impact (dependent CT):** list affected types in the printed Affected table.
  For each `Needs Review` / `Likely Stale` dependent type, **recommend** a re-author pass
  to `unikit-gd-content` — verify writes **nothing** (no `doc_status` bump, no
  `CONTENT-TYPE.md` header write, no section-F note, no `## Content Map [gen]`
  re-render). Acting on the recommendation is the owner's call.

## Phase 4 — Triage Conflicts (4 tracks)

A verify conflict is **precise** (the grep found a real disagreement) but its **fix is
not always predetermined**, and it can **never be declined** — only resolved or routed.
Using the shared **handoff engine** (`gd-critique` → Handoff Engine), sort every conflict
into one of **four tracks**:

1. **Freshness — print-only** — verify is read-only, so it **prints**, never fixes. The
   `[gen]`-map **freshness** (Phase 2) is announced as a stale-rows notice; the owning zone
   re-renders on its next write (**B1**). A status / version header ↔ `GD-IDS` disagreement
   (where `GD-IDS` is the machine truth) is **not** healed here — its correction (set the
   header to `GD-IDS`) is a clean entailed fix and goes to Track 2.

2. **Entailed → apply-ready** — the conflict's fix passes the silent **ENTAILED** criterion
   (one concrete target · the correct value already authoritative in `GD-IDS` · exactly one
   local fix · no external knowledge) but needs an **owner write** verify cannot make
   (verify writes nothing): a **status / version header** to correct to `GD-IDS`, a
   **duplicate id** to renumber, a **terminology drift** to swap to the canonical term, a
   **dangling reference** to repoint. Put it in the **apply-ready** set — the named fix
   handed to `unikit-gd-apply` (Phase 6) as a prose delta, authored by the owner, not here.

3. **Direction fork → interview** — the conflict admits **more than one valid direction**:
   a **value conflict** (the document or the registry could each be right), a **dangling
   `GOAL → SYS` / `AC`** fixable three ways across three zones, a **roster ↔ disk** mismatch
   (register vs delete), an **unregistered cross-doc `FORM-`/`ENT-`** (register vs remove).
   The user picks the **direction** — never *whether* to act (decline-vs-direction,
   `gd-critique`). The interview is **direction-only** and batched (`AskUserQuestion`, ≤ 4
   per call); it is **suppressed under the in-apply flag** (Phase 1 sentinel):

   ```
   AskUserQuestion: CONFLICT — <doc/section> vs GD-IDS: <the disagreement>. Which direction?
   Options:
   1. Fix as A — e.g. registry is right → correct the document
   2. Fix as B — e.g. document is right → update GD-IDS to <X> (with approval; record it)
   3. This is authoring / needs a decision → route to the owner or /unikit-gd-explore
   ```

   There is **no "Decline"** — a consistency conflict is a fact, not an opinion. A chosen
   A/B that is a clean local edit becomes an **apply-ready** prose delta (it joins Track 2);
   option 3 routes it to Track 4.

4. **Authoring → owner / explore** — the conflict needs **authoring**, not a mechanical
   fix: an **empty section H** / **missing AC**, a **placeholder leak** in a `detailed`+
   document, a **core section deferred past the floor**. It is neither entailed nor a
   direction pick — route it to the owning zone (`unikit-gd-system` / `unikit-gd-flow` /
   `unikit-gd-content` / `unikit-gd-spec`), or to `/unikit-gd-explore` when it needs a
   design decision first.

verify never writes the registry — it is read-only; the registry-wins rule still governs
the **direction** of a fix (apply / the owner sets the document to match `GD-IDS`), and a
deprecated ID is never deleted. Log every conflict + its track + resolution in the printed
report (Phase 5). The coherence-vs-presence split still holds underneath: a **coherence**
conflict (status / version / Depends 3-way, where `GD-IDS` is authoritative) is now
**Track 2** (entailed → apply-ready — the header corrected to `GD-IDS`), and the
`[gen]`-map **freshness** is **Track 1** (print-only); a **presence** conflict (empty H,
duplicate id, placeholder leak, unregistered cross-doc fact) is Track 2 (entailed →
apply-ready) or Track 4 (authoring), resolved by editing the document, never the registry.

## Phase 5 — Report (printed to the console)

**verify is read-only — the report is printed to the console, never written to a file.**
A clean full PASS is a single chat line. On `CONFLICTS FOUND` or a changed-scope pass,
print the full report block:

```markdown
# Verify: <scope> — <YYYY-MM-DD>
> Result: <PASS | CONFLICTS FOUND>  ·  Scope: <SYS-slug | changed | all>

## Conflicts
| Severity | Document / Section | Check | Conflict (evidence) | Recommended fix |
|----------|--------------------|-------|---------------------|-----------------|

## Affected (changed-scope only)
| System / Flow | Relation | Verdict |
|---------------|----------|---------|

## Freshness
<[gen]-map rows stale → owner re-renders on next write (B1), or "up to date">
```

This is **printed**, not a file — a verify pass is ephemeral and cheap to re-run (the
single-session verify → apply pair is by design: a `/clear` between them is fixed by
re-running verify). The asymmetry with `unikit-gd-review` (which leaves a durable
two-bucket report) is intentional. When the same conflict recurs across systems, record it
as a `gamedesign` `library` rule via `/unikit-memory --module gamedesign` — durable domain
knowledge, not re-discovered each pass.

## Phase 6 — Handoff (standalone only; inline prose, recommend-only)

> **LOOP-GUARD.** This phase runs **only on a standalone `/unikit-gd-verify`**. Under the
> **in-apply flag** (the `apply-phase3` sentinel resolved in Phase 1), **skip this phase
> entirely** — verify prints freshness (Track 1) and the report (Phase 5), but never offers
> a handoff back to `unikit-gd-apply`. That is the silent gate that stops
> `apply → verify → apply` from looping.

When Tracks 2 and 3 produced **apply-ready deltas** (the entailed fixes + the
direction-resolved edits), hand them to `unikit-gd-apply` **in one move** rather than
routing each conflict into an owner skill by hand. verify's handoff is **inline prose from
this session** — it writes **no** file (Phase 5): verify **prints the deltas as plain
prose** (each citing its `target` + `zone`), then ends with a **bare `/unikit-gd-apply`**.
A bare `/unikit-gd-apply` (no argument, no fence) reads the deltas from the **last verify
output in the session** — apply's no-arg session mode.

**Hand off — recommend-only (never a `Skill` call).** Neither `unikit-gd-review` nor
`unikit-gd-verify` carries `Skill` in `allowed-tools`; each **prints** the
`/unikit-gd-apply` recommendation for the user to run, and on Codex the auto-invoke nudge
runs it — the two handoff tails are identical by contract.

<!-- unikit:agents codex -->
### Auto-invoke the handoff — BLOCKING PRE-REQUISITE

When this phase prints the `/unikit-gd-apply` recommendation, automatically invoke it
(`$unikit-gd-apply`, bare — it reads the printed deltas from this session) rather than
asking the user to run it by hand — the printed command is the recommend-only fallback for
agents without auto-invocation. This is a single handoff: invoke `unikit-gd-apply` once and
let it route the deltas to the owners (it closes with its own `apply-phase3` verify — no
loop).
<!-- unikit:end -->

- **apply-ready non-empty:** print the deltas as plain prose (each citing `target` +
  `zone`), then the bare command on its own line —
  ```
  /unikit-gd-apply
  ```
  `unikit-gd-apply` reads the printed deltas from the session (no file, no argument —
  verify writes none), dispatches them to the owning zones, and closes with its own
  `apply-phase3` verify pass. A single-zone set is bounced to its owner by apply's GATE 2.
- **apply-ready empty** (only freshness + authoring / research routes): **no apply
  handoff** — list the Track-4 routes instead (`/unikit-gd-system` / `/unikit-gd-flow` /
  `/unikit-gd-content` / `/unikit-gd-spec`, or `/unikit-gd-explore` for the ones needing a
  design decision).

## Final: Compact Report

Follow the **Handoff Tail contract** (`gd-critique` → Handoff Engine): the runnable
command is the **last block** on screen — the report and any route note go above it,
nothing prints after it. Under the `apply-phase3` sentinel the handoff is
**suppressed**, so there is no command tail (the loop-guard).

Print the compact report:

```
Scope: <SYS-slug | changed | all>
Result: <PASS | CONFLICTS FOUND (<n>)>
Checks: facts · terms · IDs · dup-IDs · dangling · unregistered-fact · roster↔disk · map-freshness · Depends-3way · status · version · AC-presence · placeholder · core-floor — <pass/fail each>
Flow checks (when flows exist): GOAL-ids · dangling-GOAL · flow-status/version · flow-Depends-3way · mode↔structure · win/lose↔terminal-GOAL · funnel-continuity · flow/funnel-freshness — <pass/fail each>
Content checks (when content_types exist): CT/CU-ids · CU⊆CT · ref<>-resolve · scale↔structure · belongs_to-3way · content-status/version · content-map-freshness · RES/TRACK/KNOB · cross-axis SYS→CT — <pass/fail each>
Affected (changed-scope): <k systems + flows + content types — Needs Review: …, Likely Stale: …>
Freshness: <## System Map [gen] stale — <rows> (· partial n/m where deferred); owner re-renders | up to date>
Tracks: <apply-ready: N · direction-interview: N · authoring/explore: N>
Handoff: <printed deltas + bare /unikit-gd-apply | apply-ready empty → routes only | in-apply (apply-phase3) → suppressed>
Report: <printed to console | none (clean PASS)>
```

The actionable routes when apply-ready is empty live in the `Tracks` line above —
read them there. No summary document beyond the conditional report file.

**Then end with the handoff as the LAST block** — one command, nothing after it:

- **apply-ready non-empty** → printed deltas (each citing `target` + `zone`), then
  `🛠️ /unikit-gd-apply` (bare — apply reads them from the session)
- **apply-ready empty, a conflict needs a design call** → `🔎 /unikit-gd-explore`
- **apply-ready empty, authoring only** → the matching owner: `🔧 /unikit-gd-system`
  / `/unikit-gd-flow` / `/unikit-gd-content` / `/unikit-gd-spec`
- **clean PASS** → `🔍 /unikit-gd-review <system>` (fresh session)
- **in-apply (`apply-phase3`)** → suppressed — no command tail.

Nothing prints after the command — no recap, no description of what the called
skill does next.

## Ownership Boundaries

- **Owns:** nothing on disk — `unikit-gd-verify` is **fully read-only**. It produces a
  **console** conflict report + Affected table, and **prints** freshness / coherence
  recommendations; every fix is performed by `unikit-gd-apply` (the apply-ready deltas) or
  the owning zones (authoring + the `[gen]`-map re-render on their next write — **B1**: the
  writer of `GD-IDS` re-renders the affected maps).
- **Read-only:** every design document, `GD-IDS.yaml`, and `GAME.md` (incl. all
  `[gen]`-map blocks) — verify writes none of them.
- **Not this skill:** quality judgment → `unikit-gd-review`; applying the apply-ready set
  in one pass → `unikit-gd-apply` (the handoff is **recommend-only** — verify prints the
  command, never invokes it); authoring → `unikit-gd-system` (systems) / `unikit-gd-flow`
  (flows) / `unikit-gd-content` (content types) / `unikit-gd-spec` (`GAME.md` + the roster);
  a conflict needing a design decision → `unikit-gd-explore`.
- **Never:** write **any** file (no report file, no `Affected (gd-verify):` line, no
  `doc_status` bump, no `[gen]`-map re-render — verify carries no `Write`/`Edit`/`mkdir`);
  use web research; guess where a grep settles it; change a `GD-IDS` value; delete or
  renumber an ID; write the roster (route to `unikit-gd-spec`); carry `Skill`/`Agent` in
  `allowed-tools` or invoke `unikit-gd-apply` itself (the handoff is a printed prose
  recommendation read by apply's no-arg session mode); offer the handoff or run the
  direction interview when invoked as apply's Phase 3 (the `apply-phase3` loop-guard); read
  the code workspace or project source.

## Quick Reference

```
/unikit-gd-verify SYS-combat        → check one system → triage conflicts (4 tracks) → handoff apply-ready to /unikit-gd-apply
/unikit-gd-verify                   → unverified diff → changed-scope impact; else full check
/unikit-gd-verify what did that change affect  → changed-scope impact from git diff
/unikit-gd-verify all               → full registry + roster + map-freshness + Depends pass
# internal: /unikit-gd-apply passes apply-phase3 as its Phase 3 — verify suppresses the handoff/interview (loop-guard)
```
