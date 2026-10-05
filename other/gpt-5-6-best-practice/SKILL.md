---
name: gpt-5-6-best-practice
description: Route GPT-5.6 tiers, reasoning effort, and subagents to minimize accepted-result cost subject to an explicit quality floor.
---

# GPT-5.6 Codex Efficiency

Use this skill as a GPT-5.6 routing, prompting, and evaluation overlay for Codex.
Safety, permissions, repository instructions, and explicit user constraints remain
authoritative.

Default objective: satisfy the acceptance contract, then minimize accepted-result
cost. Lower latency, higher quality beyond the contract, or mandatory topology is a
different objective; pursue it at higher cost only when the user explicitly chooses
that tradeoff.

## Product snapshot

As verified on 2026-07-10, Sol is the flagship tier, Terra the balanced tier, and Luna
the fastest, lowest-cost tier. The `gpt-5.6` alias resolves to Sol. Light in the app and
IDE maps to Low in the CLI; Extra High maps to `xhigh`. Max deepens one agent, while
Ultra is multi-agent orchestration rather than an API `reasoning.effort` value. Codex
cloud currently does not expose model selection. Availability, UI labels, credits,
defaults, and Fast-mode behavior are volatile; read `references/evidence-notes.md`
before quoting them as current.

## Terms

- `acceptance contract`: observable acceptance criteria, required safety and
  verification, and approval boundaries.
- `tier`: a vendor-defined capability class: Luna, Terra, or Sol.
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
guardrails. Cached-input and reasoning tokens are breakdowns of input and output, not
extra tokens to add again. If the surface exposes no comparable spend signal, describe
relative resource intensity instead of claiming an exact cheapest route.

## Interpret explicit delegation requests

A request to “use subagents/workers with proper models to save cost” authorizes
delegation and worker-lane selection within scope; it does not mandate fan-out, lower
the acceptance contract, choose a Sol lead, or waive the premium gate. Treat the cost
purpose as conditional: compare the three routes below and delegate only when the
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

Follow this order. Later sections explain GPT-specific mappings but do not override the
procedure.

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
4. **Apply the premium gate.** When the active lead is Sol, pause before the first
   task-execution tool call, state-changing write, or substantive multi-step analysis
   and wait for
   confirmation only when a cheaper lane is likely
   non-inferior, an actionable switch or complete new-task handoff exists, and expected
   remaining savings exceed duplicated prompt, context, restart, and handoff cost.
   Recommend one lane, one task-specific reason, and the supported switch or compact
   handoff. Do not continue while waiting. If the user chooses Sol, continue without
   repeating the gate. If any condition fails, continue and give at most one
   future-task reminder.
5. **Compare three routes before delegating for cost.** Prospectively assess the
   current single-agent route, the cheapest likely non-inferior single-agent lane, and
   an appropriate lead with routed workers. Use local history or task-shape evidence;
   do not execute all three merely to route a one-off task. Use the routed design for
   cost when—and only when—it is expected to be the cheapest accepted route and the
   work has independent scopes, compact handoffs,
   controlled write ownership, and affordable verification. Never manufacture workers
   to justify a Sol lead.
6. **Bound the chosen route.** Pin every worker model and effort when supported;
   otherwise do not claim tier-routing savings. Give each worker a goal, owned scope,
   distilled inputs, output contract, verification including residual semantic review,
   and a stop condition. Cap fan-out, depth, attempts, retries, and returned context.
   Higher-cost parallelism requires the explicit higher-cost objective from step 1.
7. **Diagnose before escalating.** Repair missing or conflicting context first. Retry
   the same lane for a transient tool failure. Raise effort one level for insufficient
   checking on a clear task. Raise tier for a
   reasoning, ambiguity, or state-tracking mismatch. Lower effort for overexploration
   and lower tier for repetitive objective volume. Keep one agent for sequential or
   shared-state work. Change only one of tier, effort, prompt/context, tools, or
   orchestration at a time; escalate only the failing workstream and route back down
   after the hard decision is settled.
8. **Verify and update policy.** Verify against the unchanged contract and account for
   every lead, worker, verifier, retry, and rescue without double counting. A one-off
   heuristic may be used for low-risk, strongly verified work, but it does not become a
   default route. Standardize a cheaper route only after paired representative runs
   meet a predeclared non-inferiority and adoption rule.

Minimal read-only inspection needed to evaluate the premium gate is allowed before the
pause; task execution is not. For a new-task handoff, include the outcome, constraints, acceptance criteria, and
necessary paths or evidence so the user does not have to reconstruct the task.

## GPT tier and effort mapping

| Tier | Good starting work | Escalation rule / next action | Avoid |
| --- | --- | --- | --- |
| Luna | Strict-schema extraction, classification, transformation, and mechanical work with objective checks | Move to Terra for sustained state, multi-step tools, ambiguity, or judgment | Raising effort to compensate for a tier mismatch |
| Terra | Repository exploration, bounded implementation, routine debugging, tests, and supporting workstreams | Move to Sol for difficult reasoning, semantic risk, architectural judgment, or expensive rework | Treating it as a universal replacement for difficult coding work |
| Sol | Ambiguous multi-file coding, architecture, difficult debugging, high-recall review, research synthesis, and high-value decisions | Repair context or raise effort only after a concrete contract failure | Using it for simple volume work |

Starting lanes:

- Luna Low: repeatable work with an objective schema and verifier.
- Luna Medium: the same work with limited reasoning or a short tool sequence.
- Terra Low or Medium: bounded engineering and everyday agent work.
- Sol Low or Medium: ambiguity, long verification chains, semantic risk, or expensive
  rescue if a weaker pass fails.
- High or `xhigh`: only after a measured gap shows that more checking or reasoning is
  needed on the chosen tier.
- Max: the hardest tightly coupled single-agent work after comparison with `xhigh`.
- Ultra: enter only through step 5. It is not a token-saving effort setting.

For difficult work, compare a stronger tier at Low or Medium with a smaller tier at
higher effort. A dated third-party suite found that Sol Low/Medium sometimes achieved
similar or higher aggregate scores with fewer reported output tokens than smaller
tiers at very high effort; it did not establish complete token efficiency or repository
cost. Read `references/evidence-notes.md` before using that observation.

## Codex worker routing

Local Codex clients support custom agents under `.codex/agents/` or
`~/.codex/agents/`. Pin `model`, `model_reasoning_effort`, and intended sandbox in the
agent file when a stable route matters. Effective permissions can still be constrained
by the parent or runtime; inspect them before dispatch.

A worker-tier cost claim requires dispatching a named custom agent whose file pins
`model` and `model_reasoning_effort`, or a runtime surface with equivalent verified
overrides. The custom agent's `name` is the dispatch identity; a profile merely existing
on disk does not bind a generic spawn. Prompt steering alone is not verified pinning.

Cost-routing workers normally use Luna or Terra. An independent verifier is different:
if the acceptance contract requires fresh-context review, its cost is part of every
eligible route and its tier follows residual semantic risk, even when that means Sol.

Concurrent writers need disjoint ownership; read-only workers may share scope, and
sequential handoffs may touch the same files with one writer at a time. Keep
`agents.max_depth = 1` unless recursive delegation is measured to help. Treat
`agents.max_threads` as a cap, not a target. Read `references/worker-profiles.md` for
copyable roles and `references/prompt-patterns.md` for worker and verifier packets.

## Prompt and migration guidance

State each instruction once. Provide outcome, relevant evidence, hard constraints,
approval boundaries, acceptance criteria, verification, budget, stop condition, and
output shape. Expose only relevant tools, trim stale context, and return distilled
evidence rather than raw logs. Read `references/prompt-patterns.md` for compact shapes.

When migrating older prompts, remove scaffolding that only compensated for weaker
models, but keep safety, data, budget, scope, style, and business constraints. Re-map
effort instead of carrying old defaults forward, then re-test tokens, latency,
accepted-result cost, and timeouts.

## Safeguards and latency

GPT-5.6 uses real-time cyber and biology safeguards. Legitimate dual-use work may pause
or be refused. Do not treat every pause as a stuck agent, retry adversarially, or hide
the failure; report it and follow the current surface's allowed recovery path.

Fast mode trades more credits for lower latency; it is not a token-saving feature.
Max spends more reasoning on one agent. Ultra adds orchestration. None is a default
cost-saving switch.

## Reference map

- `references/prompt-patterns.md`: lead, worker, and verifier packets.
- `references/worker-profiles.md`: copyable Luna, Terra, and Sol custom agents.
- `references/routing-and-evaluation.md`: cost accounting, one-off routing, and route
  adoption procedure.
- `references/evidence-notes.md`: dated product, benchmark, and surface provenance.

Read only the reference needed for the current task.
