---
name: close
description: Step 6 of the flow. End a session. Choose Complete or Suspend, write the handover, update the issue, ask the production question, route lessons, and clean up.
---

# close: exit gate

Run this when you stop, for any reason.

## 1. Choose the mode

Run `ws-delivery-status` to verify physical delivery state before ending.

To declare **Complete**, you MUST run `ws-delivery-status --assert-complete --reality-probe "<command>"`.

| Condition | Task Mode | Issue & Production Disposition |
|---|---|---|
| `ws-delivery-status --assert-complete ...` exit 0, single-PR scope or no service deploy | **Complete** | Clean up worktree/branch; acceptance walk (2.6); close issue; disposition `none` |
| `ws-delivery-status --assert-complete ...` exit 0, service change in batched-staging repo (`auto-release-staging.yml`) before the staging release verifies it | **Complete** | Clean up worktree/branch; keep the issue open with scope note until staging verifies it; disposition `batched-staging` |
| `ws-delivery-status --assert-complete ...` exit 0, staging verified by the reality probe (2.5, run against staging), also while a release promotion awaits the answer to `[PROD GATEKEEPER]` | **Complete** | Clean up worktree/branch; acceptance walk (2.6); close issue; disposition `staging` (`hold` when the owner answered "hold") |
| `ws-delivery-status --assert-complete ...` exit 0, release promotion task with owner "deploy" + prod verified | **Complete** | Clean up worktree/branch; acceptance walk (2.6); close issue; disposition `deployed` |
| `ws-delivery-status` exit 0 (Stage 1 only, no reality probe) | **Suspend** | Report state strictly as `Stage 1 Landed (Unverified)`; issue stays open |
| `ws-delivery-status` exit 1 (PR in review) | **Suspend** | Report state strictly as `In review` with PR URL |
| `ws-delivery-status` exit 3 (unmerged branch, draft changes, or probe failed) | **Suspend** | Run `auto` to merge or write handover |
| `ws-delivery-status` exit 4 (could not read git or GitHub) | **Suspend** | Fix the cause in `reasons[]` and re-run; never read it as a pass |

An umbrella issue closes with its last lane. Earlier lanes keep it open with a scope note.
Unmerged work is never Complete. Merge to main without a verified Business Reality Probe is never Complete.
Do not close the issue and do not delete the worktree in Suspend.
Never declare complete or done when `ws-delivery-status` exits non-zero.
Untracked files under `.agents/runs/` and unstaged submodule pointer moves do not block; the tool lists them.
Complete also needs the predecessor gone: each file, branch, worktree, stash or flag that this issue's change replaces is deleted, or the issue states why it stays. Delete only what this issue created or replaced. Never delete what another session's worktree or stash owns.
Push any local branch or record it in the handover so commits are never stranded locally.

## 2. Prove the running process is new

Skip this step when no process serves the change. Otherwise compare the process age with the file edit time.

```bash
python3 - "$FILE" "$PID" <<'PROBE'
import os, re, subprocess, sys, time

path, pid = sys.argv[1], sys.argv[2]
age = time.time() - os.stat(path).st_mtime
r = subprocess.run(["ps", "-o", "etime=", "-p", pid], capture_output=True, text=True)
raw = r.stdout.strip()
m = re.fullmatch(r"(?:(?:(\d+)-)?(\d+):)?(\d+):(\d+)", raw)
print(f"file changed {age:.0f}s ago; ps reports etime={raw!r}")
if r.returncode != 0 or not m:
    print("verdict: UNDETERMINED (ps gave no parseable etime: process gone, no permission, or other platform format)")
    sys.exit(2)
d, h, mi, sec = (int(x or 0) for x in m.groups())
elapsed = ((d * 24 + h) * 60 + mi) * 60 + sec
print(f"process running for {elapsed}s")
print("verdict: STALE (process is older than the edit, so it runs old code)" if elapsed > age
      else "verdict: FRESH (process started after the edit)")
PROBE
```

Use `ps -o etime=`. The keyword `etimes` exists only in procps-ng: macOS prints its keyword list to stdout and the output looks like a measurement.
Report "cannot measure" as UNDETERMINED. Never turn it into "not stale".

## 2.5 Business Reality Probe (verify the goal in physical reality)

Merge to main is Stage 1 only. Before declaring **Complete**, you MUST execute a physical reality probe proving the change works in reality:

1. **Data / Metrics / Factor tasks**: Execute live DB, API, or MCP query. Assert `records > 0`, `status == available` (reject `unavailable` or `lines: 0`).
2. **Refactoring / Code Slimming tasks**: Run physical diff/metrics (`wc -l` before/after or token counts) proving net reduction of complexity or lines (reject peripheral lint fixes).
3. **Pipeline / Benchmark tasks**: Execute against real non-empty input datasets or statements (reject 0-transaction / empty accounts).
4. **Bugfix tasks**: Reproduce against the original failing trigger payload and verify it now succeeds.

If the reality probe fails, is empty, or is unperformed, the session MUST exit as **Suspend** (`Stage 1 Landed`), never Complete.

## 2.6 Acceptance walk and claim check (skip when no issue closes)

1. Issue and PR text carry no acceptance; this walk does. For each deliverable in the issue body, run the `smoke` section "Acceptance checks". Write one row: the check, where it runs again, the result.
2. The completion comment names only code that exists on the merge commit. Save it to `$COMMENT_FILE`. In the repository, with the merge commit fetched, run:

```bash
ws-claim-check --commit "$(gh pr view <n> --json mergeCommit --jq .mergeCommit.oid)" "$COMMENT_FILE"
```

Exit 3 lists each MISSING name: correct the comment. Exit 4 means the check did not run: fetch the commit and run it again. Post the comment at exit 0 only.
The check proves that a name exists in code on that commit. The walk proves that production calls it.

## 3. Production gatekeeper (release promotion tasks)

Merge, staging deploy, and production deploy are three separate stages. In repositories with batched or debounced automatic staging releases (`auto-release-staging.yml`), ordinary PR merges complete at Stage 1 (`batched-staging`) without prompting `[PROD GATEKEEPER]`. When executing a release promotion after Stage 2 staging (`deploy-release.yml` and `walk-release.yml`) is verified for `vX.Y.Z`, report all three with evidence, then ask:

```text
[PROD GATEKEEPER]
- Stage 1 merge: release tag vX.Y.Z = commit <sha>
- Stage 2 staging: run <url>, soak <duration>, health <result>
- Stage 3 production: image <digest>, watchdog <state>
Authorize production deployment of vX.Y.Z? Reply "deploy vX.Y.Z" or "hold".
```

- Claim "deployed" only with an evidence chain: image digest, ledger entry, and a real end-to-end probe (the real browser or TUI).
- Only a production change requires owner approval, with the owner present (Root section `Production reservation`). Ask once, then finish the non-production close. Closing in silence is forbidden.
- Do not wait for the answer to close the issue: close it when the acceptance walk passes on staging. Production state is not an issue state. infra2 owns the production release process (`https://github.com/wangzitian0/infra2/blob/main/docs/ssot/ops.pipeline.md`). Read the state in the infra2 root with `uv run python -m tools.harness status --fetch --online`. Add no label.
- After a "hold", write the release tag and `hold` into a handover note with the command of section 4. The `init` scan reads it.
- A "deploy" covers only the release it names. Immediately before a production dispatch, the owner must answer you live in this session; an earlier or relayed answer is not enough. Without approval, do not deploy production (Root section `Production reservation`).
- Refuse bare "deploy" keywords without release tags or commits. If the owner replies only "deploy", request explicit disambiguation naming the target: "Please confirm release target: deploy vX.Y.Z". Without explicit approval, do not deploy production.
- After "deploy vX.Y.Z", you own the whole loop, including the physical check. Never ask the owner to run a command.

## 4. Suspend: handover and issue

Write the handover with four parts. Include the exact next command.

1. **Done:** commit SHAs, changed files, tests that passed.
2. **Blocked:** the cause (CI, or a fact that the agent cannot get).
   List a step for the owner only when it needs the owner's hands or presence, for example a production deploy. Other examples: a setting that the agent token cannot change, a credential root.
   Other work is your next step. If a gate holds non-production work, the gate is the defect.
   Name the missing physical fact, then do the agent work that supplies it.
3. **Decisions:** contracts you fixed and assumptions you overturned.
4. **Next:** the first command for the next session. For each check due after the session, name
   where it is recorded: an issue comment, a label or a scheduled task. An in-session timer
   does not count.

```bash
ws-bm write-note --folder memory/handover --tags handover --title "Handover: issue-<N> <slug>" --content "..."
```

Also update the issue with the same four parts. Search for an existing issue first. Create one only when none matches.

## 5. Complete: clean up

1. Kill every background task, watcher, and subagent bound to the worktree.
   Check for busy files with a 15-second timeout guard:
   ```bash
   python3 - "$WORKTREE" <<'EOF'
   import subprocess, sys
   wt = sys.argv[1]
   try:
       r = subprocess.run(["lsof", "+D", wt], capture_output=True, text=True, timeout=15)
       if r.returncode == 0 and r.stdout.strip():
           print("WARNING: Worktree has active processes:\n" + r.stdout.strip())
   except subprocess.TimeoutExpired:
       print("WARNING: lsof timed out after 15s (filesystem may be remote/virtual); skipping busy check.")
   except Exception as e:
       print(f"WARNING: lsof check failed ({e}); skipping.")
   EOF
   ```
   Removing a tree under a running task corrupts it.
2. Remove only the CLI issue worktree `../<repo>_issue<N>_<slug>` (never auto-remove IDE worktrees under `~/.gemini/antigravity/worktrees/`):
   ```bash
   git worktree unlock "../<repo>_issue<N>_<slug>" 2>/dev/null || true
   git worktree remove --force "../<repo>_issue<N>_<slug>" || git worktree prune
   ```
3. Delete the merged branch when `gh pr view <n> --json state,headRefOid,isCrossRepository` shows `MERGED`, no cross-repository head, and `git rev-parse <branch>` equals `headRefOid`.
   Run `git branch -d` first. A squash or rebase merge can make it refuse. The equal tip proves that nothing is lost, so `-D` is then safe. A host gate that blocks `-D` stays in force: leave the local branch and say so in the handover.
   Delete the remote branch only at that tip: `git push --force-with-lease=refs/heads/<branch>:<headRefOid> origin --delete <branch>`. GitHub may have deleted it already.
   The PR keeps `refs/pull/<n>/head`, so the commits stay recoverable. A different tip means commits that the PR did not merge: open a new PR for them or write them into the handover.
4. Close the issue with the merge proof when every row of the acceptance walk (2.6) passes. The disposition must be `none`, `staging`, `deployed`, or `hold`. Otherwise keep it open and post the failing rows as a scope note. Reopen an issue that the merge closed. Otherwise means: `batched-staging`, a failing row, or an open sibling lane of an umbrella issue.
5. Delete scratch files. Record each leftover TODO in the handover.

## 6. Route each lesson (distill)

Every finding from the session has exactly one destination, or an announced discard. Use a read-only agent to decide.
The agent that wrote the code does not judge its own lessons.

Ask in order. The first YES decides:

1. True only this time (one SHA, one count, one temp path)? **Discard, and say so in the report.**
2. Can an automatic check catch it? **Build the check. Do not write a rule.** A red assertion works every time. Prose works when read.
3. Would it change a future judgment? **Write it as a criterion.** Choose the tier by what it depends on:
   - holds on any machine: Root rules;
   - holds only with this environment's shared infrastructure: Workspace rules;
   - holds only for this project's goal: Repo rules.

   If you cannot name the tier, you do not yet know what it depends on. Do not write it.
4. Unfinished work, or state for someone else? **Issue or handover.**
5. A location of an external thing (dashboard, ticket, log path)? **Memory reference.**
6. True only for this checkout, or tier unclear? **Put it in the local holding area** for the read-only agent to place.

Red lines:

- **R1** No rule without the measurement that triggered it: which session, what went wrong, what it cost.
- **R2** Resident text holds criteria only. Move steps, lists, and templates to a skill and leave a pointer.
- **R3** The distiller is not the executor.
- **R4** Discard out loud.
- **R5** One invariant lives in one tier. Copies drift. Skills may restate a criterion but must point back to the owner.
- **R6** A pointer must resolve to the same literal string in the target. A pointer to a dropped invariant disguises the loss as convergence.

A finding that is both a criterion and unfinished work becomes two records. One record inside an issue dies when the issue closes.

## 7. Report

Report in the owner's language, in a short table. Show the mode, merge proof, verification that ran on which machine,
the oracles you did not touch, the sample size, the data age, and the discarded findings.

End with the **Falsification Probe** instead of formulaic prose:
- **Target**: What physical probe would expose if this change were secretly broken, empty, or un-deployed?
- **Command**: `<exact probe command>`
- **Physical Output**: `<raw stdout snippet proving non-empty real-world effect>`
