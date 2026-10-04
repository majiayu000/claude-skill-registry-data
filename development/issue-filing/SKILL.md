---
name: issue-filing
description: Create and label GitHub issues (including epics) for kajet-turbo following the project's established conventions — title prefix, body template by type, label mapping, landing on the project board in Inbox, native blocked-by links, epic sub-issues and tracking order, anonymization before publish. Use when filing a new issue, spinning off a follow-up from code review, or creating an epic to track a milestone's execution order. Prioritizing filed issues is backlog-triage; choosing what goes into Next is next-selection.
---

GitHub issues are the only backlog for kajet-turbo — nothing gets mirrored into the kajet notebook. Filing is the first of three stages (filing → `backlog-triage` → `next-selection`); board ids, the priority scale, and blocking rules shared by all three live in [`../_shared/board.md`](../_shared/board.md).

Issues stay open once filed; don't close-with-a-redirect-comment. Closing an issue that turned out already done or superseded is a triage/selection decision, made with the user, per `_shared/board.md`'s Staleness section.

## Title

Every title starts with a prefix — this is the canonical type signal; labels are derived from it, never hand-picked independently.

- `fix:` — current behavior is wrong
- `feat:` — new capability
- `perf:` — performance work, no behavior change
- `refactor:` — cleanup/restructuring, no behavior change
- `epic:` — tracking issue for a milestone's execution order (see Epics)
- `risk:` — a latent problem, not yet triggered, not necessarily asking for action
- `investigate:` — unexplained behavior that needs root-causing before a fix can be scoped
- `Decide:` — an open design question with real options, no proposal yet
- `hardening:` — defensive improvement, not a response to an active bug
- `ci:` — CI/build pipeline
- `test:` — test coverage/quality issue

If none fit, ask rather than inventing a new prefix.

## Labels

Apply exactly one type label, mapped from the prefix: `fix`→🐛 bug, `feat`→✨ enhancement, `perf`→⚡ perf, `refactor`→♻️ refactor, `epic`→🧭 epic, `hardening`→✨ enhancement, `risk`→🐛 bug. `investigate:`/`Decide:`/`test:` issues get ❓ question unless a behavior-change label obviously fits better.

Additional labels only when unambiguous — never guess:
- `🎨 area: frontend` / `🌐 area: api` / `🔧 area: mcp` — issue is scoped to one surface
- `🔒 security` — security-relevant

There is no blocked label and no priority label: blocking is a native link and priority is the board's `Priority` field (see `_shared/board.md`). Most issues in this repo carry only their type label and nothing else — that's normal, not incomplete.

## Project board

Every new issue goes on the "Kajet Turbo" project board: `gh issue create ... --project "Kajet Turbo"` at creation, `gh issue edit <N> --add-project "Kajet Turbo"` for one filed without it (note the flag name differs between the two subcommands). Idempotent — safe to run even if the project has an auto-add workflow that already caught it. Needs the `project` auth scope; if it fails with a scope error, `gh auth refresh -s project`.

A new issue lands in `Inbox` with **no priority**, even when it looks obviously urgent or obviously trivial — the filer sees one issue, triage weighs it against the whole board. If it truly can't wait (an active production leak, a broken core path), say so to the user right away instead of setting P0 yourself. Moving it further is not this skill's job: `Backlog` + priority is `backlog-triage`, `Next` is `next-selection`, `In Progress` happens when a branch or PR exists. Status edits go through `python3 .claude/skills/_shared/board.py set N --status "In Progress"`.

## Blocking relationships

When issue A can't be worked until issue B lands, link them natively, not just in prose: `gh issue edit A --add-blocked-by B` (or `--blocked-by B` at creation with `gh issue create`). This is a real GitHub relationship — it shows in both issues' sidebars, is filterable (`gh issue list --search "is:blocked"`, `"blocked-by:B"`), clears itself when B closes, and is queryable (`gh issue view A --json blockedBy,blocking`) — unlike a body sentence saying "blocked on #N" which nothing tracks.

A wait on something that is not an issue (more production data, an upstream release) gets a `## Blocked on` section naming it, and triage sets Status `Blocked` — see `_shared/board.md`.

## Body — regular issue

```
## Problem
<what's wrong / missing, with file:line references>

## Impact
<who/what is actually affected, how badly — say so plainly if it's cosmetic>

## Proposal
<the fix, briefly>

## Acceptance
- [ ] <testable criterion>
- [ ] <testable criterion>
```

`risk:` / `investigate:` / `Decide:` issues replace `## Proposal` with `## Options` — a real question gets a menu, not a foregone proposal.

If the issue is a spin-off from code review or another issue, end the body with a one-line provenance trailer: `Found during #N code review.` or `Found during review of <feature> (PR #N).`

## Body — epic

Title: `epic: <what it tracks>` (the `— execution order` suffix is optional, only #152 uses it — don't mandate it).

````
Tracking issue for the *<Milestone>* milestone. Decisions and contracts live in the linked issues; this one holds order and what blocks what.

## Order
- [ ] #N — <one-line summary of what it does/decides>
- [ ] #M — <...>

## Dependencies
```
#N ──► #M ──► ...
```
<narrative for anything that isn't a straight chain>

## Done when
<the concrete end state — what it looks like working, not "all boxes checked">
````

Check a box and append `(#PR)` once the linked issue's PR merges — `board.py tick-epic <epic>` does this for every closed child (dry run first, then `--apply`). Note absorption inline (`Absorbs #146.`) when one issue's work folds into another's PR instead of landing separately.

Every real issue in `## Order` is also a native GitHub sub-issue of the epic: `gh issue edit <epic> --add-sub-issue <N>` for an existing issue, or `gh issue create --parent <epic> ...` when filing a new one straight into the epic. This gets the epic a native progress bar and puts a "tracked by" breadcrumb on each child — but it doesn't carry ordering or dependency semantics, so `## Order`/`## Dependencies` in the epic body stays the authoritative sequencing; back the `──►` arrows with real `--add-blocked-by` links between the sub-issues too (see Blocking relationships). Placeholder items that aren't real issues yet (e.g. `#156`'s `E0`–`E5` letter codes) get promoted to a real sub-issue — replacing the letter code with `#N` in `## Order` — only once picked up, not upfront.

If a matching GitHub Milestone exists (`gh api repos/{owner}/{repo}/milestones`), attach the epic *and* every issue it tracks to it with `gh issue edit N --milestone "<name>"`. If the epic is new and none matches, create one first: `gh api repos/{owner}/{repo}/milestones -f title="<Milestone>" -f description="<one line>"`.

## Cross-linking

- PRs close issues via `Closes #N` lines at the top of the PR body — rely on GitHub's auto-close on merge for issues that get a PR.
- `Decide:` / `investigate:` issues usually don't get their own PR — close them by hand with a comment stating the outcome, linking the issue that carries the actual implementation if any (e.g. `#47` closed by decision, removal landed in `#89`).
- A review finding that's out of scope for the current PR gets filed as a new issue, not fixed inline — reference it in the PR body ("found but filed separately") and in the new issue's provenance trailer.

## Before publishing

If the body touches production data (real note content, real queries, names), anonymize per CLAUDE.local.md before `gh issue create` / `gh issue edit`. After creating, `gh issue view N --json body` and read the full published body back — grep is not enough for this rule.

## Branch naming

For the PR that closes the issue: `feat/...`, `fix/...`, `perf/...`, `refactor/...` — matches the issue-title prefix.
