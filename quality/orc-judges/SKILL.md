---
name: orc-judges
description: Design, build, attach, verify, and report banded ORC quality assessments using built-in judges, custom judge behavior trees, or score-only decision models such as Jev. Use whenever an ORC workflow needs quality monitoring, judge feedback, rubric calibration, node or specialist performance reports, or assessment of a whole tree or selected group of executions.
---

# Judge ORC work from its evidence

A judge assesses actual work against a described rubric. It can itself be an
ordinary behavior tree: gather evidence, delegate specialist checks, reconcile
findings, choose a band, and persist an assessment. Start with the consuming
project's instructions, ORC principles, actual dependency revision and public APIs.

## Choose the assessment scope and evidence

Record what is being judged before selecting a model:

- **Execution:** one actual node instance, including its item/attempt identity.
- **Subbehavior:** a completed specialist and its relevant delegated work.
- **Tree:** the root goal, delivered artifact and relevant execution family.
- **Group:** an explicitly selected immutable set, with inclusion policy and IDs.

Individual executions and the assembled result answer different questions. Ten
good child scores do not establish that the final report meets the user's goal.
Give a parent or group assessment its own rubric and evidence. Read
[evidence and runtime](references/evidence-and-runtime.md) before attachment or
event subscription, and [reporting](references/reporting.md) before aggregation.

Resolve recorded inputs, outputs, instructions, source contents and actual tool
effects for the assessed instance. Current blackboard values can belong to later
work. A producer's claim of success is something to evaluate; it is not a tool
receipt. Missing evidence differs from observed absence of the required effect.

## Design a described band contract

Separate the criterion, reviewer stance, band descriptions, evidence and verdict.
Use one dimension per rubric unless the requested outcome is deliberately holistic.
Describe observable differences at every band and explain consequential failures.
Every band must stand on its own. Adjectives such as "poor" and "excellent" alone
do not tell a model which result belongs where.

The model selects a finite band. Code validates that selection and computes
`(level - minimum) / (maximum - minimum)`; five bands map to
`0.0, 0.25, 0.5, 0.75, 1.0`. An invalid or absent band is a failed assessment,
not a legitimate lowest grade. Verify nonempty descriptions yourself: the
inspected native scale constructor does not reject blank descriptions.

For feedback judges, require concise evidence and useful improvement guidance.
Requesting evidence before the grade is an observable output convention, not a
guarantee of internal reasoning or correct judgments. Read
[rubrics and calibration](references/rubrics-and-calibration.md) for boundaries,
reference labels, bias probes and measured acceptance.

## Choose the judging mechanism

| Need | Mechanism |
| --- | --- |
| Source support, compliance, reasoning or coverage feedback | Built-in judge, after checking its exact criterion and evidence contract |
| Domain effects, multiple evidence steps or reusable specialists | Custom judge BT with described typed blackboard |
| Scores for monitoring without prose | Native decision-model code capability or delegated wrapper |
| Immediate permission to continue or repair | Inline checker/decision in the active tree |
| Reports after completion | Background assessment with durable identity and lifecycle |

An asynchronous judge observes completed work; it does not retroactively change
what the workflow delivered. Use an inline checker when quality determines whether
the next tool or publication action may proceed. Route semantic work through
models; code validates identities, schemas, permissions, arithmetic and effects.
Do not detect meaning using regex, word lists or canned answer templates.

## Compose the judge as a real BT

When inline rejection drives revision, pass the [correction packet](../orc-compose-specialists/references/authored-controller.md#carry-substantive-correction-to-the-owner) to the artifact owner and assess its replacement; recording a failed grade alone does not correct what is delivered.

1. Define an immutable typed evidence packet, a versioned rubric, and a typed
   verdict. Describe every blackboard key, including parent/delegate input keys
   and intermediate audit/result maps, rather than relying on generated type
   summaries. Avoid `:any`. Resolve references before judging their content.
2. Build the smallest adequate assessment: direct banded judge; evidence audit
   followed by grading; delegated specialist; or independent parallel checks
   followed by reconciliation. Read [composition](references/compose-judges.md).
3. Use ordinary `llm` nodes for ordinary structured provider reasoning so native
   model configuration, usage and execution evidence remain visible. Use `code`
   for an unsupported native primitive such as Score or an adapter that actually needs it; registered boolean/Choice providers use finite nodes. Wrapping
   an ordinary chat call in code bypasses native LLM accounting. Give each LLM
   leaf a leading, node-scoped rationale write before its result,
   following the consuming ORC principles. Keep the rationale brief and evidence
   based; it is public assessment explanation, not private chain-of-thought proof.
   Assign an appropriate model to each model node. Keep configuration adjustable
   and send only supported parameters; temperature is not universally supported.
   Use [orc-model-sio](../orc-model-sio/SKILL.md) for real request construction.
4. Validate verdict structure, evidence readiness and feedback requirements.
   Preserve semantic uncertainty, missing evidence, transport failure and malformed
   output separately. Bound evidence retrieval and follow-up checks.
5. Persist the assessment through Grain commands, then verify tenant-scoped events
   and projected readback. Attach or schedule it through an explicitly supported
   route; do not invent a native API to hide a library limitation.

Use [orc-compose-specialists](../orc-compose-specialists/SKILL.md) for reusable
delegates, [orc-tools](../orc-tools/SKILL.md) for evidence tools and recursive
actions, and [orc-blackboard-contracts](../orc-blackboard-contracts/SKILL.md) for
read/write seams and independent parallel output ownership.

### Decision-model option

Jev uses typed native questions, not a normal chat/SIO protocol. A described Score
rubric returns a distribution over ordered levels and their expected position.
Choose the highest-probability band for the main grade. Keep the native weighted
score and complete distribution separately; rounding the expectation is not band
selection. Exact ties remain ambiguous, and confidence is not measured accuracy.
Do not invent feedback for a model that produces none.

Read [score-only decisions](references/decision-judges.md) and
[orc-decision-models](../orc-decision-models/SKILL.md). Score-only assessments can
support monitoring and manual prioritization. Feedback-dependent improvement
consumers require actual feedback and must reject or exclude score-only inputs.

## Before feeding assessments into optimization

Read [GEPA readiness](references/gepa-readiness.md) when judgments will train or
select instructions. Verify exact example/artifact attribution, stable grading
goals, genuine feedback and evaluator-failure handling through the consuming
optimizer path. Working background judges do not prove the direct GEPA metric
path is ready. Preserve untouched final evaluation cases outside optimization.

## Verify runtime support before promising it

At merged ORC `250de6e6de2ad95647ef6da4c69220c2bd631279`, source review establishes that explicit attachments run without Living Description and may target any existing sheet node, including composites, delegates and root. The flag gates only default researcher judges; an explicit empty attachment suppresses defaults. Assessment identity now includes subject completion ID, judge name and judge revision, with durable requested and scored/failed/ungradable outcomes. Attached assessment execution still launches process-local futures: durable pending visibility does not establish automatic restart execution, bounded capacity or body joining. Managed GEPA recovery is a separate path; see [GEPA readiness](references/gepa-readiness.md). These are source-backed corrections, not a new runtime proof.

Preserve the following findings at their historical pin; do not apply the repaired attachment, enablement and assessment-identity restrictions to the merged path.
At ORC main `490816267b76b0428c53437052980a25f5905209`:

- Native attachments admit leaves and researchers; composites and delegates are
  rejected. Arbitrary assessment scopes require explicit application composition
  or an engine change.
- The native completion handler is gated by the ontology Living Description flag,
  even for explicit attachments. Do not enable learning silently for monitoring.
- Launching futures is asynchronous execution, not a durable capacity queue.
  Pending-job admission, bounded workers and restart recovery need separate proof.
- Multiple executions of one node in one tick can share native score identity.
  A repeated-item proof produced three judge invocations but one stored score.
- Custom judges receive resolved host inputs/outputs, but their `host-trace` is a
  minimal node-ID summary. Preserve richer evidence in an explicit typed packet.

Read [source status](references/source-status.md) for reproduced gaps and intended
contracts. Recheck the consuming revision before adopting a workaround. Keep
application-owned assessment orchestration distinguishable from native support.

## Prove useful and observable judgments

Run deterministic public-interface tests for all bands, invalid output, missing
evidence, score-only feedback policy, duplicates, retries and scope isolation.
Then run real ticks and model calls using actual sources and tool receipts. Capture
the complete credential-free provider request and response, including SIO output
schema or native decision questions. Verify descriptions and source contents that
actually reached the model; traces alone do not prove the provider payload.

Count physical provider attempts across nested steps and retries. A client timeout
or ORC cancellation does not prove worker bodies stopped. Drain owned workers
before closing the store; preserve unfinished work and lifecycle findings.
Use [orc-runtime-bootstrap](../orc-runtime-bootstrap/SKILL.md) and
[orc-observe-debug](../orc-observe-debug/SKILL.md).

Report eligible and selected work, scored/pending/failed/ungradable counts, sampling,
band distributions, rubric/model versions and aggregate weights. Rebuild reports
from durable events after restart. Use [orc-grain-application](../orc-grain-application/SKILL.md)
for application commands, processors, read models and queries.

Finish with the scope, rubric, tree structure, actual evidence, runtime support,
executed proof, remaining failures and monitoring coverage. Synthetic judges
establish mechanics. Handcrafted construction expectations are not human gold;
successful model calls alone do not establish reliable grading.

## Current decisions and tools

At ORC `1851212396cced2fc4533fda30b824bd4b691390`, use [decision models](../orc-decision-models/SKILL.md) for one-answer boolean/Choice nodes and registered native providers, and [tools](../orc-tools/SKILL.md) for authored tool leaves and enforced code/tool/researcher contracts. Delegate context, family budgets/usage and execution leases are integrated. Native Score still needs a custom client; these updates do not repair judge jobs, attachment, evidence scopes or score identity. Contracts do not replace authorized domain commands or callee idempotency.

## Judging adaptive and reused behaviors

For recursive generated work use [orc-repl-researcher](../orc-repl-researcher/SKILL.md). Resolve the actual producer inputs, source, output and execution instance before interpreting a grade; the prime may have seen previews while a child saw full values. For feedback entering future descriptions use [researcher pattern reuse](../orc-researcher-pattern-reuse/SKILL.md). Preserve attribution and the full evidence→description→index→next request→behavior→quality chain. A score-only monitor, empty evaluator context or description version increment does not prove useful feedback-driven learning.
