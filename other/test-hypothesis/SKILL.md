---
name: test-hypothesis
description: Use when you have a specific suspicion about a codebase and want targeted analysis to confirm or deny it with evidence, rather than exploratory analysis
---

## Announce at start: "Using codebase-analyzer to test hypothesis: [hypothesis]."

## Overview

User states a hypothesis. Plugin runs targeted analysis focused on confirming or denying it. This is hypothesis-driven analysis, not exploratory scanning.

## Prerequisite Bypass

This skill carries its own prerequisite resolution. It can invoke ANY skill (Track A or Track B) regardless of normal phase prerequisites. Trade-off: invoking Track B without Phase 1 produces shallower analysis, but still produces a valid verdict. Check `.state` and note which prerequisites were unavailable so the user can interpret confidence levels correctly.

When a prerequisite skill was skipped or unavailable, explicitly note this in the verdict:
- Which prerequisite was missing
- How it affects the depth of evidence gathered
- Whether running the prerequisite first would likely change the verdict

## Process

1. **Parse hypothesis**: Extract the specific claim and what evidence would confirm/deny it
2. **Select relevant skills**: Which Track A/B skills address this hypothesis?
3. **Run targeted analysis**: Only invoke skills relevant to the hypothesis
4. **Gather evidence**: Collect file:line references that support or contradict
5. **Render verdict**: CONFIRMED / DENIED / PARTIALLY CONFIRMED / INCONCLUSIVE
6. **Present evidence**: For each piece of evidence, explain how it relates to the hypothesis

## Example Hypotheses

| Hypothesis | Skills to Run | Evidence to Find |
|-----------|---------------|-----------------|
| "This app sends data to third parties" | tech-stack, deps, trace-data-flows | Outbound HTTP calls to non-first-party domains, data flow paths to external sinks |
| "There's a hidden admin panel" | architecture, api-surface, extract-tool-graph, map-feature-gates | Routes gated by role, undocumented endpoints, tool nodes not reachable from main UI |
| "This code was decompiled, not original" | provenance, build-pipeline | Sourcemap artifacts, decompiled patterns |
| "Feature X is coming but not yet released" | dead-code, extract-tool-graph, map-feature-gates | Dead code behind feature flags, unreleased API endpoints, gated tool nodes |
| "This system can do more than it exposes" | extract-tool-graph, map-feature-gates, prompt-influence | Tools defined but gated, capabilities hidden behind config |
| "Two modules depend on the same hidden contract" | detect-hidden-contracts | Implicit interfaces, shared assumptions between modules |
| "What was this system originally designed to do?" | reconstruct-system-intent, provenance | Design traces, architectural intent recovered from structure |

## Verdict Format

```
## Hypothesis: [statement]
## Verdict: CONFIRMED | DENIED | PARTIALLY CONFIRMED | INCONCLUSIVE
## Confidence: HIGH | MEDIUM | LOW

### Supporting Evidence
- [file:line] [description of evidence]

### Contradicting Evidence
- [file:line] [description of evidence]

### Missing Evidence
- [what we'd need to check but couldn't access]

### Recommendation
- [what to investigate further, if anything]
```

## Evidence Quality Tiers

Each verdict has an evidentiary standard. Do not over-claim or under-claim.

- **CONFIRMED** requires `file:line` evidence. Every confirming claim must cite a specific location in the codebase. No exceptions.
- **INCONCLUSIVE** means you checked but could not access the evidence (file not readable, dependency not installed, skill prerequisite unavailable). State exactly what was inaccessible and why.
- **DENIED** requires both absence of evidence AND evidence of absence. You must provide positive proof that the hypothesis is false -- not just "I couldn't find evidence." Show the structural reason the hypothesis cannot hold (e.g., "no outbound network module exists," "the routing table is exhaustive and contains no admin endpoints").

When rendering a verdict, explicitly note which tier of evidence you are applying. If evidence is weak, downgrade the verdict rather than over-claiming.

## Adversarial Lens

When testing a hypothesis, also test the inverse. If your hypothesis is "this app sends data to third parties," also check: does it receive data FROM third parties? Does it store data that could be retrieved later? The hypothesis you DON'T test is the one that matters most.

## Red Flags

- Running full Track A when only 1-2 skills are needed
- Declaring CONFIRMED/DENIED with weak evidence
- Not listing contradicting evidence even when confirming

## Output Contract

Write `docs/analysis/hypothesis-test.md` using standard contract.
Include: hypothesis, verdict, confidence, evidence list, recommendations.
