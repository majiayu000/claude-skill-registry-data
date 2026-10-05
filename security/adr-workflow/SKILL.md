---
name: adr-workflow
description: >
  Scaffold, accept, index, and link Architectural Decision Records (ADRs).
  Use when the user says "write an ADR", "record this decision", "resolve
  [deferred item] with an ADR", "supersede ADR-NNNN", or otherwise wants to
  capture a hard-to-reverse decision in `docs/decisions/`. Also use when a
  refinement-todo entry needs to be marked RESOLVED with a link back to the
  ADR. Do NOT use for ad-hoc design discussion that hasn't crystallized into
  a decision yet — wait until the choice is firm.
user-invocable: true
---

> Spec 005 created this skill from scratch. The mechanics live in `adr.py`;
> Claude owns the judgment (what the decision actually says).

## What this skill does

Codifies the ADR lifecycle that ADR-0001 and ADR-0002 were written by hand to
exercise. Five deterministic operations:

- **`new`** — scaffold `docs/decisions/adr-NNNN-<slug>.md` from the template, with
  auto-numbering and a slug-collision check. The scaffold carries
  `status: Proposed` in frontmatter (from the template) alongside the prose
  `Proposed (date)` line (spec 073-02 / ADR-0026).
- **`accept`** — stamp the canonical `status: Accepted` frontmatter field and
  flip the prose Status line to `Accepted (YYYY-MM-DD)` in the **same** atomic
  write. Frontmatter is the authoritative status home; the prose line is a
  best-effort mirror, rewritten only when it is canonical
  (spec 073-02 / [ADR-0046](../../docs/decisions/adr-0046-adr-status-frontmatter-authority.md),
  which supersedes ADR-0026).
- **`supersede`** — append `Superseded by [ADR-NNNN](./adr-NNNN-<slug>.md) (date)`
  to an Accepted ADR's Status block and `Supersedes ADR-NNNN` to the replacement's
  Status block, and stamp the **old** ADR's `status: Superseded` frontmatter field
  in the same atomic write (the replacement retains `status: Accepted`). This is
  the **one** edit allowed on an immutable ADR per the Nygard convention. Atomic
  write on both files.
- **`index`** — regenerate the `## Index` section of `docs/decisions/README.md`
  from the actual ADR files present. Idempotent. The index is a **pure
  function of the ADR files**; see [section 4](#4-regenerate-the-index) for
  what that means for hand-edits and for records it cannot summarize.
- **`check-index`** — read-only audit of that index: exits non-zero if it no
  longer matches the ADR files, or if two ADRs claim one number. Writes
  nothing.
- **`resolve-todo`** — strike through a `### Decision: ...` heading in
  `docs/refinement-todo.md` and append `**Resolved by:** [ADR-NNNN: ...](...)`.

The script does file mutation deterministically. Claude is responsible for
the prose inside the ADR (Context, Options Considered, Recommended Decision,
Consequences, Open questions).

## How to use

### 1. Author a new ADR

**Reference moved? Reframe first.** If this ADR is a reaction to a *load-bearing
reference* changing from outside the system (a design system, vendor / API
contract, test infra, compliance regime, platform, or product-positioning /
strategic-vision shift), reach for `/jig:reframe` **before** hand-authoring — it
drafts the keystone reframe-ADR (new reference authoritative, old premise
superseded) + the re-baselining manifest for you, so the fallout is dispositioned
rather than patched (spec 067 / [ADR-0024](../../docs/decisions/adr-0024-reference-reframe.md)).

**Step 0 — confirm the project is scaffolded (spec 066 / ADR-0011).**
BEFORE reserving an ADR number or drafting ANY `docs/decisions/` structure,
confirm this project is a scaffolded jig project. If it isn't, **route — do
not hand-roll directories**:

- **Greenfield** (no jig structure yet) → tell the user to run
  `/jig:scaffold-init`. It lays down conventions, templates, hooks, the
  status board, and the `docs/decisions/` tree (with its README).
- **Existing spec/`docs/decisions/` layout, but not jig-scaffolded** (no
  `scaffold.json`) → tell the user to run `/jig:migrate`. It adopts the
  existing layout into jig structure.

You don't have to decide the state yourself: `adr.py new` (below)
**classifies and routes** for you (spec 066-01) — a `scaffold.json`-bearing
project proceeds; a greenfield project is refused naming
`/jig:scaffold-init`; an adoptable spec-driven project is refused naming
`/jig:migrate`. The deterministic gate and this human-readable precondition
agree by construction, so **don't restate the detection heuristic here** —
run the helper and let it route. (Bypass for a deliberate out-of-band flow:
`JIG_SCAFFOLD_PRECONDITION=0`.)

**The anti-pattern this step exists to kill:** an auto-triggered
`adr-workflow` run improvising a loose `docs/decisions/` skeleton (folder +
README, or just dropping an `adr-NNNN-*.md` into a hand-made directory)
because `/jig:scaffold-init` was skipped. That produces a non-jig layout
that then needs migrating — the ADR-side of the reported failure. When in
doubt, route to setup first; never invent the structure by hand.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/adr-workflow/adr.py" new <slug> \
  [--title "<Title>"] [--project-dir DIR] [--no-push | --pr]
```

Run from the project root (the script looks for `./docs/decisions/`,
or use `--project-dir DIR` to target a different root). The slug is
kebab-case (`my-decision`). `--title` is optional — defaults to the
title-cased slug.

**Reserve-on-origin/main is the default (slice 028-01).** The helper
fetches `origin/main`, computes the next free `NNNN` from the
just-fetched view, scaffolds the file, commits as
`docs(decisions): reserve adr-NNNN-<slug>`, and pushes to
`origin/main`. If the push is refused by branch protection /
permissions, the helper automatically falls back to a
`reserve/adr-NNNN-<slug>` branch + `gh pr create`. This locks the
ADR number **team-wide** before any drafting begins, killing the
parallel-worktree numbering-collision failure mode that motivated
spec 028.

**Works from any branch or worktree** (ADR-0015 / spec 051, mirroring
`workflow.py new`). The helper routes on the current branch: on `main`
it runs the proven in-place flow (clean tree required); off `main` — a
feature branch or a linked `.claude/worktrees/*` worktree — it reserves
via an *ephemeral detached worktree* at `origin/main`, never touching
your branch, cwd, or working tree. No need to switch to `main` (a linked
worktree can't, anyway).

Flags:

- `--no-push` — commit locally only; skip fetch / push entirely. On
  `main` it commits on `main`; off `main` it commits a *provisional*
  reservation on the current branch (the number is local-view and may
  collide at merge — treat it as provisional). Pathspec-scoped, so
  unrelated staged work is not swept into the reservation commit.
- `--pr` — skip the direct-push attempt; go straight to branch + PR.
  Useful when you already know main is protection-locked. Mutually
  exclusive with `--no-push`.

Race-on-push (someone advanced `origin/main` while you were
reserving) surfaces as `race-on-push: ...` and drops the stranded
local commit + the stranded ADR file from your working tree. Re-run
the same `adr.py new <slug>` to pick the next free number — there
is no auto-renumber.

Then Claude fills in Context / Options Considered / Recommended Decision /
Consequences. Keep it tight: one decision per ADR.

### 2. Accept the ADR

Once the prose is settled and the human (or the workflow gate) approves:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/adr-workflow/adr.py" accept <NNNN>
```

This stamps the canonical `status: Accepted` frontmatter field and flips the
prose `Proposed (date)` line to `Accepted (date)` in the same atomic write
(spec 073-02 / ADR-0046). Refuses if the ADR is already Accepted (ADRs are
immutable; supersede instead — see below) or Superseded; the refusal names
the state it found.

**Prose is best-effort ([ADR-0046](../../docs/decisions/adr-0046-adr-status-frontmatter-authority.md)).**
The state that gates the flip is read from the frontmatter `status:` field,
falling back to a lenient prose classifier for legacy ADRs — never from the
prose *formatting*. A hand-edited or decorated Status line such as

```markdown
Proposed (2026-07-22) — awaiting owner acceptance.
```

no longer blocks `accept`. The frontmatter flips; the authored line is left
**exactly** as written (never truncated, never rewritten into a
self-contradictory `Accepted (…) — awaiting owner acceptance`), and `accept`
prints a note on stderr naming the file and the value the prose should carry.
**Reconciling that line is your job** — deterministic tooling does not rewrite
prose it cannot fully parse. Until you do, frontmatter and prose are briefly
out of step; every reader in `adr.py` is frontmatter-first, so the divergence
is cosmetic, not behavioural.

**Frame-critique gate (spec 064-05 / ADR-0020 OQ2/OQ3).** `accept` also gates
the flip on a passing adversarial **frame-critique** verdict — the ADR's
pre-commitment moment to catch a wrong premise (the ADR-0011 / ADR-0008 failure
mode). It applies **iff** the ADR carries a truthy `frame_review` flag: `new`
stamps `frame_review: true` on every ADR it creates (OQ3 — ADRs always-on), so
new ADRs are gated; a legacy markerless Proposed ADR is grandfathered (no
refusal). To clear it: build the prompt with `review.py frame-critique
docs/decisions/adr-NNNN-*.md`, run a reviewer, then `review.py record-review
--adr NNNN --pass frame-critique --verdict pass …` (writes
`docs/decisions/reviews/adr-NNNN-frame-critique.md`). Soft / bypassable with
`JIG_REVIEW_EVIDENCE_GATE=0` (a deliberateness signal, ADR-0011 — not human-only
enforcement).

### 3. Supersede an Accepted ADR

When a previously-Accepted decision is replaced by a newer one, **don't edit
the old ADR's prose** — write a new ADR (per `new` above), accept it, then run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/adr-workflow/adr.py" \
  supersede <old-NNNN> <new-NNNN>
```

Both ADRs must already be Accepted. The helper:

- appends `Superseded by [ADR-<new>](./adr-<new>-<slug>.md) (today)` to the
  old ADR's `## Status` block,
- appends `Supersedes ADR-<old>` (plain text, no link, no date) to the new
  ADR's `## Status` block,
- preserves both `Accepted (date)` lines (this is the one edit allowed on
  an immutable ADR per the Nygard convention),
- stamps the **old** ADR's `status: Superseded` frontmatter field in the same
  atomic write (the replacement keeps `status: Accepted`) — spec 073-02 /
  ADR-0026, so a dependency on a superseded ADR correctly fails,
- writes both files atomically.

Refuses (exit 2) if either ADR is Proposed (accept it first), if either
ADR is already Superseded, if `<old> == <new>` (self-supersession), or if
either NNNN is malformed. State is read frontmatter-first, as for `accept`.

Unlike `accept`, `supersede` also refuses when an ADR is Accepted but its
prose `## Status` carries no canonical `Accepted (YYYY-MM-DD)` line: the
supersession lines are *inserted* after that anchor and are load-bearing, so
there is no best-effort path — put the Status line in canonical form and
re-run (ADR-0046 ruling 5). The refusal happens before either file is
written, and it checks **both** ADRs. Re-run `adr.py index docs/decisions`
after to refresh the index entries.

Writing that canonical line needs the acceptance date, and a diverged ADR
does **not** hold it: the prose date belongs to the pre-acceptance state, and
frontmatter `last_verified` is a *freshness* field (`/jig:reframe`'s
`reaffirm` disposition refreshes it), not an acceptance date. The refusal
prints the `git log` invocation that recovers the date from the accept
commit — use that rather than the metadata. Reconciling the prose when
`accept` first warns about it avoids this entirely.

### 4. Regenerate the index

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/adr-workflow/adr.py" index docs/decisions
```

Reads every `adr-NNNN-*.md` (skipping `README.md`) and rewrites only the
`## Index` section of `docs/decisions/README.md`. Everything else in the README
(header, format spec, "When to write" section) is preserved. Re-running on a
current README is a no-op.

**The Index section is derived, never hand-edited.** Each bullet's summary is
generated from that ADR's `## Context` opening, so a better sentence written
straight into the README is overwritten on the next regen. If a row reads
badly, fix the ADR's opening paragraph — that is the summary's source.

**When there is nothing to derive, `index` says so instead of inventing.**
A summary needs a complete sentence to come from. Three openings have none: a
lead-in to a list or a table (the common one), a paragraph that simply lacks a
final period, and a record still carrying the template's `_TODO` stub. Each
renders as `(no description)` with a warning on stderr naming the record and
the reason (bug 020). Before that, the lead-in was written out verbatim —
colon and all — or cut at 120 characters with a trailing `…`, which read like
a summary and was not one:

```
adr.py index: ADR-0040 (adr-0040-richer-skill-discovery-explicit-candidate-channel.md)
  — its `## Context` is still the template stub; rendering (no description).
adr.py index: reword each record's `## Context` opening into a standalone
  sentence and re-run. The index is derived from the ADR files, so the fix
  belongs at the source, not in README.md.
```

The remedy is the one ADR-0006 already prescribes: reword the opening into a
standalone sentence and keep the list behind it. `index` exits 0 either way —
this is a report, not a gate.

**A record with nothing written in it is meant to keep warning.** ADR-0040 on
`main` is a template stub in every section; `(no description)` is the honest
line for it and the warning is the reminder that it is unwritten. Do not
invent decision prose to silence it — write the decision, or leave it.

An authored trailing `…` is not truncation and is left alone: jig no longer
emits one, so an ellipsis in a summary is the author's own writing.

**Audit the index before landing.** `check-index` is a read-only companion to
`index`:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/adr-workflow/adr.py" \
  check-index docs/decisions
```

Exits non-zero on either problem it can find. **Stale index** — an ADR changed
and `index` wasn't re-run (or a summary was hand-edited). **Duplicate ADR
number** — two ADRs claim one number, which is what parallel branches produce
when the number was never reserved on the trunk. The index renders both bullets
without complaint and a staleness check can't see it (both *are* faithfully
derived), so it needs its own detector; the message names both files so you
know which to renumber.

### 5. Resolve a deferred decision

If the new ADR resolves a `### Decision: ...` entry in
`docs/refinement-todo.md`:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/adr-workflow/adr.py" \
  resolve-todo <NNNN> "<heading fragment>"
```

The fragment is a case-insensitive substring (same lenient style as
`workflow.py`'s slice fragment). The helper:

- wraps the heading line in `~~strikethrough~~`,
- appends ` — RESOLVED YYYY-MM-DD`,
- wraps the first `**Deferred:**` line in strikethrough,
- appends a `**Resolved by:** [ADR-NNNN: ...](decisions/adr-...)` line at the end of
  the section.

Refuses (exit 2) if the fragment is ambiguous, the section is already struck
through, or the ADR hasn't been Accepted yet.

## Immutability rule

**Never edit an Accepted ADR.** The Nygard convention treats ADRs as
historical record — if the decision changes, write a new ADR that supersedes
the old one. The supersession lines (one on each side) are the **only**
edit allowed on an immutable ADR. Use the `supersede` subcommand
(section "3. Supersede an Accepted ADR" above) — `adr.py supersede
<old-NNNN> <new-NNNN>` writes those lines deterministically on both ADRs
and refuses self-supersession, Proposed-ADR inputs, or double-supersession.

What the helper does (so you can spot-check the result):

1. Old ADR's `## Status` block gains a line appended after the existing
   `Accepted (date)` line:
   `Superseded by [ADR-<new>](./adr-<new>-<slug>.md) (today)`.
2. New ADR's `## Status` block gains a plain-text line after its
   `Accepted (date)`: `Supersedes ADR-<old>` (no link, no date).
3. Both `Accepted (date)` lines are preserved.

If a user asks to "supersede ADR-NNNN", route them to the `supersede`
subcommand — both ADRs must already be Accepted; if the replacement
isn't drafted yet, walk them through `new` + `accept` for the new ADR
first.

## End-to-end example (full lifecycle)

The canonical lifecycle is `new → edit → index (preview) → accept → index (final)`.
The preview-`index` pass surfaces a truncated or ugly first-bullet line
while the ADR is still mutable (per [ADR-0006](../../docs/decisions/adr-0006-adr-accept-then-index-ordering.md)).
Skip the preview only if the Context first sentence is known to be
index-friendly (no abbreviations outside the helper's allowlist,
fits in one short clause).

```bash
# 1. Identify the deferred decision in docs/refinement-todo.md.
#    Fragment: "scaffold-stable" (matches "### Decision: scaffold-stable …").

# 2. Scaffold the ADR.
python3 .../adr.py new scaffold-stable --title "scaffold-stable trigger"
# → docs/decisions/adr-0003-scaffold-stable.md

# 3. Claude edits the file: fills Context, Options, Recommended, Consequences.

# 4. Preview the index BEFORE accept, while the ADR is still mutable.
python3 .../adr.py index docs/decisions
# Inspect the new bullet line. If it looks wrong (truncated mid-
# abbreviation, missing the key noun, etc.), edit the ADR's first
# Context sentence and re-run this command. Iterate freely.

# 5. Accept.
python3 .../adr.py accept 0003
# → flips Proposed → Accepted (today).

# 6. Final index regen (idempotent re-run; updates only the Accepted line).
python3 .../adr.py index docs/decisions

# 7. Mark the refinement-todo entry resolved.
python3 .../adr.py resolve-todo 0003 "scaffold-stable"
```

## Boundary-change nudge

A `PostToolUse` hook (`jig-boundary-change-warn`) fires on
`Edit`/`Write`/`MultiEdit` of a canonical external-interface
contract-artifact file (OpenAPI `openapi.yaml`/`.yml`/`.json`, AsyncAPI
`asyncapi.yaml`/`.yml`/`.json`, `*.proto`, `*.graphql`/`*.graphqls`, or
`*.schema.json`). It emits a soft `additionalContext` nudge pointing
the author at `/jig:adr-workflow new <slug>` (capture the rationale if
the change is breaking) plus the surface-appropriate breaking-change
ecosystem tool (`buf breaking`, `graphql-inspector diff`,
`redocly diff` / `spectral`, AsyncAPI parser diff, JSON-Schema diff).
The nudge is informational, never a gate — set
`JIG_BOUNDARY_CHECK=0` to silence it. The filename + tool list is sourced
manually from the [contracts skill's per-surface table](../contracts/SKILL.md);
the `contracts` skill is the source of truth for which artifact governs
which surface.

## Gotchas

- **Auto-numbering does not fill gaps.** If `0001` and `0003` exist (no
  `0002`), the next new ADR is `0004`. The gap is preserved as historical
  record.
- **Slug collisions refuse regardless of number.** `adr-0001-foo.md` exists →
  `adr.py new foo` exits 2. Either pick a different slug or write a
  superseding ADR.
- **resolve-todo touches only three lines.** Heading, first `**Deferred:**`
  line, and one new `**Resolved by:**` line appended at the section end.
  Other fields (`**Resolution trigger:**`, `**Mitigation idea:**`,
  `**Watch-list:**`, etc.) are left intact. If a section needs more
  intricate updates, edit it by hand.
- **Index description extraction may produce ugly first lines.** The helper
  takes the first non-empty paragraph from `## Context`, truncating at the
  first sentence-ending punctuation when the paragraph is multi-line, runs
  past 120 chars, or ends in a colon. When it has no complete sentence at
  all, see section 4 — the bullet gets `(no description)` and a warning.
  Common abbreviations (`e.g.`, `i.e.`, `etc.`, `Mr.`, `Dr.`,
  …) are skipped by an explicit allowlist; abbreviations outside that
  list may still cause a mid-word cut. If the resulting bullet reads
  oddly, edit the ADR's first Context sentence to be index-friendly.
  Per [ADR-0006](../../docs/decisions/adr-0006-adr-accept-then-index-ordering.md),
  edits to Context-section *prose* to fix index-rendering are NOT
  decision-content and do not violate the immutability rule. Edits to
  Status, Recommended Decision, or Consequences DO violate immutability
  and require a superseding ADR. Run `index` BEFORE `accept` as a preview
  pass to catch this while the ADR is still freely mutable.
- **The helper does NOT spawn a Task or commit anything.** It only mutates
  files. Claude is responsible for orchestration (e.g. running
  `workflow.py status-board` afterward, writing commit messages,
  invoking the reviewer subagent).
- **Substring matching mirrors `workflow.py`.** `0001-01` does not collide
  with `0001` since ADR numbers are matched as exact 4-digit prefixes,
  not free-form substrings (unlike slice fragments).
- **`adr.py new` is worktree-aware (ADR-0015 / spec 051).** It routes on
  the current branch: on `main` it runs the proven 028-01 in-place flow
  (clean tree required); off `main` — a feature branch or a linked
  worktree — it reserves via an ephemeral detached worktree at
  `origin/main` (push mode) or commits a provisional reservation on the
  current branch (`--no-push`), without disturbing your branch or tree.
  You no longer need to `git checkout main` first (and a linked worktree
  can't, since the primary worktree holds `main`). The earlier
  off-main/dirty-tree refusal — and its impossible `git checkout main`
  workaround — is gone.

## Reconciliation checklist

After using this skill in a real session:

- [ ] Did the index regen produce sensible descriptions, and did it warn
      about any record it could not summarize? For a written record, reword
      its first Context paragraph into a standalone sentence and re-run
      `adr.py index` — the index is derived, so the fix belongs at the
      source. For an unwritten stub, leave the warning: it is the reminder.
- [ ] Was the refinement-todo entry actually resolved by this ADR, or did
      a partial overlap make `resolve-todo` apply to the wrong section?
      Verify before committing.
- [ ] Did the human approve the Recommended Decision before `accept`? If
      not, walk back to the Proposed state by editing the Status line
      (this is the one situation where editing a not-yet-Accepted ADR
      is fine — it's not yet immutable).
