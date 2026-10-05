---
name: synergy-tracker
description: "Manage cross-project synergy tracking between sibling projects. Use when the user wants to log a shared pattern, a divergence, an extraction candidate, or something a sibling project has that this one doesn't. Also use when the user wants to promote synergy entries to Basic Memory (workflow 5). NOT for upstream dependency bugs or vendor friction (use /upstream-tracker for those). Trigger phrases: 'synergy', 'sibling project', 'cross-project', 'extraction candidate', 'compare with [project]', 'both projects do', 'they have X we don't', 'shared pattern', 'divergence', 'cross-project alignment', 'review synergies', 'log this pattern', 'we should extract this', 'they handle this differently', 'promote synergy', 'promote to basic memory', 'promote synergy entries', 'sync synergy to memory', or any mention of patterns, divergences, shared practices, or BM promotion across related projects."
user-invocable: true
argument-hint: "[workflow] [project-name]"
paths:
  - "SYNERGY-*.md"
  - "PRIVATE-SYNERGY-*.md"
  - ".claude/synergy-registry.json"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - mcp__basic-memory__search_notes
  - mcp__basic-memory__read_note
  - mcp__basic-memory__edit_note
---

# Synergy Tracker

Manage the `SYNERGY-*.md` files that track shared patterns, divergences,
extraction candidates, and capabilities observed in sibling projects while
building this one. This skill tracks patterns and capabilities across
peer/sibling projects under the same maintainer — not upstream dependency
friction (use `/upstream-tracker` for that).

## Tracking Files

### Sibling projects (permanent files)

Sibling projects are declared in `.claude/synergy-registry.json` (if it exists)
as an array of `{name, file, remote, bm-entity, relationship}` objects. See
`references/synergy-entry-format.md` for the full registry schema.

To discover which projects are registered, read `.claude/synergy-registry.json`
if it exists. If it does not exist, glob for `SYNERGY-*.md` to infer sibling
names from existing files. If neither is present, ask the user which sibling
project is involved before proceeding.

### File naming

Files are named `SYNERGY-<project-name>.md`. The project name is taken from
the `name` field in the registry (tier 3 of the canonical derivation
algorithm — synergy-tracker's subject is always sibling). For projects
outside the registry, fall back to tier 4 (directory basename), then
normalize. Full algorithm:
`references/project-name-derivation.md`. Examples: `vp-knowledge` →
`SYNERGY-vp-knowledge.md`, `@scope/shared-utils` →
`SYNERGY-scope--shared-utils.md`.

See `references/synergy-entry-format.md` for the full naming convention
(normalization rules) and `references/project-name-derivation.md` for the
tiered derivation algorithm shared with `/sibling-sync`.

### Lifecycle

SYNERGY files are **permanent** — they always exist for registered sibling
projects, even when all sections are empty. When an entry is resolved or
dismissed, remove it and restore the `_No entries yet._` placeholder for that
section. Do not delete the file.

### Private overlay (`PRIVATE-SYNERGY-*.md`)

For entries that must stay out of a public repo (a proprietary sibling's
internal paths, client names, unreleased plans), use a **gitignored**
`PRIVATE-SYNERGY-<project-name>.md` companion to the committed
`SYNERGY-<project-name>.md`. It holds additional private entries under the same
four section headings.

**The `PRIVATE-` prefix is the privacy mechanism.** It keeps the overlay
OUTSIDE the `SYNERGY-*.md` glob namespace, so every public consumer (this
skill's boundary-crossing workflows, `/sibling-sync`, `/retrospective`, the
`sprint-review` agent, `session-start.sh`) **structurally cannot read it** — no
per-consumer exclusion is needed or used. Only the deliberate *local-only* read
in workflow 2 (Review) additionally globs `PRIVATE-SYNERGY-*.md` to assemble the
combined private view.

**Invariant: private-overlay entries are NEVER promoted to Basic Memory
(workflow 5 (Promote to Basic Memory)) and NEVER reciprocated/written to a
sibling.** With the prefix scheme this is enforced structurally — the promote
and reciprocate paths glob `SYNERGY-*.md`, which cannot match
`PRIVATE-SYNERGY-*.md`. This keeps the public view a sibling sees stable (so
bilateral convergence still works) and prevents a proprietary↔public leak.

When a `PRIVATE-SYNERGY-*.md` overlay exists, the committed
`SYNERGY-<project-name>.md` carries a one-line pointer noting it (gitignored
files are invisible to collaborators and `git grep`). Gitignored via the
explicit `PRIVATE-SYNERGY-*.md` line; `session-start.sh` warns if any is
tracked. Full convention: CLAUDE.md `### Synergy tracking convention`.

**Same-title shadowing (workflow 2 (Review) only).** When a private entry shares
a title with a committed entry, surface **both** in the review view — the
committed row (still promotable/reciprocable) labelled `[committed, shadowed]`
and the private row labelled `[local]` — so the reviewer never loses sight that
a public twin exists. This local-view assembly never participates in
`/sibling-sync`'s title-keyed bilateral matching, which reads committed entries
only.

### Structure

All SYNERGY files use the same four-section structure:

```
## Shared Patterns

_No entries yet._

## Divergences

_No entries yet._

## Extraction Candidates

_No entries yet._

## They Have / We Don't

_No entries yet._
```

Section semantics:

- **Shared Patterns** — practices, conventions, or implementations that exist
  in both projects and should stay aligned
- **Divergences** — places where the two projects intentionally or accidentally
  differ in approach to the same problem
- **Extraction Candidates** — code, patterns, or logic in this project that is
  a strong candidate for extraction into a shared package or library
- **They Have / We Don't** — capabilities in the sibling project that this
  project lacks and may want to adopt. Apply the **domain-fit test** before
  logging:

  > Pass test: "this project has the underlying need but lacks the implementation."
  > Fail test: "the sibling has a capability in a different domain than this project's."

  Without this test, every comparison run produces noise the user must
  dismiss. Worked failures from Sprint 19: vp-beads's `swarm-wave` (sprint
  orchestration is a different domain from vp-claude's research fan-outs)
  and vp-beads's `vendor-sync` (vp-beads vendors content; vp-claude has no
  vendored surface to sync) both passed the surface filter but failed the
  domain-fit test.

## Workflows

Determine which workflow the user needs based on their request. If ambiguous,
default to workflow 1 (log) for "synergy" or "log this" requests, workflow 2
(review) for "review synergies" or "what's open" requests, and workflow 3
(compare) for "compare with" requests.

### 1. Log a synergy entry

When the user observes a shared pattern, a divergence, an extraction candidate,
or a capability gap between this project and a sibling — add it to the correct
file. Infer the details from the current conversation context: what code was
being discussed, what pattern was noticed, what contrast was made.

**Steps:**

1. Identify which sibling project is involved from the conversation context.
   If the user named a sibling project in their request (e.g., "compare with
   vp-knowledge", "log this for vp-knowledge"), use that name directly — do
   not ask again. Otherwise, check `.claude/synergy-registry.json` first. If
   the registry does not identify the sibling, glob for `SYNERGY-*.md` as a
   fallback. If neither resolves it, ask the user.

**Step 1b — Guided registry creation (only when
`.claude/synergy-registry.json` is absent AND a sibling has been named in
step 1).** If the registry file already exists (returning user adding a
second sibling, or any case where a registry was hand-written), skip this
step silently and proceed to step 2 — do not modify hand-written
registries. **Append-to-existing is not supported**; that case falls back
to manual editing of `.claude/synergy-registry.json` (add a new
`{name, file, remote, bm-entity, relationship}` entry per the schema in
`references/synergy-entry-format.md`). Tracked separately as a future
enhancement (`vp-beads-bma`). Otherwise, run the following bootstrap so
the project can route future syncs and comparisons through the registry
rather than re-asking each time.

- **Confirm the sibling name** resolved from step 1. If step 1 deferred to
  asking the user, defer this step too — only proceed once a name is in
  hand.

- **Derive both project names before proceeding.**
  - `<sibling>` — the name confirmed in step 1. In practice this is already
    the tier-3 registry `name` field (or, for unregistered siblings, the
    directory basename: tier 4). No additional derivation is needed; just
    carry the value forward.
  - `<this-project>` — this project's own canonical name, derived using
    the four-tier algorithm in
    `skills/synergy-tracker/references/project-name-derivation.md` (self
    subject: tiers 1-4, starting with the sibling's back-pointer). In the
    common case — `vp-beads` with a registered sibling — tier 1 or tier 2
    resolves immediately. Use the normalized result as `<this-project>`
    everywhere below: in the `bm-entity` value and in any reciprocal file
    references.

- **Auto-derive the four registry fields** that have unambiguous defaults:
  - `name` — already known from step 1.
  - `file` — mechanical: `SYNERGY-<sibling>.md`.
  - `remote` — probe the sibling's git origin if the sibling repo is
    accessible on disk at `../<sibling>/`:

    ```bash
    git -C ../<sibling> remote get-url origin 2>/dev/null | sed 's/\.git$//'
    ```

    If the command fails or the path is not accessible, leave `remote` as
    an empty string in the preview.
  - `bm-entity` — apply the canonical convention
    `engineering/agents/vp-plugins-<this-project>-and-<sibling>` (see
    `references/synergy-entry-format.md`).

- **Prompt only the residuals.** At most three `AskUserQuestion` calls
  (Anthropic SDK caps the `header` field at 12 characters):
  - **First, a `header: "Visibility"` (10 chars) call** — "Public (committed
    registry) or Private (gitignored — the sibling's name is never committed)?"
    Default **Public**. Choose **Private** for a proprietary partner whose very
    existence must stay out of a public repo. When the user picks **Private**,
    switch to the private-sibling path:
    - Write the entry to `.claude/synergy-registry.local.json` only (never the
      committed base), with `file` set to `PRIVATE-SYNERGY-<sibling>.md`.
    - **Omit `bm-entity` entirely** — a private name in a Basic Memory path would
      leak it (the validator warns if present).
    - Create the gitignored content file `PRIVATE-SYNERGY-<sibling>.md` from the
      four-section template (it is the sibling's sole synergy file — there is no
      committed `SYNERGY-<sibling>.md`).
    - Verify both `.claude/synergy-registry.local.json` and the
      `PRIVATE-SYNERGY-*.md` wildcard are gitignored (`git check-ignore -q`).
      **Never add a per-name `PRIVATE-SYNERGY-<sibling>.md` line to `.gitignore`**
      — that line would itself commit the name; the `PRIVATE-SYNERGY-*.md`
      wildcard already covers it. If the wildcard is missing, warn the user to
      add the wildcard line (not a per-name one).
    - The preview shows ONLY the `.local.json` block (no committed-registry
      block, no `bm-entity`). Skip the Relationship-into-base step; relationship
      still goes into the `.local.json` entry.
  - One call with `header: "Relationship"` (12 chars). The validator's
    `KNOWN_RELATIONSHIPS` set caps options at six; `AskUserQuestion` caps at
    4 visible options + auto "Other". Surface the four most common —
    `sibling-plugin` (default), `shared-tooling`, `fork`, `consumer` — and
    let the auto "Other" route to a free-text fallback that the workflow
    then validates against the remaining two (`coordinated-release`,
    `dependency`). If the user types anything else, warn that the value will
    trigger a `validate-plugin.mjs` warning and confirm before writing. See
    `references/synergy-entry-format.md` "Relationship vocabulary" for the
    canonical set.
  - Only when `../<sibling>/` does not resolve to an accessible directory, a
    second call with `header: "Local path"` (10 chars) — free-text or
    skip. If the user provides a path, it goes into
    `.claude/synergy-registry.local.json`, never into the base registry.

- **Preview both files in a single message** before writing anything. Use
  this shape (omit the `.local.json` block when no local-path was
  supplied). Show BOTH the placeholder schema and a worked substitution so
  the user can see how `<this-project>` and `<sibling>` resolve. **Annotate
  auto-derived fields with their source** as inline comments after rendering
  (e.g. `"remote": "https://github.com/voxpelli/vp-claude"  # from <sibling>
  git origin`, `"bm-entity": "engineering/agents/..."  # canonical
  convention`) so the user can spot derivation errors before approving:

  ```
  Proposed .claude/synergy-registry.json (schema):
  [
    {
      "name": "<sibling>",
      "file": "SYNERGY-<sibling>.md",
      "remote": "<derived-or-blank>",
      "bm-entity": "engineering/agents/vp-plugins-<this-project>-and-<sibling>",
      "relationship": "<chosen>"
    }
  ]

  Worked example (this-project = vp-beads, sibling = vp-knowledge):
  [
    {
      "name": "vp-knowledge",
      "file": "SYNERGY-vp-knowledge.md",
      "remote": "https://github.com/voxpelli/vp-claude",
      "bm-entity": "engineering/agents/vp-plugins-vp-beads-and-vp-knowledge",
      "relationship": "sibling-plugin"
    }
  ]

  Proposed .claude/synergy-registry.local.json (only if local-path given):
  [
    { "name": "<sibling>", "local-path": "<path>" }
  ]

  Confirm? [yes / edit / skip]
  ```

- **Handle the user's response.** On `yes`, proceed to write. On `edit`,
  re-prompt each derived field individually so the user can correct
  `name`, `remote`, `bm-entity`, `relationship`, or the optional
  `local-path`, then re-render the preview. On `skip`, continue the
  workflow without writing the registry — resume to step 2.

- **Write the files using the `Write` tool.** Always write
  `.claude/synergy-registry.json`, and additionally write
  `.claude/synergy-registry.local.json` only when a `local-path` was
  provided. The `.local.json` is always a separate file — never embed
  `local-path` in the committed base registry.

- **Verify round-trip.** Use the `Read` tool to re-read each written file,
  then validate the JSON via
  `node -e 'JSON.parse(require("fs").readFileSync(process.argv[1],"utf8"))' <path>`
  (any non-zero exit signals invalid JSON). Confirm: base registry contains
  entries with `name` and `file` set; if `.local.json` was written, it
  contains `name` and `local-path`. On base-registry parse failure or
  missing required fields, abort step 1b — report the problem and offer to
  re-run; do not proceed to step 2 with a broken base registry. On
  `.local.json` parse failure only, warn and continue without the local
  override (the base registry is still usable).

- **Check that `.local.json` is gitignored** when one was written:

  ```bash
  git check-ignore -q .claude/synergy-registry.local.json
  ```

  Exit status semantics: `0` = file is gitignored (no action); `1` = file
  is **not** gitignored — warn the user with the exact line to add: "Add
  `.claude/*.local.json` to your `.gitignore` (covers both
  synergy-registry.local.json and vendor-registry.local.json, and is
  forward-compatible with future `.local.json` registries)." Do not
  auto-edit `.gitignore` — it is user-owned. `128` = the check itself
  failed (not a git repo, or another git error) — report the underlying
  error and skip the gitignore warning rather than emitting a
  false-positive.

- **Resume to step 2** (Basic Memory pre-check).

2. **Basic Memory pre-check.** If Basic Memory MCP tools are available, make
   two `mcp__basic-memory__search_notes` calls: one with the sibling project
   name, one with 2-4 keywords describing the topic being logged (e.g.,
   "PreCompact prompt command hook" or "edit\_note append gotcha"). If either
   search returns a matching note with synergy-related or engineering-pattern
   content, surface it to the user: "This pattern is already tracked in Basic
   Memory: \[summary]. Logging it locally as well so this project tracks it."
   If Basic Memory tools are not available, skip this step silently.
3. If no `SYNERGY-<project>.md` file exists yet, create it from the template
   in `references/synergy-entry-format.md` (four sections with placeholders).
4. Classify the entry into one of the four sections:
   - **Shared Pattern** — the same approach exists in both projects
   - **Divergence** — the projects handle this differently
   - **Extraction Candidate** — this project has something worth extracting
   - **They Have / We Don't** — the sibling has something we lack
5. Read the target file. **If the entry is proprietary** (names a private
   sibling's internal paths, client names, or unreleased plans that must not
   reach a public repo), target the gitignored `PRIVATE-SYNERGY-<project>.md`
   overlay instead of the committed `SYNERGY-<project>.md` (see
   `### Private overlay`). Before the first write to a new overlay, verify it is
   ignored: `git check-ignore -q PRIVATE-SYNERGY-<project>.md` (exit 0 = ignored,
   safe; exit 1 = NOT ignored — stop and have the user add `PRIVATE-SYNERGY-*.md`
   to `.gitignore` first). Then, **only for a public sibling that has a committed
   `SYNERGY-<project>.md`**, add a one-line pointer to that committed file
   (e.g. "*A private `PRIVATE-SYNERGY-<project>.md` overlay exists for this
   sibling.*") so collaborators know it may exist. **For a fully-private sibling**
   (registered only in `.local.json` with `file: PRIVATE-SYNERGY-<name>.md`),
   there is **no** committed `SYNERGY-<name>.md` and you write **no** pointer — a
   pointer would commit the private name. Otherwise (a public sibling, ordinary
   entry) target the committed `SYNERGY-<project>.md`.
6. Compose the entry from this project's perspective using the entry format from
   `references/synergy-entry-format.md`. Focus on impact and adoption cost, not
   implementation internals.
7. Add the entry under the correct section heading, using today's date. When
   adding the first entry to a section, replace the `_No entries yet._`
   placeholder. Keep entries concise — 1-3 sentences. The title should be
   scannable. **Entries written to a `PRIVATE-SYNERGY-*.md` overlay are never
   promoted to Basic Memory or reciprocated to a sibling** (privacy invariant —
   structurally enforced by the prefix).

**Structured fields** (all optional — omit fields that add no signal):

| Field               | Values                                                  | Section                                     |
| ------------------- | ------------------------------------------------------- | ------------------------------------------- |
| `Status:`           | `aligned` · `drifting`                                  | Shared Patterns                             |
| `Last verified:`    | `YYYY-MM-DD` (use today's date for new entries)         | Shared Patterns                             |
| `Convergence path:` | `accept-difference` · `adopt-theirs` · `propose-shared` | Divergences                                 |
| `Readiness:`        | `ready` · `needs-cleanup` · `proof-of-concept`          | Extraction Candidates                       |
| `Priority:`         | `adopt-soon` · `consider` · `deferred`                  | They Have / We Don't                        |
| `Effort:`           | `trivial` · `moderate` · `significant`                  | Extraction Candidates, They Have / We Don't |

See `references/synergy-entry-format.md` for full entry format templates and
field value definitions.

**Bilateral reciprocation mandate.** When the sibling has already written
entries from their side (resolve the sibling path via the registry-with-override
pattern from workflow 3 (Compare with sibling) — `local-path` from the merged
registry, falling back to `../<sibling>/`; check
`<resolved-path>/SYNERGY-<this-project>.md` if the sibling repo is accessible
on disk), reciprocate by re-verifying each
entry from this project's angle, recording your verification dates, and
noting any drift you observe. Do not skip duplicates — the reciprocation IS
the verification step. As captured in BM
`engineering/agents/vp-plugins-vp-beads-and-vp-knowledge`:

> SYNERGY entries describe two parallel implementations that *happen* to be
> aligned, not one shared thing — both sides need their own record so each
> can verify from their POV at their own cadence. "Reciprocation IS the
> verification step."

Sprint 19 evidence: vp-claude reciprocated 9 shared-pattern entries from
vp-beads's `SYNERGY-vp-knowledge.md` to a new `SYNERGY-vp-beads.md`, and the
re-verification surfaced 3 actively drifting artifacts
(`validate-plugin.mjs` 358 vs 333 lines; `scripts/check-hooks.mjs` 366 vs
284 lines; `npm-run-all2` since-converged) plus 1 stale `aligned` row
(PreCompact retired post-v0.28.0 on the vp-claude side). When logging an
entry with no reciprocal yet on the sibling, prompt the user to file the
reciprocal entry on the sibling project (typically a follow-up task in the
sibling repo's bd backlog).

8. **Eager promotion check.** If Basic Memory MCP tools are available, assess
   the project's tempo:

   ```bash
   git rev-list --count --since="90 days ago" HEAD 2>/dev/null
   ```

   Guard: skip if the repo has zero commits total
   (`git log --oneline -1 2>/dev/null` returns empty). Also skip if this is
   the first entry in any SYNERGY file for this project (the user is still
   learning the workflow — promotion is premature).

   | Tempo        | Commits in 90 days | Promotion behavior                                           |
   | ------------ | ------------------ | ------------------------------------------------------------ |
   | **Dormant**  | 0–4                | Offer inline promotion for any promotable entry              |
   | **Moderate** | 5–14               | Offer only for Extraction Candidates with `Readiness: ready` |
   | **Active**   | 15+                | Skip — the normal sprint cadence handles promotion           |

   When offering inline promotion, say: "This project has low commit
   frequency — SYNERGY entries can sit unread for months. This entry looks
   promotable to Basic Memory. Want to promote it now?"

   If the user agrees, defer to workflow 5 (Promote to Basic Memory) for the
   actual write — invoke its single-entry path scoped to this entry (steps 3-4
   of workflow 5 (Promote to Basic Memory)). Step 8 only **offers** promotion;
   workflow 5 (Promote to Basic Memory) **performs** it. This split keeps
   `## Cross-Project Synergy` writes within workflow 5 (Promote to Basic Memory)'s
   sole-owner boundary.

   If the user declines, or if Basic Memory tools are not available, or if the
   project is active, skip silently.

### 2. Review open synergies

Summarize the current state of all synergy tracking files.

**Steps:**

1. Glob for all `SYNERGY-*.md` files and read them. **This is the one local-only
   review, so ALSO glob `PRIVATE-SYNERGY-*.md` private overlays** and assemble
   the combined view per `### Private overlay`: merge public + private entries
   per section and **label every private (`PRIVATE-SYNERGY`-sourced) row
   `[local]`**. When a `[local]` entry shares a title with a committed entry,
   show **both** (committed row `[committed, shadowed]`, private row `[local]`)
   so the promotable public twin stays visible. A `[local]` row is review-only:
   never offer it as a reciprocation or Basic Memory promotion candidate (those
   paths glob `SYNERGY-*.md`, which structurally cannot reach
   `PRIVATE-SYNERGY-*.md`).
2. Present a summary grouped by file, showing counts per section and listing
   each open entry with title and date.
3. Flag stale entries (older than 3 months with no activity). A Trend Review
   entry resets the staleness clock for the entire file.
4. Highlight actionable items:
   - Extraction Candidates with `Readiness: ready` — extractable now
   - Divergences with `Convergence path:` of `adopt-theirs` or `propose-shared`
   - They Have / We Don't with `Priority: adopt-soon`
5. **Inverse-file glob staleness detection (optional).** For each sibling
   represented by a `SYNERGY-<sibling>.md` file on this side, attempt to
   read the inverse file — the sibling's `SYNERGY-<this-project>.md` —
   to surface cross-side drift that single-side review cannot detect.
   Reuse the registry-with-override path-resolution pattern from workflow 3
   (Compare with sibling): prefer the `local-path` field on the merged
   `.claude/synergy-registry.json` + `.claude/synergy-registry.local.json`
   entry (relative paths resolve from the current project root); if absent,
   fall back to `../<sibling>/SYNERGY-<this-project>.md`. `<this-project>`
   is this project's canonical name derived per
   `references/project-name-derivation.md` (tiers 1–4, sibling
   back-pointer first; in the common case the registered sibling's own
   registry resolves it immediately).

   **Bilateral first.** When the sibling repo is accessible AND the user wants
   more than a single-side enrichment — full reciprocation gaps, status drift
   in both directions, auto-reciprocation — defer to `/sibling-sync`
   workflow 2 (Sync sibling SYNERGY) instead. Step 5 here only surfaces
   inverse-file findings as a side-channel of the single-side review;
   `/sibling-sync` is the authoritative bilateral tool.

   **Degradation.** If the registry is missing, the sibling path does not
   resolve, the inverse file is not present, or any read fails for any
   reason, **skip this step silently and continue with the regular
   single-side review.** Never hard-fail. The inverse-file step is a
   best-effort enrichment, not a gate.

   When the inverse file IS accessible, surface two classes of drift:

   - **Stale `aligned` rows** (staleness threshold: workflow 4
     (Trend review (quarterly)) canonical — `Last verified:` more than two
     trend-review cycles, ≈8 sprints). Entries marked `Status: aligned` on
     this side whose corresponding entry on the sibling side shows measurable
     drift — either the sibling lists the entry under `## Divergences`
     (contradicting our `aligned`), or the sibling's entry carries
     `Status: drifting`, or the sibling has annotated the entry as
     resolved/retired. The motivating example: vp-knowledge retired
     `PreCompact` in v0.28.0 while this project's
     `SYNERGY-vp-knowledge.md` still tagged `PreCompact aligned 2026-04-05`
     — no automated detection caught the staleness until manual
     reciprocation. Flag each such row with the sibling's contradicting
     state so the user can reconcile.
   - **Missing-this-side rows.** Features the sibling tracks under
     `## Shared Patterns` (or any section) that no longer exist in this
     project — typically because this project retired the feature without
     updating the sibling-tracked entry. Surface them so the user can
     either re-add the feature, mark the entry as resolved on both sides,
     or escalate to `/sibling-sync` for bilateral reconciliation.

   For deeper bilateral reconciliation (reciprocation gaps, status drift
   in both directions, auto-reciprocation), defer to `/sibling-sync`
   workflow 2 (Sync sibling SYNERGY) — workflow 2 (Review) here only
   surfaces inverse-file findings as part of the single-side review
   summary.

**Output format:**

```
## Synergy Status

### <project-name>

- Shared Patterns: N (N drifting)
- Divergences: N (N with active convergence path)
- Extraction Candidates: N (N ready)
- They Have / We Don't: N (N adopt-soon)
- [list each entry with title and date]

### Notes

- [stale entries]
- [actionable items]
- [inverse-file findings, if any: stale aligned rows, missing-this-side rows]
```

If all files are empty or no SYNERGY files exist, say so and suggest whether a
comparison run (workflow 3 (Compare with sibling)) would be useful — note that it
works best when the sibling repo is accessible on disk at the registry-resolved
path (`local-path` from the merged `.claude/synergy-registry.json` +
`.claude/synergy-registry.local.json`, falling back to `../<project-name>`).

**Source.** The inverse-file glob step is sourced from
`../vp-claude/UPSTREAM-vp-beads.md` entry 3 (2026-05-04).

### 3. Compare with sibling

Perform a direct comparison between this project and a named sibling to surface
unlogged synergy observations.

**Steps:**

1. Identify the sibling from the user's request or the `argument-hint` — if
   the user named a project, use that name directly without re-asking. Load
   the registry with override merge:

   1. Read `.claude/synergy-registry.json` for the sibling's `remote` and any
      metadata.
   2. If `.claude/synergy-registry.local.json` exists, read it and merge it on
      top of the base registry. Match entries by the `name` key (the
      human-stable identifier across machines and BM entity paths); for each
      matched entry, fields present in `.local.json` win. A `.local.json`-only
      entry (no matching base `name`) is **added** as a private sibling when its
      `file` is `PRIVATE-SYNERGY-<name>.md`, and otherwise **ignored** (the base
      registry is the authoritative source of which *public* siblings exist).
      See `references/synergy-entry-format.md` "Private sibling entries".

   If no project is identified from the argument, merged registry, or existing
   SYNERGY files, ask the user which sibling project to compare with.
   If no registry exists at all, also offer to create one via workflow 1 (Log a synergy entry) step 1b before proceeding with the comparison.
2. **Gather sibling context.** Resolve the sibling's local path: prefer the
   `local-path` field on the merged registry entry (relative paths are resolved
   from the current project root); if absent, fall back to `../<project-name>`
   relative to the current project root. If the resolved path is not
   accessible, ask the user for the path (and suggest they record it in
   `.claude/synergy-registry.local.json` to avoid re-prompting). Read the
   sibling's key files if accessible:

   - `package.json` — dependencies, scripts, entry points
   - `CLAUDE.md` — conventions, architecture, workflow documentation
   - Skill files (`Glob` for `skills/**/SKILL.md`) — what skills exist, their
     workflows, trigger phrases
   - Hook definitions (`hooks/hooks.json`) — event handling patterns
   - Agent files (`Glob` for `agents/*.md`) — what agents exist

   If neither local files, conversation context, nor Basic Memory provides
   substantive information about the sibling, stop and tell the user that a
   meaningful comparison requires access to the sibling repo or prior
   knowledge. Do not generate speculative entries.
3. **Diff patterns.** Compare against this project's equivalent files.
   Identify observations in each of the four categories:
   - Shared Patterns: conventions both projects use (same frontmatter fields,
     same BM integration approach, same commit style)
   - Divergences: structural or stylistic differences (different hook handling,
     different reference doc organization, different BM section ownership)
   - Extraction Candidates: logic in this project that would apply to the
     sibling (validation scripts, shared reference formats, utility functions)
   - They Have / We Don't: features or patterns in the sibling absent here
     (agents, skills, hooks, conventions this project lacks)
4. **Propose new entries.** Present each observation as a candidate entry with
   draft text matching the format in `references/synergy-entry-format.md`. For
   each, ask: "Log this as a \[category] entry for \[sibling]?" The user
   approves, edits, or skips each candidate. **No mutations without approval.**
5. Log confirmed entries by classifying, reading the file, composing, and
   adding per workflow 1 (Log) steps 4–7. Skip step 8 (eager promotion) for batch
   entries to avoid prompt fatigue. Offer a single summary at the end:
   "N entries logged. Run workflow 2 (Review) to review the full picture."

   If the user skips all candidates, report that no entries were logged and
   suggest whether a follow-up comparison with different focus areas would be
   useful.

### 5. Promote to Basic Memory

Promote generalizable cross-project synergy entries from project-local
`SYNERGY-*.md` files into sibling project entity notes in Basic Memory. This
creates or extends a `## Cross-Project Synergy` section in the target sibling
note (typically at `engineering/agents/vp-plugins-<this-project>-and-<sibling>`).
Use only MCP tools from this skill's `allowed-tools` —
`mcp__basic-memory__search_notes`, `mcp__basic-memory__read_note`,
`mcp__basic-memory__edit_note`. If Basic Memory MCP tools are not available,
report that promotion is unavailable and suggest checking Basic Memory manually.

**Steps:**

1. **Scan for candidates.** Glob all `SYNERGY-*.md` files and read them. (This
   glob structurally excludes every `PRIVATE-SYNERGY-*.md` — both private
   *overlays* of public siblings and the sole content file of a *private
   sibling* registered via `.local.json`. Neither is ever promoted; their names
   must never reach Basic Memory. See `### Private overlay` and
   `references/synergy-entry-format.md` "Private sibling entries".) Filter
   eligible entries by section + structured fields:
   - Extraction Candidates with `Readiness: ready` (always)
   - Shared Patterns with `Status: aligned` (always)
   - Shared Patterns with `Status: drifting` (flag the drift in the draft)
   - Extraction Candidates with `Readiness: needs-cleanup` or
     `proof-of-concept` (lower priority — surface but mark as such)
   - Divergences with `Convergence path: adopt-theirs` or `propose-shared`
     (skip `accept-difference` — by definition not promotion-worthy)
   - They Have / We Don't with `Priority: adopt-soon` (skip `deferred`)
   - **Skip any entry already annotated with `_(Promoted YYYY-MM-DD)_`** —
     that annotation is the dedup signal written in step 4 below.
2. **Present candidates to the user.** Per-entry, never auto-promote. For
   each candidate, show:
   - Sibling project name and target BM note path
   - Section (Shared Pattern / Divergence / Extraction Candidate / They
     Have / We Don't) and entry title
   - A draft generalized version. Apply the transforms documented in
     `references/synergy-bm-format.md`: strip dates from titles,
     project-specific file paths, sprint numbers, and bd issue IDs;
     rewrite the prose from a neutral symmetric POV (so any sibling can
     read the entry as authoritative); keep `Status:`, `Convergence path:`,
     `Readiness:`, `Priority:`, and `Effort:` fields verbatim because they
     carry cross-project meaning.
   - Whether a Basic Memory note already exists for this sibling.
     Let the user approve, edit, or skip each candidate.
3. **Route by target.** For each approved candidate, look up the sibling's
   `bm-entity` value from `.claude/synergy-registry.json` (with
   `.claude/synergy-registry.local.json` merged on top by the `name` key).
   If `bm-entity` is present, use it as the BM note path. If absent, call
   `mcp__basic-memory__search_notes` with the sibling project name and
   surface the candidate matches to the user. **Legacy `bm-entity` form
   warning:** if the registered `bm-entity` does NOT start with
   `engineering/agents/vp-plugins-` (the canonical convention from v0.12.1
   onward), warn the user before proceeding: "Registered bm-entity
   `<value>` does not match the canonical
   `engineering/agents/vp-plugins-<this-project>-and-<sibling>` form. This
   may be a pre-v0.12.1 registry pointing at a single-project entity note
   (e.g. `npm/<sibling>`) — workflow 5 (Promote to Basic Memory) will
   write to that legacy location, which may scatter cross-project content.
   Recommended: update the registry to the canonical form and migrate any
   existing `## Cross-Project Synergy` content to
   `engineering/agents/vp-plugins-<this-project>-and-<sibling>` first." Ask
   the user whether to proceed anyway, abort, or migrate. **Stale
   `bm-entity` fallback:**
   if `bm-entity` is present but step 4's `read_note` returns not-found
   (the registry path has been renamed or deleted), warn the user
   ("BM note not found at `<bm-entity>` — registry may be stale") and
   fall through to `mcp__basic-memory__search_notes` exactly as the
   absent-`bm-entity` row does. The full routing table — including the
   fallback search order (`engineering/agents/` for relationship notes,
   then `projects/` and `npm/` as last-resort fallbacks for unregistered
   siblings) — lives in `references/synergy-bm-format.md`.
4. **Write or flag.** Three branches per approved candidate:
   - **Note exists, has `## Cross-Project Synergy` with target subsection** —
     call `mcp__basic-memory__read_note` first to fetch exact content, then
     `mcp__basic-memory__edit_note` with `find_replace` anchored to the next
     `###` heading for uniqueness, `expected_replacements=1`. Deduplicate by
     entry title (case-insensitive, whitespace-trimmed) before appending — if
     the title already appears in the subsection, skip. If `find_replace`
     returns zero replacements despite `expected_replacements=1`, the note was
     edited between `read_note` and `edit_note` — do NOT annotate the local
     entry; defer this candidate (increment a deferred-count) and continue
     with the next candidate. The step 6 report includes deferred entries
     under "deferred (BM note changed mid-write): N entries — re-run
     workflow 5 (Promote to Basic Memory) once BM writes settle." Do NOT
     re-invoke workflow 5 (Promote to Basic Memory) automatically inside
     the same run; persistent contention would otherwise loop.
   - **Note exists, no `## Cross-Project Synergy` section** — call
     `mcp__basic-memory__edit_note` with `insert_before_section` on
     `Relations` to add the full section block (all five subsections per the
     template in `references/synergy-bm-format.md`).
   - **No note exists** — do NOT create a thin note. Flag for enrichment:
     "No Basic Memory note for `<sibling>`. Enrich it first (manual creation
     under `engineering/agents/`), then re-run workflow 5 (Promote to Basic
     Memory)."
   - **After successful write,** annotate the local SYNERGY entry with
     `_(Promoted YYYY-MM-DD)_` via the `Edit` tool. This is the dedup signal
     that step 1 consults on subsequent runs.
   - See `references/synergy-bm-format.md` for `edit_note` gotchas (never
     use `append` with `section`, always `read_note` first, anchor
     `find_replace` matches to the next `###` heading).
5. **Prune pass.** For entries already annotated `_(Resolved ...)_` in the
   local SYNERGY file, offer to move the corresponding BM entry to the
   `### Resolved` subsection of `## Cross-Project Synergy` in the sibling
   note. The user confirms each. Mirrors upstream-tracker workflow 6
   (Promote to Basic Memory) prune-pass behavior.
6. **Report.** Summarize: promoted count, pruned count, skipped count
   (already-promoted), and flagged-for-enrichment count. Suggest verifying
   the result with
   `build_context("memory://engineering/agents/vp-plugins-<this-project>-and-<sibling>")`.

See `references/synergy-bm-format.md` for the target section structure,
generalization transform rules, and `edit_note` gotchas.

**Division of labor:** This workflow owns the `## Cross-Project Synergy`
section of sibling project entity notes in Basic Memory. The
upstream-tracker skill's workflow 6 (Promote to Basic Memory) owns
`## Upstream Friction` in package/tool entity notes. The retrospective
skill's step 7 owns `engineering/*` notes (patterns, conventions, lessons).
These three sections never overlap — synergy entries are cross-project,
upstream friction is package-specific, learnings are domain-specific.

### 4. Trend review (quarterly)

Every 4th sprint, perform a cross-cutting analysis of all SYNERGY tracking
files. This cadence aligns with the every-4th-sprint trend review used by
`/retrospective` and `/upstream-tracker` (see CLAUDE.md and MEMORY.md). It
replaces the interim workaround of running workflow 2 (Review) manually at
trend-review boundaries.

**Input signals:**

1. Glob for all `SYNERGY-*.md` files and read them. (Trend review is a
   boundary-crossing path — step 5 cross-references Basic Memory and step 8
   recommends workflow 5 (Promote to Basic Memory) — so private overlays must be
   excluded; the `SYNERGY-*.md` glob does this structurally, since it cannot
   match `PRIVATE-SYNERGY-*.md`. Private entries are reviewed via workflow 2
   (Review)'s local-only view, never trend-promoted. See `### Private overlay`.)
2. For each file, count entries per section (Shared Patterns, Divergences,
   Extraction Candidates, They Have / We Don't) and note the date of the last
   Trend Review entry, if any.
3. Compute entry aging from the parenthesized `(YYYY-MM-DD)` on each bullet.
   Flag entries older than 3 months without a follow-up Trend Review note.

**Processing steps:**

1. **Drift audit.** For every Shared Patterns entry marked `Status: aligned`,
   check whether the `Last verified:` date is more than two trend-review cycles
   old (≈8 sprints). Flag stale `aligned` rows — alignment claims decay; the
   Sprint 19 reciprocation pass on `SYNERGY-vp-knowledge.md` surfaced one such
   row (PreCompact retired post-v0.28.0 on the sibling side) that had no way
   to be detected without re-verification.
2. **Reciprocation check.** For each shared-pattern entry, ask whether the
   sibling project has a corresponding entry in its own `SYNERGY-<this-project>.md`.
   Resolve the sibling path via the registry-with-override pattern from
   workflow 3 (Compare with sibling) — `local-path` on the merged registry
   entry, falling back to `../<project-name>`. Where the resolved path is
   accessible, glob for the reciprocal file and grep for the entry title.
   Asymmetric tracking silently misses drift — see workflow 1 (Log) bilateral
   reciprocation mandate.
3. **Status sweep on Extraction Candidates.** List all Extraction Candidates
   with `Readiness: ready` that have not moved (no annotation, no resolution)
   for more than 2 trend-review cycles (≈8 sprints). These are either
   stalled — escalate to a beads issue — or no longer relevant — recommend
   closing.
4. **They Have / We Don't sweep.** List entries with `Priority: adopt-soon`
   older than one trend-review cycle (≈4 sprints). Either adopt now or
   downgrade to `consider`/`deferred`.
5. **BM cross-reference.** Cross-reference each open entry against the
   `## Cross-Project Synergy` section in the corresponding BM entity note
   (workflow 5 (Promote to Basic Memory) populates this) to identify
   entries already promoted (no need to re-promote) and entries that should
   be promoted now.
6. **Dormancy-aware scaling.** In projects with ≤4 commits in the last 90 days
   (see project tempo in Guidelines), double the staleness thresholds — entries
   in dormant repos age by calendar, not by sprint cadence.
7. Add a per-file Trend Review entry to each SYNERGY file under a
   **Trend Reviews** section. A Trend Review entry resets the staleness clock
   for the entire file (see workflow 2 (Review) staleness rules). If no
   **Trend Reviews** section exists at the bottom of the file, create it
   before adding the entry.
8. Present aggregate findings to the user. Suggest follow-up actions: open
   beads issues for stalled extractions, run workflow 5 (Promote to Basic
   Memory) for promotion candidates, or downgrade stale `adopt-soon`
   entries.

**Trend Review entry format** (mirrors upstream-tracker workflow 4 (Trend Review)):

```
### Review — YYYY-MM-DD (Sprint N)

- **Themes:** [common patterns across open entries — e.g., recurring drift in
  validation tooling, shared infra still un-extracted]
- **Still valid:** [entries confirmed as still relevant this cycle]
- **Recommend closing:** [entries obsolete, dismissed, or no longer applicable]
- **Escalate:** [stalled Extraction Candidates needing beads issues; stale
  `aligned` rows needing reciprocation refresh; `adopt-soon` items past their
  window]
```

**Output integration with `/retrospective`:** at trend-review sprint boundaries
(every 4th sprint), `/retrospective` chains into this workflow's per-file
review entries and includes a "Synergy trend review" subsection summarizing
themes and escalations across all SYNERGY files.

## Sprint Workflow Integration

synergy-tracker runs as a parallel track to upstream-tracker at sprint
boundaries:

- **Sprint end:** sprint-review agent globs `SYNERGY-*.md` alongside
  `UPSTREAM-*.md` and reports extraction candidates. `/retrospective` includes
  a "Synergy observations" section.
- **Sprint start:** session-start hook emits a dormancy nudge for SYNERGY files
  in low-activity repos.

Workflow 5 (Promote to Basic Memory) is invocable as
`/synergy-tracker workflow 5 (Promote to Basic Memory)` and writes generalized synergy entries into
the `## Cross-Project Synergy` section of sibling project entity notes.
Workflow 4 (Trend Review) feeds it by surfacing promotion candidates at
trend-review boundaries.

## Guidelines

- **Consumer perspective.** Write entries from this project's point of view.
  Focus on impact: "We can't reuse the validation logic without copying it"
  rather than "The validation function in vp-knowledge is not exported."
- **Scope boundary with upstream-tracker.** Package-specific friction always
  goes to upstream-tracker, even if discovered via sibling comparison.
  synergy-tracker tracks patterns, practices, and capabilities — not bugs or
  API issues in shared dependencies.
- **Registry awareness.** Always check `.claude/synergy-registry.json` before
  globbing for `SYNERGY-*.md`. The registry is the authoritative source for
  sibling project metadata.
- **No thin BM notes.** Never create a Basic Memory note for a sibling project
  as a side effect of promotion. If no note exists, flag for enrichment and
  stop.
- **Stale threshold.** Individual entries are stale after 3 months without
  activity. A Trend Review entry resets the staleness clock for the entire file.
- **No auto-mutations.** Every proposed entry requires explicit user approval
  before being logged. Never write to SYNERGY files or Basic Memory without
  confirmation.
- **Private overlays never cross the boundary.** Entries in a
  `PRIVATE-SYNERGY-<project>.md` overlay are private to this checkout: never
  promote them to Basic Memory and never reciprocate or write them to a sibling.
  This is enforced structurally — every boundary-crossing path globs
  `SYNERGY-*.md`, which cannot match the `PRIVATE-` prefix — which is what makes
  the overlay safe for proprietary↔public sibling pairs.
- **Division of labor.** synergy-tracker owns `## Cross-Project Synergy` in
  sibling project entity notes in Basic Memory (workflow 5 (Promote to Basic Memory)). upstream-tracker
  owns `## Upstream Friction` in npm/tool entity notes. retrospective owns
  `engineering/*` notes. These three sections never overlap.
- **Project tempo classification.** Measure with
  `git rev-list --count --since="90 days ago" HEAD 2>/dev/null`: **dormant**
  (0–4 commits), **moderate** (5–14), **active** (15+). Dormant and moderate
  repos get earlier promotion nudges at workflow 1 (Log) time.
- **Design rationale: why cross-project tracking lives in Basic Memory, not bd.**
  The bd v1.0.0 Integration Charter (`gastownhall/beads@5d524cf7:docs/INTEGRATION_CHARTER.md`)
  establishes a "no cross-tracker orchestration" rule — bd will never grow a
  feature that routes a synergy item from project A's bd to project B's bd.
  synergy-tracker's `SYNERGY-*.md` files plus the `## Cross-Project Synergy` BM
  section (workflow 5 (Promote to Basic Memory)) are exactly the
  workflow-automation layer the Charter punts to external tools.
