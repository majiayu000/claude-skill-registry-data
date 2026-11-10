---
name: delivery-common
description: Shared worker dialogue, local review procedure, risk tier, and completion policy for GitHub issue and Azure DevOps Work Item delivery. Read when a delivery workflow dispatches workers through its start skill, has workers draft the shared understanding and design preflight for the coordinator to ask, hands the settled scope to preflight and implementation, sets a change's risk tier, requires normal, adversarial, and security reviews, selects focused follow-up of a committed implementation, decides whether local reviews repeat or advance, keeps a progress record, resumes a delivery, checks the published head before advancing, prepares a merge confirmation, stops at a bound or a missing prerequisite, or reports completion and follow-up candidates. Also states the delegated authorization rule that the PR, review request, and delivery skills link.
---

# Delivery Common

Use [Worker Dialogue](references/worker-dialogue.md) for worker dispatch through
the start skill and for each target's shared understanding, design preflight,
and implementation: workers draft, and the coordinator asks the user. Use
[Local Review](references/local-review.md) when a delivery workflow
reaches its local reviews or selects focused follow-up, and apply its Assess
findings to local and hosted findings. Use [Risk Tier](references/risk-tier.md)
to set the tier before preflight and on each reviewed head, and to select the
tier's review procedure, including the security reviewer and the recommended
human review. Local Review also sets local review
escalation, advancement, and round limits. Use
[Delivery Completion](references/completion.md) for the progress record,
resume, the decision summary shown before publication and at merge, the
published-head check and advance after publication, the merge confirmation,
bounds, the final report and `Complete` rule, and follow-up candidates. Apply
[Missing Prerequisites](#missing-prerequisites) whenever a phase lacks what it
needs.

The calling workflow owns implementation, assessment decisions, how its hosted
review runs, publication, and approvals;
[Delegated Authorization](#delegated-authorization) says how those approvals
pass to the skills it calls. Where shared text names the calling workflow's
additions, the calling workflow lists its provider-specific items next to its
link. Return the completed results, review scope, reviewed snapshot, and tier
to that caller.

## Delegated Authorization

A delegated call carries the user's actual request, the exact target, and the
existing approvals. The caller forwards them to each skill it calls; the called
skill acts only within them and, before an action they do not cover, prepares
the concrete result and asks for the missing approval. A skill reference,
automatic selection, or automatic discovery authorizes nothing. Reuse approval
already given for the same scope instead of asking again. Each called skill
keeps its own approval model: what an explicit request approves and what still
needs asking.

The PR, review request, and Codex review cycle skills and the delivery skills
of both providers link this section instead of restating it.

## Missing Prerequisites

A missing prerequisite, such as a component skill, a required reviewer, or a
tool a step runs, stops the phase that needs it for the affected targets.
Report it as a blocker, naming what is missing and, for a skill, the profile
that installs it, such as `base,github`. Never install it, substitute another
skill or an informal check for it, or skip the phase. Independent work that
does not depend on it continues under Delivery Completion's
[Bounds](references/completion.md#bounds). The delivery skills of both
providers and [Local Review](references/local-review.md) link this section
instead of restating it.

## Shared Scripts

[`scripts/check-branch-name.mjs`](scripts/check-branch-name.mjs) is the shared
**safe branch name** check. The start, delivery, PR, and cleanup skills of every
provider, including Beads, run it from their own step; its header gives the
usage and exit codes.

[`scripts/check-push-target.mjs`](scripts/check-push-target.mjs) is the shared
**push target rule** check. The PR publish skills of both providers, and
`github-pr-create` and `github-pr-codex-review-cycle`, run it to resolve the push
remote and to check the upstream before and after the push; its header gives the
usage and exit codes.

[`scripts/check-cleanup-targets.mjs`](scripts/check-cleanup-targets.mjs) is the
shared **remote branch deletion check** and **cleanup target manifest**. The
worktree cleanup skills of both providers run it to decide whether to delete the
remote branch, to build the targets the user confirms or a Caller preview, and
to compare them right before any removal; its header gives the usage and exit
codes.
