---
name: learn-with-docs-refresh
description: Audit and maintain the learnings in `docs/solutions/` against the current codebase — fix drifted paths and links, merge overlapping docs, replace guidance the code no longer supports, delete obsolete docs, reconcile the `CONCEPTS.md` glossary, then report and commit. Also bootstraps `CONCEPTS.md` on request and, when asked, culls docs whose reasoning the code already explains. Use for "refresh the learnings", "audit docs/solutions", "are our solution docs still accurate", "clean up / prune the learnings", "create a CONCEPTS.md", or after a refactor, rename, migration, or dependency upgrade that likely invalidated documented solutions. Not for capturing a new learning — use `learn-with-docs`.
argument-hint: "[optional scope: directory, filename, module, or keyword] [mode:non-interactive]"
---

# Learn With Docs Refresh

Every learning in `docs/solutions/` should still be true and still distinct. Check each one against the current code, apply what the evidence supports, and deliver a full per-doc report plus a commit. The store is only worth reading if every doc in it can be trusted.

## Hard boundaries

- **Never change product code, skills, runbooks, or instruction files** (except the consented discoverability line). When code violates guidance that has independent support, the guidance stays and the conflict goes in the report as a possible regression.
- **Never archive.** No `_archived/`, no redirect stubs — git history is the archive.
- **Act on contradiction, not on absence.** A claim the repo cannot confirm (an ops practice, an environment behavior) is not false. Age alone is not staleness.
- **No churn.** Never edit for typos, wording, or style alone.

## Paths

| Path | Role |
| --- | --- |
| `docs/solutions/**/*.md` | Candidates, excluding `README.md` and anything under `_archived/` |
| `CONCEPTS.md` (repo root) | Glossary, reconciled each run |
| `AGENTS.md` / `CLAUDE.md` | Discoverability line only, with consent |

READMEs are not reviewed, but when an action deletes, moves, merges, or replaces a doc a README lists, fix its row. If `_archived/` exists, flag it as legacy and recommend what to do with its files.

## Modes

- **Interactive** (default) — apply clear-cut Keep, Update, and Consolidate directly; ask only on real judgment calls (listed in `references/classify.md`). Ask one question at a time, multiple choice, recommended option first. Use the host's question tool when it has one; otherwise ask in chat.
- **Non-interactive** (`mode:non-interactive`) — never pause. Apply safe actions; when a call is ambiguous or Replace evidence is thin, stale-mark the doc instead (`status: stale`, `stale_reason`, `stale_date` in frontmatter). Relocations apply only under the four-condition gate; splits are recommend-only. A failed write becomes a **Recommended** item and the run continues. The report is the deliverable.

## Scope

Strip operation words (`refresh`, `audit`), mode tokens, and worth-lens wording from the arguments; the rest is the scope hint. Narrow with the first match: subdirectory → frontmatter `module`/`component`/`tags` → filename → content keyword. A hint that matches nothing never widens to the whole store — ask (interactive) or report the miss and stop (non-interactive).

Empty store: report `No learnings found in docs/solutions/ — capture one with learn-with-docs after solving a problem.` and stop.

For 9+ docs, triage first: read all frontmatter, cluster by module and category, spot-check that key referenced files exist, and start with the highest-impact cluster (interactive: confirm the starting cluster; work in batches and confirm before continuing). Review learnings before any pattern docs built on them.

## Worth lens (opt-in)

The normal refresh judges accuracy only and never deletes an accurate doc. If the user asks to clean up, cull, prune, or trim the store — any wording that is about value rather than drift — confirm first:

```text
You asked to clean up the learnings. Which do you want?
1. Delete or shorten docs the codebase already explains — each cut quotes the test, comment, or instruction file that states the same reasoning. Drift is fixed too. Scope: <scope>.
2. Fix drift only — stale paths and links, duplicates, guidance the code no longer supports. Nothing accurate is deleted.
```

On option 1, read `references/worth-audit.md` before investigating. Non-interactive runs cannot confirm: they gather the worth evidence but only recommend.

## Workflow

1. **Investigate** — validate all frontmatter in scope in one pass (the whole-store snippet in `references/verify-claims.md`), then read `references/classify.md` (investigation section). Check each doc against the code, then the set for overlap, supersession, and contradiction. Contradictions actively mislead, so they outrank individual staleness.
2. **Classify** — every doc gets one outcome: Keep, Update, Consolidate, Replace, or Delete, under the rules in `references/classify.md`.
3. **Execute** — read `references/actions.md` and follow the flow for each doc's outcome.
4. **Vocabulary** — see below.
5. **Report** — see below.
6. **Commit** — see below.
7. **Discoverability** — read `references/discoverability.md` and follow it. If it edits an instruction file after the commit, amend the unpushed commit or add a small follow-up commit.

## Vocabulary

Read `references/concepts-vocabulary.md` first — its bar is not obvious, so "nothing qualifies" without it is a guess. Then reconcile the terms flagged during investigation:

1. Merge the same term seen with different shades of precision into one entry.
2. **`CONCEPTS.md` exists** — add missing terms, refine drifted ones, backfill missing core nouns, and route every entry in scope that fails the bar to fold, retire, or delete. Scrub violations (implementation details, drifting config values, metadata). An unscoped run covers the whole file; a scoped run stays in its area.
3. **Missing, and a term qualifies** — create it with the preamble, seeding the in-scope area's core nouns.
4. Do not add `(see CONCEPTS.md)` pointers to learnings.

Apply without asking, in both modes.

**Bootstrap requests.** When invoked just to "create CONCEPTS.md" or "build the concept map", ask whether the user wants a repo-wide glossary only (skip the learnings review; seed from the whole project's declared domain model, run discoverability, commit) or a full refresh cycle. Non-interactive defaults to the refresh cycle and notes that no repo-wide bootstrap ran.

## Report

Print the full report as markdown. It is the deliverable, not a summary — never abbreviate it.

```text
Learnings Refresh
=================
Scanned: N
Kept: X · Updated: Y · Consolidated: C · Replaced: Z · Deleted: W · Marked stale: S · Skipped: V
Worth lens: confirmed | recommended-only | off
CONCEPTS.md: <scanned, no qualifying terms | created with N entries | updated — N added, N refined, N folded, N retired, N deleted, N scrubbed>
```

Then for every doc: path, outcome, evidence, and the action taken or recommended. For Consolidate, name the canonical doc, what merged, and what was deleted. Group Keeps under "Reviewed, no changes". Report `retire_when` checks with the date checked.

Split actions into **Applied** and **Recommended**. Recommended holds failed writes (with enough context to apply by hand), relocations that failed the gate, proposed splits, category-shape observations, possible product regressions, named guidance files that contradict a learning, worth-lens cuts in non-interactive mode, and the discoverability recommendation.

## Commit

Skip if nothing changed. Stage only the files this refresh touched, and write the message in the repo's convention (e.g. `docs(solutions): update 3 stale learnings, merge 2 duplicates, delete 1`).

- **Interactive** — ask, recommended option first. On the default branch: new branch + commit + PR / commit here / don't commit. On a clean feature branch: commit here / new branch / don't commit. On a dirty branch: commit only the refresh files / don't commit.
- **Non-interactive** — on the default branch, create `docs/refresh-<area>-learnings`, commit, and try to open a PR (report the branch if that fails). On a feature branch, commit there. On any git failure, put the commands in the report and continue.
