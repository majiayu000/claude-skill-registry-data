---
name: deep-research-lcot
description: >
  Use for deep research, literature reviews, technical due diligence, scientific
  explainers, market/technical reports, and reasoning-first knowledge synthesis.
  Turns a question into a verified research plan, evidence matrix, derivation graph,
  contradiction audit, and cited final report. Activates on: research, investigate,
  deep dive, literature review, technical due diligence, market report, reasoning
  synthesis, evidence matrix, fact-check with citations. Do not use for casual
  questions or tasks that do not need source-backed research.
metadata:
  version: "1.0.0"
---

# Deep Research LCoT Skill

## Purpose

Perform deep research by retrieving and synthesizing verifiable reasoning chains, not just isolated facts. Favor first-principles derivations, explicit assumptions, evidence quality, cross-domain links, and contradiction checks.

## Required behavior

1. Clarify the research objective only when a missing constraint would materially change the answer. Otherwise make reasonable assumptions and state them.
2. Convert the user request into a research brief with: objective, scope, exclusions, decision/use case, time sensitivity, required evidence quality, and output format.
3. Decompose the topic into atomic concepts, claims, mechanisms, prerequisites, and unknowns.
4. Search for sources using a tiered source strategy:
   - primary sources: papers, standards, official docs, datasets, regulatory filings, laws, patents, source code
   - secondary expert sources: textbooks, review papers, technical blogs from recognized experts
   - tertiary sources only for orientation: encyclopedias, summaries, general media
5. Build an evidence matrix. For every important claim, include source, date, author/org, evidence type, confidence, limitations, and whether it is directly supported or inferred.
6. Build reasoning chains. Each chain must include: starting principles, assumptions, intermediate steps, endpoint claim, falsification tests, and unresolved gaps.
7. Run adversarial verification:
   - find contradictory evidence
   - check whether sources share a common upstream source
   - distinguish empirical evidence from model/speculation
   - flag circular citations and unsupported causal claims
   - check dates for obsolete facts
8. Synthesize with citations. Do not overstate certainty. Separate facts, estimates, interpretations, and recommendations.

## Output modes

Use the mode that best fits the user request.

### Research brief

Return:
- Executive answer
- Key findings
- Evidence matrix
- Reasoning chains
- Disagreements/uncertainties
- Practical implications
- Next research steps

### Inverse knowledge search

For a target concept, return:
- Definition
- Upstream prerequisite map
- Multiple derivation paths
- Cross-domain analogies
- Where each path breaks
- Best sources to verify each step

### Technical due diligence

Return:
- Claim inventory
- Architecture or mechanism map
- Competitive landscape
- Evidence grade
- Failure modes
- Risks and mitigations
- Decision recommendation

## Citation rules

- Cite every non-obvious factual claim.
- Prefer direct source citations over secondhand citations.
- Include publication or update dates when recency matters.
- Never cite a source that does not support the sentence it is attached to.
- Mark unsupported but plausible reasoning as inference.

## Final quality checklist

Before finalizing, verify:
- The answer addresses the user's actual decision or goal.
- Major claims have citations or are clearly labeled as inference.
- Dates are explicit for changing facts.
- Contradictions and uncertainties are visible.
- The final answer is useful, not just comprehensive.
