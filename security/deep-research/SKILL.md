---
name: deep-research
description: Use when a decision-relevant question needs multi-source search, claim-level citations, contradiction handling, uncertainty, or a durable wiki handoff.
metadata:
  version: "8.1.0"
  updated: "2026-08-18"
  profile: "high-risk"
  assumes: "The question benefits from multiple sources and authorized source access is available."
  conflicts_with: "Link collection without synthesis, uncited material claims, privacy leakage, or autonomous experiments without objective evaluation."
---

# Deep Research

<skill_contract>
  <input>Decision-relevant question, audience, scope, recency, source and privacy boundaries, budget, and required deliverable.</input>
  <output>An answer-first synthesis with source and claim ledgers, citations, contradictions, uncertainty, and durable handoff.</output>
  <done>Decision-critical claims are traceable and adversarially checked, unresolved gaps are explicit, and the stop rule is met.</done>
  <non_goals>Link collection, uncited material claims, privacy leakage, exhaustive search, or autonomous high-impact experiments.</non_goals>

Research is an evidence loop, not a volume contest. Define the decision, gather the minimum diverse evidence, maintain source and claim ledgers, attack the synthesis, then stop when additional search no longer changes the answer.

## Usage Template

Provide: research question, audience/decision, scope, recency, allowed/excluded sources, privacy boundary, budget, output format, and wiki destination if durable. Load `references/research-ledgers.md` for ledger schemas.

## Workflow

<intake>

Choose one mode: evidence brief, knowledge curation, recency pulse, domain intelligence, scientific-method audit, or heavy research. Convert the question into 3-7 information requirements, decision criteria, interruption points, and a source-access plan.

</intake>

<unknowns_gate>

If the decision, recency window, private-data authority, or source boundary materially changes the result, return `NEEDS_INPUT`. Record known, probeable, testable, and inaccessible unknowns. Do not treat inaccessible sources as supporting evidence.

</unknowns_gate>

<execute>

1. Run a broad discovery pass; rank sources by authority, directness, recency, independence, and relevance.
2. Prefer primary and official evidence for consequential claims; use secondary sources for context and disagreement discovery.
3. Build a source ledger and claim ledger while reading, not after drafting.
4. Triangulate central claims; record dates and whether sources are independent or repeating one origin.
5. Run a gap-fill pass only for decision-critical unknowns.
6. Draft an answer-first synthesis separating evidence, inference, uncertainty, disagreement, and implications.
7. Run an adversarial pass: strongest counterevidence, alternative mechanism, stale data, selection bias, and missing base rate.
8. For science/AI experiments, specify problem, data/simulator, intervention, objective metric, uncertainty, reproducibility, and human judgment boundary.
9. Produce an activity trace and, when requested, a STOW handoff packet for `wiki-ingest` rather than writing source claims directly into governed concepts.

For high-stakes conclusions, use independent review. Obtain approval before accessing private systems, publishing, or launching experiments. Any durable write needs a diff-based rollback path.

</execute>

<evaluate>

Audit every material claim against the ledger. Check citation entailment, source independence, freshness, contradiction coverage, privacy, and whether the recommendation changes under plausible uncertainty. Stop when new searches repeat known evidence or cannot change the decision.

</evaluate>

<retry_policy>

`max_attempts: 3` research passes: discovery, gap-fill, adversarial. A retry must target a named gap with a changed query/source class. Stop on duplicate evidence, repeated access failure, or `NO_PROGRESS`.

</retry_policy>

<state_contract>

Persist `{run_id, status, attempt, budget, evidence, unknowns, last_error, next_action}` plus question version, mode, information requirements, source/claim ledgers, search trace, contradictions, privacy decisions, approval, draft version, and rollback/write receipts.

</state_contract>

## Failure Protocol

- `NEEDS_INPUT`: scope, decision, privacy, or freshness boundary is ambiguous.
- `INSUFFICIENT_EVIDENCE`: sources cannot support the requested confidence or recommendation.
- `BLOCKED_PERMISSION`: private or restricted evidence is unavailable; exclude it explicitly.
- `VERIFY_FAILED`: citation does not entail the claim or key contradiction is unresolved.
- `NO_PROGRESS`: a changed pass yields no decision-relevant evidence.
- `BUDGET_STOP`: synthesize covered scope and list gaps. `max_attempts: 3`.

## Output Contract

Return `status`, `result` (answer-first synthesis and recommendation), `evidence` (claim/source ledgers and citations), `unknowns`, and `next_action` including approval or wiki handoff.

## Edge Cases

- Ten articles repeat one press release: count one underlying evidence origin and lower independence confidence.
- Sources disagree on a current metric: show dated values and definitions, explain the mismatch, and withhold a false single number.

## Success Metrics

- Material claims have direct, current, claim-level support.
- Disagreements and confidence are visible where they affect the decision.
- Search stops by evidence saturation or budget, not arbitrary link count.

## Quality Gates

- [ ] Decision, scope, recency, privacy, and source boundaries are explicit.
- [ ] Source and claim ledgers are inspectable.
- [ ] Independent/adversarial verification covers central claims.
- [ ] Approval and rollback controls cover external actions and durable writes.
- [ ] Handoff preserves source provenance and unresolved gaps.

</skill_contract>
