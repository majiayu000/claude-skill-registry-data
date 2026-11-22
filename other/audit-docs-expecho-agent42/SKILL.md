---
name: audit-docs
description: Verify every claim in CLAUDE.md and .agentic/ against the actual code and report drift. Run periodically, after large refactors, or before a release.
user-invocable: true
argument-hint: "[optional: area to limit the audit to]"
---

# Audit agent docs against code

Docs drift; this skill is the immune system. Every claim is a hypothesis — verify
it by reading code, not by plausibility. (The triage discipline here is adapted from
the workspace `experts-*-improve` family: sync first, then Add/Update/Remove-stale
per entry, then a before/after report.)

## Step 0 — Sync gate

Offer to `git pull` first — auditing docs against a stale checkout produces false
verdicts in both directions.

## Step 1 — Mechanical pass

Run `node .agentic/scripts/check-doc-paths.mjs`. Fix or flag every missing path.

Also check gotchas.md size: if it exceeds ~40 entries, flag it. The fix order is
(1) demote entries that could be lint rules/analyzers, (2) move rationale-shaped
entries to ADRs, (3) delete stale ones — and only if 40+ survive, propose the
by-area split described in the gotchas.md header. Bloat there means the `/gotcha`
admission test lapsed; treat it as a finding, not a filing problem.

## Step 2 — Semantic pass (parallelize with `scout` subagents on big repos)

Dispatch one `scout` subagent (`.claude/agents/scout.md` — cheap tier, read-only)
per area/claim-batch to do the verification reading; the Add/Update/Remove triage
in step 3 stays in the main session.

For each of:
- **CLAUDE.md commands table:** run each command (or `--help`). Broken → fix table.
- **CLAUDE.md stack/rules/notes:** confirm each statement against config and code.
- **gotchas.md constraints:** for each entry, open the evidence file and check the
  claim still holds. Holds → bump `verified:` date. Doesn't → correct or delete.
- **gotchas.md exemplars:** confirm each exemplar still embodies the canonical
  shape (compare against 2–3 recently-written instances of the same pattern; if
  the codebase has moved on, point at a newer exemplar).
- **Active ADRs** (no `superseded_by`): spot-check that the decision is still what
  the code does. Code moved on → that's an undocumented supersession; draft the
  new ADR via `/decide` with the user.
- **quality-gates.yaml:** compare thresholds against actual CI configuration.

## Step 3 — Triage every finding as Add / Update / Remove

- **Add** — code reveals a trap or exemplar the docs miss (apply the `/gotcha`
  admission test before adding).
- **Update** — claim is directionally right but details moved; fix and re-date.
- **Remove** — the constraint no longer exists or the file is gone. Removing stale
  entries is the highest-value action in this skill; do not skip it out of caution.

## Step 4 — Report and fix

Produce a before/after summary: entries checked, added, updated, removed, plus a
drift table (claim | file | OK / STALE / BROKEN | action taken). Apply
uncontroversial fixes directly (dates, paths, corrected claims); ask before deleting
entries or superseding ADRs. Zero findings is a valid, reportable result.
