---
name: durin
description: Use when the user runs /durin [--repo <path>] [--scope mine|all] [--dry-run] [--auto] [--confirm]. Sweeps every open PR/MR in a repo's forge that bears unaddressed comments, dispatches /narvi per URL with --no-confirm, and aggregates one report. --auto skips the outer confirm gate and forges the manifest unattended. The forge is auto-detected from the repo's origin remote (github | gitlab). One repo per invocation — cd into the project tree first, or name it with --repo <path>.
purpose: Sweeps a repo's open PRs and MRs for unaddressed comments and answers them with code.
user_invocable: true
stage: vigil
composes: narvi:dispatch+mend
---

# Durin — The Sweep at the Doors

Narvi was the dwarf-smith who wrought the West-gate of Khazad-dûm; Durin the Deathless was the king whose halls Narvi served. So this skill: where Narvi answers the comments left upon one PR or MR, Durin walks every doorway in turn, summons Narvi at each that bears an unaddressed word, and brings back one report of all.

## Ethos

- **Durin walks; Narvi still answers.** Per-URL behavior matches `/narvi --no-confirm` exactly. Durin never amends more than Narvi would.
- **One repo per invocation.** The sweep scopes to one repo — the cwd's git tree, or the `--repo <path>` tree when that flag is given — read through its `origin` remote, the same source-repo contract Narvi enforces, just applied across many PR/MR URLs. `--repo` retargets the single sweep; it does not enable a multi-repo sweep. Fanning out across many repos is `/moria`, which calls `/durin --repo <root>` once per repo in your global mend list.
- **One outer gate, not N inner ones.** The human approves the whole sweep once after seeing the manifest; per-URL confirm prompts would make the sweep painful at scale. The gate is on for non-dry-run runs unless `--auto` is passed, which stands in for the human's word up front.
- **Silent skip on quiet PRs.** A PR with zero unaddressed comments (after Narvi's trail-marker dedup) is dropped from the manifest before the gate. Durin shows only what merits work.
- **Silent skip on pending PRs.** A PR whose title bears the bracketed tag `[PENDING]` (case-insensitive) or whose body/description contains the word `pending` is dropped at the list step — the author has marked the door closed for now, and Durin does not knock.

## Argument parsing

`/durin [--repo <path>] [--scope mine|all] [--dry-run] [--auto] [--confirm]`

| Argument | Required | Meaning |
|---|---|---|
| `--repo <path>` | no | Sweep the repo at `<path>` instead of the cwd's git tree. The path must be a git tree; its `origin` decides the forge. Absent → the cwd, as before. |
| `--scope mine\|all` | no | `mine` (default) — PRs/MRs the user authored. `all` — every open PR/MR in the repo. |
| `--dry-run` | no | Render the manifest, never write to the forge. Overrides `--auto` — a dry run writes nothing. |
| `--auto` | no | Skip the outer confirm gate; forge the manifest unattended. Mirrors `/aule --auto`. |
| `--confirm` | no | Redundant with the default-on outer gate; included for parallel with `/glorfindel`. |

The forge is **not** an argument — it is auto-detected from `git remote get-url origin` (host containing `gitlab` → gitlab, otherwise github). If the origin URL matches neither pattern, Durin stops with a plain error.

## Forge dispatch

| Forge | List hook | Per-URL skill |
|---|---|---|
| `github` | `~/.claude/hooks/durin-github-list.sh` | `/narvi <url> --no-confirm` |
| `gitlab` | `~/.claude/hooks/durin-gitlab-list.sh` | `/narvi <url> --no-confirm` |

Both list hooks emit the same JSON shape — `[{url, number, title, head, base}, ...]` — so Durin's body is forge-blind below this line. The comments hooks Narvi already owns (`narvi-github-comments.sh` / `narvi-gitlab-comments.sh`) are reused per URL to build the manifest; Durin does not duplicate their fetch logic.

## Workflow

### 1. Pre-flight

In order:

a. **Source repo.** If `--repo <path>` was given, the source repo is that path — validate it with `git -C <path> rev-parse --show-toplevel`; if that fails, stop with: *"Durin cannot ride from there — <path> is no git tree."* Otherwise run `git rev-parse --show-toplevel` from cwd; if cwd is not in a git tree, stop with: *"Durin cannot ride from here — there is no git tree at this place."*

b. **Forge detection.** Run `git -C <source-repo> remote get-url origin`. If absent, stop with: *"This repo has no `origin` remote — Durin has no road to walk."* If the host portion contains `gitlab` (case-insensitive), resolve forge as `gitlab`; otherwise as `github`. Bind the matching list hook and per-URL skill from the dispatch table.

c. **Forge auth sanity.** Run `gh auth status` (github) or `glab auth status` (gitlab). If either fails, surface the message and stop.

d. **Fetch.** Run `git -C <source-repo> fetch origin` so the `origin/<base>..origin/<head>` refs step 3b's dedup reads are current. Without this, a comment addressed and pushed by another session (or a prior sweep whose refs were never fetched here) could re-manifest.

There is **no clean-tree gate** on the source repo — Narvi never commits there, and Durin never branches it either. The human may be mid-edit on a wholly unrelated branch while Durin sweeps.

### 2. List the open PRs/MRs

Invoke the resolved list hook:

```bash
<list-hook> <scope>
```

`<scope>` is `mine` unless `--scope all` was passed. Parse the JSON array.

- If the hook prints `{"error":"..."}`, surface the error and stop.
- If the array is empty, stop with: *"The road lies empty — no open PR/MR matching the scope."*
- The list hook itself drops entries whose title bears `[PENDING]` (case-insensitive) or whose description contains `pending`; the skill body never sees them. If every open PR/MR is pending, the array arrives empty and the "road lies empty" message stands.

### 3. Build the manifest

For each PR/MR in the list (in the order the hook returned), dispatch Narvi's existing comments hook to find what stands unaddressed:

```bash
<narvi-comments-hook> <url>
```

Where `<narvi-comments-hook>` is `~/.claude/hooks/narvi-github-comments.sh` (github) or `~/.claude/hooks/narvi-gitlab-comments.sh` (gitlab).

For each PR/MR:

a. Parse the comments-hook JSON. On `{"error":"..."}`, record the URL as `error` with the message and continue to the next URL — one PR/MR's failure does not halt the sweep.

b. **Trail-marker dedup.** For each comment entry, extract the first comment's URL and check the head branch for an existing `See: <url>` footer:

   ```bash
   git -C <source-repo> log "origin/<base>..origin/<head>" --format=%H --grep="See: <url>" --fixed-strings
   ```

   Drop entries whose URL is already in the log — Narvi addressed them on a prior run. Note: this dedup reads from the source repo's refs only (no workspace acquired here); pre-flight step 1d's fetch is what makes "reflects what has actually been pushed" true — without it, these refs could be stale.

c. **Silent skip if the remainder is empty.** A PR/MR with zero unaddressed comments after dedup is dropped from the manifest entirely. No row, no report.

The manifest's row count is the PRs/MRs that actually carry work.

### 4. Render the manifest and the gate

Print one table:

```
Durin at <repo-slug> — <forge> — scope <mine|all>

| # | PR/MR | Title | Unaddressed |
|---|---|---|---|
| 1 | #42  | feat: add session summary hook | 3 |
| 2 | #45  | fix: avoid empty list crash    | 2 |
| 3 | #48  | chore: bump deps               | 2 |

Total: 3 PR/MR(s), 7 unaddressed comment(s).
```

Then:

- **`--dry-run`**: stop. The manifest is the deliverable; nothing further.
- **`--auto`** (and not `--dry-run`): skip the gate; proceed straight to step 5. The flag is the user's word for the whole sweep, given up front.
- **Otherwise**: AskUserQuestion (options: `forge all <N>` / `abort`). On `abort`, stop. On `forge all`, proceed to step 5.

The slash invocation alone is not authority for a forge-write across N PRs/MRs; the outer gate is always on unless `--dry-run` or `--auto`.

### 5. Per-URL Narvi dispatch

For each URL in the manifest, in order, invoke the Narvi skill:

```
/narvi <url> --no-confirm
```

Use the Skill tool with `skill: narvi`, `args: "<url> --no-confirm"`. Each invocation re-enters Narvi's full workflow (worktree acquire, smith dispatch, verify, weigh, push, reply, workspace release) for that one URL. The `--no-confirm` flag bypasses Narvi's inner gate — Durin has already taken the user's word for the whole sweep.

Capture each Narvi run's outcome for the report. A Narvi-side abort (smith scope-miss, push failure, malformed return) does not stop the sweep — Durin records the row and proceeds to the next URL.

### 6. Aggregate the report

Print one block:

```
Durin at <repo-slug> — <forge>

| # | PR/MR | Title | Outcome | Detail |
|---|---|---|---|---|
| 1 | [#42](<url>) | feat: session summary hook | forged 3/3 | workspace released |
| 2 | [#45](<url>) | fix: avoid empty list crash | forged 1/2 | scope-miss on comment #2; workspace kept at <path> |
| 3 | [#48](<url>) | chore: bump deps           | aborted    | smith aborted both comments; workspace kept at <path> |

Total: 3 PR/MR(s) — 1 fully forged, 1 partial, 1 aborted, 0 errors.
```

Outcome vocabulary:

| Outcome | Meaning |
|---|---|
| `forged N/N` | Every unaddressed comment landed as a commit, push succeeded, replies posted. |
| `forged M/N` | Some comments forged, some aborted; push succeeded for the ones that did. M < N. |
| `aborted` | No comments forged — smith aborted every entry. No push. |
| `verify-failed` | Smith forged commits but Narvi's mandatory pre-push verification (tests/lint) failed. No push attempted. Commits live in the workspace. |
| `weigh-failed` | Smith forged commits and they passed tests and lint, but Narvi's pre-push weigh of its own amendments left a Blocker standing after its one mend round. No push attempted. Commits live in the workspace. |
| `push-failed` | Smith forged commits but the push (or earlier git step) failed. Commits live in the workspace. |
| `error` | The list-hook or comments-hook failed for this URL. The PR/MR was never dispatched. |
| `dry-run` | Reached only when `--dry-run` was set — not present in this report; the dry-run path stops at step 4. |

Do not reproduce per-comment commit shas in this report — they live on Narvi's per-URL report blocks (already rendered by each Narvi dispatch in step 5). Durin's aggregate is the bird's-eye view.

## Rules

- One repo per invocation. The sweep scopes to one repo — the cwd's git tree, or the `--repo <path>` tree when given — via its `origin` remote only. `--repo` retargets that single sweep; it does not make the sweep span repos. Many repos are swept by calling Durin once per root (what `/moria` does).
- Forge is auto-detected from the origin host. The skill does not accept a forge argument.
- `--dry-run` stops at the manifest. No outer confirm, no per-URL dispatch.
- The outer confirm gate is always on for non-dry-run runs, unless `--auto` is passed. The slash invocation alone is not authority; `--auto` is the explicit word that stands in for the gate.
- Per-URL Narvi dispatch uses `--no-confirm`. Durin owns the gate; Narvi answers without re-asking.
- A Narvi-side abort or error on one URL does not halt the sweep. Record and continue.
- Do not duplicate Narvi's per-comment commit-and-push logic — dispatch the skill instead. One source of truth for the per-URL workflow.
- Do not surface forge tokens in logs, responses, or saved files.
- Sweep order is the order returned by the list hook.
