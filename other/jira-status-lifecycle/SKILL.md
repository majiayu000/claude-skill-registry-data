---
name: jira-status-lifecycle
version: "1.0.1"
user-invocable: false
description: "Developer-owned Jira bug status decisions. Before analysis, claim 「解决中」 when the bug is assigned to the session user and still 「待处理」. After the fix merges, decide 「已修复」. Triggers — 「Jira 状态生命周期」「分析前改解决中」「待处理改解决中」「合并后已修复」「Jira 生命周期」 / jira status lifecycle, claim before analysis, mark fixed after merge. Do NOT use to set 验证通过 or 关闭, to read an issue, or to post the repair comment. Load before analyzing a Jira bug and before the post-merge status decision."
---

# Jira Status Lifecycle

> Shared decision for developer-owned Jira bug status. Hosts load it after the issue is read and before analysis. `jira-status-writeback` loads it before the post-merge transition and still owns the repair comment. This skill does not post that comment and does not depend on `jira-status-writeback`.

The executable matrix is [scripts/decide.mjs](scripts/decide.mjs) (`decidePreAnalysis`, `decidePostMerge`, `applyTransitionResult`). Classify the status, call the function, then act on the returned outcome. After a transition call, pass boolean `true` to `applyTransitionResult` only when that call succeeded. Pass `false` for every other result. Do not pass the raw API result. `transition-fixed` keeps `lifecycleComplete` false until that call returns `true`.

## Status classes

Compare the authenticated session user with the issue assignee using the same stable identity the read step already has (account id when both sides have it).

| Class | Canonical name | Also matches |
|---|---|---|
| `todo` | 待处理 | A project status with the same meaning: not started, waiting for the developer |
| `in-progress` | 解决中 | A project status with the same meaning: the developer is working on it |
| `fixed` | 已修复 | A project status with the same meaning: the developer has finished, QA has not closed it |
| `other` | — | Everything else, including 验证通过 and 关闭 |

验证通过 and 关闭 stay `other`. This skill never selects a transition whose target means verified or closed.

## Before analysis

Run this after the issue's assignee and status are known, and before the first analysis stage.

Resolve the authenticated user of the Jira session that read the issue. Pass that user as `actor`. An empty `actor` is `stop-identity-unresolved`: report it, do not call the issue unassigned to the operator, and do not start analysis.

| Outcome | What the host does |
|---|---|
| `stop-identity-unresolved` | Report and stop before analysis |
| `stop-transition-failed` | Report and stop before analysis. The claim was required and the transition failed or had no same-meaning target |
| `need-claim` | Transition to the `in-progress` status with no comment on the transition call, then `applyTransitionResult` |
| `continue-claimed` | Start analysis |
| `continue-already-in-progress` | Start analysis. Do not transition again |
| `continue-unchanged` | Start analysis. Do not transition |
| `continue-not-assignee` | Tell the operator the status was left unchanged because the issue is not assigned to them. Start analysis |

## After merge

`jira-status-writeback` calls `decidePostMerge` only after the fix PR/MR is on the target branch. `transitionAvailable` is true when the workflow exposes a transition to the `fixed` status.

| Outcome | What writeback does |
|---|---|
| `incomplete-identity` | Do not transition and do not treat the issue as someone else's. Post the repair comment. Leave the lifecycle incomplete. Keep the merge |
| `incomplete-not-assignee` | Do not transition and do not post the repair comment. Tell the operator. Leave the lifecycle incomplete. Keep the merge |
| `status-satisfied` | The status is already `fixed`. Skip the transition. Post the repair comment. The status obligation is met |
| `transition-fixed` | Transition to `fixed` with no comment on the transition call, then `applyTransitionResult`. The lifecycle stays incomplete until that call returns boolean `true` |
| `incomplete-transition` | Post the repair comment when `comment` is true. Leave the lifecycle incomplete. Keep the merge |

A failed transition call on `transition-fixed` becomes `incomplete-transition`. The repair comment still posts. The merge stays. The host reports the lifecycle incomplete and does not describe the bug as 已修复.

## Integration

Hosts that analyze a Jira bug, and `jira-status-writeback`, declare `jira-status-lifecycle` in frontmatter `dependencies` and abort when it is missing (`npx skills add FuDesign2008/open-skills -g --skill jira-status-lifecycle --yes`).

Keep the decision table in this skill. Hosts keep a load pointer and follow the outcome. Under `ai-proxy`, these two developer-owned transitions still run. Merge, 验证通过, and 关闭 stay with a person.
