---
name: standup
owner: baseline
description: Read-only release + backlog recap. Reports the last release, commits-since-tag classified by conventional-commit type with the semver bump they trigger and pushed-vs-origin state, the backlog bucketed (open/picked-up/dropped with epic parent→child nesting), the roadmap epics with their per-task tallies, and condensed open questions — then recommends the next pickup. One `cli.mjs recap` call returns all six recap keys. Invoke any time (on demand) to plan a release or choose the next thing to build; a compact form is also surfaced at session start. Not a workflow phase; never writes CHANGELOG; never starts or commits work.
disable-model-invocation: true
---

# standup — where are we, what's next

A read-only recap utility in the family of `audit-baseline` / `rca`: it reads state and reports, it never mutates. Run it whenever you sit down to plan a release or pick the next piece of work. It is **not** a workflow phase — it does not enter the Track Guard ordering and never blocks a commit.

## What it answers

1. **Shipped** — the last released version (from `CHANGELOG.md` / the latest tag).
2. **Staged but unreleased** — every commit since the last tag, classified by conventional-commit type, with the aggregate semver bump those commits will trigger (read from `.releaserc.json` at runtime, so it never drifts from the release config) and the pushed-vs-origin state.
3. **Backlog** — entries bucketed `open` / `picked-up` / `dropped`, with epic children nested under their parent.
4. **Open questions** — `pending-questions.md` condensed to id + question + blocker.
5. **Roadmap** — the execution plan's epics with their status and per-task tallies, the rows still open under each, plus the Progress bullets, read from `project.json → roadmap.path`.
6. **Recommended next pickup** — assembled in main context (see Article II below).

## How to run

One invocation returns the whole recap. Use the CLI front door:

```
node .claude/skills/standup/cli.mjs recap [--json] [--root <repo-root>] [--remote]
```

Without `--json` it prints the bounded rendering; with `--json` it prints the raw `StandupRecap`.

The bound is a **threshold, not a blanket collapse**. Detail renders while the pile is small and degrades to counts once printing it back would reproduce the cost the CLI exists to remove:

| Section | At or below the bound | Above it |
|---|---|---|
| Unreleased commits | one line per commit: type, bump, subject | counts-by-type plus the aggregate bump (`COMMIT_DETAIL_MAX` = 20) |
| Roadmap epics | each epic's OPEN rows listed beneath it — planned and in-progress, never done | per-task tallies only (`OPEN_TASK_DETAIL_MAX` = 20, measured across the whole plan) |

Collapsing at every size was the older behaviour, and it cost a second `--json` pass to answer "what is actually in this pile?" for a four-commit pile. Done rows are never listed at either size: they are the bulk of a finished epic and carry no pickup signal.

Alongside those, the pushed-vs-origin state and the declared completeness gate each render as their own line, so the two questions that decide whether to cut — *is this even pushed?* and *may a half-wired feature ship?* — are answered without opening git or `project.json`.

Every rendered detail line is whitespace-collapsed, clipped to 96 characters, and stripped of C0/C1 control characters. Roadmap titles, commit subjects and question bodies are all repository-controlled content on its way to a terminal, and a row title in this repo already runs past 1000 characters.

### `--remote` — prove the release picture against the remote

Every release figure in the recap is read from **local** refs: `git describe --tags` for the last tag, `rev-list @{upstream}...HEAD` for the pushed-vs-origin state. On a clone that has not fetched, both answer from a stale view. On 2026-08-13 that reported `v0.21.0` with 70 unreleased commits while `v0.22.0` was already tagged, published to npm, and released — the operator read a shipped release as an unshipped pile.

The default run therefore states its own limitation in the Release block (`Figures read local refs, not fetched`) and names the remedy. Pass `--remote` to check instead of caveat:

- `git ls-remote --tags origin` and `--heads origin <branch>` are read-only; nothing is fetched and no ref is mutated.
- A newer remote tag or a diverged branch head adds **`stale-remote-refs`** to `degraded[]` and fills `release.remote` with `{probed, stale, remoteTag, remoteHead, reason}`.
- A probe that cannot run — offline, no remote, auth, timeout — adds **`remote-probe-failed`** instead, keeps the local figures untouched, and still exits 0. "I could not check" never renders as "you are current", and never as "you are stale" either.
- `release.remote.headState` reports the branch-head comparison as one of `diverged` / `matched` / `unreachable` / `not-comparable`. The last two are distinct on purpose: `unreachable` means the branch tracks a remote and the probe failed, while `not-comparable` means there was no upstream to compare against (a detached HEAD, a branch never pushed, or a branch the remote does not carry). A checkout with nothing to compare is never reported as one whose refs match.
- Tag comparison is numeric on strict semver, so `v10.0.0` beats `v9.0.0`; any ref the remote advertises that does not parse is discarded before it can influence the answer.

`release.remote` is `null` on the default path, which is how a reader tells *not checked* from *checked and current*.

**`StandupRecap` carries six keys. All six come back in that one call:**

| Key | What it holds |
|---|---|
| `release` | `lastVersion`, `lastTag`, `commitsSinceTag[]` classified by conventional-commit type with the semver `bump` each triggers, and `upstream` — `{state, ahead, behind}`, where `state` is `ahead` / `behind` / `up-to-date` / `no-upstream` |
| `releaseModel` | the declared release POLICY from `project.json → release` — drives the regime-aware recommendation below |
| `backlog` | entries bucketed `open` / `picked-up` / `dropped`, epic children nested under their parent |
| `pendingQuestions` | `pending-questions.md` condensed to id + question + blocker |
| `roadmap` | the execution plan's `epics[]` (number, title, tag, status, per-task tallies, plus `openTasks[]` of `{id, status, title}` for the rows still open) and its Progress bullets |
| `degraded` | one marker per source that could not be read — `no-roadmap-plan`, `no-release-model`, and so on |

Do not re-derive any of these by hand afterwards. Re-reading the roadmap file or re-running `git log` after this call is the multi-pass behaviour the CLI replaced; every key above is already in the result.

Six is the whole list, and it stays six. New data nests inside an existing key rather than becoming a seventh — `openTasks` sits on the roadmap epic, `upstream` and `remote` sit on `release`. `tests/standup-cli-recap.test.mjs:71` asserts the count, so widening the top level breaks a contract other readers depend on.

It degrades gracefully — on a non-git tree, a repo with no tags, or missing memory files it names the missing precondition in `degraded[]`, still exits 0, and never throws. `gather.mjs` remains importable as the collector for in-process callers such as the session-start hook.

## Article II — where the judgment lives

Per CLAUDE.md Article II, decisions live in main context. The helper only **gathers** the mechanical recap; it does not pick what to build next. After reading the helper's JSON, the recommendation — the single suggested next pickup and its one-line rationale (smallest unblocker first) — is reasoned out **in main context**, not emitted by the helper. The session-start surface (the `memory_session_start` hook) shows only the compact mechanical recap plus a pointer back to `/standup`; the full judgment recommendation is on-demand here.

### Release-model-aware recommendation (AC-303)

When `gatherSync` surfaces a `releaseModel` (from `project.json → release`), the "can this unreleased pile ship?" judgment becomes **regime-aware** — the model tells main context which regime it is in, the way `git.workflow_model` overrides generic branching instincts:

- **`release_trigger: on-push` / `release_cycle: continuous` / `consumer_upgrade_cadence: frequent`** → recommend **pushing early and often**; an unpushed pile is the risk. Fix-forward is cheap.
- **`release_trigger: on-tag`|manual / `release_cycle: sprint-based`|manual / `consumer_upgrade_cadence: rare`** → a release is a CD pressing: recommend **gating the cut on a completeness/coherence audit**. When `release.completeness_gate.half_wired_blocks_release` is true, do **not** recommend cutting while any feature in the unreleased set is half-wired-on-the-disc (shipped-dark but opt-in-broken).

A `no-release-model` marker in `degraded` means no policy is declared — fall back to the pre-model behavior (report the semver bump from `.releaserc` and let the human decide). The judgment stays in main context (Article II); `collectReleaseModel` only surfaces the config.

## Constraints

- **Read-only.** Reads git, `.releaserc.json`, `CHANGELOG.md`, and the memory files. Writes nothing.
- **Never writes `CHANGELOG.md`** — semantic-release owns it in CI.
- **Never starts, stages, or commits work** — it recommends; you act.
- **Deterministic, offline core** — identical repo + memory state yields identical helper output (no clock read, and no network call, in the core path). `--remote` is an explicitly non-deterministic opt-in that sits **outside** this guarantee: its result depends on a remote that can change between two otherwise identical runs. The guarantee is narrowed in scope, not weakened — every caller that does not pass `--remote`, which is every in-process caller on disk including the `memory_session_start` hook, keeps exactly the property it had before.
- **Read-only over the network too** — the probe runs `git ls-remote` only. It never fetches, never writes a ref, and never changes what a later `git status` or `/commit` sees.
