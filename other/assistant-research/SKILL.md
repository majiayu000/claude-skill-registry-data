---
name: assistant-research
description: "Gathers and synthesizes source-backed information. Use for research, topic investigation, current evidence, or requests to compare options."
---

# Research

## Shared operating guidance

Load [the common outcome guidance and shared stagnation policy](references/operating-guidance.md).


Answer with source-backed evidence, conclusions, conflicts and gaps. Scale effort
to decision risk; stop searching when further work cannot materially help within budget.

## Ordinary source research

1. Establish the question, context, and decision criteria. Ask only about material
   information that cannot be discovered or safely inferred.
2. Prefer primary evidence, independent corroboration and warranted counterevidence.
   Comparisons and understanding ordinarily remain `source_research`.
3. Check source identity, freshness, applicability, and disagreement. Verify every
   URL presented or omit it; repository, authenticated, and offline evidence can
   use safe stable locators. Never expose secrets or private host references.
4. Place citations close to supported claims. Distinguish observation, source statements, inference,
   and unknowns. Assess each claim's evidence quality, directness, independence,
   and conflicts, not source counts; copies add no independent support. Report
   material conflicts and gaps; omit empty sections.

Apply [request alignment](references/operating-guidance.md#request-alignment) to
research answers: organize them around the requested outcomes, leading with the
requested conclusions or recommendations, one row or section per outcome unless
the user or target format requires another structure. Citations, evidence
quality, conflicts and gaps from step 4 stay attached to the answers they
qualify; broader context and labelled additional findings go in supporting
sections. For example, a comparison asking each option's benefit and cost plus a
recommendation gets a per-option benefit/cost/recommendation table, with
overhead analysis kept as an additional finding where it changes a
recommendation. Five-lens synthesis keeps its structure; this governs the human
presentation only.

Finance, legal, medical, safety-critical and other high-impact recommendations
need educational due diligence with risks/context limits. A stronger recommendation
needs verified decision-critical sources and explicit relevant user context;
otherwise state gaps and recommend investigation. High stakes alone require
neither five lenses nor serialization.

Use [research.md](research.md) for sources, [investigate.md](investigate.md) for
entities and [url-verify.md](url-verify.md) for uncertain URLs; for a substantial
report (a deliverable report, any five-lens run, or an explicit request for
checkable citations or fact-checking), also use
[source-provenance.md](source-provenance.md). Why/how/improvement
questions may yield candidate mechanisms; retain their support, counterevidence,
gaps, and validation method. Never claim proven causality or improvement without
executed validation.

## Five-lens research

Select `five_lens_briefing` for an explicit method request or when a
consequential contested decision actually needs independent perspectives,
contradiction mapping, synthesis, and peer critique. Explain why; comparison,
"deep understanding", breadth, or high stakes alone does not trigger it. Load
[five-lens-briefing.md](five-lens-briefing.md).

Freeze five sibling-blind assignments: practitioner, academic/technical expert,
skeptic, incentives analyst and historian/pattern matcher. Later waves remain
blind. Retain each lens's research, material follow-ups, evidence and gaps. The root alone maps contradictions and writes final synthesis after five usable returns; separate peer review
precedes presentation. Address revisions or downgrade unsupported claims.

Current Research v5 requires five distinct sibling-blind lens actors and a newly
created independent peer, disjoint from root and lenses. Bind retained native
creation, handoff/source identity and fresh context; Codex uses `fork_turns=none`.
Unavailable isolation leaves completion incomplete. Explicit user opt-out may
change the method to ordinary source research; sequential fallback cannot certify
an independent v5 run. Source research stays direct-capable.

## Consumer and compatibility boundaries

For structured consumers/persisted packets/audits/evals/handoffs, load
`contracts/index.yaml` and needed entry/method, phase, handoff/completion sets.
Invalid selectors load the full named contract. Preserve frozen packet digests,
accepted results/follow-ups, synthesis, peer-input preimages, revision closure,
high-stakes bindings and schemas.

Compatibility fixtures retain tier budgets/source-count rules and consumed
process evidence. Human answers may summarize findings, conflicts, peer critique,
conclusions and limits; ordinary claim assessment uses evidence quality.

Stop or qualify answers with inaccessible, stale, conflicting, or weak
evidence. Unverified URLs and unsupported causal claims cannot be finalized.

Preserve historical labels, evidence and the shared task guard; missing progress
is a gap. For persisted pre-v5 records, v2/v3 follow-ups or historical v4
fallback evidence, load [legacy-compatibility.md](legacy-compatibility.md).
