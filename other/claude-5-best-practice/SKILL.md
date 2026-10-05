---
name: claude-5-best-practice
description: Route Claude 5 tiers (Haiku/Sonnet 5/Opus 5/Fable 5), effort, and subagents for cost-effective accepted results, and handle Claude 5 prompting, long-running execution, API behavior, refusals, and fallback.
---

# Claude 5 Best Practices

Use this skill as a routing and runtime overlay for the Claude 5 generation. Safety,
permissions, repository instructions, and explicit user constraints remain
authoritative.

Default objective: satisfy the acceptance contract, then minimize accepted-result
cost. Lower latency, higher quality beyond the contract, or mandatory topology is a
different objective; pursue it at higher cost only when the user explicitly chooses
that tradeoff.

## Product snapshot

As checked on 2026-07-26:

| | Claude Fable 5 | Claude Opus 5 | Claude Sonnet 5 | Claude Haiku 4.5 |
| --- | --- | --- | --- | --- |
| API ID | `claude-fable-5` | `claude-opus-5` | `claude-sonnet-5` | `claude-haiku-4-5` |
| Price /MTok | $10 in, $50 out | $5 in, $25 out | $3 in, $15 out (intro $2/$10 to 2026-08-31) | $1 in, $5 out |
| Context / max output | 1M / 128k | 1M / 128k | 1M / 128k | 200k / 64k |
| Adaptive thinking | Always on | On by default | Yes | No |
| Effort levels | `low`–`max`, default `high` | `low`–`max`, default `high` | `low`–`max`, default `high` | Not supported |
| Zero data retention | Not available; 30-day retention required | Available | Available | Available |
| Priority Tier | Not supported | Supported | Supported | Supported |

Claude Opus 5 launched 2026-07-24 at half Fable 5's price with the same context and
output limits, and it is the documented starting point for complex agentic coding and
enterprise work. Fable 5 remains the most capable widely released model. These facts
are volatile. Read `references/evidence-notes.md` before quoting them as current.

## Terms

- `acceptance contract`: observable acceptance criteria, required safety and
  verification, and approval boundaries.
- `tier`: a vendor-defined capability class: Haiku, Sonnet, Opus, or Fable.
- `effort`: reasoning and checking depth within one tier.
- `lane`: one `tier + effort` single-agent configuration.
- `orchestration`: the single-agent or lead/workers/verifier topology.
- `route`: lead lane, worker lanes, orchestration, and verification plan together.
- `accepted-result cost`: total spend required to pass the contract, measured in the
  surface's primary accounting unit: API dollars or subscription credits, never both.
- `non-inferior`: acceptance performance within a predeclared tolerance on
  representative work; it does not mean identical output on every run.
- `surface`: the active product/client, account entitlements, model controls, worker
  overrides, permissions, and accounting system.

Track tokens, latency, calls, and human correction as separate diagnostics or
guardrails. If the surface exposes no comparable spend signal, describe relative
resource intensity instead of claiming an exact cheapest route.

## Interpret explicit delegation requests

A request to “use subagents/workers with proper models to save cost” authorizes
delegation and worker-lane selection within scope; it does not mandate fan-out, lower
the acceptance contract, choose a premium lead, or waive the premium gate. Treat the
cost purpose as conditional: compare the three routes below and delegate only when the
routed route is expected to be the cheapest accepted route.

If the user requires subagents as a topology independent of cost, follow that topology
only when it preserves the acceptance contract. “Use subagents regardless of cost” is
already an explicit higher-cost objective. If the user instead requires subagents “to
save cost” but routing evidence predicts higher cost, pause and ask whether topology or
cost governs. If mandatory topology cannot preserve the acceptance contract, pause and
ask the user to relax either topology or the contract; never weaken or silently replace
one requirement.

Pin and verify each worker's effective model and effort where supported. If overrides
are unavailable, inherited, ignored, or unverified, do not dispatch workers for cost
savings and do not claim worker-tier savings. Prefer the qualified single-agent lane
or a handoff. A separately confirmed mandatory topology may still use such workers,
but it is not a cost-saving route. Before dispatch, state the topology, worker lanes,
cost rationale, and uncertainty compactly. After completion, report verification,
observable effective lanes, retries/rescues, and the spend signal; without comparable
spend data, report only relative resource intensity.

## Cost-aware routing procedure

Follow this order. Later sections explain vendor-specific mappings but do not override
the procedure.

1. **Fix the contract and objective.** Define the required deliverable, checks,
   semantic review, safety constraints, and approvals. Record any explicit user choice
   to trade higher cost for latency, quality beyond the contract, or mandatory
   topology.
2. **Inspect the surface.** Identify the active model, available tiers and effort
   values, lead-switch or new-task handoff mechanism, worker-model overrides and
   inheritance, orchestration limits, permissions, and accounting unit. If a
   capability is unavailable or unverified, do not promise savings from it.
3. **Choose direct-lane candidates.** Judge ambiguity, coupling, state depth, semantic
   risk, objective checkability, and expected rework. For recurring work, reuse
   validated evidence. Without a baseline, include both the cheapest plausible lane
   and a stronger reasonable baseline; do not treat the premium tier as ground truth.
   Label one-off task-shape judgments as heuristics.
4. **Prefer effort escalation within Opus 5 over tier escalation to Fable 5.** Fable 5
   costs twice as much per token, so an Opus 5 run at `xhigh` or `max` can spend
   roughly twice the tokens of a Fable 5 run at `high` before it costs more. Exhaust
   the effort ladder on Opus 5 before treating Fable 5 as the answer to a quality gap,
   unless the failure is a task-shape mismatch that more effort does not address.
5. **Apply the premium gate.** When the active lead is Fable 5, pause before the first
   task-execution tool call, state-changing write, or substantive multi-step analysis
   and wait for confirmation only when a cheaper lane is likely non-inferior, an
   actionable switch or complete new-task handoff exists, and expected remaining
   savings exceed duplicated prompt, context, restart, and handoff cost. Since Opus 5
   ships near-Fable capability at half the price, treat “a cheaper lane is likely
   non-inferior” as presumptively satisfied for coding, review, research, and
   knowledge work; the burden is on task-specific evidence that Fable 5 is needed.
   Recommend one lane, one task-specific reason, and the supported switch or compact
   handoff. Do not continue while waiting. If the user chooses Fable 5, continue
   without repeating the gate. If any condition fails, continue and give at most one
   future-task reminder.
6. **Compare three routes before delegating for cost.** Prospectively assess the
   current single-agent route, the cheapest likely non-inferior single-agent lane, and
   an appropriate lead with routed workers. Use local history or task-shape evidence;
   do not execute all three merely to route a one-off task. Use the routed design for
   cost when—and only when—it is expected to be the cheapest accepted route and the
   work has independent scopes, compact handoffs, controlled write ownership, and
   affordable verification. Never manufacture workers to justify a premium lead.
7. **Bound the chosen route.** Pin every worker model and effort when supported;
   otherwise do not claim tier-routing savings. Give each worker a goal, owned scope,
   distilled inputs, output contract, verification including residual semantic review,
   and a stop condition. Cap fan-out, depth, attempts, retries, and returned context.
   Higher-cost parallelism requires the explicit higher-cost objective from step 1.
8. **Diagnose before escalating.** Repair missing or conflicting context first. Retry
   the same lane for a transient tool failure. Raise effort one level for insufficient
   checking on a clear task. Raise tier for a reasoning, ambiguity, or state-tracking
   mismatch that effort does not fix. Lower effort for overexploration and lower tier
   for repetitive objective volume. Keep one agent for sequential or shared-state work.
   Change only one of tier, effort, prompt/context, tools, or orchestration at a time;
   escalate only the failing workstream and route back down after the hard decision is
   settled.
9. **Verify and update policy.** Verify against the unchanged contract and account for
   every lead, worker, verifier, retry, and rescue without double counting. A one-off
   heuristic may be used for low-risk, strongly verified work, but it does not become a
   default route. Standardize a cheaper route only after paired representative runs
   meet a predeclared non-inferiority and adoption rule.

Minimal read-only inspection needed to evaluate the premium gate is allowed before the
pause; task execution is not. For a new-task handoff, include the outcome, constraints,
acceptance criteria, and necessary paths or evidence so the user does not have to
reconstruct the task.

## Claude tier and effort mapping

| Tier | Good starting work | Escalation rule / next action | Avoid |
| --- | --- | --- | --- |
| Haiku 4.5 | Strict-schema extraction, classification, formatting, and isolated mechanical work with objective checks | Move to Sonnet 5 for sustained state, multi-step tools, ambiguity, or judgment | Compensating for a tier mismatch with more prompting |
| Sonnet 5 | Repository exploration, bounded implementation, routine debugging, tests, verification workers, and supporting workstreams | Raise effort first; move to Opus 5 for difficult bounded reasoning, semantic risk, or expensive rework | Treating it as a universal replacement for difficult coding work |
| Opus 5 | Default lead for complex multi-file coding, difficult debugging, high-recall review, research synthesis, and long-horizon agentic work | Exhaust `xhigh` and `max` here before considering Fable 5 | Using it for simple volume work, or skipping past it straight to Fable 5 |
| Fable 5 | The residual hardest cases: sustained global judgment and arbitration where measured evidence shows Opus 5 at `max` still falls short | Repair context or raise effort only after a concrete contract failure | Using prestige, file count, or elapsed time as justification; using it when the workload needs zero data retention or Priority Tier, which Fable 5 does not offer |

Effort settings (Fable 5, Opus 5, and Sonnet 5 share the same ladder, default `high`):

- `low`: bounded work where cost and speed dominate; a reasonable default for
  mechanical subagents.
- `medium`: interactive exploration or a balanced pass.
- `high`: default, and the normal starting point for serious work without a
  calibrated route.
- `xhigh`: long-horizon agentic and coding work; the first thing to try when a run
  under-checks on a clear task.
- `max`: highest supported setting; reserve it for a demonstrated quality gap, and
  prefer it on Opus 5 over a tier move to Fable 5.

Model-specific notes: on Opus 5, effort controls thinking volume rather than visible
response length, so prompt for brevity instead of lowering effort to shorten output,
and do not carry effort settings over from Opus 4.8 without a fresh sweep. On Fable 5,
lower effort levels still often exceed `xhigh` on prior-generation models. At `xhigh`
or `max` on either model, set a large `max_tokens` — 64k is a reasonable starting
point — because it caps thinking plus response together.

Reduce effort when successful runs explore unused alternatives or produce unactionable
detail. Increase it only after ruling out prompt, context, tool, and verification gaps.

## Delegation and verification

Cost-routing workers should normally use Haiku, Sonnet 5, or Opus 5 according to task
shape; at Opus 4.8-level pricing, Opus 5 is now an affordable implementer lane rather
than a reserved one. An independent verifier is different: if the acceptance contract
requires fresh-context review, its cost is part of every eligible route and its tier
follows residual semantic risk, even when that means Opus 5 or Fable 5.

Prefer one lead when work is sequential, shares mutable state, or would copy most of
the parent context. Concurrent writers need disjoint ownership; read-only workers may
share scope, and sequential handoffs may touch the same files with one writer at a
time. Read `references/prompt-patterns.md` for worker and verifier packets.

Deterministic gates reduce risk only for the properties they encode. They can justify
testing a cheaper worker but never replace semantic review for unencoded requirements.
For multi-phase projects where the lead should carry only judgment, the
field-validated lead-orchestrator loop (distill to contract files on disk → routed
implementers → independent semantic verifier → bounded fixer → lead gates and
commits) is documented in `references/prompt-patterns.md`, with the supporting run
and its adoption limits in `references/evidence-notes.md` (2026-07-25).

In one unversioned Claude Code observation, workers with no explicit model inherited
the premium lead and fork-style workers ignored overrides. In a later run (2026-07-25),
explicit overrides on 21 non-fork workers behaved as requested, though effective
models were pinned, not independently verified. Verify current inheritance and
override behavior before relying on it; avoid forks when cost behavior is uncertain.

## Prompting and migration

For substantial work, provide outcome, relevant evidence, hard constraints, approval
boundaries, acceptance criteria, verification, budget, and stop condition. Let the
model choose intermediate steps. Read `references/prompt-patterns.md` for compact
shapes.

When migrating older prompts, remove scaffolding that only compensated for weaker
models, but keep safety, data, budget, scope, style, and business constraints. Never ask
for hidden reasoning. Re-test prompt tokens, latency, accepted-result cost, timeouts,
streaming, and asynchronous UX.

Migrating from Opus 4.8 to Opus 5 has two behavioral breaks: requests with no
`thinking` field now run with adaptive thinking, so revisit `max_tokens`; and
`thinking: {"type": "disabled"}` is rejected with a 400 at `xhigh` or `max` effort.
Re-run an effort sweep rather than carrying 4.8 settings across.

## Claude 5 API behavior

- Adaptive thinking is on by default across Fable 5, Opus 5, and Sonnet 5; control
  depth with `effort`, not a manual thinking budget.
- Raw thinking is not returned. `thinking.display` is `summarized` or `omitted`;
  preserve returned thinking blocks unchanged in same-model multi-turn conversations.
- `max_tokens` covers thinking and response output. Give high-effort runs enough room.
- `effort` is a request-level setting that reshapes the prompt, so changing it
  mid-conversation invalidates prompt caching. Pick a level per workload and hold it.
- Task budgets cover a full agentic loop and are distinct from `max_tokens`. They are a
  Messages API beta and are not supported by Claude Code or Cowork in this snapshot.

Read `references/evidence-notes.md` before depending on beta headers or current surface
support. Read `references/api-runtime.md` before implementing task budgets, refusals,
or fallback.

## Long-running execution

- Use asynchronous workers, scheduled checks, or harness-native waiting; never use an
  unbounded sleep or polling loop inside a tool call.
- Keep the lead context to decisions, risks, current state, and compact evidence.
- Ground progress and completion claims in tool results from the current run.
- Preserve only durable decisions, constraints, corrections, confirmed approaches,
  and the next action across sessions; keep one compact state snapshot when needed.
- Pause for destructive or irreversible actions, external commitments, real scope
  changes, or information only the user can provide.
- Report outcome first, then the evidence that determines what to trust or do next.

Read `references/operations.md` for the complete scope, progress, state, and reporting
rules used by analysis-only and long-running work.

## Refusals and fallback

Both Fable 5 and Opus 5 run safety classifiers. Detect a refusal with HTTP 200 plus
`stop_reason: "refusal"`; treat any partial result as incomplete. Refusal categories in
`stop_details.category` are monitoring metadata, not a license to bypass safeguards.

Choose exactly one fallback mechanism per request path: server-side fallback where
supported, SDK middleware retry, or one manual retry on a different model. Do not
combine mechanisms or create a fallback loop. Before retrying side-effecting work,
confirm idempotency or that no action completed. Implementation details are in
`references/api-runtime.md`; provenance and confidence boundaries are in
`references/evidence-notes.md`. Reverify both before implementation.

## Reference map

- `references/prompt-patterns.md`: lead, worker, and verifier packets.
- `references/routing-and-evaluation.md`: cost accounting, one-off routing, and route
  adoption procedure.
- `references/api-runtime.md`: thinking, budgets, refusal fields, and fallback matrix.
- `references/operations.md`: scope control, long-running state, progress, and output.
- `references/evidence-notes.md`: dated product/API provenance and field observations.

Read only the reference needed for the current task.
