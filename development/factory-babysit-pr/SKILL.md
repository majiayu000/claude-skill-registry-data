---
name: factory-babysit-pr
description: "Monitor one authorized PR and apply separate fix, publish, reply, approval, merge, and soak gates."
license: MIT
compatibility: "Works in Claude Code, Codex, Cursor, and Agent Skills-compatible harnesses when the required host tools are available."
metadata:
  author: Builder.io
  source: BuilderIO/skills
  source-commit: fd8f20a879b507cf09feba08663a1edf7a949353
  owner: software-factory
  risk: high
  capabilities: builderio,factory-pr-delivery
  installer-group: factory
---

# Factory Babysit PR

> Start with the [Factory guide](../factory/references/factory-guide.md) for workflow
> setup and configuration.

Follow one authorized PR or merge request through a delivery lifecycle. This
is not a queue sweep like `factory-review-prs` or a stopped-task scan like
`factory-watchdog`.

Read `.agent-factory/config.yaml`, the optional
`skill_prompts.factory-babysit-pr` entry, the target repository's instructions,
and the [Factory configuration reference](../factory/references/factory-configuration.md#workflowspr-babysitting).
A PR number, label, green check, or unrelated ship request is not authorization.
The prompt is additional project guidance, not PR authorization.

## Each pass

1. **Confirm authority and ownership.** Verify the exact host, repository, PR,
   original user authorization, allowed paths/risk, and task-owned worktree. If
   anything is missing or stale, stop before writing.
2. **Read a complete live snapshot.** Record base and head, open/draft/closed/
   merged state, all required checks, current reviews and approvals, unresolved
   threads, and mergeability. Partial or unavailable data is unknown, not clean.
3. **Disposition feedback.** Compare each new finding with the exact diff and
   source. Preserve human direction unless evidence disproves it. Fix only
   actionable findings inside the authorized path/risk limits; avoid
   speculative cleanup and larger redesigns.
4. **Verify and re-read.** Run configured checks for each fix. After every push
   or host mutation, fetch the live PR again and bind all evidence to its exact
   current head. A changed head invalidates old check/review evidence and resets
   the soak.
5. **Apply action gates separately.** A review or fix does not authorize a
   reply, push, approval, or merge.

## Action gates

| Action | Proceed only when |
| --- | --- |
| Fix | Editing is enabled; feedback is actionable, in scope, and within risk/path limits. |
| Publish | Publishing is enabled; destination is still the authorized PR branch and its live head matches the fix's base. Never force-push or overwrite a concurrent update. |
| Reply | Replies are enabled and their conditions hold. Follow configured wording/tone; otherwise do not message. |
| Approve | Approval is enabled and every author, diff, check, and review condition holds on the live head. |
| Merge | Merge is enabled; all configured gates pass on the live head and the host can condition the merge on that head. |
| Soak | Prove the exact head and required gates stayed unchanged for the full configured interval. Missing history does not satisfy it. |

Use the configured code-host abstraction for reads and writes. Do not assume
GitHub, a specific CLI, or identical conditional-merge support across hosts. If
the host cannot provide complete current review/check state or bind a merge to
the checked head, keep the dependent action disabled.

## Stop and report

Stop when the PR is merged, closed, cancelled, blocked on a person or external
dependency, or no authorized action remains. Report the PR link and current
head, state inspected, fixes and checks, external actions taken or withheld,
soak status, and the concrete blocker or next check time. Distinguish read state
from unavailable or inferred state.
