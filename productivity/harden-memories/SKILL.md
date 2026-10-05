---
name: harden-memories
description: "Audit the `bd remember` store and recommend which entries to prune, so each one earns its per-session `bd prime` injection cost. Read-only: it proposes a triage table plus the exact `bd forget` / migration commands; you run them. Use when `bd remember` entries have accumulated, feel stale, redundant, or conflicting, or when session-startup token cost from injected memories is high. Trigger phrases: 'harden memories', 'audit bd remember', 'prune bd remember', 'bd remember bloat', 'bd remember audit', 'trim bd remember', or '/harden-memories'. NOT for Claude Code auto-memory (`/dream` / Auto Dream files), NOT for Basic Memory graph hygiene (use vp-knowledge's memory-defrag / memory-lifecycle skills), and NOT for beads issues or the backlog (use /backlog-groomer)."
user-invocable: true
paths:
  - ".beads/**"
allowed-tools:
  - Bash
  - Read
  - mcp__basic-memory__search_notes
  - mcp__basic-memory__read_note
---

# Harden Memories

Audit the project's `bd remember` entries and recommend which to prune down to
the few that genuinely earn their cost. `bd prime` injects **every** `bd remember`
entry in full at session start (they are persisted in the beads Dolt database),
so entries accumulate as a silent, scaling token tax — conventions drift, skills
ship, and facts graduate to CLAUDE.md / the auto-memory `MEMORY.md` / Basic
Memory, but nothing automates the cleanup until a manual pass. Periodic audits
(≈ every 4 sprints) reliably recover \~40% of that token budget.

**This skill is READ-ONLY by design.** It audits and *proposes* — it never edits
a durable file, never writes to Basic Memory, and never runs `bd forget` itself.
For each entry it presents a recommendation plus the exact command(s) for **you**
to review and run. This deliberately keeps the irreversible step (`bd forget`,
which destroys the only copy of a fact) and the migration write under your
control — no automated "verify-then-delete" can be trusted to gate an
irreversible delete (a Basic Memory write can fail `schema_validate`
asynchronously; an `Edit` can land in the wrong file; an append can hit the
wrong section). Proposing keeps you in the loop for both halves.

**Scope — strictly the `bd remember` store.** NOT Anthropic's Auto Dream /
`/dream` (which prunes Claude Code auto-memory files, a different store), and NOT
Basic Memory graph hygiene (defer that to vp-knowledge's graph-maintenance
skills). It audits `bd remember` and nothing else.

## Beads availability

Beads is available iff a `.beads/` directory exists **and** `command -v bd`
succeeds; this component is **Tier B** per CLAUDE.md
`### Beads-availability convention`. The `bd remember` store only exists when
beads does — with no beads there is nothing to audit. Stop cleanly, naming the
missing predicate (no `.beads/` directory, or `bd` not on `PATH`). There is no
beadless equivalent to redirect to.

## Workflow

### 1. Read the current memories

```bash
bd memories --json
```

Returns a JSON object keyed by memory key. **Keep only entries whose value is a
string** — memory entries are always strings; scalar metadata (e.g.
`schema_version`) are numbers or booleans:

```bash
bd memories --json | jq 'to_entries | map(select(.value | type == "string")) | from_entries'
```

The surviving entries are the audit set. If there are none, report that there is
nothing to prune and stop.

### 2. Classify each entry

For every entry, run the canonical three-question checklist (from Basic Memory
`engineering/agents/three-memory-systems-taxonomy-and-graduation`):

1. **Already in Basic Memory or the auto-memory `MEMORY.md` / CLAUDE.md? →
   recommend remove.**
2. **Describes stable project-architecture state? → recommend migrate** (to
   CLAUDE.md for a project working-instruction, the auto-memory `MEMORY.md` for
   project state, or Basic Memory for generalizable engineering knowledge), then
   remove.
3. **Only helps recover from context loss mid-task? → recommend keep.**

To answer question 1, cross-reference each entry against the live sources:

- `Read` CLAUDE.md (small enough to read whole) and scan for the entry's key
  facts. (The auto-memory `MEMORY.md` lives outside the repo at the Claude Code
  project memory path — name it as a target in proposals, but you need not read
  it here.)
- Call `mcp__basic-memory__search_notes` with 2-4 keywords from the entry. **For
  any match, `mcp__basic-memory__read_note` and confirm the specific fact is
  actually present** before recommending `remove` — a keyword co-occurrence is
  NOT confirmation of capture. If you cannot confirm the fact is captured, do
  not recommend `remove`.

Tag each entry with the bloat category that justifies its disposition:
**redundancy** (duplicates a live source), **staleness** (describes a state that
no longer holds — e.g. an entry that says "STALE" or names a shipped/abandoned
plan), **granularity drift** (early-project specifics that became standard
practice), or **conflicting** (contradicts another entry or a live source).

### 3. Present the triage table

| Key     | Summary  | Category                                     | Recommendation                     | Rationale |
| ------- | -------- | -------------------------------------------- | ---------------------------------- | --------- |
| `<key>` | one line | redundancy / staleness / drift / conflicting | remove / migrate→`<target>` / keep | one line  |

### 4. Present the action plan (do not execute)

For the user to review and run. Group by disposition:

- **migrate→`<target>`** — show the **drafted text** to add and the **explicit
  target** (a named CLAUDE.md section; the auto-memory `MEMORY.md`; or a Basic
  Memory note path + section). For the auto-memory `MEMORY.md`, give its real
  path — `~/.claude/projects/<project-slug>/memory/MEMORY.md`, where
  `<project-slug>` is the project's absolute path with `/` → `-` — and **ask the
  user to confirm it** rather than emitting a bare `MEMORY.md` (which would
  resolve to a non-existent repo-root file). Then the `bd forget` command,
  clearly marked "run only after you have written and verified the migration":

  ```bash
  bd forget <key>   # after the fact is durably captured at <target>
  ```

  For a Basic Memory target, note the gotcha: use `edit_note` with `find_replace`
  / `insert_before_section`, never `append` with a `section` (it appends to
  end-of-file, not end-of-section).
- **remove** — show the evidence that the fact is already captured (which source,
  confirmed in step 2), then the command:

  ```bash
  bd forget <key>   # already captured elsewhere or no longer true
  ```

  Note for the user: `bd forget` prints `No memory with key "..."` and exits 1 if
  the key is already gone (benign); any other non-zero exit is a real failure
  (DB locked/missing) worth investigating — verify with `bd memories`, not the
  exit code.
- **keep** — no command; the entry earns its injection.

### 5. Report

Summarize: recommended-remove count, recommended-migrate count (with each
target), keep count, and the approximate per-session token reduction if the user
applies the removals (entries removed × their injected length). Note that the
audit cadence is ≈ every 4 sprints.

## Guidelines

- **Read-only — propose, never execute.** This skill never edits a file, writes
  to Basic Memory, or runs `bd forget`. It presents recommendations and exact
  commands; the user performs the irreversible write and delete steps, keeping
  both under explicit human control.
- **Graduation before deletion (in the proposed order).** A fact worth keeping
  must be migrated to its durable home and confirmed there **before** its
  `bd forget` is run. The action plan always presents the migration first and
  marks the `bd forget` as "run only after the migration is verified."
- **Conservative pruning.** When unsure whether an entry still earns its cost,
  recommend keep and flag it for the next audit rather than recommending
  removal. Signal preservation beats aggressive trimming.
- **Confirm capture before recommending remove.** A keyword search hit is not
  proof a fact is captured — read the matched note/section and verify the
  specific fact is present (step 2). A false "already captured" recommendation,
  if acted on, is data loss.
- **Keep the survivors short.** `bd remember` entries are injected every session;
  a kept entry should be a single-sentence recovery trigger. If a kept entry is
  long, propose tightening it (the user re-runs `bd remember` with `--key` to
  upsert) as part of the audit.
- **Scope boundary.** This skill audits only `bd remember`. Basic Memory graph
  hygiene (orphans, schema, duplicate notes) belongs to vp-knowledge's
  graph-maintenance skills; do not perform it here.
