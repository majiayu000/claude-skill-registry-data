---
name: cx-qa-appeal-process
description: Use to design or audit a QA dispute and appeal workflow with timeboxes, adjudication standards, and second-level consistency so appeals improve trust instead of rewriting scores without rules. Trigger for "QA appeal process", "agents disputing scores", "who adjudicates QA disputes", "overturn rate too high", second-level review standards, or calibration erosion from ad-hoc score changes.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# QA appeal process

Agents will disagree with scores. Without a defined process, disputes become informal
lobbying — team leads rewrite numbers, calibration erodes, and the agents who complain
loudest win rather than the agents who were right.

**An appeal process that lacks adjudication standards is a second scoring system with
weaker rules than the first.**

## Diagnose a broken process

| Symptom | Underlying fault |
| --- | --- |
| Overturn rate varies wildly by team lead | No adjudication standard |
| Agents win appeals on likability | Outcome linked to escalation skill, not evidence |
| Second reviewer always sides with agent | Reviewer is not independent |
| Disputes take weeks | No timeboxes; scores used while open |
| Calibration perfect; dispute rate high | Criteria fine in lab, ambiguous in production |
| Winning appeal does not update grader feedback | No loop back to QA |

## Step 1: Separate contest types

Route differently:

| Type | Question | Adjudicator |
| --- | --- | --- |
| **Factual error** | Wrong conversation, wrong agent, transcript incomplete | QA ops — fast track |
| **Criterion misapplication** | Evidence does not support verdict on a defined rule | QA lead or calibrated panel |
| **Criterion dispute** | Agent argues the rule itself is wrong | Not an appeal — rubric feedback channel |
| **Procedural** | Evaluation broke process (no evidence, bias, timing) | QA programme owner |

**Criterion dispute** is not overturnable through appeal — it goes to rubric review.
Allowing agents to "win" on undefined standards trains everyone that rules are
negotiable per conversation.

## Step 2: Define eligibility and limits

Publish clearly:

- **Window** — e.g. 5 business days from evaluation published to agent.
- **Scope** — which verdicts appealable (scored criteria yes; auto-fail yes with
  expedited track for hard fails).
- **Frequency cap** — e.g. 3 appeals per agent per quarter without pre-approval —
  prevents infinite resubmission.
- **Grounds required** — agent must cite criterion id and evidence, not "unfair".

Reject appeals that are **new arguments not visible in the conversation record** —
coaching belongs in 1:1, not retroactive score manufacture.

## Step 3: Timeboxes

| Stage | Target | Max |
| --- | --- | --- |
| Agent submits | — | Within eligibility window |
| Acknowledge | 1 business day | 2 |
| First-level adjudication | 3 business days | 5 |
| Second-level (if escalated) | 5 business days | 10 |
| Total | — | 15 business days hard stop |

During open appeal:

- **Score stands for reporting** unless policy explicitly freezes gating decisions.
- **Do not coach from the contested evaluation** — both parties anchor on it.
- **Auto-fail hard tier** — parallel compliance track continues; appeal does not pause
  regulatory clock without compliance sign-off.

Missed SLA escalates to QA programme owner automatically.

## Step 4: Who adjudicates

**First level:** senior QA analyst or calibrated lead grader — not the original grader,
not the agent's team lead.

**Second level:** panel of 2 — QA programme owner + independent ops/compliance rep.
Never the agent's direct manager alone.

Independence rules:

- Adjudicator did not score the original evaluation.
- Adjudicator has no performance management stake in the agent this quarter.
- Adjudicator uses **published criterion text pinned to evaluation version**, not
  memory.

For auto-fail hard tier: compliance must concur on any overturn.

## Step 5: Adjudication standards

Decision options (constrained):

1. **Uphold** — original verdict stands; brief evidence note.
2. **Overturn** — verdict changes; must cite criterion clause and transcript evidence.
3. **Partial overturn** — only where scorecard supports partial credit per criterion.
4. **Remand** — send back to original grader only for missing evidence capture, not
   re-negotiation.

**Burden of proof:** on appeal, agent must show the original verdict was wrong against
the written rule — not that a kinder interpretation exists.

Document **precedent-sensitive** criteria: if overturn sets new interpretation, flag
for rubric clarification — one-off overturns without rubric update recreate
ambiguity.

## Step 6: Second-level consistency

Track:

- **Overturn rate at L1 vs L2** — large gap means L1 is inconsistent or L2 is soft.
- **Overturn direction** — always toward pass suggests systematic leniency at appeal.
- **Inter-adjudicator agreement** on sample of appeals — same standard as calibration.
- **Criterion-level overturn rate** — high rate = under-specified criterion, regardless
  of who wins.

Monthly review: top 5 overturned criteria → rubric or training fix, not more appeals.

## Step 7: Close the loop

On every overturn:

- **Update evaluation record** with appeal id, adjudicator, reason code.
- **Notify original grader** — learning, not punishment, unless pattern of error.
- **Feed calibration** — anonymised appeal cases into gold set refresh if they
  expose genuine ambiguity.
- **Agent communication** — outcome with criterion citation; not "we changed it".

On uphold: agent receives reason; repeated frivolous appeals trigger manager
conversation, not score change.

## Step 8: Metrics that do not lie

| Metric | Use | Misuse |
| --- | --- | --- |
| Dispute rate | Criterion/spec health | Agent "troublemaker" ranking |
| Overturn rate (contested only) | Adjudication consistency | Overall QA quality |
| Time to resolve | Process health | — |
| Criterion overturn share | Rubric rewrite priority | — |
| Repeat dispute same criterion | Agent confusion or bad rule | — |

**Never rank agents by appeal count.** Dispute rate rises when criteria are ambiguous
— often the best agents notice first.

## Present results to the user

1. **Process diagnosis** — which failure modes apply, with overturn/dispute stats if
   available.
2. **Contest taxonomy and routing** — types, adjudicators, fast tracks.
3. **Eligibility and timebox table** — windows, SLAs, freeze rules during appeal.
4. **Adjudication standard** — decision options, burden of proof, independence rules.
5. **Second-level consistency plan** — metrics, monthly review, rubric feedback loop.
6. **Closure workflow** — record updates, grader notification, gold set feed.
7. **Reporting spec** — metrics to publish and explicit misuses to avoid.
