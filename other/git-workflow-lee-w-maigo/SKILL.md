---
name: git-workflow
description: This skill should be used when assembling git commits — deciding what to stage, how to scope a bash/agent command's working directory, whether to amend an unreleased commit or stack a new one, and how to size a diff against the correct baseline. Applies to the commit-assembly step of /maigo:go, /maigo:quick, /maigo:team, and /maigo:address-comments, and to the orchestrator generally.
---

<!-- mkdocs-include-start -->

# Git Workflow

**Consumers**: commit-assembly step of `/maigo:go`, `/maigo:quick`, `/maigo:team`, `/maigo:address-comments`; the orchestrator generally whenever it runs git commands or briefs an agent that will.

## Why this skill exists

Committing a scoped change and running git commands correctly across
worktrees are mechanical steps that are easy to get subtly wrong: staging
too broadly, mutating shell state with `cd`, fixing a CI failure on the
wrong branch, or reasoning about diff size against the wrong baseline. None
of these mistakes fail loudly at the time — they surface later as unrelated
noise in a PR, a confusing force-push, or a wrong claim in a summary. This
skill collects the conventions that keep git operations scoped to exactly
what was intended.

## Scoping and staging

Default to one commit per logical concern, and branch before the first
commit the user will actually test — don't land straight on main. See
[`references/commit-hygiene.md`](https://github.com/Lee-W/maigo/blob/main/skills/git-workflow/references/commit-hygiene.md#staging-discipline-one-commit-per-concern-branch-before-its-testable).

### Stage explicit files, never `git add -A`

When committing a scoped change, stage the specific files by path. Do not
use `git add -A` / `git add .` — the working tree often carries regenerated
or drift files (lockfiles, generated dependency manifests, build caches)
that a blanket `add` will sweep into the commit as unrelated noise.

How to apply: run `git status` first and read it. Stage only the intended
paths: `git add <file1> <file2>`. Be especially careful after a rebase, a
package-manager sync/install step, or after a delegated subagent ran — those
can leave unexpected generated changes in the working tree.

**Treat drift as drift, not just "don't stage it" — revert it.** A
package-manager install/codegen step (backend or frontend) can silently
rewrite a lockfile's security-relevant sections (e.g. deleting a version
`overrides:`/pin block) or scaffold a placeholder config file, in addition
to ordinary dependency-drift noise. After any such step, run
`git diff HEAD --stat` and scan for lockfiles, workspace-config files, and
other generated artifacts; `git checkout HEAD -- <file>` (or delete a
scaffold file) anything not intentional. Leaving it unstaged still risks a
later blanket `add` or a teammate sweeping it in — and a dropped security
pin is a real regression, not just noise.

### Don't `cd`; use absolute paths

Never `cd` into worktrees or other directories when running git/bash
commands or briefing another agent. Always:

- Use **absolute paths** for file arguments.
- Use **`git -C <worktree-path>`** for git commands targeting a different
  worktree.
- Use tool-specific working-directory flags when available (e.g.
  `pytest --rootdir`, a package manager's `--project`/`--cwd` flag).
- When briefing another agent that will run commands: state the working
  directory as **context** ("Working dir: /abs/path/to/worktree") but don't
  hand it a `cd <path> && <cmd>` instruction — the agent should use absolute
  paths or `git -C` directly.

Why: `cd` mutates shell state, complicates tool composition, and most
harnesses already handle per-tool working directory cleanly via absolute
paths or `-C`-style flags.

**Exception**: if a human explicitly asks to `cd` somewhere, do it.
Otherwise default to no-`cd`.

This matters most in multi-worktree setups, where several worktrees off the
same repo exist at once and it's easy to accidentally run a command against
the wrong one after a `cd`.

## Commit assembly (amend vs. new commit vs. which branch)

`--amend` only ever operates on HEAD — briefing an amend target needs a HEAD
check baked in, not just a hash. See
[`references/commit-hygiene.md`](https://github.com/Lee-W/maigo/blob/main/skills/git-workflow/references/commit-hygiene.md#amend-target-must-be-head).

### Fold polish into the unreleased introducing commit

When the underlying feature commit on a local branch has never been
released, fold review-driven polish — parameter renames, docstring updates,
perf nits, additional tests — into the introducing commit via
`git commit --amend --no-edit` (or `--amend` with an updated message; see
[`commit-message`](https://github.com/Lee-W/maigo/blob/main/skills/commit-message/SKILL.md))
rather than keeping it as a follow-up commit.

Why: a parameter or symbol that never existed in a release doesn't need its
rename preserved as a historical artifact — squashing means it's born with
the right name and the rename never shows up in history. If the repo
squash-merges on merge, the end PR result is identical either way, but
cleaner local history helps the author's own rebase / pre-push self-review
workflow.

How to apply:

- Default to "amend into the introducing commit" framing when drafting how
  to land polish on a local feature branch.
- Only suggest a separate commit when the polish is genuinely independent —
  different feature scope, separate user-visible change, or the introducing
  commit has already been published to a PR that reviewers are mid-review
  on.
- Don't preserve a rename as a historical artifact when the renamed symbol
  was never released to users.

### When polish hunks are tangled, amend into the tip — don't reconstruct

The rule above says to amend polish into the *relevant* introducing commit.
When the polish is per-thread localized (a rename, a docstring, one new
test), do that — amend into the specific commit each thread targets. But
when multiple review threads all reshape **the same function or loop
together**, splitting the polish across commits requires hand-reconstructing
intermediate file states for an interactive rebase — a high-error-rate
operation that doesn't survive a later force-push cleanly.

In that case, default to amending everything into the **tip** (most recent)
of the unreleased commits, rather than reconstructing a midpoint version of
the function that never existed in isolation.

How to apply: during commit-assembly planning, inspect the actual staged
diff before committing to a split-amend plan. If hunks for multiple threads
collide in the same function and the intermediate state isn't naturally
meaningful on its own, fold everything into the tip commit instead. Surface
the deviation from a split-amend plan explicitly so the plan's author (or
the user) can override.

### A fix belongs on the branch that surfaced it, not a fresh branch off main

When an in-flight branch (e.g. a CI-environment-upgrade PR) is itself what
surfaces a new lint/type/test failure, the fix belongs **on that branch**
(folded into the same PR), not on a fresh branch cut from the main/default
branch.

Why: CI runs against the in-flight branch. A fix sitting on a separate
branch does nothing for the failing CI, and the failure often only exists
*because of* that branch's own changes (e.g. an upgraded dependency
revealing a type error that didn't exist before).

How to apply: before branching off the default branch to fix something,
check whether the failure was introduced by the currently in-flight branch.
If yes, apply the fix there and consider folding it into the introducing
commit (see "Fold polish into the unreleased introducing commit" above).

### Referencing private-layer files: path only, never content

Public-repo commit messages, PR bodies, and file contents may cite a
private-layer file by its **path** (e.g. `~/.claude/rules/model-dispatch.md`)
but must not copy or excerpt its **content** — including quoting its
judgment/rule text verbatim. When the semantics need conveying, summarize in
one sentence instead of reproducing the source.

## Sizing a diff

Editing a single JSON field (a version bump) should stay a 1-line diff — use
precise string replacement, not a full `json.load`/`json.dump` re-serialize.
See
[`references/commit-hygiene.md`](https://github.com/Lee-W/maigo/blob/main/skills/git-workflow/references/commit-hygiene.md#edit-a-json-field-with-precise-replacement-not-full-re-serialize).

### Diff against the real merge-target baseline, not the branch tip

When quantifying a change's footprint — "what gets deleted", "is this a big
diff", "much smaller than what" — establish the real baseline **first**:
`git diff upstream/main..HEAD` (or the repo's actual merge target) and
`git show upstream/main:<file>`. Don't reason against the current branch tip
as if it were the merge target.

Why: it's easy to describe a change as "net-delete N lines of `symbol`"
without checking whether `symbol` exists on the merge target at all — if the
symbol was introduced by the branch's own unmerged feature commit, the
"deletion" is actually reworking in-flight work, which completely changes
the framing (an amend of the feature commit, not a deletion stacked on top —
see "Fold polish into the unreleased introducing commit" above).

How to apply: before stating diff sizes or "what gets removed", run
`git rev-list --count upstream/main..HEAD` and check whether the code being
"deleted" actually exists on the merge target
(`git show upstream/main:<file> | grep <symbol>`). If the branch carries
unmerged feature commits, the honest comparison is "reworked commit vs.
current commit" (an amend), not "vs. the merge target". Verify empirically
against `git show`/`git diff` output — don't assert sizing from memory of
the working tree.

### Enumerate "new lines" from a merge-base baseline, not a two-dot diff

When the judgment is "which lines did *this* diff add" — naming
enumeration, "is this symbol new in this PR", scanning for a private/secret
token that must not leak — the baseline must be `git merge-base <base> HEAD`
or the three-dot form `git diff <base>...HEAD`. Do not use the two-dot form
`git diff <base>`.

Why: a two-dot diff compares two commits directly. If the local `<base>` ref
has advanced past the point this branch actually forked from (someone else
pushed to it, or it's a shared/moving ref like `main` in a long-lived
worktree), the two-dot diff mixes in **every commit that landed on `<base>`
since the fork point** — changes nobody on this branch wrote. Enumerating
"new" defs, symbols, or added lines against that diff produces false
positives that look identical to real ones: no error, a plausible-looking
line number, a name that reads like it could be new.

How to apply: `git merge-base <base> HEAD` first, then diff from that SHA
(`git diff <merge-base-sha>...HEAD` or equivalently the three-dot form
against `<base>` directly) before treating any line as "added by this
branch." This applies wherever "diff 新增行" is the judgment basis — see the
naming-enumeration and change-site-enumeration uses of this pattern in
[`strict-review`](https://github.com/Lee-W/maigo/blob/main/skills/strict-review/SKILL.md)
and
[`change-site-enumeration`](https://github.com/Lee-W/maigo/blob/main/skills/change-site-enumeration/SKILL.md).

Case: a review's naming-enumeration pass ran a two-dot diff against a local
`main` that had moved ahead; the diff pulled in an unrelated commit that
had touched `sandbox/modal.py`, and two of that commit's pre-existing names
got flagged as naming violations introduced by the branch under review —
neither line was written by that branch.

## Pushing and opening a PR

**A widget selection is not authorization to open a PR.** Never run `gh pr create`
(including `gh pr create --web`, which only opens a pre-filled browser tab) unless
the user explicitly asks for it in the current turn. Picking a multi-choice option
like "Commit and open PR" from an AskUserQuestion-style widget is ambiguous for the
PR-creation half specifically — confirm once more (plain text is fine) immediately
before calling `gh pr create`. After committing and pushing a branch, default to
stopping there: report the branch/compare URL and ask if a PR should be opened.

**Outward git/GitHub operations are the user's to run, not just PR creation.**
- **`git commit` is authorized; pushing is not.** Once verification is green, commit directly on the branch (never `SKIP=`, never `git add -A`) and report the hash and `--stat` — don't stop at "here's the command, paste it yourself".
- Everything outward stays drafted-and-stopped — never auto-run `git push` / `--force-with-lease` / `gh pr create` / `gh issue create` unless the user explicitly asks this turn.
- A "Recommended" pick inside a batch `AskUserQuestion` is not authorization to open an issue — show the draft, wait for "post this".
- Fixing an already-pushed branch: commit/amend locally and stop; mention `--force-with-lease` but neither run it nor frame it as the recommended next step. Case studies: `references/outward-ops-authority.md`.

## Worktree hygiene (references)

Fourteen conventions for worktree lifecycle and git-attribution — worktree
layout naming, when to open a separate worktree for a pre-existing issue,
deferring colliding work, batch cleanup safety, squash-merge-aware "already
merged" checks, and not over-attributing surprising git state
(commits/rebases/wrong commit subject) to a rogue agent when it's more likely
the user working in parallel or an unverified delegate report. Details and
recipes in `references/worktree-hygiene.md`:

- **Worktree layout** — worktrees live nested under the main worktree's own
  `.worktrees/<topic>` (branch `<topic>`), matching the same path template a
  personal worktree manager (e.g. worktrunk) already uses for the repo.
- **Start a task in its own worktree from the outset, not midway** — a
  mid-task switch costs more than staying (untracked files don't follow a
  branch switch, running agents get interrupted); correct on the *next* task.
- **`ListAgents` before touching the git index** on a shared checkout — a
  peer session can be on the same checkout/branch with zero mutual awareness,
  and `git status` alone won't reveal it.
- **Pre-existing fix → new worktree off upstream/main**, not folded into the
  current feature branch (proportionality counter-case for trivial diffs).
- **Colliding work gets deferred** — when approved work overlaps an
  in-flight branch's files, do the non-colliding subset now and defer the
  rest, rather than forcing everything through and creating merge conflicts.
- **Batch cleanup**: show the exact command list before running; don't chain
  many worktree/branch ops in one shell call (timeout risk).
- **Squash-merge "already merged" check** needs `gh search prs`, not
  `git branch --merged` (squash breaks ancestry).
- **Don't over-attribute unexpected git state to a rogue agent** — verify
  quietly (reflog, staged files) before alarming; on a delegated task, verify
  git state (reflog/log/status) before committing on top of it.
- **Verify the landed commit subject** with `git log --oneline -1` after every
  commit — don't trust the tool's echoed command string.
- **"Fix the commit message" on a tmp/mislabeled branch** means squash the
  whole branch into one commit, not reword just the tip.

Read `references/worktree-hygiene.md` when opening/cleaning up worktrees or
when git history looks surprising after a delegated task.

### Worktree automation (`--worktree` flag)

How `/maigo:go` / `/maigo:take-issue`'s opt-in `--worktree` flag actually opens
a nested worktree, and where `.maigo/` artifacts written during that task
belong (per-task artifacts vs. the Work Board, which only ever lives in the
main checkout). Details in
[`references/worktree-automation.md`](https://github.com/Lee-W/maigo/blob/main/skills/git-workflow/references/worktree-automation.md).

## Shared worktree state volatility (references)

A shared worktree's branch, commits, or push/PR state can change from
something other than the current session — in both directions (external
revert/rebase/deletion *and* external forward progress) — so re-verify live
before restating a status claim, reusing a cached base ref, or running a
destructive reset. Recovery recipes, base-ref staleness, and CI/changelog
proxy traps in
[`references/shared-worktree-state.md`](https://github.com/Lee-W/maigo/blob/main/skills/git-workflow/references/shared-worktree-state.md).

## What this skill does NOT cover

- Drafting the commit message text itself — see
  [`commit-message`](https://github.com/Lee-W/maigo/blob/main/skills/commit-message/SKILL.md).
- Deciding *whether* to commit at all, or when in a flow the commit happens
  (e.g. after Soyo + Taki pass) — that's the calling command's own policy.
- Drafting the PR title / description content itself — separate skill
  ([`github-title-description`](https://github.com/Lee-W/maigo/blob/main/skills/github-title-description/SKILL.md)).
  This skill only governs *when* it's okay to actually run `gh pr create`
  (see "Pushing and opening a PR" above).
