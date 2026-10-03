---
name: releases
description: Read, synthesize, diagnose, clean, author, and publish the releases.db planning ledger (or legacy RELEASES.md where retained) through one routed workflow. Use for /releases; release status or health checks; stale-plan review against merged PRs, commits, and CHANGELOG entries; disciplined release creation or updates; ledger cleanup; historical anchors or backfill; publishing a planned GitHub Release; or deciding whether Radar or Finish Line is the better follow-up. Default invocation is read-only and every write or publication requires a preview and confirmation.
---

# /releases — one release-planning router

Treat the release ledger as an optional forward-looking planning aid, never as a second
`CHANGELOG.md`. Start every invocation by reading and synthesizing the ledger. Route into a mutating
subroutine only when the operator explicitly chooses or requests one.

## Routes

```text
/releases                         read-only synthesis, findings, and relevant route choices
/releases check [window]          refresh the evidence-backed health assessment
/releases clean [version|active]  preview a spec-aligned cleanup
/releases plan [version]          create or explicitly update an upcoming release
/releases anchor <version...>     add only the named shipped historical anchors
/releases backfill                show eligible historical anchors as an optional menu
/releases publish <version>       publish one planned entry to GitHub
```

Natural-language requests route the same way. Do not make the operator remember the route names.

## The DB's second subsystem — the ROADMAP shadow (GH-69)

`releases.db` also mirrors `ROADMAP.md`'s ledger (`roadmap_items`, one-way, lossless). This skill
does not own roadmap edits — `ROADMAP.md` stays the human file — but if a task you are part of
edited that ledger, finish with `releases roadmap sync` (a no-change sync is a free no-op;
`--dry-run` previews, `roadmap list` reads back). Contract: RELEASES-DB-FAQS.md.

## Preflight

1. Resolve the repository root. Require `utils/pdda/pdda.sh`; stop if PDDA is absent because there
   is no fallback release-ledger format.
2. **Detect the ledger backend (GH-32 / GH-568).** If `releases.db` exists at the repository root, this repo
   is **app-managed**: the SQLite database is the sole source of truth (`RELEASES.md` is retired per GH-568),
   and **every mutation this skill performs MUST go through the
   `releases` CLI (`utils/py/releases_app.py`).**
   If `releases.sql` exists at the repository root but `releases.db` is absent, the ledger is in an
   incomplete state — stop with an error prompting `releases check --rebuild`.
   Only if neither app-managed marker (`releases.db` nor `releases.sql`) exists is this a **legacy-managed**
   repo where legacy `RELEASES.md` procedures apply.
3. Read `PROJECT/PDDA.md`'s release ledger contract, `releases.db` (or `RELEASES.md`), and
   `CHANGELOG.md`. A missing, empty, sparse, or apparently old ledger is valid. In an app-managed
   repo, also run `releases check` and surface any findings before proceeding.

   **In an app-managed repo, read the ledger through the CLI's readers, not raw SQL.** All three
   are read-only, take no lock, and mutate nothing:

   ```text
   releases next [--verbose]        the next unshipped release, by target date
   releases show --version 0.6.0    one full record (or --gid; --full disables elision)
   releases list [--status ...]     one line per release (--all-repos aggregates siblings)
   ```

   There is no generated Markdown mirror of the database to read: `RELEASES-PREVIEW.md` was removed
   2026-08-19. For a whole-ledger view, use `releases list`, open `releases.db` in a SQLite viewer,
   or read the release cards `releases project sync` (GH-39) pushes to GitHub Projects.

   **After any merge that touched the ledger, run `releases check` before anything else.** The
   merge procedure resolves `releases.sql` as text and then requires `releases check --rebuild` to
   regenerate the DB from it; skipping that leaves a DB that disagrees with the dump, and the DB is
   what every reader above trusts. `test/gh32-releases-artifacts.sh` gates this on every full-suite
   run, but it catches the mistake after the fact — checking first is cheaper. Never run
   `--rebuild` to make a red check go away without reading what diverged: it is for merge
   resolution only, never crash recovery. See [RELEASES-DB-FAQS.md](https://github.com/HiQS-Labs/XYZ-forge/blob/development/RELEASES-DB-FAQS.md).
3. Treat GitHub as optional for checks and required for publication. If `gh` is unavailable, run
   the local assessment and state exactly which PR, milestone, issue, or Release conclusions are
   unavailable. Never convert missing network evidence into a clean verdict.
4. Parse a block from one `Release:` line to the next `Release:` line or end of file. Blank lines do
   not end blocks.

## Default route — read and synthesize

Run this route before every other route unless the same invocation already established fresh state.

1. Run `utils/pdda/pdda.sh releases` and `utils/pdda/pdda.sh releases-current`. Preserve their
   warn-only semantics.
2. Select the evidence window: use an operator-supplied window, otherwise 21 days. Resolve the
   active integration branch from repo policy (`development` in this repo; otherwise the declared
   WIP branch, then `main`/`master`). State the exact dates and branch.
3. Read reachable non-merge commits plus merged and closed-unmerged PRs targeting that branch during
   the window. Use merged PRs as completion evidence. Surface a closed-unmerged PR only when it
   contradicts a block's claim that work is in flight or materially changes the cleanup decision.
   A push is transport, not evidence; count the commits that reached the branch. Read exact
   bracketed versions and dated entries from `CHANGELOG.md`.
4. When GitHub is available, inspect matching releases, milestones, and manifest issues. Verify PR
   base branches and merge state before using them as evidence.
5. Summarize, without dumping the file:
   - shipped entries;
   - active and upcoming entries, target dates, iteration bands, and milestones;
   - strong inconsistencies and advisory drift signals;
   - description or manifest discipline warnings;
   - evidence that could not be obtained.
6. Offer only routes relevant to the findings or the user's stated goal. Make no writes.

## Staleness and drift rules

Call something stale only when evidence contradicts a block, not because the ledger is sparse or
has not changed recently.

Treat these as strong inconsistencies:

- `CHANGELOG.md` records the exact version as shipped while the block remains unshipped.
- A GitHub Release exists but `GH_URL:` is empty, points elsewhere, or `Status:` contradicts the
  actual publish state.
- `Target Date:` is past while `Status:` is not `Shipped`.
- A block says work is open, absent, or unbuilt while a merged PR, reachable commit, or canonical
  project document proves the opposite.
- Iteration bands overlap or a non-owner release sits inside another block's band.

Treat these as advisory drift signals:

- Recent merged work materially follows a different theme than an active description.
- A manifest contains replaced, duplicated, unrelated, or silently added scope.
- A target date no longer fits explicit dependencies or the observed delivery rate.

Do not infer shipment from a closed-but-unmerged PR, an issue closure alone, a branch push, a commit
on an unmerged branch, or a populated `GH_URL:` that points to a draft.

## Discipline and abuse warnings

Warn, without blocking, when:

- `Description:` exceeds four sentences, becomes multi-paragraph execution history, or duplicates
  `CHANGELOG.md`. Recommend a one-to-four-sentence theme and move history to `CHANGELOG.md` and
  implementation detail to the canonical `PROJECT/**` document.
- `Manifest:` names more than seven issues. The count triggers review, not condemnation.
- A manifest mixes unrelated themes, lacks a fixed denominator, grows without a dated re-scope,
  crosses several release dependencies, or has no runnable/observable exit criterion.
- A block copies an issue inventory that should be represented by the `Milestone:` join key.

Explain which signal fired. Never call a large manifest abusive solely because of its issue count.

## Clean subroutine

1. Default to active/unshipped blocks. Touch a shipped block only when the operator explicitly names
   it.
2. Propose the smallest cleanup that restores the documented shape: compact descriptions, preserve
   theme and dependencies, reduce manifests to a fixed list or milestone pointer, preserve dated
   re-scope decisions, and move historical narrative to `CHANGELOG.md` or execution detail to its
   existing project doc. Never create a new doc merely to shorten the ledger.
3. **App-managed repo:** render the cleanup as the exact `releases update --gid <id> ...` (and
   `releases manifest ...` / legacy-line disposition) command set, preview those commands, and get
   one confirmation. On confirmation run them, then finish with `releases check`.
   The CLI's own preimage/lock handling replaces the hash dance below.
4. **Legacy-managed repo:** record the file hash before preview. Render the exact patch and get one
   confirmation. Immediately before writing, re-read `RELEASES.md` and compare its hash. If it
   changed, discard the patch, synthesize again, and preview a new patch. Edit only the confirmed
   blocks. Never reorder unrelated blocks.
5. Run `utils/pdda/pdda.sh releases` and report every finding.

## Plan or update subroutine

1. Apply the admission rule. A block earns a place only when it represents a named arc worth
   planning toward. A restatement of shipped changes belongs only in `CHANGELOG.md`. A version inside
   another block's `Iterations:` band is already accounted for.
2. If no version was supplied, compare the highest bracketed `CHANGELOG.md` version with the highest
   ledger version. Propose the next semantic version and explain the patch/minor/major judgment; let
   the operator override it.
3. Ask only for unanswered fields:
   - status;
   - optional iteration band;
   - target date or blank/TBD;
   - optional codename;
   - optional GitHub milestone title;
   - a one-to-four-sentence description of the theme;
   - optional concise manifest;
   - optional executable or observable exit criterion;
   - optional QA fields (`Front-door reviewed`, `Shakedown reviewed`, `License file`).
4. Draft the flat block below, omitting blank optional fields except `GH_URL:` when publication is
   expected:

```text
Release: 1.2.0
Iterations: 1.2.0-1.2.4
Status: Draft
Target Date: 2026-12-01
Codename: Example
Description: One coherent release theme in no more than four sentences.
Exit criterion: `command --that-proves-the-release` exits 0.
Manifest: FROZEN YYYY-MM-DD — #101, #102, #103.
GH_URL:
Milestone: Example
Front-door reviewed: No
Shakedown reviewed: No
License file: Yes
```

5. **App-managed repo:** preview the equivalent `releases add ...` (or `releases update --gid ...`)
command set — including the required tracking issue (a real URL, or a `TMP-` ref if GitHub is down)
— and get one confirmation, then run it. **Legacy-managed repo:** preview the complete new or
replacement block and get one confirmation. Re-check the file hash before writing. Append new blocks
after the last block; replace only an explicitly selected existing block. Never silently edit
neighboring blocks.
6. Run `utils/pdda/pdda.sh releases` and report findings.

## Anchor and backfill subroutine

Run only when explicitly requested.

- For `anchor`, draft exactly the shipped versions the operator named. Trace each one-line summary
  to its bracketed `CHANGELOG.md` section and set `Status: Shipped`. In an app-managed repo the
  draft is a previewed `releases add ... ` + `releases ship ...` command pair, not a file patch.
- For `backfill`, show bracketed `CHANGELOG.md` versions that are not already represented and do not
  sit inside an existing iteration band. Present them as an optional menu, never as missing work.
  Draft only the versions the operator selects; drafting none is valid.
- Never initiate either route because the ledger looks incomplete.

## Publish subroutine

1. Require `gh` authentication and a specific existing release block. Stop if it is already
   `Shipped`. If `GH_URL:` exists but status is unshipped, inspect the existing Release and ask how
   to handle the draft or conflicting object.
2. Run `utils/pdda/pdda.sh releases` and surface its findings.
3. Build release notes from the block's `Description:` plus concise codename, exit-criterion, and
   manifest context when useful. Never invent notes. Ask for missing release-facing prose.
4. Preview together:
   - the exact `gh release create <version> --title ... --notes ...` action;
   - the full release body;
   - the `GH_URL:` and `Status: Shipped` write-back.
5. Get one explicit confirmation, publish live, and capture the returned URL. If creation fails,
   report the error verbatim and make no ledger edit.
6. On success only: **app-managed repo** — write back via
   `releases update --gid <id> --gh-release-url <url>` and `releases ship --gid <id> --evidence ...`
   (never a direct file edit); **legacy-managed repo** — re-check the file hash, write the returned
   URL, set `Status: Shipped`. Then run `utils/pdda/pdda.sh releases` either way.
7. Remind the operator that shipped history and lessons belong in `CHANGELOG.md`; do not write that
   entry unless separately asked.

## Complementary routing

Offer at most one goal-matched follow-up; do not append generic reminders.

- Offer `/radar` when the question is whether recent work, recurring defects, and release themes are
  strategically aligned. State that Radar is broader than this ledger check and owns its own report
  workflow. Never copy Radar's analysis into this skill or invoke it automatically.
- Offer `/finish-line` when the operator has selected a release checkpoint and wants a frozen,
  shortest safe path to ship it. State that Finish Line owns the done-list and parking workflow.
  Never invoke it automatically.
- Stay within `/releases` when the task is ledger synthesis, cleanup, authoring, or publication.

## Guardrails

Schema009 adds nullable exact `roadmap_items.status_label` (`in-progress` or NULL).
Only accepted starts establish it; metadata/migration/backfill never infer one
from old markers. NULL is not proof of completion. Use the existing command
`roadmap update --gid OWNED_ROW --accepted-start` after approved execution admission;
it validates owned URL/native open issue, refuses PRs and preserves repeated starts.
Use `--dry-run` to preview. Schema migration and remote projection remain opt-in.

An explicitly configured `work_connectors.github_labels` block with `enabled: true`
and `repos: ["owner/repository"]` projects only that exact label. No default network
calls; failures retain replay cursors. Native direct closes require preview-first
`roadmap reconcile-state`, then `--apply`. For terminal cleanup drift, use
`work reconcile --connector github_labels --reset` when witnessed events exist;
for zero-event Completed/Deferred rows, seed `work emit --event label_repair
--roadmap-gid OWNED_ROW`, then reconcile. This qualified repair is labels-only,
not a start/completion claim, and unestablished NULL/open issues are preserved.
Disabling this connector rolls back projection, not the schema; old writers are
unsupported against migrated ledgers because their digests/dumps omit the field.

- Default to read-only synthesis.
- In an app-managed repo (`releases.db` present) every mutation goes through the `releases` CLI;
  never edit `RELEASES.md` directly there (`RELEASES.md` is retired in this repo per GH-568).
  Preview the exact command set instead of a patch — the confirmation UX is unchanged, only the write path moves.
- Preview every file mutation and public action; obtain one confirmation per atomic write/publication
  group.
- Re-read before writing and refuse stale patches.
- Never top up the optional ledger, fabricate release notes, or treat absence as failure.
- Keep `CHANGELOG.md` authoritative for shipped history and `PROJECT/**` authoritative for execution
  detail.
- Use repo-relative paths in edited documents.
- Never create, edit, install, or synchronize a Codex skill from this workflow.
