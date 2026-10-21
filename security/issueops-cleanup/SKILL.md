---
name: issueops-cleanup
description: Safely finish a merged IssueOps cycle by closing its linked issue, removing its local worktree, and deleting its local branch. Use when the user asks for IssueOps cleanup, post-merge cleanup, worktree/branch deletion plus issue closure, or says "이슈옵스 정리", "워크트리 지우고 브랜치 지우고 이슈 닫아줘".
---

# IssueOps Cleanup

Finish one record-backed, merged IssueOps cycle through harness-owned surfaces.

**User's request:** $ARGUMENTS

Exactly three effects are authorized after target confirmation: close and verify
the linked parent issue, remove the recorded local worktree, delete its local branch.
Remote branch deletion is a separate decision and `cleanup remote-branch` flow.

This body is the complete actor contract for copied or body-only use. Installed
`issueops`, `issueops-remote-write`, `git-operations`, and `gitlab-usecase` can supply
additional recipes; their absence never requires installation or evaluator material.
Resolve optional links from this file's real, symlink-resolved location, not cwd.
Use only observed CLI contracts; report missing inputs/tools rather than inventing them.

## Entry and authority

Resolve the exact ID as below, then run `issueops next --id "$ISSUEOPS_ID" --json`.
Require `stage.key=done`; otherwise follow the named stage/`next_command`, not cleanup.
Before each durable mutation, re-read the record and `execution whoami --json`.
Use its `record_actor_flags` for records and `claim_actor_flags` for execution
operations where the CLI requires them; never assemble identity flags yourself.
Preserve the exact ID, recorded generation, native actor, source cwd and target
worktree. A released completion is not permission to reclaim or bypass a holder.
`issueops status` and `issueops feedback add` are supported aliases; authenticated
recording belongs to this stage. `quality inspect` is not a semantic skill runner;
`issueops skill-bench` is unsupported.

## Preconditions

1. Prefer the supplied ID/`$ISSUEOPS_ID`; otherwise `issueops list --repo "$PWD" --json`.
   Ask which ID only if zero or multiple plausible cycles remain.
2. Run from the record's source repository, never the worktree being removed.
3. Require `done`, a released execution lease, and provider-verified merged PR/MR.
   `execution complete` owns done/release; this skill never records completion.
4. Linked child tasks must already have verified close evidence.
5. Dirty worktree, branch mismatch, unreadable provider state
   or pending external intent blocks cleanup. Occupants do NOT block: preview
   lists `workspace_processes` (pid, command, start time, descendant/collateral
   counts); typed apply stops them.
   Requester occupancy still blocks: `requester_occupies_worktree` includes
   ancestors. `worktree_is_source_checkout` also
   blocks. Use a different terminal/worktree, never manual process killing.
6. The remote source branch must be absent, or the user must have chosen to
   leave it. On `remote_branch_absent`, present both exits and let the user pick:
   - delete through the separately authorized `issueops cleanup remote-branch` flow, then finish;
   - finish with `--keep-remote-branch`. Record deletion prevents later typed
     deletion through this record. Report `kept_remote_branch` and the audit
     fragment `remote_branch_kept=<branch>@<oid>`. The issue-number branch name
     and provider link keep it discoverable; finish does not write the issue body.
   A remote that cannot be read blocks the same way and takes the same two
   exits; `--keep-remote-branch` records `state: "unreadable"` instead of an OID.
7. Prepared and provider-observed merged base must match (`base_branch_drifted`).
   Exemption: the prepared base is observed **absent from origin** AND the merged
   base is the repository default. Preview reports `retargeted_base` with both
   bases, default branch and absence evidence. Failed observation blocks with
   `merged_base_remote_unobserved`; no flag may assert a base.
   A deliberate retarget must be recorded **before** finish with
   `issueops branch retarget --id ID --base-branch REF --reason TEXT`: it accepts
   only a base the provider currently shows as the PR/MR target and that exists on
   `origin`, then appends `branch_prepare.retargets[]` and moves the prepared base,
   so finish compares against that recorded decision.
   Check absence with `git ls-remote --heads origin
   refs/heads/<prepared-base>` (empty output means gone); do not reach for
   `ls-remote --symref`, which the command policy rejects.

Unmerged retirement (draft PR/MR, issue and remote branch closure) belongs to
`issueops-abandon`/typed `cleanup abandon`, not this path. An unmerged PR/MR the
developer approved is merged first by `issueops-merge`: `issueops remote merge-pr`
merges without deleting the branch, and that skill's step 6 deletes the remote branch
through `issueops cleanup remote-branch` before handing off here.

## Project docs

Before the preview, read the `.issueops/CAUTIONS.md` index and route the task through
`project_docs_route` (or `issueops project route-docs --repo "$PWD" --task "<cleanup
summary>" --json` when MCP is unavailable) to pick the dated `cautions/` and `adr/`
records about cleanup, worktree processes, and remote branches. Recorded cleanup
failures are the first things to check in the preview. In the confirmation summary,
record each caution that applies with its path, or "none applied".

## Preview the exact targets

Read the lifecycle and cleanup inventory:

```text
issueops status --id "$ISSUEOPS_ID" --json
issueops cleanup status --id "$ISSUEOPS_ID" --merged --json
issueops remote close-issue --id "$ISSUEOPS_ID" \
  --provider "$PROVIDER" --json
```

Without `--confirm`, close is a dry-run. Verify live Git targets:

```text
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" symbolic-ref --quiet --short HEAD
git -C "$WORKTREE_PATH" rev-parse --verify HEAD
git -C "$REPO_ROOT" rev-parse --verify "refs/heads/$BRANCH"
```

Require a clean status, a symbolic branch exactly equal to `$BRANCH`, and a
worktree HEAD OID exactly equal to the local branch OID. If the provider exposes
the merged artifact head OID, require it to equal the local branch OID too.
A detached, repurposed, mismatched, or advanced worktree blocks cleanup.

Before confirmation, status `missing` may contain only `completion_reflected`
and `issue_closed`. Its other gates (`pr_phase`, `remote_artifact_*`,
`child_tasks_closed`, `worktree_*`, `branch_match`, `remote_branch_*`) must pass.
Finish preview renders the same two completion gates and their `next_command`;
after reflection only `issue_closed` remains. Do not wait for an empty list
before steps 1-2; only afterward must both previews be clear.
The close-issue dry-run must report `ok: true`. Any other missing gate or provider
error blocks closure: report it and stop before writing.

From these results, state:

- lifecycle ID and issue URL;
- provider and verified merged PR/MR;
- exact local worktree path;
- exact local branch, worktree HEAD OID, local branch OID and available merged-head match;
- that the remote branch will not be deleted;
- every process the apply will stop (`workspace_processes`
  with pid/command/start time and descendant/collateral counts),
  because unsaved work in those processes is lost;
- every readiness blocker.

Missing/ambiguous targets or other blockers mean stop. Never infer targets from an issue title.

## Confirmation boundary

Obtain one explicit confirmation naming all three destructive/external effects:

```text
이슈 <URL>을 닫고, HEAD <WORKTREE_HEAD_OID>인 로컬 워크트리 <PATH>와
OID <BRANCH_OID>인 로컬 브랜치 <BRANCH>를 삭제할까요?
apply가 먼저 종료하는 것: 프로세스 <N>개(<pid:command …>).
원격 브랜치는 삭제하지 않습니다.
주의사항: <Project docs에서 고른 caution마다 "문서 경로: 해당 문장 인용", 없으면 "열어 본 caution <경로 목록>, 해당 없음">
```

If no processes are listed, say nothing will be stopped. The `주의사항:` line is the
record the `Project docs` section asks for; write it in the confirmation itself.

The latest user message must confirm these exact targets; generic "cleanup" authorizes preview only.

## Apply in fail-closed order

### 1. Reflect completion into the issue

Preserve the team's progress report before closing; otherwise finish blocks on
`completion_reflected`. Every remote write uses preview → identical confirm →
readback. Changed body means a new preview; uncertain results mean reconcile,
never repeat a create/write or bypass the harness with raw provider mutations.

- Read the merged PR body and `issueops status --id "$ISSUEOPS_ID" --json`.
- Write one or two result sentences, then three to six flow lines (plan, what the
  review changed, implementation with the PR link, what was checked, what is
  left). Call `fluent-korean` if installed; otherwise directly review complete
  Korean sentences, clear subjects, concrete results and unnecessary modifiers.
  Remove secrets. Fix readability warnings or record why each remains.
- Save a temporary file outside the worktree; the issue body is the enduring record.

```text
issueops remote reflect-completion --id "$ISSUEOPS_ID" \
  --provider "$PROVIDER" --body-file "$RESULT_FILE" --json
issueops remote reflect-completion --id "$ISSUEOPS_ID" \
  --provider "$PROVIDER" --body-file "$RESULT_FILE" --confirm --json
```

Require no `readability` critical finding: full SHA, local path or over 2,000 characters is refused.

Require confirmed `ok: true` and matching body/URL readback; already-reflected is idempotent success.

### 2. Close and verify the issue

```text
issueops remote close-issue --id "$ISSUEOPS_ID" \
  --provider "$PROVIDER" --confirm --json
```

Require `ok: true`, `closed: true`, verified closed state; already-closed is idempotent success.

### 3. Re-preview local cleanup

Closure changes readiness: obtain a fresh fingerprint.

```text
issueops cleanup finish --id "$ISSUEOPS_ID" \
  --provider "$PROVIDER" --preview --json
```

Carry the user's `--keep-remote-branch` choice into this preview; it reports
`kept_remote_branch` and includes the flag in `next_command`. Without it, a
remaining remote branch blocks on `remote_branch_absent` and yields no fingerprint.

If `worktree_present=true`, repeat all four live Git checks after closure and before apply.

If a prior typed apply removed the worktree but retained the record (`worktree_present=false`):

- do not run `git -C "$WORKTREE_PATH"` commands;
- require prior-result/record evidence of successful worktree removal;
- require `git worktree list --porcelain` not to contain `$WORKTREE_PATH`;
- when `branch_present` is true, re-read `refs/heads/$BRANCH` and require its
  OID to equal the OID previously confirmed by the user;
- when `branch_present` is false, require `git show-ref --verify --quiet
  "refs/heads/$BRANCH"` to exit `1`.

Require:

- `ok: true`;
- an empty `missing` list;
- a non-empty `fingerprint`;
- `worktree_path` and `branch` equal the targets the user confirmed;
- when the worktree remains present, its live HEAD OID and local branch OID
  equal the confirmed OIDs;
- during typed partial-failure recovery, every still-present branch OID equals
  the confirmed branch OID.

Changed path/name/OID means stop and reconfirm new targets. Never reuse a stale fingerprint.

### 4. Apply the emitted command

Execute the preview's `next_command` exactly. It must be the typed form:

```text
issueops cleanup finish --id "$ISSUEOPS_ID" \
  --apply --confirm --fingerprint "$FINGERPRINT" --json
```

Never substitute raw `git worktree remove`, `git branch -d/-D`, `git update-ref`,
`git push origin --delete`, or manual terminal/process stops.
The fingerprint binds worktree, branch OID and occupant receipts.
Apply stops occupants with HUP+TERM, KILL, and re-observation, and
failure stops at `workspace_processes_stop`; it then removes
the worktree and CAS-deletes the local branch; emits audit and deletes the record.
Any destructive failure retains the record. `workspace_processes_stop` failure
means remaining occupants; re-preview rather than improvise.
Never append remote branch deletion to this flow.

## Verify the observable result

After apply:

1. Require `ok: true` and `record_deleted: true`.
2. If the worktree was present, require `worktree_removed: true`, and report
   `workspace_processes_stopped` exactly as the
   apply returned it.
3. If the local branch was present, require `branch_deleted: true`.
4. From the source repository, verify:

```text
git worktree list --porcelain
git show-ref --verify --quiet "refs/heads/$BRANCH"
```

The removed worktree path must be absent, and `show-ref` must exit `1`.
5. Re-read the remote issue with the provider and require a closed state.
6. Report the issue URL, removed worktree, removed local branch, remote issue
   state, and explicitly state that the remote branch was untouched.

On partial failure report `failed_step` and `next_command`; recover only through the retained
record and the worktree-aware rules above. Do not improvise or report partial work as complete.
