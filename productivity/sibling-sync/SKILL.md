---
name: sibling-sync
description: "Bilateral SYNERGY/UPSTREAM reconciliation across sibling projects. Use when the user wants to sync sibling SYNERGY/UPSTREAM files, compare both sides to surface drift, find reciprocation gaps (entries here but not there, or vice versa), flag stale-aligned rows, detect status drift across sides, surface friction the sibling tracks ABOUT this project (their UPSTREAM-<this-project>.md), or apply a reciprocation batch with --auto-reciprocate. Workflow 3 covers two UPSTREAM pairing modes: shared third-party dependencies AND reciprocal sibling-friction pairs (UPSTREAM-<sibling>.md here ↔ UPSTREAM-<this-project>.md there). NOT for logging entries on this side (use /synergy-tracker workflow 1 (Log a synergy entry)) — sibling-sync compares both sides without writing by default. NOT for upstream → project drift (use /vendor-sync); sibling-sync handles peer-to-peer drift between sibling vp-* projects. Trigger phrases: 'sibling sync', 'compare siblings', 'sync sibling', 'reconcile siblings', 'reciprocation gap', 'sync drift', 'bilateral sync', 'sync SYNERGY', 'sync UPSTREAM both ways', 'auto-reciprocate', 'check sibling drift', 'peer-to-peer drift', 'cross-project drift', 'sibling reconciliation', 'sibling has friction about us', 'what does the sibling say about us', 'reconcile sibling-tracked friction', 'reciprocal upstream friction', 'friction filed against this project', 'sibling follow-up', 'act on sibling drift', 'after sibling-sync', 'follow-up actions', 'what to do about sibling findings'."
user-invocable: true
argument-hint: "[--auto-reciprocate] [sibling-name]"
paths:
  - "SYNERGY-*.md"
  - "PRIVATE-SYNERGY-*.md"
  - "UPSTREAM-*.md"
  - ".claude/synergy-registry.json"
  - ".claude/vendor-registry.json"
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - Skill
  - AskUserQuestion
  - mcp__basic-memory__search_notes
  - mcp__basic-memory__read_note
---

# Sibling Sync

Bilateral reconciliation of `SYNERGY-*.md` and `UPSTREAM-*.md` files between
this project and its sibling vp-\* projects. Read-only by default — surfaces
drift, reciprocal gaps, stale-aligned rows, and status drift across sides
without mutating anything. The opt-in `--auto-reciprocate` flag writes
reciprocal entries to the sibling's SYNERGY file via per-entry confirmation.

Companion to `/vendor-sync` (which handles upstream → project drift); this
skill handles peer-to-peer drift between siblings registered in
`.claude/synergy-registry.json`.

## Design Rationale

The bd v1.0.0 Integration Charter
(`gastownhall/beads@5d524cf7:docs/INTEGRATION_CHARTER.md`) explicitly punts
cross-tracker orchestration out of bd's scope: bd will never grow a feature
that routes a cross-project item from project A's tracker to project B's
tracker. `/sibling-sync` is exactly the workflow-automation layer the Charter
defers to external tools — file-based reconciliation between sibling vp-\*
projects, mediated by registries and confirmation prompts rather than
synchronous tracker calls.

This mirrors the rationale already cited by `/synergy-tracker` for keeping
cross-project state in `SYNERGY-*.md` plus Basic Memory rather than in bd.

## Cross-skill boundaries

`/sibling-sync` is a *comparison and reconciliation* layer that sits alongside
the per-side logging skills. It owns nothing in Basic Memory and nothing on
this project's side of the SYNERGY/UPSTREAM files.

- **Does NOT write SYNERGY entries on this project's side.** `/synergy-tracker`
  workflow 1 (Log a synergy entry) owns logging on this side.
- **Does NOT pull upstream subtrees.** `/vendor-sync` owns subtree pulls and
  the upstream → project drift workflow.
- **Does NOT write Basic Memory notes.** `/synergy-tracker` workflow 5
  (Promote to Basic Memory) owns `## Cross-Project Synergy` writes
  to sibling entity notes; `/upstream-tracker` workflow 6 (Promote to Basic
  Memory) owns `## Upstream Friction` writes. Basic Memory write tools are
  intentionally absent from this skill's `allowed-tools`.
- **Does NOT write `## Trend Reviews` entries** to SYNERGY files. Those belong
  to `/synergy-tracker` workflow 4 (Trend review (quarterly)). Even under
  `--auto-reciprocate`, /sibling-sync only mirrors content entries into
  reciprocal sections — never trend-review summaries.
- **Stale-row detection is INLINE here** for the threshold values used during
  comparison runs. The canonical staleness-threshold definition lives in
  `/synergy-tracker` workflow 4 (Trend review (quarterly)) — workflow 2 (Sync
  sibling SYNERGY) below cites it. Per RETRO-10 YAGNI guard: extract this to
  a shared helper only when a third skill needs the same logic.
- **Surfacing reciprocal-friction findings is in scope; acting on them is
  not.** Workflow 3 (Sync sibling UPSTREAM) Mode B (see below) reads the sibling's
  `UPSTREAM-<this-project>.md` to surface friction the sibling tracks about
  this project. Filing the resulting work as bugs/features/opportunities on
  this side is `/upstream-tracker` workflow 1 (Log a new entry)'s job.
  Annotating the sibling's entry as resolved is `/upstream-tracker` workflow
  3 (Resolve an entry)'s job, performed on the sibling's side. /sibling-sync
  reports only.
- **Orchestrator role for follow-up actions (v0.14.0).** Workflows 2 (Sync
  sibling SYNERGY) and 3 (Sync sibling UPSTREAM) end with a per-sibling
  action menu (see "Action-menu protocol" below) that delegates writes to
  the owning skill (`/vp-beads:synergy-tracker`,
  `/vp-beads:upstream-tracker`) via the `Skill` tool, or runs `bd create`
  directly for beads issues. /sibling-sync still owns nothing in Basic
  Memory and nothing in this project's SYNERGY/UPSTREAM files —
  ownership boundaries are unchanged.

## Registry and path resolution

Sibling projects are declared in `.claude/synergy-registry.json` (array of
`{name, file, remote, bm-entity, relationship, local-path?}` entries). The
optional `local-path` field gives the on-disk path to the sibling checkout
(relative paths resolve from this project root). When absent, fall back to
`../<name>/`.

`.claude/synergy-registry.local.json` is a gitignored companion that overrides
fields in the committed registry — same per-entry merge by `name` pattern as
`.claude/vendor-registry.local.json` — **and** can add fully-private siblings
(see "Private sibling handling" below). Resolution order:

1. Read `.claude/synergy-registry.json`.
2. If `.claude/synergy-registry.local.json` exists, merge it on top by `name`
   key, in two modes:
   - **Override mode** (entry `name` matches a base entry): fields in
     `.local.json` win; absent fields keep the base value.
   - **Private-add mode** (entry `name` not in the base registry AND its `file`
     is a `PRIVATE-SYNERGY-<name>.md` value): the entry is **added** to the
     merged result as a private sibling. The `PRIVATE-` prefix on `file` is the
     marker (there is no boolean); it governs the restrictions below.
   - Entries in `.local.json` whose `name` is not in the base registry and whose
     `file` is NOT `PRIVATE-SYNERGY-*` are **ignored** (backward compatibility —
     typos and accidental entries stay silent).
3. For each merged entry, resolve `local-path` (registry value or
   `../<name>/`).
4. If the resolved path does not exist on disk, report informatively and SKIP
   that sibling. Do not error out — continue with siblings that are
   accessible.

Workflow 3 (Sync sibling UPSTREAM) additionally consumes the merged
`.claude/vendor-registry.json` (+ `.local.json`) to identify shared vendor
dependencies across siblings. (The vendor registry has no private-add mode —
private siblings are synergy-registry only.)

### Private sibling handling

A **private sibling** is one whose merged registry entry has a
`file: PRIVATE-SYNERGY-<name>.md` value (added via private-add mode above, or —
in principle — a base entry, which the validator forbids because it would commit
the name). Its `name` lives only in the gitignored `.local.json` and
`PRIVATE-SYNERGY-<name>.md`; **it must never reach a committed file.** This skill
therefore treats private siblings under a strict read-vs-write split, keyed on
the `PRIVATE-SYNERGY-*` `file` predicate:

- **Read (allowed) — hybrid read-diff.** Unlike a *public* sibling's
  glob-discovered `PRIVATE-SYNERGY-*.md` overlay (which this skill never reads),
  a private sibling's `PRIVATE-SYNERGY-<name>.md` **is** its registry `file`, so
  workflows 1 (Discover sibling(s)), 2 (Sync sibling SYNERGY), and 3 (Sync
  sibling UPSTREAM, Mode A only) read it to produce **read-only diff findings**.
  Findings appear in the **ephemeral terminal report only** — never written.
- **Write (blocked) — every committed surface.** For a `PRIVATE-SYNERGY-*`-filed
  sibling:
  - **Reciprocation:** workflow 4 (Apply reciprocation batch) skips it entirely
    (writing `SYNERGY-<this-project>.md` on the sibling's side would expose the
    relationship).
  - **`bd create`:** the action menu suppresses the UPSTREAM "file beads issues"
    option (a committed `.beads/*.jsonl` entry would leak the name) — findings
    stay report-only.
  - **Logging on this side:** any "log unreciprocated entry" follow-up routes to
    the gitignored `PRIVATE-SYNERGY-<name>.md`, never a committed
    `SYNERGY-<name>.md` (delegated to `/synergy-tracker`).
  - **BM promotion:** never (this skill has no BM tools; `/synergy-tracker`
    workflow 5 (Promote to Basic Memory) skips `PRIVATE-SYNERGY-*` siblings).
  - **UPSTREAM Mode B:** out of scope for private siblings — an
    `UPSTREAM-<name>.md` filename would itself leak the name. Workflow 3 (Sync
    sibling UPSTREAM) runs Mode A (shared dependencies — names no sibling) but
    skips Mode B for `PRIVATE-SYNERGY-*` siblings.

The `PRIVATE-SYNERGY-*` `file` predicate is the single structural marker — the
same prefix that keeps content outside the `SYNERGY-*.md` glob also gates every
write path here.

## Workflows

Determine which workflow the user needs based on their request. If ambiguous,
default to running workflow 1 (Discover sibling(s)) followed by workflow 2
(Sync sibling SYNERGY) and workflow 3 (Sync sibling UPSTREAM) as a single
report. Workflow 4 (Apply reciprocation batch) only fires under explicit
`--auto-reciprocate`.

### 1. Discover sibling(s)

Resolve which siblings will participate in this run.

**Steps:**

1. Read `.claude/synergy-registry.json`. If the file does not exist, redirect:
   tell the user no sibling registry is configured and offer to invoke
   `/synergy-tracker` workflow 1 (Log a synergy entry), which will run the
   guided registry creation flow at step 1b for the first sibling. If the
   user names a sibling now, follow the synergy-tracker step 1b prose from
   this conversation (re-reading
   `skills/synergy-tracker/SKILL.md` workflow 1 (Log a synergy entry) step 1b
   and applying its logic in-session — Claude Code has no actual
   inline-skill-invocation mechanism, so this means executing step 1b's
   instructions verbatim from sibling-sync's context). After the registry
   is created, resume from step 2 below. Otherwise stop, and instruct the
   user to invoke `/synergy-tracker` directly with the sibling name and
   then re-run `/sibling-sync`.
2. If `.claude/synergy-registry.local.json` exists, merge it on top per the
   per-entry merge rules in the Registry section above. This includes
   **private siblings** — `.local.json`-only entries whose `file` is
   `PRIVATE-SYNERGY-<name>.md`, which are added to the participating set (they
   read-diff like any sibling but are blocked from every committed-write path —
   see "Private sibling handling").
3. If the user named a specific sibling in their request or argument, filter
   the merged list to that entry. Otherwise, all merged entries participate.
4. For each entry, resolve `local-path` → `../<name>/` fallback. Probe each
   resolved path with a directory existence check.
5. Build the participation lists:
   - **Accessible siblings** (path exists) — proceed to workflow 2 (Sync
     sibling SYNERGY) and workflow 3 (Sync sibling UPSTREAM) for each. Mark any
     private sibling (registry `file` is `PRIVATE-SYNERGY-*`) with a `[private]`
     label so the user can see which relationships are private.
   - **Inaccessible siblings** (path missing) — report them so the user
     knows what was skipped, with the resolved path and a hint that
     `.claude/synergy-registry.local.json` can override the path
6. Report the participation list before continuing.

**Output:**

```
Siblings participating:
- vp-knowledge → /Users/.../vp-claude  (registry local-path)
- acme-partner → /abs/path/to/acme-partner  [private]

Siblings skipped (path not accessible):
- vp-other → ../vp-other  (set local-path in synergy-registry.local.json)
```

If no siblings are accessible, stop and report. The user can either correct
the paths via `.claude/synergy-registry.local.json` or accept that this run
has no work to do.

### 2. Sync sibling SYNERGY

For each accessible sibling from workflow 1 (Discover sibling(s)), compare
the bidirectional SYNERGY files and surface drift findings. Report only —
no writes.

**Steps:**

1. Read this project's SYNERGY file for the sibling, by the registry `file`
   value — `SYNERGY-<sibling>.md` for a public sibling, or
   `PRIVATE-SYNERGY-<sibling>.md` for a **private** sibling (its registry `file`;
   the hybrid read-diff exception). For a *public* sibling, never pull in a
   glob-discovered `PRIVATE-SYNERGY-*.md` overlay — the `PRIVATE-` prefix keeps
   those outside the `SYNERGY-*.md` namespace, so reading the committed file by
   name never touches them (see `/synergy-tracker` `### Private overlay`). For a
   private sibling, all downstream findings are read-only and stay in the
   ephemeral report (the write blocks in "Private sibling handling" apply). If
   the file is absent, treat as zero entries and proceed (the gap will surface as
   "Unreciprocated entries on sibling" if the sibling has any entries).

2. Read the sibling's `SYNERGY-<this-project>.md` at
   `<resolved-local-path>/SYNERGY-<this-project>.md`. If absent, treat as
   zero entries.

3. Parse each side's entries section-by-section (Shared Patterns,
   Divergences, Extraction Candidates, They Have / We Don't). Build a
   bidirectional entry map keyed by **title**, normalized per the rule in
   Guidelines below (2-pass matching: deterministic lead-clause pass, then
   judgment pass on residuals).

   **Section migration is its own signal — not silently merged.** Matching
   is within-section: an entry's title is paired only with same-section
   titles on the sibling. If an entry has migrated sections on one side
   (e.g., Shared Pattern here, Divergence on sibling — typical when one
   side promoted after noticing drift), it surfaces as (a) on the
   originating section and (b) on the destination section, NOT as a
   finding (d) Status drift. The section migration is itself the drift
   signal worth surfacing, and the (a)/(b) framing tells the user
   precisely which side moved. Finding (d) applies within-section only.

   **Section asymmetry — excluded from findings (a)/(b):** the
   `They Have / We Don't` section is intrinsically asymmetric. Entries here
   describe what the *sibling* has that we don't; reciprocally on the
   sibling's side, the same-named section describes what *we* have that
   they don't — a different semantic set. Bilateral title comparison is
   meaningless for this section. Skip its entries when computing findings
   (a) and (b). The user can read the section directly to act on adoption
   candidates; logging an adoption decision is `/synergy-tracker`'s job,
   not /sibling-sync's.

4. Walk the merged map and classify each entry into one of four findings:

   - **(a) Reciprocal gaps** — entries on this side with no matching title
     on the sibling. The sibling lacks the reciprocal entry. Candidates for
     workflow 4 (Apply reciprocation batch) under `--auto-reciprocate`.
     Excludes entries from `They Have / We Don't` (asymmetric — see step 3).
   - **(b) Unreciprocated entries on sibling** — entries on the sibling
     with no matching title here. The user may want to invoke
     `/synergy-tracker` workflow 1 (Log a synergy entry) to log these on
     this side. /sibling-sync does NOT write to this side automatically.
     Excludes entries from `They Have / We Don't` (asymmetric — see step 3).
   - **(c) Stale alignment claims** — entries with `Status: aligned` and
     `Last verified:` more than 8 sprints old (≈ two trend-review cycles).
     Inline threshold; canonical definition is `/synergy-tracker` workflow
     4 (Trend review (quarterly)). Treat 1 sprint ≈ 2 weeks if no other
     calibration is available; if the entry has no `Last verified:` field,
     fall back to the entry's date stamp.
   - **(d) Status drift** — matched entries whose `Status:` field differs
     across sides. Applies to two cases:

     1. **Shared Patterns** where one side records `aligned` and the other
        records `drifting` or `diverging` (or any disagreement on the
        Status value). Often signals that one side has converged or
        re-diverged without the reciprocal note being refreshed.
     2. **Divergences** with `Convergence path: adopt-theirs` or
        `Convergence path: propose-shared` where one side has moved to
        `adopted`/`converged` while the other still says `drifting` or
        similar.

     Excludes Divergences with `Convergence path: accept-difference` —
     those are intended-asymmetric and have no drift signal to flag.

5. Output a structured report grouped first by sibling, then by finding
   category. Include each entry's title, both sides' values where they
   differ, and a one-line action hint per category.

**Output format (per sibling):**

```
## SYNERGY drift — vp-knowledge

### (a) Reciprocal gaps (here, missing on sibling)
- "Hook event coverage" (Shared Patterns) — sibling has no matching entry
  → /sibling-sync --auto-reciprocate to file the reciprocal

### (b) Unreciprocated entries on sibling
- "validate-plugin tool-reference audit" (Shared Patterns) — we don't track this
  → /synergy-tracker to log on this side

### (c) Stale alignment claims (>8 sprints since Last verified)
- "PreCompact prompt command hook" — Last verified: 2026-01-15 (here),
  2026-01-15 (sibling). Re-verify now.

### (d) Status drift
- "npm-run-all2 parallel check stages" (Shared Patterns) — Status here:
  diverging. Status sibling: aligned. Sibling converged; refresh this row.
- "BM section ownership scheme" (Divergences, propose-shared) — Status
  here: drifting. Status sibling: aligned.
```

6. **Offer follow-up actions.** After workflow 3 (Sync sibling UPSTREAM)
   has also finished printing for this sibling, prepare the SYNERGY tier of
   the action menu (built from this workflow's findings) and let workflow 3
   (Sync sibling UPSTREAM) step 6 pair it with the UPSTREAM tier into a
   single `AskUserQuestion` call. Do NOT issue the prompt from this step —
   the prompt is dispatched from workflow 3 (Sync sibling UPSTREAM) step
   6 once both reports are on screen. Full protocol — which findings map to which menu options,
   the `header` values, the `--auto-reciprocate` precedence rule, and the
   plugin-namespaced `Skill` invocations — lives in the "Action-menu
   protocol" section below.

### 3. Sync sibling UPSTREAM

For each accessible sibling, build two kinds of UPSTREAM file pairs and
compare friction tracking on each. Same report-only contract as workflow 2
(Sync sibling SYNERGY).

**Two pairing modes coexist; both can fire on a single sibling:**

- **Mode A — shared-dependency pairing.** Both sides have `UPSTREAM-<dep>.md`
  with the same basename (e.g., both have `UPSTREAM-basic-memory.md`). The
  files describe the same third-party dependency `<dep>`. Findings (a)–(d).
- **Mode B — reciprocal sibling-friction pairing.** This project has
  `UPSTREAM-<sibling-name>.md` (friction we log about the sibling) AND/OR the
  sibling has `UPSTREAM-<this-name>.md` (friction the sibling logs about us).
  Different basenames; same bilateral relationship. Owner-side semantics
  invert relative to Mode A: an entry in the sibling's `UPSTREAM-<this-name>.md`
  with `Ownership: upstream` means THIS project is the upstream that must
  act. Findings (e)–(h).

**Steps:**

1. **Build Mode A pairs.** Glob this project for `UPSTREAM-*.md`. Glob the
   sibling's resolved `local-path` for `UPSTREAM-*.md`. Compute the
   intersection by basename — each match is one Mode A pair. Record both
   sides' full UPSTREAM basename lists for use in step 2.
2. **Detect Mode B pair.** **Skip Mode B entirely for private siblings**
   (merged registry `file` is `PRIVATE-SYNERGY-*`): a Mode B file is named
   `UPSTREAM-<sibling-name>.md`, whose filename would commit the private name.
   Private siblings are SYNERGY-only; Mode A above (keyed on shared *dependency*
   names, never the sibling) still runs. For a non-private sibling, derive this
   project's canonical name per the four-tier algorithm in
   `skills/synergy-tracker/references/project-name-derivation.md` to
   compute `<this-name>`. Apply the same algorithm (tier 3 for the sibling
   subject) to the registry `name` field for `<sibling-name>`.
   **Stale `local-path` guard:** if the registry entry specifies a
   `local-path` that does not resolve to an accessible directory, tier 1
   (sibling-registry back-pointer) silently falls through to tier 2
   (this project's `plugin.json`). Warn the user before falling through:
   "Sibling local-path is not accessible — tier 1 derivation skipped;
   `<this-name>` may diverge from how the sibling registered this project.
   Update `.claude/synergy-registry.local.json` if the sibling moved."
   Then check:

   - Does the sibling have `<resolved-local-path>/UPSTREAM-<this-name>.md`?
   - Does this project have `UPSTREAM-<sibling-name>.md`?

   If either file exists, this sibling has a Mode B pair (one-sided or
   two-sided). Both files absent is normal — no reciprocal friction tracked
   on either side. Skip Mode B for this sibling and continue.

   The Mode B file pair is `<this-root>/UPSTREAM-<sibling-name>.md` ↔
   `<sibling-root>/UPSTREAM-<this-name>.md`. By construction these basenames
   differ from any Mode A pair's basename (Mode A keys on shared
   third-party dep names; Mode B keys on sibling project names that appear
   in the synergy registry). No deduplication guard needed.
3. **Process Mode A pairs.** For each Mode A pair, read both copies and
   parse entries (Bugs, Feature Requests, Upstream Opportunities,
   Resolved). Build a bidirectional entry map by **title** using the same
   2-pass matching rule as workflow 2 (deterministic lead-clause Pass 1 +
   judgment Pass 2 on residuals — see Guidelines). UPSTREAM titles are
   typically more structured than SYNERGY titles, so Pass 2 fires less
   often, but the rule is identical for consistency. Classify each entry:

   - **(a) Duplicate friction** — same title on both sides. Sanity check:
     are the workarounds, dates, and status fields aligned? If not, it's a
     candidate for category (b).
   - **(b) Complementary workarounds** — same title both sides but the
     `Workaround:` field (or equivalent) differs. The sibling may have
     found a better mitigation. Flag for cross-pollination.
   - **(c) Stale entries** — entries dated more than 3 months ago without a
     Trend Review annotation since. Either side. Stale ≠ wrong, but worth
     re-verifying.
   - **(d) Sibling-only entries** — friction the sibling tracks for a
     shared dependency that we don't. Potential adoption: invoke
     `/upstream-tracker` workflow 7 (Sync from Basic Memory) or workflow 1
     (Log a new entry) to bring matching entries over here. /sibling-sync
     does NOT write here automatically.
4. **Process Mode B pair.** Read whichever side(s) of the pair exist.
   Parse entries the same way as step 3. Match titles bidirectionally with
   the same 2-pass rule. Classify each entry:

   - **(e) Sibling's unresolved friction against this project** — entries
     in `<sibling-root>/UPSTREAM-<this-name>.md` that are NOT prefixed with
     `_(Resolved ...)_` and NOT in a `## Resolved` section if one exists.
     `Ownership: upstream` on these entries means THIS project owns the
     fix (we are upstream from the sibling's perspective). Surface ALL
     unresolved entries — every one is a request directed at us. Action
     hint: file beads issues here or address inline; consider logging a
     cross-reference in our `UPSTREAM-<sibling-name>.md` if a workaround
     is built.
   - **(f) Our unresolved friction against the sibling** — entries in
     `<this-root>/UPSTREAM-<sibling-name>.md` that are unresolved on our
     side and have no corresponding `_(Resolved ...)_` annotation on
     either side. Informational: documents work blocked on the sibling.
     Action hint: check sibling release notes or changelog for shipped
     fixes the sibling forgot to annotate.
   - **(g) Cross-side staleness — our entry, sibling may have shipped.**
     Entry in `<this-root>/UPSTREAM-<sibling-name>.md` unresolved on our
     side, but the sibling shows a "shipped" signal (see "What 'shipped'
     means" below). Use 6 months as the look-back horizon for git-log
     scanning. Action hint: re-verify against the sibling's current
     release; annotate with `_(Resolved ...)_` via `/upstream-tracker`
     workflow 3 (Resolve an entry) if confirmed shipped.
   - **(h) Reverse cross-side staleness — sibling tracks us, we may have
     shipped.** Entry in `<sibling-root>/UPSTREAM-<this-name>.md` unresolved
     on the sibling's side, but this project shows a "shipped" signal
     (recent CHANGELOG entry, `_(Resolved ...)_` in our cross-reference,
     or git tag/commit subject within 6 months matching the entry title).
     Read-only finding: /sibling-sync cannot write the sibling's file.
     Action hint: notify sibling maintainer, or raise on their side via
     `/upstream-tracker` workflow 3 (Resolve an entry) so they can
     annotate.

   **What "shipped" means** (pinned definition for findings (g) and (h)):
   a fix is shipped when (1) a CHANGELOG or `_(Resolved ...)_` annotation
   exists on the owner's side, OR (2) the feature/fix is referenced in a
   git tag message or commit subject within the relevant release window
   (use `git -C <owner-path> log --oneline --since="6 months ago"` as a
   heuristic proxy — string-match the entry title or its lead clause; do
   not parse). A `Workaround: full` on the filing side without a
   corresponding shipped version on the owner's side is NOT sufficient;
   that is the filing project's mitigation, not upstream resolution.
5. **Output.** Report Mode A findings first (grouped by sibling, then by
   shared dependency, then by finding category), then Mode B findings
   (grouped by sibling) under a separate header. This ordering keeps the
   existing Mode A output shape intact and adds Mode B as an additive
   block.

**Note on UPSTREAM coverage gaps:** /sibling-sync now handles two cases:
shared third-party dependencies (Mode A, basename intersection) and
reciprocal sibling-friction pairs (Mode B, inverse-name detection).
One-sided UPSTREAM files about non-sibling, non-shared dependencies are
still out of scope — those are the sibling's responsibility to discover
via `/upstream-tracker` workflow 7 (Sync from Basic Memory) on its own.

**Output format additions for Mode B:**

```
## UPSTREAM reciprocal-friction — vp-knowledge

(Mode B: this-side UPSTREAM-vp-knowledge.md ↔ sibling-side UPSTREAM-vp-beads.md)

### (e) Sibling's unresolved friction against this project (we should action)
- "vp-beads: new /sibling-sync skill" (Feature Requests, 2026-05-04) — sibling
  marks Workaround: partial; we shipped in v0.12.0. See finding (h).
- "synergy-tracker: mandate bilateral reciprocation" (Feature Requests, 2026-05-04)
  Ownership on their side: upstream (us) · Workaround on their side: full
  → file beads issue or address inline

### (f) Our unresolved friction against the sibling
- "Agent effort defaults not overridable from parent" (Feature Requests, 2026-04-05)
  Ownership: upstream (them) · Workaround: none

### (g) Cross-side staleness: our entry the sibling may have shipped
- (none this run)

### (h) Reverse staleness: sibling tracks us but we may have shipped
- "vp-beads: new /sibling-sync skill" — v0.12.0 tag (2026-05-05) matches.
  Sibling should annotate _(Resolved 2026-05-05, vp-beads v0.12.0)_.
  → notify sibling maintainer; cannot write their file from here
```

6. **Offer follow-up actions.** This is the dispatch point. After this
   workflow finishes printing (and workflow 2 (Sync sibling SYNERGY) has
   already finished for the same sibling), build a single `AskUserQuestion`
   call combining workflow 2 (Sync sibling SYNERGY)'s SYNERGY tier with
   this workflow's UPSTREAM tier. The "Action-menu protocol" section below
   specifies the full UPSTREAM tier: findings (b) and (d) collapse into a
   single "Update our UPSTREAM" option that delegates to
   `/vp-beads:upstream-tracker`; finding (e) routes directly to `bd
   create`; finding (g) delegates to `/vp-beads:upstream-tracker` workflow
   3 (Resolve an entry). Findings (a), (c), (f), and (h) are informational
   and not present in the menu. If no UPSTREAM findings are actionable AND
   no SYNERGY findings are actionable for this sibling, skip the prompt
   for this sibling. If only one tier has actionable findings, issue a
   single-question call.

### 4. Apply reciprocation batch

Opt-in mutation path. Only runs when the user supplies `--auto-reciprocate`
in their invocation, or explicitly confirms intent like "yes, apply all the
reciprocal gaps". Mirrors `/upstream-tracker` workflow 7 (Sync from Basic
Memory)'s per-entry confirmation pattern.

**Steps:**

1. **Exclude private siblings first.** Drop any sibling whose merged registry
   `file` is `PRIVATE-SYNERGY-*` before doing anything else — reciprocation would
   write `SYNERGY-<this-project>.md` on the sibling's side and expose that the
   private relationship exists. Announce each exclusion: "Skipping reciprocation
   for `<name>` — private sibling (existence must not cross to the sibling's
   side)." This guard runs at the top of the loop, before any read of the
   sibling's SYNERGY file.
2. Re-run workflow 2 (Sync sibling SYNERGY) finding (a) (reciprocal gaps)
   for each remaining (non-private) accessible sibling, applying the stricter
   matching rules from the Hard Limits section below: Pass 1 (deterministic)
   matches only; any Pass 2 (judgment) matches from workflow 2 (Sync sibling
   SYNERGY) are added back to the reciprocation queue with an extra
   disambiguation prompt rather than suppressed silently. These are the entries
   on this side that the sibling demonstrably lacks.
3. For each reciprocal gap, in order:
   1. Read the source entry from this project's `SYNERGY-<sibling>.md`
      (full entry text including title, date, structured fields).
   2. Determine the destination file at the sibling:
      `<resolved-local-path>/SYNERGY-<this-project>.md` (derive
      `<this-project>` per
      `skills/synergy-tracker/references/project-name-derivation.md`).
      If it does not exist yet, plan to `Write` a new file using the
      four-section template from
      `skills/synergy-tracker/references/synergy-entry-format.md`.
   3. Determine the destination section from the source entry's section
      (a Shared Pattern on this side becomes a Shared Pattern on the
      sibling, etc.).
   4. Show the user: source entry text + destination file path +
      destination section. Ask: "Write reciprocal entry to
      `<sibling-path>/SYNERGY-<this-project>.md` under `### <Section>`?
      \[y/n/skip-rest]".
   5. On `y`: append the entry under the destination section using `Edit`
      (or `Write` if the file is new). Replace any
      `_No entries yet._` placeholder in that section with the entry. Keep
      the entry text *as-is* from this side — do not rewrite to the
      sibling's voice; reciprocation IS the verification step (per
      `/synergy-tracker` workflow 1 (Log a synergy entry) bilateral
      mandate). The sibling will re-verify on their next reciprocation
      pass.
   6. On `n` or `skip-rest`: skip and continue (or stop the batch on
      `skip-rest`).
4. After the batch, report:
   - Entries written, with destination file paths
   - Entries skipped, with reason
   - **Verification reminder for the user**: run `git status` in the
     sibling repo, review the appended entries, commit on that side. /sibling-sync
     does not commit on the sibling's behalf. Also remind the user to file
     a beads follow-up on the sibling for re-verification next sprint, per
     `/synergy-tracker` workflow 1 (Log a synergy entry)'s reciprocation
     mandate.

**Hard limits on workflow 4 (Apply reciprocation batch):**

- Only mirrors entries from workflow 2 (Sync sibling SYNERGY) finding (a).
  Does NOT mirror UPSTREAM entries from workflow 3 (Sync sibling UPSTREAM)
  — `/upstream-tracker` workflow 7 (Sync from Basic Memory) is the right
  channel for cross-project UPSTREAM adoption (BM is the cross-project
  bridge for friction; SYNERGY is the cross-project bridge for patterns).
  This applies equally to Mode A findings (a)–(d) AND Mode B findings
  (e)–(h): finding (e) entries get filed natively on this side via
  `/upstream-tracker` workflow 1 (Log a new entry), not mirrored;
  finding (h) annotations get written by the sibling via their own
  `/upstream-tracker` workflow 3 (Resolve an entry), not by us.
- **Never sources a reciprocal entry from a `PRIVATE-SYNERGY-*.md` private
  overlay.** Those entries are private to this checkout (the proprietary↔public
  boundary); writing one to a sibling would leak it. This is enforced
  structurally: reciprocation reads the committed `SYNERGY-<project>.md` (by
  exact name, workflow 2 (Sync sibling SYNERGY) step 1), and the `PRIVATE-`
  prefix keeps overlays outside the `SYNERGY-*.md` namespace so no glob here can
  reach them. See
  `/synergy-tracker` `### Private overlay`.
- **Never reciprocates for a private sibling** (merged registry `file` is
  `PRIVATE-SYNERGY-*`). Step 1 of this workflow excludes them before the loop;
  writing `SYNERGY-<this-project>.md` on the sibling's side would commit the
  private relationship's existence to their repo. See "Private sibling
  handling".
- Never mirrors entries from `## They Have / We Don't`. The section is
  intrinsically asymmetric (entries here describe sibling capabilities
  WE lack; the sibling's same-named section describes the inverse
  asymmetry). Workflow 2 (Sync sibling SYNERGY) already excludes this section from finding (a),
  but this is restated here as a mutation-side guard: even if a future
  edit relaxes the workflow 2 (Sync sibling SYNERGY) exclusion, workflow 4 (Apply reciprocation batch) must never write a
  `They Have / We Don't` entry to the sibling.
- The reciprocal-gap list is computed using **Pass 1 matches only**.
  Entries that paired via Pass 2 (judgment) in workflow 2 (Sync sibling SYNERGY) are added back
  to the reciprocation queue and presented to the user with a flag:
  "This entry may already exist on the sibling as `<pass-2-matched-title>`
  — does that match? \[y=skip / n=write reciprocal anyway / skip-rest]".
  Defaulting to caution at the mutation boundary inverts the read-only
  cost asymmetry: under `--auto-reciprocate`, suppressing a write that
  should happen (false-positive Pass 2 match) is more expensive than
  proposing a duplicate the user can reject (false-negative).
- Never writes to `## Trend Reviews` sections on either side.
- Never writes to this project's side. Reciprocal entries go to the
  sibling only — logging on this side is `/synergy-tracker` workflow 1
  (Log a synergy entry)'s job.
- Never writes to Basic Memory (no BM edit tooling allowed in this skill).
  BM writes are `/synergy-tracker` workflow 5 (Promote to Basic Memory)
  and `/upstream-tracker` workflow 6 (Promote to Basic Memory)'s
  territory.

## Action-menu protocol

This skill never writes SYNERGY/UPSTREAM/BM directly — even the menu options
dispatch to the owning skill via the `Skill` tool, or run `bd create` for
beads issues. The menu is a navigation aid, not a write path. The default
read-only contract from earlier versions still holds: a user who picks
"None" for both questions receives the report and exits without any
mutation.

After workflows 2 (Sync sibling SYNERGY) and 3 (Sync sibling UPSTREAM) have
printed their per-sibling reports, sibling-sync issues a single
`AskUserQuestion` call with up to two single-select questions per sibling.
The `AskUserQuestion` SDK contract caps options at 2-4 per question
(plus an auto "Other"); we therefore split SYNERGY and UPSTREAM into
separate questions rather than one flat menu. Skipping a question is just
selecting its "None" option; both tiers default to read-only on skip.

### Two-tier menu shape

**Q1 — SYNERGY follow-up** (`header: "Synergy"`, 7 chars). Options listed
only when their finding count is nonzero:

| Option                                    | Trigger         | Dispatch                                                                                |
| ----------------------------------------- | --------------- | --------------------------------------------------------------------------------------- |
| 1. Apply reciprocal gaps (N)              | finding (a) > 0 | re-enter workflow 4 (Apply reciprocation batch) in-skill — no `Skill` call              |
| 2. Log unreciprocated sibling entries (N) | finding (b) > 0 | `Skill(skill="/vp-beads:synergy-tracker", args=...)` → workflow 1 (Log a synergy entry) |
| 0. None — synergy report only             | always          | exit SYNERGY tier without action                                                        |

**Q2 — UPSTREAM follow-up** (`header: "Upstream"`, 8 chars). Options listed
only when their finding count is nonzero. Findings (b) and (d) collapse
into a single option to keep the question within the 4-option SDK cap:

| Option                                          | Trigger                            | Dispatch                                                                                                                                                              |
| ----------------------------------------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Update our UPSTREAM (b/d, N total)           | finding (b) > 0 OR finding (d) > 0 | `Skill(skill="/vp-beads:upstream-tracker", args=...)` — args route to workflow 1 (Log a new entry) and/or workflow 7 (Sync from Basic Memory) inside upstream-tracker |
| 2. File beads issues for sibling's friction (N) | finding (e) > 0                    | `Bash` → `bd create` per entry                                                                                                                                        |
| 3. Resolve cross-stale entries (N)              | finding (g) > 0                    | `Skill(skill="/vp-beads:upstream-tracker", args=...)` → workflow 3 (Resolve an entry)                                                                                 |
| 0. None — upstream report only                  | always                             | exit UPSTREAM tier without action                                                                                                                                     |

If neither tier has actionable findings for a sibling, skip the
`AskUserQuestion` call entirely for that sibling. If only one tier has
actionable findings, issue a single-question call (the SDK supports 1-4
questions per call).

**Private-sibling guard (no-commit-leak).** When the sibling's merged registry
`file` is `PRIVATE-SYNERGY-*`, every committed-write menu option is removed
because it would commit the private name:

- **Q2 option 2 (`bd create`) is suppressed** — a `.beads/*.jsonl` entry naming
  the sibling would leak it. The finding stays in the report only. (Finding (e)
  does not arise anyway: workflow 3 (Sync sibling UPSTREAM) skips Mode B for
  private siblings.)
- **Q1 option 2 (Log unreciprocated sibling entries) redirects** — its
  `/synergy-tracker` dispatch targets the gitignored `PRIVATE-SYNERGY-<name>.md`,
  never a committed `SYNERGY-<name>.md` (pass the private destination in the
  `args` prose).
- **Q1 option 1 (Apply reciprocal gaps) is absent** — workflow 4 (Apply
  reciprocation batch) already excludes private siblings.

If that leaves no actionable options for a private sibling, skip the prompt and
present the read-only findings as report-only.

### Per-action argument templates

Pass natural-language prose in the `Skill` tool's `args` field. The
delegated skill receives the prose as narrative context. Templates:

- **SYNERGY 2 (Log unreciprocated sibling entries):**
  `Log unreciprocated entries from sibling <sibling-name>: <bullet list of titles + sections>. Invoke workflow 1 (Log a synergy entry) for each.`
- **UPSTREAM 1 (Update our UPSTREAM, b/d collapse):**
  `From sibling-sync findings against <sibling-name>: adopt complementary workarounds for <package, title> entries (sibling's workaround text: <quoted>); also scan sibling-only entries <package, titles>. Use workflow 1 (Log a new entry) and workflow 7 (Sync from Basic Memory) as appropriate.`
- **UPSTREAM 3 (Resolve cross-stale entries):**
  `Resolve entries in UPSTREAM-<sibling-name>.md: <titles>. Verify against the sibling's recent changelog/tags first. Invoke workflow 3 (Resolve an entry) for each.`

For UPSTREAM 2 (`bd create`), construct each call with:

- `--title="<entry title from sibling>"`
- `--type=task` always. The sibling's UPSTREAM file body is plain prose
  and lacks the structured sections that `bd`'s `validation.on-create=error`
  requires for `--type=bug` (`## Steps to Reproduce`, `## Acceptance
  Criteria`) and `--type=feature` (`## Acceptance Criteria`). Filing as
  `task` always succeeds; the user can refile the resulting issue with
  `bd update --type=bug` after adding the required sections, or supersede
  with a properly structured bug-type issue. Note this in the post-batch
  report: "Filed N task-type beads issues from sibling friction; refile as
  bug/feature with required sections if needed."
- `--description="<entry body verbatim>\n\nSibling <sibling-name> tracks this against us in their UPSTREAM-<this-name>.md. Source section: <Bugs | Feature Requests | Upstream Opportunities>."`

### Precedence with `--auto-reciprocate`

The `--auto-reciprocate` flag is the explicit non-interactive consent path.
Its semantics relative to the new menu:

| Invocation                                                         | Behavior                                                                                                                                            |
| ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--auto-reciprocate` flag set                                      | Skip the action menu entirely. Run workflow 4 (Apply reciprocation batch) directly with its existing per-entry `[y/n/skip-rest]` confirmation gate. |
| No flag, user picks Q1 option 1 (Apply reciprocal gaps)            | Enter workflow 4 (Apply reciprocation batch) with the same per-entry confirmation. The menu surfaces the same path interactively.                   |
| No flag, user picks any "None" option                              | No writes. Default read-only contract holds.                                                                                                        |
| No flag, user picks any non-"None" option (other than Q1 option 1) | Dispatch per the table above. The delegated skill applies its own confirmation gate.                                                                |

### Idempotency and re-runs

Most actions self-resolve on the next sibling-sync run:

- Q1 option 1 closes finding (a) (the sibling now has the reciprocal entry).
- Q1 option 2 closes finding (b) (this side now has the entry; titles match).
- Q2 option 1 closes findings (b) and (d) on the UPSTREAM side.
- Q2 option 3 annotates `_(Resolved ...)_` so workflow 3 (Sync sibling UPSTREAM)'s matching logic suppresses finding (g) thereafter.

Only Q2 option 2 (`bd create` for finding (e)) does not self-resolve: the
sibling's `UPSTREAM-<this-name>.md` still carries the entry until the
sibling annotates it as resolved on their side. Finding (e) will re-fire
on subsequent sibling-sync runs until that happens. This is expected
behavior — it reminds the user the friction is real and the local `bd`
issue tracks our intent. No "skip-already-filed" cache is maintained.

### Failure modes

- **Delegated `Skill` call returns "skill not found" or errors.** Fall back
  to printing the original copy-paste hint and continue to the next
  sibling. Never abort the whole run on a delegation failure.
- **Subagent context.** When sibling-sync runs as a Task subagent (e.g.,
  inside a swarm-wave research agent), `AskUserQuestion` is **explicitly
  unavailable** per the Anthropic Agent SDK
  (<https://code.claude.com/docs/en/agent-sdk/user-input> — "Limitations:
  Subagents"), and `Skill` tool calls may silently no-op (undocumented
  behavior — subject to change). In subagent context the entire action
  menu cannot fire: skip the `AskUserQuestion` call, print the original
  copy-paste hints from workflows 2 (Sync sibling SYNERGY) and 3 (Sync
  sibling UPSTREAM) under the existing "→" arrow style, and let the
  parent agent decide whether to re-invoke `/sibling-sync` directly. No
  formal subagent probe is required — best-effort detection by attempting
  the `AskUserQuestion` call and falling back on the SDK error suffices.
- **`bd create` failure** (e.g., missing required `--description` field for
  bug type). Report the specific failure and continue to the next entry;
  don't abort the whole run.

## Sprint Workflow Integration

`/sibling-sync` runs as an optional parallel diagnostic alongside
`/synergy-tracker`'s review and trend-review workflows. Recommended cadences:

- **Before `/synergy-tracker` workflow 4 (Trend review (quarterly))** —
  every 4th sprint, run `/sibling-sync` first so the trend review has up-to-
  date drift findings to act on.
- **Before `/synergy-tracker` workflow 2 (Review open synergies)** —
  optional; surfaces drift the per-side review wouldn't catch.
- **After significant sibling activity** — when the user knows the sibling
  shipped a release or restructured a skill, run `/sibling-sync` to
  catch resulting drift early.

This skill is read-only in its default mode, so it's safe to run proactively
without commitment to any follow-up action.

## Guidelines

- **Read-only by default.** Default invocations only call workflows
  1 (Discover sibling(s)), 2 (Sync sibling SYNERGY), and
  3 (Sync sibling UPSTREAM), surfacing findings only. `Edit` and `Write`
  are in `allowed-tools` solely to support workflow 4 (Apply reciprocation
  batch). Never mutate without `--auto-reciprocate` (or equivalent
  explicit user intent).
- **Per-entry confirmation under `--auto-reciprocate`.** Even with the flag,
  every write requires explicit per-entry confirmation. Mirrors
  `/upstream-tracker` workflow 7 (Sync from Basic Memory)'s confirmation
  pattern.
- **Skip inaccessible siblings, don't error.** A missing local-path is
  informational, not fatal. Continue with what's available and report what
  was skipped so the user can correct via
  `.claude/synergy-registry.local.json`.
- **Title-keyed comparison runs in two explicit passes.** Entries on the
  two sides are written by different sessions and naturally drift in title
  formatting; deterministic matching catches the obvious wins, judgment
  ratifies the residual ambiguous cases. The two passes are separate so
  the deterministic rule stays testable and the judgment rule stays
  bounded.

  - **Pass 1 — deterministic lead-clause match.** For each title:
    lowercase, collapse whitespace runs to a single space, then take the
    **lead clause** = the substring before the first occurrence of `:`,
    `—`, `--`, or ` (` (whichever is earliest; if none of those
    appears, the lead clause is the full normalized title). Two entries
    pair in pass 1 iff their normalized lead clauses are byte-identical.
    Examples that should pair here:
    - `wc -l portability guard` ↔ `wc -l portability guard (|| count=0 + tr -d ' ')`
    - `edit_note append-with-section gotcha: independently documented by both plugins` ↔ `edit_note append-with-section gotcha — independently documented`
    - `Frontmatter features` ↔ `Frontmatter features (skills, user-invocable, effort)`
  - **Pass 2 — judgment on residuals only.** For entries that did NOT
    pair in pass 1, scan the still-unmatched residuals on the other side
    once for qualifier-phrase reorderings or token rearrangements that
    clearly describe the same idea. Pair only when the subjects are
    unambiguously the same. Pass 2 examples:

    - `PreCompact hook retired in vp-knowledge v0.28.0` ↔ `PreCompact hook retired in v0.28.0` (qualifier prepositional phrase)
    - `Skill invocation layering: three levels vs two levels` ↔ `Skill invocation layering: two-level vs three-level` (token reordering after the colon)

    Pass 2 may NEVER override or relax pass 1: do not unmatch a pair pass
    1 produced, and do not collapse two pass-1-residual entries that have
    a shared *prefix* but materially different scopes (`Hook validation`
    vs `Hook validation regression test` → leave both as one-sided).
    Rationale for the cost asymmetry: in **default read-only mode**, a
    duplicate entry surviving on both sides outlives sprint cycles
    silently, while an over-merge surfaces immediately at workflow 4
    (Apply reciprocation batch)'s per-entry confirmation gate where the
    user can reject. Under `--auto-reciprocate` this asymmetry inverts —
    a false-positive pass-2 match can suppress a reciprocal entry that
    should be written. Therefore: workflow 4 (Apply reciprocation batch) re-runs pass 1 only and
    treats pass 2 matches as advisory candidates that REQUIRE the user's
    per-entry confirmation to count as matches (mirrors the existing
    write-confirmation gate; the spec defaults to caution at the mutation
    boundary).
- **Stale threshold is inline.** 8 sprints (≈ two trend-review cycles) for
  SYNERGY `Status: aligned` rows; 3 months for UPSTREAM entries; 6 months
  for the workflow 3 (Sync sibling UPSTREAM) Mode B "shipped" look-back horizon (findings (g) and
  (h)). Canonical definitions for the 8-sprint and 3-month thresholds
  live in `/synergy-tracker` workflow 4 (Trend review (quarterly)) and
  `/upstream-tracker` workflow 4 (Trend review (quarterly)). The 6-month
  Mode B horizon is /sibling-sync's own choice — broader than the
  staleness flag because it requires cross-side evidence, not just age.
  When the canonical thresholds change, this skill must be updated to
  match — the validate-plugin convention check (vp-beads-9we) catches
  bare workflow refs but not threshold drift.
- **Canonical project-name derivation.** Workflow 3 (Sync sibling UPSTREAM) Mode B needs this
  project's own name to compute `UPSTREAM-<this-name>.md` at the sibling's
  root; workflow 4 (Apply reciprocation batch) needs it to name
  `SYNERGY-<this-project>.md` on the sibling. Derivation uses a four-tier
  precedence (sibling-registry back-pointer → plugin manifest → package
  manifest → directory basename), followed by normalization. Full
  algorithm, worked examples, and limitations:
  `skills/synergy-tracker/references/project-name-derivation.md`. The
  same algorithm computes `<sibling-name>` from this project's
  `synergy-registry.json` (tier 3 for the sibling subject). If derivation
  fails, see Error handling below.
- **No new SYNERGY/UPSTREAM sections.** /sibling-sync only writes entries
  into existing section schemas (`## Shared Patterns`, `## Divergences`, …).
  It does not introduce new section types. Schema evolution is
  `/synergy-tracker`'s job.
- **Companion to /vendor-sync.** vendor-sync handles upstream → project
  drift (subtree pulls, UPSTREAM auto-resolve). sibling-sync handles
  peer-to-peer drift along two axes: SYNERGY reciprocation/status
  divergence (workflow 2 (Sync sibling SYNERGY)), and UPSTREAM friction tracked across both sides
  (workflow 3 (Sync sibling UPSTREAM) — both shared-dependency Mode A and
  reciprocal-friction Mode B). Both skills default to reporting / read-only paths and gate
  mutations on explicit user intent.
- **Project tempo classification.** When a sibling has been dormant for
  more than 90 days (`git -C <sibling-path> rev-list --count --since="90 days ago"
  HEAD` returns 0), surface findings under that sibling with a
  "(dormant — drift expected)" note. Don't suppress findings — the user
  may still want to apply reciprocations to dormant siblings to keep them
  in lockstep — but contextualize them.

## Error handling

- **Registry not found** — tell the user this project has no
  `.claude/synergy-registry.json`. Offer to redirect to
  `/synergy-tracker` workflow 1 (Log a synergy entry), which includes
  guided registry creation at step 1b. If the user names a sibling
  inline, follow step 1b's instructions verbatim from this conversation
  (Claude Code has no real cross-skill handoff, so this means executing
  step 1b's prose in-session by re-reading
  `skills/synergy-tracker/SKILL.md`), then resume this skill from
  workflow 1 (Discover sibling(s)) step 2. Otherwise stop, and direct
  the user to invoke `/synergy-tracker` first and re-run `/sibling-sync`
  afterwards.
- **All siblings inaccessible** — report which paths were tried and stop.
  Suggest `.claude/synergy-registry.local.json` for per-machine path
  overrides.
- **Sibling SYNERGY file missing** — treat as zero entries and proceed. The
  comparison will surface "Unreciprocated entries on sibling" findings if
  applicable.
- **Sibling UPSTREAM file present but malformed** — report the parse error
  with the file path and skip that file's findings. Continue with the rest
  of the sibling's UPSTREAM files.
- **`--auto-reciprocate` with zero reciprocal gaps** — report "no reciprocal
  gaps to apply" and exit cleanly without touching any file.
- **Project-name not derivable** — if both `.claude-plugin/plugin.json` is
  absent (or has no `name`) AND the project root directory basename is
  empty (e.g., the working directory is `/`), skip workflow 3 (Sync sibling UPSTREAM) Mode B for
  every sibling and report the limitation in the workflow 3 (Sync sibling UPSTREAM) output. Mode A
  still runs normally; SYNERGY workflow 2 (Sync sibling SYNERGY) is unaffected.
