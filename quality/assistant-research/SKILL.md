---
name: assistant-research
description: "Gather and synthesize source-backed information. Use for explicit research, topic investigation, current evidence, or requests to compare options."
---

# Research

## Goal

Answer proportionally with source-weighted findings, verified URLs, explicit
conflicts, and honest evidence gaps.

## Success Criteria

- Research depth matches decision risk and available evidence.
- Findings cite supporting sources and calibrated confidence.
- Every URL presented is verified or omitted.
- Conflicts and gaps are reported, even when empty.
- Candidate mechanisms remain hypotheses until a validation method is executed.

## Constraints

- Ask only when scope changes source selection, jurisdiction/domain, depth, or
  decision criteria and cannot be inferred safely.
- HIGH requires 3+ independent agreeing sources plus primary/official evidence;
  one authoritative source is MEDIUM.
- Keep `source_research` direct-capable. For `five_lens_briefing`, use the
  declared five-lens Process handoffs and do not substitute a single-agent
  perspective scan for independent lens evidence.

## Progressive Contract Loading

Canonical tier files are `contracts/input.yaml`, `contracts/output.yaml`,
`contracts/phase-gates.yaml`, and `contracts/handoffs.yaml`.

Read `contracts/index.yaml` first and load only the active boundary:

- `entry` for question, tier, method, role/goal, purpose, known context, and
  resolved subagent policy/execution/fallback evidence;
- `current_phase` for SEARCH, SYNTHESIZE, or VERIFY;
- `source_research`, `five_lens`, or `investigate` only after method selection; and
- `selected_handoff` before every LensResearcher or ResearchPeerReviewer dispatch and return validation; and
- `completion` only for the artifact being returned.

Missing or invalid selectors fall back to the full named canonical contract. Do
not load every contract or research method at entry.

Migration note: assistant-research contracts are v3.0. Convert v2 follow-up
fields to typed `follow_ups`, retaining each material follow-up or one
`none_needed`. v3 requires five frozen, sibling-blind assignment packets,
root-only synthesis, distinct peer review, canonical packet/peer-input
preimages, tier resolution, and high-stakes bindings. Reject or re-run
incomplete v3 artifacts.

## Ownership

assistant-research owns source selection, synthesis, confidence, and URL
verification. Its specialist gates are authoritative.

For `five_lens_briefing`, the root Orchestrator freezes exactly five
assignment packets before dispatching one independent LensResearcher per named
lens. Orchestrator alone builds the contradiction map and initial synthesis
after validated returns. A distinct ResearchPeerReviewer then critiques that
synthesis. Sequential fallback is constrained to the documented admissible
bases and records reduced independence; it never claims delegated independence.
Resolve `subagent_policy_state` before dispatch: this skill instruction makes
five-lens delegation `delegation_triggered` without another permission prompt.
Only documented opt-out, real unavailability, or an exact policy block permits
`sequential_fallback`; `source_research` remains `not_required/not_applicable`.

## Method Selection

- **source_research** — factual lookup and comparison. Load `source_research`;
  choose tier by risk.
- **five_lens_briefing** — decision-grade work needing perspectives,
  contradictions, incentives, synthesis, and peer review. Load `five_lens`.
- **investigate** — deep entity/domain analysis with ethical boundaries. Load
  `investigate`.

Quick tier may use one strong primary source. Standard uses multiple sources.
Extensive/deep tiers expand perspectives and primary evidence only when the
decision warrants the cost.

Every finding needs confidence grounded in source quality and agreement. For
causal or improvement questions, return candidate mechanisms with evidence,
counterevidence, gaps, and a validation method—not proven-cause language.

## Output

Return status/confidence, concise answer, source-backed findings, candidate
mechanisms when applicable, verified sources, conflicts, gaps, and five-lens
artifacts only when that method ran.

For five_lens_briefing, include FIVE-LENS PROCESS EVIDENCE: tier resolution,
frozen packet-set ID/digest and retained canonical packet preimages,
pre-dispatch ordering, exact lens execution records,
assignment/packet-set bindings, return validation, peer assignment/identity or
fallback, execution modes, reduced-independence state, and the bounded search
resource budget. Bind final synthesis to the exact peer-reviewed input or a
complete revision closure. The root Orchestrator owns this lifecycle record.

## Stop Rules

- Ask every material, non-discoverable question when missing scope changes interpretation; group them by topic and keep them concise.
- Report a gap when sources are inaccessible, stale, conflicting, or too weak.
- Do not finalize with any unverified URL.
- Do not present candidate mechanisms as causes without executed validation.
