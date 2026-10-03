---
name: sanity-check
description: >-
  Assess whether a claimed problem or blocker is real, consequential, and worth
  fixing now. Use at the first failure that blocks a task, when investigation
  stops producing evidence, or when asked whether a feature, CI test, or other
  machinery is necessary. Ground the decision with recon, debug-mantra, and
  ponytail; defer low-risk work through PRS-rated GitHub intake and propose
  feature retirement or required-gate changes for operator decision.
---

# Sanity-check

Before investing in a fix, establish what failed, what consequence matters, and
why it must block the user's goal. A real failure is not automatically an urgent
blocker. An inconvenient failure is not automatically dispensable.

This skill assesses and routes work. It does not need scripts, a new scoring
system, a CI gate, or a full audit to judge one blocker.

## Activation and authority

Run a brief relevance check at the first blocker. Reuse current evidence and
prior operator decisions. Deepen only when the consequence is uncertain, the
proposed disposition needs more evidence, or investigation stops advancing.
Do not repeat the assessment on every retry without new information.

Ask about a core or user-facing capability's importance only when it is unclear.
Explain the concrete consequence first; ask a product question the operator can
answer, not whether an unfamiliar internal function is "important."

Within the authorized task, defer demonstrated low-risk, nonblocking work and
file or update its PRS-rated GitHub issue. Propose feature retirement and any
weakening or removal of a required gate for operator decision; execute only
when existing or newly supplied authorization covers the concrete change.
Deferring a repair does not waive a required gate or establish merge readiness.
Updating expected content after an intentional, authorized change is ordinary
repair when the protected contract is preserved; narrowing coverage is weakening.
Follow the repository's existing intake, safety, and change procedures.

## Reuse existing skills

Resolve these skills in the installed collection or the repository's `skills/`
tree, including the siblings below. Relative links describe the repository
layout; in a flat installed collection resolve by skill name. Read the relevant
instructions before using them; do not pretend an
unavailable skill ran. Reuse evidence already collected for this task.

| Skill | Contribution |
|---|---|
| `recon` | Trace the relevant consumers, contracts, state, and consequences of changing or omitting the mechanism. |
| `debug-mantra` | Observe raw evidence, trace the fail path, falsify the claim, and preserve experiment findings. |
| `ponytail` | Minimize the mechanism once the requirement and evidence are established. |
| `triangulate` | Determine evidence depth when the risk of overbuilding and the risk of insufficient investigation conflict. |
| `ci-suite-audit` | Consult its contract, unique-coverage, and assertion-quality criteria for CI retention questions. A full audit remains a separately invoked workflow. |
| `start-task` | Reuse its task-rating policy and the target repository's intake procedure when recording deferred work. Reading that policy does not launch its execution lifecycle. |
| `unstuck` | Resume the original task when the disposition has removed a false prerequisite or resolved a stalled decision. |

Keep the initial assessment small. A known, necessary failure can route directly
to its existing repair workflow. Full root-cause diagnosis is required before
claiming a root-cause fix, not before making an evidence-supported decision to
defer a low-risk issue.

## Decision ladder

1. **Name the goal and test the dependency.** State: "The user wants X; Y
   failed; Y allegedly blocks X because Z." Identify the source of Z: actual
   behavior, an explicit requirement, repository policy, an external dependency,
   or an agent assumption. Ask what concrete outcome becomes unsafe or
   impossible if Y remains unresolved. A red status alone does not explain
   product harm; an enforced gate can still be a real delivery blocker even
   when the underlying check deserves reconsideration.

2. **Check for credible immediate harm.** Identify the affected data or asset,
   the reachable failure or exposure path, and the supporting observation.
   Distinguish confirmed harm, credible potential harm, and an unsupported
   concern. For ongoing corruption, data loss, or security exposure, prioritize
   reversible containment within existing authority and escalate consequential
   actions. Do not replay a destructive failure against live data. Do not delay
   containment to debate feature popularity. Conversely, the words "security"
   or "integrity" without a supported path do not justify an unlimited audit.
   Record unknown exposure explicitly; do not label it safe by default.

3. **Establish requirement value.** Read the stated project purpose, accepted
   requirements, current consumers, and relevant operator decisions. When a
   core or user-facing capability's importance remains unclear, ask:
   "If we leave this unresolved, [specific consequence]. Is this capability
   essential now, useful later, or expendable?" Explain any indirect integrity
   or security consequence separately. Continue independent read-only work
   while awaiting an answer; do not treat silence as agreement to reduce scope.
   A low-value feature can still contain a high-severity defect.

4. **Validate the claim with proportionate evidence.** Inspect the actual
   failure artifact, revision, environment, and relevant contract. Use recon
   to bound the affected path and debug-mantra to test the load-bearing claim.
   Classify the observation: product defect, test defect, environment failure,
   obsolete expectation, or unresolved. Inspect existing evidence before
   rerunning expensive work. Run mutation-heavy probes in the isolation required
   by the repository. A passing retry does not establish a harmless flake;
   failure to reproduce is uncertainty, not disproof. Trace enough to support
   the proposed disposition and name what remains unverified.

5. **Challenge necessity and choose the smallest sound response.** Assess the
   capability and its implementation separately. For a test or guard, identify
   the behavior it protects, the credible regression that makes it fail, and
   whether another verified check covers the same inputs and failure boundary.
   Similar names or shared entry points do not prove duplicate coverage. For
   other machinery, name its active consumers and what changes if it is absent.
   Compare repair, simplification, deferral, and retirement against the actual
   requirement. Check recovery and rollback where consequences warrant it.
   Slow, complex, old, or historically green is not by itself a removal reason.
   Required safety and recovery properties survive simplification; removal of
   a redundant implementation requires evidence that those properties remain.

6. **Rate, record, and resume.** Select a disposition below and explain why the
   evidence supports it. Use existing PRS ratings and preserve operator choices.
   Record deferred valid work durably, then resume the original task wherever
   its acceptance requirements permit. If the task is still blocked, name the
   exact remaining dependency or decision. Never report the original task as
   complete merely because its blocker received an issue.

## Dispositions

| Disposition | Required basis and next action |
|---|---|
| Contain now | Credible ongoing harm; preserve sanitized evidence, take authorized containment, and route repair. |
| Fix now | Necessary capability, correctness property, or required gate blocks the goal; route to the existing repair workflow. |
| Simplify | Preserve the needed behavior with less machinery; verify the retained contract through existing checks or appropriate manual evidence. |
| Defer | Evidence supports bounded, low residual risk; no required acceptance condition is silently waived. Record an issue and revisit trigger. |
| Propose retirement | Obsolete requirement or demonstrated redundancy; present the affected users/contracts, surviving protection, rollback, and authorization needed. |
| Unresolved | Evidence or product intent is insufficient. Name one discriminating observation or one exact operator question. Do not translate uncertainty into low risk. |
| Dismiss the claim | Direct evidence disproves the alleged problem or dependency. Explain what was disproved; retain any separately valid defect. |

## Sibling recommendations

Recommend a sibling only when observed evidence supports its scope:

- **[ci-debug](../../2-daily/ci-debug/SKILL.md):** a validated CI failure needs
  repair now. Pass the failure artifact, affected revision, known consequences,
  and sanity-check disposition to its existing diagnosis/repair ladder. Resume
  an already-authorized CI repair without asking again; do not restart diagnosis
  or reassess the same blocker on unchanged evidence.
- **[ci-optimize](../../4-occasional/ci-optimize/SKILL.md):** measured pipeline
  cost, repeated orchestration failures, or test-selection problems warrant a
  broader CI architecture review. State the evidence and scope before recommending
  it; one red check alone does not justify a pipeline audit. Reuse an existing
  review, and run a new one only within the operator's requested/authorized scope.
- **[whack-a-mole](../../3-weekly/whack-a-mole/SKILL.md):** distinct incidents,
  reopens, or repeated fixes suggest a recurring defect class. Pass the concrete
  incidents, suspected shared mechanism, and any existing umbrella. It verifies
  the cluster and root cause under its own rules; repetition does not establish
  a shared cause or automatically make the work top priority.
- **[radar](../../3-weekly/radar/SKILL.md):** evidence suggests repair churn spans
  multiple areas, repeatedly displaces planned delivery, or warrants a broader
  review of development health and roadmap alignment. Pass the relevant window,
  affected work, and existing reports. One red check alone is insufficient.
- **[unstuck](../unstuck/SKILL.md):** when an in-flight session is stalled, trapped in
  passive waiting, or debating prerequisites rather than changing goal state.
  Pass the concrete blocker assessment to unfreeze execution and advance the milestone.

Recommend by default, stating the evidence and decision the sibling would inform.
Run a sibling when the operator requests it or existing authorization clearly
covers that investigation; preserve its separate publication/approval rules.
Sanity-check's low-risk issue-filing authority does not authorize a whack-a-mole
umbrella or radar report publication. If both fit, reuse a current radar report
as input to whack-a-mole; do not require a new radar run before cluster diagnosis.

These are handoffs, not recursive calls. Reuse a current sanity-check disposition
for the same scope and evidence; a sibling must not send it straight back for
another identical assessment. New contradictory evidence may reopen it. A
recommendation does not pause unrelated work or start a scheduled monitor.

## Stop investigation loops

**After two investigation attempts yield no new evidence, reassess before another
retry.** Count consecutive attempts; eliminating a plausible cause is new evidence. An attempt is a probe
or experiment, not a commentary update. Reassess sooner when cost or scope expands
materially beyond the original blocker. This is a review trigger, not a timeout
that permits ignoring a necessary defect.

State what the next experiment could distinguish and how either result would
change the disposition. Continue when that experiment is justified by the
consequence; otherwise defer genuinely low-risk work or surface the exact
missing evidence/decision. Do not cycle through skills, add instrumentation, or
raise retry caps merely to remain active. Fresh evidence can reopen a decision;
the same failed hypothesis cannot.

## Deferred work and PRS

Check for an existing issue before creating another. Record the observed defect
separately from the machinery proposed for removal. Include the affected
revision/environment, evidence, user consequence, confidence and unknowns,
reason for deferral, residual risk or mitigation, and a concrete revisit trigger
(for example, before enabling the affected feature). Use the target repository's
required issue, document, and ledger writers; do not install PRS to score work.

Use `rated priority/severity/appeal/effort`, four integers from 1–100:

- **Severity:** consequence and reach, including credibly supported potential
  harm and recovery difficulty. Keep serious corruption or exposure serious
  even when the feature is unpopular or incidents are rare.
- **Priority:** urgency, blocked work, recurrence, and the operator's scheduling
  intent. Explain an operator decision to defer despite high severity; do not lower the
  severity to rationalize it.
- **Appeal:** 50 unless an explicit operator preference supplies or supports
  another value; preserve prior explicit choices.
- **Effort:** cheapness/ease of delivery; higher means easier, not more work.
  Label uncertain estimates and retain evidence-supported existing values.

Follow the current `start-task` rating policy for recurrence and provenance.
Preserve operator `ovr` and existing rating rationale; use the supported writer
and read back the saved result. Never alter the sum formula or invent an
urgency multiplier. A rank is scheduling information, not permission to ignore
immediate harm. Without GitHub access, preserve an issue-ready Markdown draft
and report it as **not filed**. Keep credentials and sensitive incident details
out of public issues; use the project's approved private reporting route.
Upon selecting a `Defer` disposition, do not drift into ad-hoc polish: re-anchor immediately to the active task's acceptance criteria or today's prioritized queue via [`start-task`](../start-task/SKILL.md) or [`workhorse`](../../2-daily/workhorse/SKILL.md).

## Report

Lead with the disposition and its consequence for the original goal. Keep the
receipt short; link existing evidence instead of duplicating an investigation:

```text
SANITY-CHECK: <disposition>
Goal and claimed blocker: <one sentence>
Evidence and consequence: <what is observed; who/data affected; uncertainty>
Necessity: <requirement and why this mechanism is or is not needed>
PRS: <P/S/A/E and brief rationale, or existing rating reference>
Decision: <action taken or concrete proposal; residual risk>
Next: <original task's next step, or exact dependency/decision>
Deferred issue / revisit trigger: <URL and condition, or not applicable>
```

Use only the fields that matter. The output must make it clear whether the
problem is real, whether it blocks this goal, and what happens next.
