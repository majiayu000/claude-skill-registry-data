---
name: forge-council
description: LLM Council (FULL) — 5 independent advisors via the Agent tool, anonymous peer review, chairman synthesis with minority report, validated record. Only via councilTrigger; never proof.
---

# forge-council — LLM Council (FULL protocol)

Use ONLY when `councilTrigger()` (forge-quality.cjs) says FULL: an explicit owner request for
pushback, or high impact + high uncertainty. Never by default, never on simple tasks — the
expected information gain must outweigh latency, cost and context load. LIGHT exists as an outcome
of the trigger but deliberately has NO protocol here yet: first a benchmark that proves its value
(anti-overengineering); until then LIGHT falls back to one targeted second opinion.

## Protocol (FULL)

**Step 0 — neutral framing.** Write the decision question NEUTRALLY (no preferred direction, no
"we lean towards X"): context, options, criteria, hard limits. Compute `context_hash` =
sha256 of that framing text (forge-quality.cjs::sha256). The framing is a run artifact.

**Step 1 — 5 fresh, independent advisors, in parallel.** Dispatch via the Agent tool (real
subagents, one message with 5 parallel calls; NO simulated agents). Each advisor gets ONLY the
neutral framing — no visibility of the others. The five fixed lenses:
- **Contrarian** — attacks the most popular option; looks for what everyone is missing.
- **First Principles** — reduces to fundamentals; ignores convention.
- **Expansionist** — widens the option space; what if the question itself is too narrow?
- **Outsider** — looks at it as an outsider/end user would; jargon-free.
- **Executor** — judges feasibility, cost, risk, rollback.

**Step 2 — anonymous peer review.** Anonymize the five pieces of advice as A-E and send them back
to each advisor (a second dispatch round): rank the other four and name the strongest critique of
each. Anonymity prevents authority bias and self-preference.

**Step 3 — chairman synthesis.** The orchestrator (or a separate chairman dispatch) weighs the
advice + peer rankings and writes the decision WITH an explicit **minority report**: dissenting
opinions don't disappear, they're recorded alongside the reason.

**Record.** Fill in a CouncilDecisionRecord: council_id, context_hash, participants (role + runtime +
dispatch_id from the REAL Agent dispatches + response_ref), responses, quorum, verdict,
minority_report, status. Validate with `validateCouncilRecord` and persist via
`node .claude/forge-bin/forge-quality.cjs council-save <run_id> <record.json>` — an invalid
record is NOT written (the refusal with a reason is the honest result), and a council_id is
never overwritten.

## Limits (permanent)
- Validation is **shape_only**: runtime/dispatch_id are not cryptographically bound; real
  provenance requires the owner-gated gateway dispatch receipt (OWNER-GATED.md).
- **Consensus is never proof.** Every council decision that touches code still requires ordinary
  tests/measurements afterward; the record points to them, never the other way round.
- An INCOMPLETE quorum is honestly marked INCOMPLETE — never padded out.
