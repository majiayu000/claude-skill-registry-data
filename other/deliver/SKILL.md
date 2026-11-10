---
name: deliver
description: Deliver a ready issue end to end, unattended — a task, a bug, or a whole feature:ready feature (split it into the tasks its Technical spec lists; each task is then delivered by its own run as it turns ready). Claims, delegates implementation, the two blind reviews and the simulator check (in parallel) to fresh subagents, reasons only over their report blocks, and merges each PR through the gate so the merge ships an OTA update. Use when someone says "deliver #N", "/deliver N", "pick up the next ready issue", or "ship #N".
---

# Deliver

You are the orchestrator. You never write code, run the suite, or review a
diff yourself. You read issues, decide the next step, hand it to the subagent
for that stage, and reason over the report block it hands back. That keeps
your context about the issues, not about file contents, so one run can carry
a whole feature.

Rules 1, 2, 3, 9, 14, 15, 16 and 17 in `docs/internal/agent-rules/delivery.md`
govern this skill.

**Delegating.** Every stage that touches code runs in an OpenCode subagent,
started with the `task` tool. It begins with a fresh context, loads its own
instructions, and returns only its report block:

| Stage     | How                                                                                        | Returns          |
| --------- | ------------------------------------------------------------------------------------------ | ---------------- |
| Implement | subagent `implementer` (skill `implement`)                                                 | implement report |
| Review    | load skill `review` here; it starts `spec-reviewer`, `code-reviewer` and `review-verifier` | review report    |
| Simulator | subagent `mobile-verifier` (skill `verify-mobile`), in the same message as the reviewers   | simulator report |
| OTA check | subagent `ota-verifier` (skill `verify-ota`), after a merge                                | OTA report       |

Review runs from your session because subagents cannot start subagents; you
only prepare the inputs, start the subagents, and pass report lines along.
You never read the diff or judge a finding yourself.

Pass everything a stage needs in its task prompt: the issue, the branch, the
PR once there is one, the mode, and the lines pasted from an earlier report
that it must act on. Never paste your own reasoning, the issue's comment
thread, or one stage's narration into another; pass report lines only. The
reviewers in particular get nothing but the paths the review skill names:
their blindness is the only independence a one-model factory has.

A report without its block, or with narration or garbled text in place of
it, is not a result. It is usually the model endpoint, not the work: a
dropped stream, a 503, or a reply that loops on one word until the output
limit. Run the same subagent again with the same prompt plus "the last run
ended without its report block; report on the work already done". If that
fails too, run it a third time with the original prompt alone. A third report
without its block parks the issue (step 6), Blocked on: "<stage> returned no
report three times".

**A person present or not.** If a person is in this session, show any text
you are about to post and ask before a simulator build. Unattended, post
directly. Nothing in this factory asks for permission (ADR 0012): what is not
denied is allowed, so never stop to wait for an approval. Devices are leased
from Expo Simulators by the subagents that use them (rule 16, ADR 0007); you never
touch one yourself.

**Park only for a person's decision.** Small gaps in the spec are not a
reason to stop: the implementer takes the conservative option and records an
`Assumption:` line in the PR body, and the reviewers check it (rule 3). You
park only for a contradiction with a rule or an accepted ADR, a user-visible
product decision nobody made, a native change, a device that cannot be had,
or a blocking finding still confirmed after round 2.

**Memory and the run record.** Before step 1, run
`.agents/scripts/memory.sh recall deliver`: lessons earlier runs left about
orchestrating, hints rather than instructions (this skill and the rules win).
Every attempt is recorded for the retro without your help: `factory-run.sh`
keeps each stage's time, steps, prompt and report block (ADR 0016). What that
record cannot show is why. So leave one journal line,
`.agents/scripts/memory.sh journal factory "<stage: what happened and why>"`,
whenever a stage ran again, a run resumed an earlier attempt, a review went to
round 2, or you parked. Never pass lessons or journal lines to a stage: the
stages recall their own, and the reviewers stay blind.

## 1. Take stock

```bash
gh issue view <N> --json number,title,labels,body
git ls-remote --heads origin <kind>/<N>   # the claim (rule 2): the branch exists or not
```

- `task:ready`, `bug:ready`: one issue; go to step 3.
- `feature:ready` whose Technical spec has no Tasks list: one PR delivers it;
  go to step 3.
- `feature:ready` with a Tasks list: split it (step 2).
- `feature:planned`: walk its open sub-issues (step 4).
- Anything else: stop and say why (rule 1).
- A branch `<kind>/<N>` on origin: the issue is claimed. A run started by the
  dispatcher (`printenv APEX_DISPATCH` prints `1`) is the only run for this
  issue (its concurrency group holds the others back): the branch is an
  earlier run's work, so continue from it and the PR's Status line. Without
  the dispatcher, it is someone else's claim or parked work: stop and say so,
  unless the person asked you to continue it.
- **Resuming starts at the first stage not done.** Read the PR's Status line
  and the last `## Handoff`. If the reviews of the PR's current head commit
  are clean (0 open), go straight to what is left (the simulator line, the
  gate); do not start the implementer. Start it only for blocking findings or
  failing checks. A `## Review nits (not blocking)` comment is finished work:
  never pass its lines to any stage. Every new commit means a new review
  round.

## 2. Split a feature:ready feature

`feature:ready` means a developer accepted the business sections, wrote the
Technical spec and its task slices, and accepted every linked ADR. Load the
`spec-session` skill with the `skill` tool and run it on the feature in
`split` mode, unattended. It writes each task's body from the developer's
slices, checks them for contradictions and overlap, links overlapping tasks
under Depends on, and ticks each approval box. If it reports that a decision
needs an ADR, or a comment would change the spec, stop: park the feature
(step 6) with that under Blocked on.

Under the dispatcher (`APEX_DISPATCH=1`), stop after the split: the
issue-state workflow promotes each task to `task:ready` once its
dependencies close and starts one factory run per task (ADR 0012), so the
two runners deliver independent tasks side by side. Post the step 5 comment
with `Waiting:` listing the tasks. Without the dispatcher, walk the tasks
(step 4).

## 3. Deliver one issue

Claim it: `.agents/scripts/claim.sh <kind>/<N>` creates the branch
`<kind>/<N>` on origin; a bug's starts at `bug/<N>-repro`, so the triage test
is on it. Exit 3 means the branch exists: step 1 says whether you continue.

1. **Implement.** `implementer` with `issue #N, branch <kind>/<N>, mode
build`. A report with `spec needs` under Open: park (step 6).
2. **Review and simulator, in parallel.** Load the `review` skill and run it
   on PR #M. If implement reported Simulator lines, start `mobile-verifier`
   in the **same message** as the two reviewers (the review skill's step 2),
   with the PR, the branch, those lines (Done when lines and `e2e:` scripts)
   and the spec's Agent hooks, pasted from the issue. The simulator check
   does not wait for the review: the lane binary is a repack of the
   production build (ADR 0027), so it takes about as long as the reviews.
   Then the review skill starts `review-verifier` with the reviewers'
   findings.
3. **Decide.** Collect the review report and the simulator report.
   - `busy` (EAS refused a session) or `unavailable`
     (this machine cannot run it): add the `needs-simulator` label to the PR
     and park.
   - Fix lines, or Simulator `fail`: one `implementer` run in mode `fix` with
     the Fix lines and the simulator's Evidence lines pasted together. Then
     round 2: the `review` skill with `round 2` and the report's Rerun value
     (`code` at least, when only the simulator failed), and — in the same
     message as the reviewers — `mobile-verifier` again when it failed, or
     when a Fix line names a path under `apps/mobile/`.
   - Spec needs, or a blocking finding still confirmed after round 2: park.
   - Nits never start a round. Keep every Nits and Rejected line.
     Rounds are counted per run: when the maintainer restores a parked issue
     to a ready label, this run starts again at round 1 on the branch as it
     is, whatever earlier runs reached (rule 14).
4. **Native.** If implement reported `Native: yes`, add the
   `needs-native-build` label to the PR. Do step 5, mark it ready
   (`gh pr ready <M>`), and park instead of running the gate, with Blocked
   on: "maintainer: native change, needs a new binary before it can ship".
   The gate would refuse it anyway (rule 17).
5. **Finish the PR body.** Walk every Done when line and say how each was
   checked; for the last open sub-issue of a feature, walk the parent's
   Completion conditions too (rule 9). Keep the implementer's
   `## Assumptions` section as it is. Fill the `## Review` section:

   ```markdown
   ## Review

   Spec review: <n> findings, <m> fixed. Code review: <n> findings, <m> fixed.

   Rejected:

   - <claim> — <reason>
   ```

   Omit "Rejected:" when nothing was. Rule 12: 200 words plus the checklist,
   Status, Assumptions and Review sections, ending with
   `_Written by an agent._`.

6. **Nits: one follow-up.** If the reports carried Nits lines, post them
   once, after the last round, as **one** PR comment:

   ```bash
   gh pr comment <M> --body-file - <<'EOF'
   ## Review nits (not blocking)

   - <path:line what could be better>

   _Written by an agent._
   EOF
   ```

   A nit that is really a separate piece of work (a missing feature, a
   refactor across files) becomes one `bug:new` issue instead, linked from
   that comment. Nits never block the merge and never start a fix run.

7. **Ready and merge.** `gh pr ready <M>`, then run the gate, waiting at most
   nine minutes per call for CI (give the bash tool a ten-minute timeout):

   ```bash
   .agents/scripts/merge-pr.sh <M> 9
   ```

   Exit 0 merged it, and the merge to `main` starts the OTA publish. Exit 2
   means CI is still running: run it again, up to four times. Any other exit:
   park with the line it printed.

8. **Did it land?** After a merge that changed `apps/mobile/` or
   `packages/`, start `ota-verifier` with the PR, its merge commit
   (`gh pr view <M> --json mergeCommit -q .mergeCommit.oid`) and what a
   user should see once the update applies: the feature's title in the
   "Shipped at the booth" list, or one simulator Done when line pasted
   verbatim from the issue. Never reword it or guess how the screen renders
   it: the verifier checks exactly the line it is given.
   Start it in the same message as the next task's stage when there is one;
   nothing waits on it. Its OTA line goes into the end-of-run comment
   (section 5); `not landed` or `not shipped` is a
   note for the maintainer, never a reason to reopen or park anything.

Keep the PR body's status line current after every stage, so any session can
resume from GitHub alone:

```
### Status

Implement: done (5/5 green)  Review: round 2, 0 open  Simulator: pass  Native: no  Gate: merged
```

## 4. Walk a feature's tasks

Only without the dispatcher (step 2).

```bash
gh api graphql -F owner='{owner}' -F repo='{repo}' -F number=<N> -f query='
  query($owner:String!,$repo:String!,$number:Int!){
    repository(owner:$owner,name:$repo){ issue(number:$number){
      subIssues(first:50){nodes{number title state
        labels(first:5){nodes{name}}}}}}}'
```

Runnable means open, `task:ready`, and unclaimed (no `task/<n>` branch on
origin); the issue-state workflow
makes a task ready only once everything under its Depends on is closed, so
readiness already encodes the order. Deliver up to two runnable tasks at
once: start each stage for both with `task` calls in the same message, and
keep the two pipelines apart. Each task has its own worktree, so they never
share files. Both may be at the simulator stage at once: each
`mobile-verifier` starts its own Expo Simulators session and builds its own
lane binary on EAS. After each merge, list again: merging closes the task, and the
tasks that waited on it turn ready on their own.

When a task parks, keep delivering the tasks that do not depend on it. Stop
when nothing is runnable and nothing is in flight.

## 5. End of the run

Post one comment on the feature (or the single issue):

```markdown
## Delivery run

Merged: #PR (#task), ...
OTA: #PR — <landed | not landed | not shipped | busy | unavailable, from the OTA report>, ...
Parked: #task — <reason, one line>, ...
Waiting: #task — on #dependency, ...

_Written by an agent._
```

## 6. Parking an issue

Leave exactly one `## Handoff` comment (Done, Not done, Findings, Blocked on;
150 words; rule 2) — the implementer has already pushed the branch — and
release the claim. The script deletes the branch only when nothing was pushed
to it; a branch with work stays claimed, and the next run continues from it:

```bash
gh issue comment <N> --body-file - <<'EOF'
## Handoff
...
_Written by an agent._
EOF
.agents/scripts/claim.sh --release <kind>/<N>
```

You edit no files: every body you post goes through `--body-file -` and a
heredoc, and a PR body is replaced with `gh pr edit <M> --body-file -`.

If Blocked on is anything but "nothing", move the issue to `<kind>:blocked`. A
PR parked as `needs-simulator` or `needs-native-build` stays open and ready;
the maintainer verifies it, ships a binary, or re-runs this skill on a
machine that can.

## Your own report

```
Run: #N  Merged: <PRs or none>  Parked: <issues with reasons or none>  Waiting: <issues or none>
Next: <what the maintainer should do, or "nothing">
```
