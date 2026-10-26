---
name: sitrep
description: Live status of this session in ≤10 lines — what's running, git state, PRs + CI, asked vs done, what needs the user, and a SAFE/NOT SAFE close verdict. Use for "how's it going", "status update", "what's running", "can I close this".
---

Read-only snapshot of right now; no file writes (progress-report covers history). The one exception is §4, through `handoff-auto`.

## 1. Gather

- **Running**: every background `Bash`/`PowerShell`, `Monitor`, and background `Agent` launched this session without a completion notification yet. Per task: age + last line of its output file. `ListAgents` → note peers that look stalled.
- **Git**, for each repo this session ran git in (not only the cwd's), per `git worktree list` entry: `git status --porcelain` plus `git status --porcelain --ignored -- skilleddocs <handoff folder>` (excluded handoffs; folder per AGENTS.md/CLAUDE.md, if set). Unpushed = `git log <ref>.. --oneline`, `<ref>` = `@{u}`, else `origin/<branch>` if it exists, else `origin/<default>` (`<default>` per the `handoff-auto` skill's `TRACKING.md`); never local `<default>` (on `<default>` it hides everything). No such ref → unpushed "unknown", counted as unpushed. 0 commits and clean → nothing to push; commits and no `origin/<branch>` → "never pushed". `git symbolic-ref -q HEAD` fails → detached: say "detached at <sha>"; `git for-each-ref --contains HEAD refs/heads refs/remotes` prints nothing → its commits are on no branch (lost on switch or worktree removal): NOT SAFE, and the fix is `git switch -c <name>`, never "push". Local branches not checked out: same unpushed rule (`git for-each-ref refs/heads --format='%(refname:short) %(upstream:short) %(upstream:track)'`); list each with commits.
- **PRs**: `gh pr list -R <o>/<r> --author @me --json number,title,url,isDraft,statusCheckRollup` (`<o>/<r>` per the `next` skill's `BOARD.md`, Target repo section; on a fork also `-R <parent>`, where its PRs land) → passing / failing / pending.
- **Asked vs done**: each distinct ask in this conversation → done / in progress / not started.
- **Needs you**: keys, approvals, manual steps, unanswered questions. "none" if none.

## 2. Verdict

**SAFE** only when nothing runs and nothing is dirty or unpushed, or the mid-flight work is covered by a handoff: committed + pushed, or saved on disk per [TRACKING.md](../handoff-auto/TRACKING.md): untracked, `skilleddocs/` excluded (the only option on forks), or a dated handoff held uncommitted on a task branch in commit mode. That held file isn't dirty; never suggest committing it. Cover is for the work the handoff describes; other dirty/unpushed code still needs commit/push or a mention in the handoff. Commits on no branch are never covered.

An untracked handoff dies with its worktree: **NOT SAFE** if that worktree is not the main one (first `git worktree list` entry) or was created this session via pair/meta-orchestrator, or if unsure it survives. Reason names the handoff path: move it out or keep the worktree.

Else **NOT SAFE** + each reason.

## 3. Output (≤10 lines, no preamble, drop empty lines)

```
Running: 2 background (12m, "tests passing") | 1 agent pending
Git: 3 worktrees, 1 dirty, 1 unpushed (feat/x, 2 commits)
PRs: #12 passing | #14 CI failing
Asked → done: 4/5 (in progress: <what>)
Needs you: <item>
Verdict: NOT SAFE — stop feat/x's shell and push first
```

## 4. On "close" / "stop them"

1. List exactly what will stop (task ids, agents) and anything that would be committed or pushed.
2. Act on an explicit yes only; anything vaguer → repeat the list.
3. `TaskStop` each (no tool → tell the user how).
4. Commit or push only if the yes named that too.
5. Mid-flight work → `handoff-auto`, print its path. Earns SAFE on forks and untracked repos too (§2 caveats apply).
