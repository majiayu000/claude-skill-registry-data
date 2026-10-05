---
name: nudge
description: "This skill (explicit /nudge only) manages Claude Code feature-adoption nudges sourced from the Basic Memory note main/reference/claude-code-noteworthy-features. Bare /nudge = Mode A (sync): re-read the note, filter out features already marked adopted or declined, and regenerate the tip cache ~/.claude/references/claude-code-nudge-tips.txt that the SessionStart hook reads. /nudge check = Mode B (adoption check): scan Claude Code session transcripts across all projects for real evidence of feature use, preview proposed adoption-status transitions, write approved changes to the note's frontmatter, then regenerate the same cache. No delegate agent exists (unlike knowledge-garden/knowledge-maintain, whose graph-wide phrasing routes through their agent) — natural-language phrasing like 'sync nudge tips' or 'nudge me on unused features' does NOT auto-invoke this skill; recognize the intent and suggest the user run `/nudge` or `/nudge check` explicitly."
user-invocable: true
disable-model-invocation: true
argument-hint: "[check]"
allowed-tools:
  - Grep
  - Read
  - Write
  - mcp__basic-memory__read_note
  - mcp__basic-memory__edit_note
---

# Nudge

Manage the Claude Code feature-adoption nudge cycle against the Basic Memory
note `main/reference/claude-code-noteworthy-features`. Two modes on the same
data (same note, same cache, same contract):

- **Bare `/nudge` (or no argument) → Mode A (sync).** Re-read the note, filter
  out adopted/declined features, and regenerate the tip cache.
- **`/nudge check` → Mode B (adoption check).** Scan transcripts for real
  feature-use evidence, preview status transitions, write approved changes to
  the note's frontmatter, then regenerate the same cache.

Route by the argument: no argument / sync phrasing → Mode A; `check` / adoption
phrasing → Mode B.

**Intentionally Claude-Code-specific, not a template for a generic mechanism.**
This skill hardcodes the note permalink
(`main/reference/claude-code-noteworthy-features`) and Claude-Code slug
vocabulary — a deliberate, stated exception to this project's general
domain-generic-skill convention, because the whole task is specifically about
Claude Code feature adoption.

The single rule and line grammar both modes share when regenerating the cache
live in [`references/tip-cache-contract.md`](references/tip-cache-contract.md) —
the single source of truth, so the two independent write paths never drift.

## Mode A: sync

Follows the same vendor-sync pattern as `tag-sync`: registry (BM note) → fetch
via MCP → filter → write to a synced local file the SessionStart hook
(`hooks/tip-fragment.sh`) reads without ever touching Basic Memory. Always
re-fetches on invocation — no same-day guard (`read_note` is one cheap call and
the hook already throttles tip display to once/day independently).

### Step 1: Fetch the note

```
mcp__basic-memory__read_note(
  identifier="main/reference/claude-code-noteworthy-features",
  output_format="json",
  include_frontmatter=true
)
```

On failure or an empty/malformed result, report the error and exit **without
writing** — never overwrite a working cache with partial content. A missing note
is reported, never auto-created (that's `/intel`'s kind of job, not this
skill's). Zero `[nudge]` observations is a legitimate state — write an empty
cache file.

### Step 2: Filter

For each `[nudge]` observation, extract its trailing `Feature: <slug>` token.
**Check the slug-uniqueness invariant first** (see
[`references/tip-cache-contract.md`](references/tip-cache-contract.md)): if any
two tokens normalize to the same slug, report the colliding lines and stop.
Otherwise look up `adoption-<slug>` in frontmatter (absent → `unseen`) and apply
the exclusion rule: exclude a line whose value, trimmed and lowercased, is
`adopted` or `declined`.

### Step 3: Write

Build the filtered list of lines **verbatim** from the note (see the contract
file's line-grammar section — never reformat or truncate) and `Write` them to
`~/.claude/references/claude-code-nudge-tips.txt` — a plain full-file overwrite,
matching `tag-sync`'s convention. The reader degrades gracefully on a partial
read, so no temp-file-and-rename dance.

### Step 4: Report

```markdown
## Nudge Tips Synced

File: ~/.claude/references/claude-code-nudge-tips.txt
Tips: <N> eligible (<M> excluded as already adopted)
```

## Mode B: adoption check

Mirrors `session-reflect`'s scan → preview → approve → write shape, but scans
*historical* transcripts across all projects.

### Error handling

- **Note missing** — report and exit; never auto-create it (that's `/intel`'s
  kind of job).
- **No `[nudge]` observations** — report "No features to check adoption for" and exit.
- **`~/.claude/projects` doesn't exist** (a "Path does not exist" tool error,
  not a clean zero-match) — the **benign** fresh-install case. Propose `nudged`
  for anything `unseen`, skip the rest; do NOT report it as a failure.
- **Either Step-2 sanity grep returns zero matches, or errors with anything
  other than the missing-directory signature** — genuine tool/mechanism
  failure; report and stop rather than proposing `nudged` on possibly-broken data.
- **A single slug's grep is a clean zero-match** — normal no-evidence; propose
  `nudged` if currently `unseen`.
- **A single slug's grep errors, or every matched file fails to `Read`** — report
  it as scan-failed in the preview and exclude it from any transition this run.
- **Some (not all) matched files for a slug fail to `Read`** — exclude only the unreadable files from evidence and keep evaluating the readable ones; never let one unreadable file suppress an `adopted` transition when another matched file already passed. Flag the count in the Step 4 preview ("N files could not be read and were excluded") even when the slug still proceeds to `adopted`. When no readable file passes either, route the slug to the scan-failed bucket rather than confidently proposing `nudged`.
- **A slug's tip has no backtick span (empty search term)** — skip and report it.
- **`edit_note` `find_replace` fails** — re-read, retry once against the current
  frontmatter value, then report and stop. Do not loop.
- **User declines all** — report "No changes made" and exit.

### 1. Load the catalog

```
mcp__basic-memory__read_note(
  identifier="main/reference/claude-code-noteworthy-features",
  output_format="json",
  include_frontmatter=true
)
```

Collect each `[nudge]` observation's `Feature: <slug>` token + tip text, and each
current `adoption-<slug>` frontmatter value (absent → `unseen`). **Check the
slug-uniqueness invariant** ([`references/tip-cache-contract.md`](references/tip-cache-contract.md)):
report a collision and stop before proposing any transitions.

### 2. Gather evidence

Follow [`references/evidence-detection.md`](references/evidence-detection.md) IN
FULL — the two once-per-invocation sanity checks, the per-slug search-term
derivation, the slash-command-vs-prose branch, and the Shape A/Shape B
genuine-dispatch confirmation. It searches transcripts by content directly and
deliberately does **not** build a `Glob`-based "recent files" working set (that
shipped a real silent bug — the reference explains why). Its dogfood-hardened
prose documents specific fixed false-positives; do not paraphrase it. Known
constraints that need no fix are listed in
[`references/adoption-limitations.md`](references/adoption-limitations.md).

### 3. Compute transitions

| Current status | Evidence found this scan | Proposed transition |
|---|---|---|
| not `adopted` | yes | `adopted` |
| `unseen` | no | `nudged` |
| anything else | no | unchanged, skip silently |

### 4. Preview and wait

````markdown
## Feature Adoption Check

### Evidence found — proposing "adopted"
- **goal** — 3 sessions

### No evidence yet — proposing "nudged"
- **rewind** — "Restores the conversation to an earlier point..."

### Scan failed — excluded this run
- **btw** — Grep call errored partway through; evidence may exist but couldn't be confirmed
- **fork** — 2 of 5 matched files could not be read and were excluded; the 3 readable files showed no evidence

Approve all, approve one (e.g. "approve goal"), or decline.
````

Never write anything before this gate.

### 5. Write approved changes

For each approved change, `edit_note` with `find_replace` anchored strictly
*inside* the YAML frontmatter block, never spanning a `---` marker (the Sprint-24
safe-edit pattern, avoiding the duplicate-frontmatter bug):

```
edit_note(
  identifier="main/reference/claude-code-noteworthy-features",
  operation="find_replace",
  find_text="adoption-<slug>: <old-status>",
  content="adoption-<slug>: <new-status>"
)
```

Re-read the note once afterward to confirm the value actually changed. On any
status change, regenerate the local tip cache directly with `Write`, using **this
step's own confirmation re-read** (not the stale Step-1 catalog) and the shared
filter/grammar in [`references/tip-cache-contract.md`](references/tip-cache-contract.md).
Write to `~/.claude/references/claude-code-nudge-tips.txt` — a plain overwrite,
matching Mode A's convention. This closes the loop with the SessionStart hook
without a second MCP read or a shell-out to Mode A.

### 6. Report

```markdown
## Nudge Adoption Complete

Updated: N (goal -> adopted, ...)
Declined: M
Skipped (no change): K
```

## Additional Resources

- **[`references/tip-cache-contract.md`](references/tip-cache-contract.md)** — the
  exclusion rule and cache line grammar both modes use.
- **[`references/evidence-detection.md`](references/evidence-detection.md)** — the
  Mode B transcript-scan detection procedure.
- **[`references/adoption-limitations.md`](references/adoption-limitations.md)** —
  accepted constraints of the transcript-evidence approach.
