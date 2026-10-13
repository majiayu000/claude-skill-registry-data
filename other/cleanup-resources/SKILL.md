---
name: cleanup-resources
description: "End-of-workflow audit of touched GitHub issues, PRs, and branches via a Sonnet subagent, plus a deterministic sweep of stale build-tool temp artifacts (e.g. zfb-shadow-session-*) to reclaim disk. Use when: (1) /big-plan, /x-as-pr, or /x-wt-teams finishes its main work and needs to verify every touched resource is in the right state (closed when done, kept when ongoing, deleted when dead), (2) User says 'cleanup resources', 'audit cleanup', 'check what should be closed', or 'clean disk / clear stale temp files', (3) A long workflow ends and the manager wants a structured paper trail of what it closed/kept/deleted. Auto-execute by default — the Sonnet agent proposes GitHub actions, the manager (you) executes the safe ones, sweeps stale temp dirs (allowlist + age gated), and prints a final report."
argument-hint: "[workflow:big-plan|x-as-pr|x-wt-teams] [-a|--auto-merged] [extra context]"
---

# Cleanup Resources

End-of-workflow audit for GitHub issues, PRs, and branches the calling workflow touched. Long workflows (big-plan, x-as-pr, x-wt-teams) tend to drop the trailing "close the source issue" / "delete the dead local branch" steps because context drifts. This skill forces an explicit checkpoint: gather a manifest of every touched resource, hand it to a fresh Sonnet agent for audit, then execute the safe actions and report.

It also runs a second, **independent** job at the same checkpoint: a deterministic sweep of stale build-tool temp dirs (Step 4). Build tools like zudo-front-builder leak large ephemeral session dirs (`zfb-shadow-session-*`, 5–8G each) into `$TMPDIR` and don't always clean up on exit; a few dev sessions silently fill the disk. Folding an allowlist-gated sweep into every workflow's cleanup checkpoint keeps that from accumulating. This part needs no agent — it's a bundled script.

> **On Claude Code on the web** (`$CLAUDE_CODE_REMOTE=true`): follow [`web/web-mode.md`](../../web/web-mode.md). Gather the manifest and execute closes / merges / branch deletes via the GitHub MCP (`issue_read` / `issue_write`, `pull_request_read`, `list_pull_requests`, `merge_pull_request`), not `gh`. Spawn the audit step as a Claude subagent (no agent teams).

## Who calls this skill

This skill is invoked at the **end** of a parent workflow — never mid-flight. Typical callers:

- `/big-plan` — at Step 10 (Close source issues). Manifest: source issues passed to the planning session.
- `/x-as-pr` — after Session Report / Requirements Verification. Manifest: tracking issue (if `--make-issue`), the working branch (if the PR was auto-merged via `-m` / Merge Mode), unrelated-findings issues raised mid-workflow.
- `/x-wt-teams` — replaces the old "Close Tracking Issue" + Step 16 cleanup. Manifest: tracking issue, sub-issues (if epic), root PR, base branch, topic branches, auto-merged status (the caller's `-m` flag).

Note on flag naming: this skill's own `-a` / `--auto-merged` flag means "the caller auto-merged the root PR." In the calling workflows that signal is their `-m` / `--merge` flag (their `-a` is the autonomy/auto-chain flag and does NOT imply a merge) — callers pass `-a` here iff `-m` was on their invocation.

Other callers can use it the same way: build a manifest, invoke, execute the returned plan.

## Workflow

### Step 1 — Manager builds the manifest

Before invoking the Sonnet agent, gather every resource the parent workflow created or touched. The manager (you) already knows these from session state — you do not need to grep git or scan the org. Build the manifest from memory of what the workflow did.

Structure the manifest as a single markdown block. Use this exact shape so the agent can parse consistently:

```markdown
## Workflow context
- workflow: <big-plan | x-as-pr | x-wt-teams>
- auto-flag (-a): <true | false>
- epic-mode: <true | false>     # true when the parent dealt with a [Epic] issue from /big-plan
- root-PR: <url-or-"none">
- root-PR-merged: <true | false>
- parent-branch: <branch-name-or-"none">

## Resources

### Issues
- #<number> — <role> — <one-line context>
- ...

### PRs
- <url> — <role> — <merged|open|draft>
- ...

### Branches
- <branch-name> — <role> — <local|remote|both> — <pr-merged: true|false>
- ...

## Notes for the agent
<any free-form context: e.g. "issue #45 has follow-up work tracked separately, KEEP it open">
```

**Roles to use** (consistent vocabulary helps the agent):

- Issue roles: `source` (existed before; the workflow superseded it), `tracking` (created by the workflow as a spec/log), `epic`, `sub` (under an epic), `super-epic` (a `/big-plan -is` sweep bundle tracking several child epics — KEEP while any child epic is open; only the terminal `/x-wt-teams` sibling that merged the super-PR closes it), `fix` (review-fix issue), `unrelated-finding` (side-effect issue raised mid-workflow), `claimed-existing` (user-supplied, not created here).
- PR roles: `root` (the main PR for the workflow), `super-pr` (a sweep bundle's `base/{sweep-slug}` → parent PR — KEEP until the last child epic has merged into the super base), `topic` (sub-PR merged into a base branch), `fix` (delegated fix PR).
- Branch roles: `base` (the base branch of an x-wt-teams session), `super-base` (a sweep bundle's `base/{sweep-slug}` — KEEP until its super-PR is merged, INCLUDING the window before that PR exists at all: the sweep pushes the base as a zero-diff ref and the super-PR is only opened after the first epic-PR merges, so "no super-PR" is a healthy state, never a dead branch), `topic` (child branch under a base), `working` (the single x-as-pr working branch), `fix` (an `agent-fix/<slug>` branch from the `-fix` auto-fix step), `parent` (the branch the parent workflow targeted).

If a resource doesn't fit, invent a short role label and explain in **Notes for the agent**.

### Step 2 — Dispatch the Sonnet audit agent

Use the Agent tool to spawn a `general-purpose` agent with `model: sonnet`. The agent's job is **analysis only** — it must NOT close, delete, or edit anything. The manager executes actions in Step 3.

Prompt template (substitute the manifest):

```
You are auditing resources from a just-completed Claude Code workflow. The manager (parent session) handed you a manifest of every issue, PR, and branch touched during the workflow. Your job is to decide which should be CLOSED, KEPT, or DELETED, and return a structured plan. **Do not take any action yourself — only propose.**

Manifest:

<paste the full markdown manifest here>

Audit procedure:

1. For every issue in the manifest, run `gh issue view <number>` to read its current state, body, and recent comments. Check:
   - Is it already closed? → action: keep, reason: "already closed".
   - Does its body declare a TODO checklist with unchecked items? → action: keep, reason: "TODO checklist has open items".
   - Was its work superseded by another issue/PR in the manifest (e.g. source issue replaced by an epic, fix issue replaced by a merged PR)? → action: close, with a one-line comment referencing the superseder.
   - Is it an `unrelated-finding`? → action: keep, UNLESS it was already closed by `-fix` (the `/x-as-pr` or `/x-wt-teams` auto-fix step closes the ones it fixed and links the fix PR). An already-closed `unrelated-finding` stays closed (action: keep, reason: "already closed by -fix"). Open ones are intentional follow-ups — never close them here.
   - Is it a `tracking` issue whose root PR is now merged (or the workflow ended cleanly)? → action: close.
   - Is it a `sub` issue whose corresponding PR is merged into the base? → action: close.
   - Is it an `epic` whose root PR is merged AND all sub-issues are closed? → action: close. Otherwise → keep.
   - Is it a `super-epic` (a `/big-plan -is` sweep bundle)? → action: **keep, ALWAYS**. Its lifecycle belongs to the terminal `/x-wt-teams` sibling, whose merge-and-close sequence runs *after* this audit — so at audit time it is always still legitimately open, even in the session that is about to close it.

2. For every PR in the manifest, run `gh pr view <url>` to read its state. PRs that are still open and intentional → keep. PRs already merged → keep (no action; they're done). PRs closed without merge (`state: CLOSED`, `merged: false`) → also keep, but add reason "manually closed without merge — investigate if the workflow expected it to merge". Do NOT propose closing open PRs unless the manifest's "Notes for the agent" explicitly asks for it.

3. For every branch in the manifest:
   - Check remote state: `gh api repos/{owner}/{repo}/branches/{name}` or `git ls-remote --heads origin <branch>`.
   - Check local state: assume the manager will check with `git branch --list <name>` before deleting.
   - **On web (`$CLAUDE_CODE_REMOTE=true`, web-mode.md §5): a branch whose role is `session-web`, or whose name matches the manifest's `protected-session-branch`, is the session branch the platform owns → action: keep, reason "web session branch — platform-owned", ALWAYS, even when pr-merged=true. Never propose delete (local or remote) for it. This protects the session branch by exact name, NOT by the `claude/*` prefix — `claude/agent-fix-*` fix branches are still deletable below.**
   - If pr-merged=true and the branch's role is `topic`, `working`, `base`, or `fix` → action: delete (both local and remote where applicable). Reason: "PR merged, branch is a dead pointer."
   - If the remote has already been deleted (e.g. by `gh pr merge --delete-branch`) but the local still exists → action: delete-local-only.
   - If pr-merged=false → action: keep.
   - NEVER propose deleting `parent` branches — those belong to other work.
   - **NEVER propose deleting a `super-base` branch (local OR remote), and never propose closing a `super-pr`** — regardless of what the manifest says about them. A sweep's super base is the head branch of a super-PR that is either already open or not yet created (it opens after the first epic-PR merges): `git push origin --delete` on it either makes GitHub auto-close an open super-PR **unmerged** or destroys the trunk every epic-PR is stacking onto — orphaning every epic in the batch. A missing super-PR is not evidence the base is dead. Their cleanup is owned by the caller's own terminal merge sequence (`gh pr merge --delete-branch` on the super-PR, then `git branch -d`), which runs after this audit — so at audit time they are always still live by design. Keep them and say so.

4. When the workflow's `auto-flag` is true (the caller auto-merged via its `-m` / `--merge` flag, passed to this skill as `-a` / `--auto-merged`) AND root-PR-merged is true, be more aggressive about deleting working/base/topic branches. The user explicitly opted into full auto-cleanup.

5. When in doubt about any resource, choose KEEP and explain in the reason. The manager will surface ambiguous cases to the user.

Return the plan as a single markdown block in this exact shape:

## Cleanup plan

### Close
- issue #<n> — <reason> — comment: "<one-line supersedes comment, or omit if no comment needed>"
- ...

### Delete (branches)
- <branch-name> — scope: <local|remote|both> — <reason>
- ...

### Keep
- <resource> — <reason>
- ...

### Ambiguous (manager: surface to user)
- <resource> — <why it's unclear>
- ...

End the response with one line: `Audit complete. <N> close / <M> delete / <K> keep / <A> ambiguous.`
```

Spawn the agent via the Agent tool with:

- `subagent_type`: `general-purpose`
- `model`: `sonnet`
- `description`: `Audit workflow resources for cleanup`
- `prompt`: the prompt above with the manifest filled in

Wait for the agent to return.

### Step 3 — Manager executes safe actions

Read the agent's plan. Execute each action **only** when it is unambiguously safe. The agent already filtered out unsafe cases into "Ambiguous", but the manager re-checks before acting.

**Close issues:**

```bash
for each "Close" entry:
  # Skip if already closed (defensive — agent may have raced with an external close)
  state=$(gh issue view <n> --json state -q '.state')
  if [ "$state" = "OPEN" ]; then
    if [ -n "<comment>" ]; then
      gh issue comment <n> --body "<comment>"
    fi
    gh issue close <n>
  fi
```

**Delete branches:**

```bash
for each "Delete (branches)" entry:
  case "<scope>" in
    local)
      # Use -d (NOT -D). If unmerged, surface as a loud failure rather than silently destroy work.
      git branch -d <branch> 2>&1 || echo "WARN: local branch <branch> not deleted — unmerged commits or already gone"
      ;;
    remote)
      git push origin --delete <branch> 2>/dev/null || echo "WARN: remote branch <branch> not deleted — already gone"
      ;;
    both)
      git branch -d <branch> 2>&1 || echo "WARN: local branch <branch> not deleted — unmerged commits or already gone"
      git push origin --delete <branch> 2>/dev/null || echo "WARN: remote branch <branch> not deleted — already gone"
      ;;
  esac
```

**Currently checked-out branch — switch off before deleting.** `git branch -d` cannot delete the current branch. If the manager is on a branch that's in the delete list, check out a safe parent (the `parent-branch` from the manifest, or the repo default) first:

```bash
CURRENT=$(git branch --show-current)
# On web (web-mode.md §5): NEVER check out off the session branch to delete it — the session branch
# is protected (role: session-web / protected-session-branch) and is not in the delete list, so this
# block never fires for it. Do not git checkout the default branch on web (it is not pushable).
if [ "$CURRENT" = "<branch-to-delete>" ]; then
  git fetch origin --prune
  git checkout <parent-branch>
  git pull origin <parent-branch>
fi
```

**Never use `-D` (force delete).** If `-d` refuses, that's the safety net working — surface the warning, do not retry with `-D`.

### Step 4 — Sweep stale temp artifacts

Independent of the audit agent and fully deterministic — no Sonnet needed. Build tools leak large ephemeral session dirs into `$TMPDIR` that don't get cleaned up on exit; the bundled script reclaims them.

```bash
$HOME/.claude/skills/cleanup-resources/scripts/sweep-tmp.sh            # dry-run: shows what WOULD be reclaimed
$HOME/.claude/skills/cleanup-resources/scripts/sweep-tmp.sh --apply    # delete the stale matches
```

Run the dry-run first, then `--apply`; fold the reclaimed figure into the Step 5 report. It is safe to run unattended because it is **allowlist + age gated**, not a blanket temp wipe:

- **Allowlist only.** It deletes only top-level entries whose name matches an entry in `STALE_PATTERNS` (seeded with `zfb-shadow-session-*`). Unrelated temp files never match — a general "delete old files in tmp" is exactly what the global `rm -rf` safety rule forbids, so this stays a tight allowlist.
- **Age gated.** It skips anything modified in the last 60 minutes (override: `--min-age-min N`), so an in-progress build's live session dir is never touched.

**Extending it:** when another tool is found leaking big session/cache dirs into a temp dir, add its glob to `STALE_PATTERNS` at the top of `scripts/sweep-tmp.sh`. Keep each pattern a specific top-level name with no slashes — the whole point is that only known-ephemeral artifacts are ever in scope.

On Claude Code on the web there are no local build sessions, so this step is a fast no-op (`nothing to sweep`).

### Step 5 — Print final report

Print a concise human-readable summary to the chat. Format:

```markdown
## Cleanup complete

### Closed
- #<n> — <title> — <reason>
- ...

### Deleted branches
- <branch-name> (local + remote) — <reason>
- ...

### Reclaimed disk
- <N> stale temp dir(s) swept — ~<size> freed (from `sweep-tmp.sh`), or "none" if nothing matched

### Kept
- #<n> — <title> — <reason>
- ...

### Warnings
- <any failed close/delete with the warning message>
- ...

### Ambiguous (please review)
- <resource> — <agent's reason>
- ...
```

If there are **no actions** (GitHub resources already in the right state AND the temp sweep matched nothing), print just: `Cleanup audit: all resources in expected state, no stale temp dirs — nothing to do.` If only the sweep did work, still report the reclaimed figure.

If the **Ambiguous** section is non-empty, do NOT auto-resolve. Surface to the user and let them decide. The agent's job was to filter the obvious cases; the manager's job is to act on those AND show the unclear ones.

## Notes on safety

- **Closing issues is reversible.** `gh issue reopen` exists. Default to closing when the agent is confident.
- **Deleting branches is harder to reverse.** The agent must show pr-merged=true before proposing delete. If `git branch -d` (without force) refuses, trust the refusal — there are unmerged commits.
- **Unrelated-findings issues are ALWAYS KEPT unless closed by `-fix`.** They are explicitly opt-in follow-up work, so the audit never closes an open one. The exception is the `-fix` / `--auto-fix` auto-fix step in `/x-as-pr` / `/x-wt-teams`: it closes the `agent-found` issues it actually fixed (linking the fix PR) before cleanup runs. The audit leaves those already-closed and keeps every still-open one. The agent's prompt enforces this; the manager doesn't second-guess.
- **On web (web-mode.md §5), the session branch is platform-owned and protected by exact name.** Callers pass it as `role: session-web` with `protected-session-branch: <name>`. The audit ALWAYS keeps it (even pr-merged=true), and the manager never checks out off it to delete it. Protect by name, not by the `claude/*` prefix — dead `claude/agent-fix-*` branches must still be deleted.
- **The caller's `-m` / `--merge` flag (passed here as `-a` / `--auto-merged`) is the signal for aggressive cleanup.** Without it, prefer keeping branches around — the user may want to inspect locally before deleting. With it and root-PR-merged, the user opted in to full cleanup including local dead branches (this is the specific bug the skill fixes: `--delete-branch` removes remote, the old workflow left local behind).
- **The temp sweep (Step 4) is allowlist + age gated, never a blanket wipe.** `sweep-tmp.sh` only removes top-level dirs matching `STALE_PATTERNS` (seeded with `zfb-shadow-session-*`) that are older than the age threshold, so live builds and unrelated temp files are always out of scope. This narrowness is deliberate: the global `rm -rf` rule forbids freehand deletes under absolute temp paths, so grow the allowlist rather than loosening the match.

## When to skip this skill

- The workflow created no GitHub resources (e.g. `/x-as-pr` with `--no-issue` and no merged PR) — the manifest is empty, so skip the GitHub audit (Steps 1–3). Step 4 (temp sweep) can still run on its own; a bare "clean disk / clear stale temp files" request runs only Step 4.
- Mid-workflow halts where resources are intentionally left open for the user to inspect.
- The parent skill is in an error state and shutting down — clean up next session.

In all other cases, the parent skill should invoke `/cleanup-resources` at its STOP point. The audit either confirms everything is already correct (nothing to do, fast) or it catches a missed close/delete.

## Invocation example (from a parent skill)

```
Skill tool: skill="cleanup-resources", args="workflow:x-wt-teams -a"
```

The manager (parent skill) then **continues in the same turn** by building the manifest and following Steps 1–4 above. The args are advisory — they tell the cleanup skill which workflow flavor invoked it, so any workflow-specific hints in this SKILL.md apply.
