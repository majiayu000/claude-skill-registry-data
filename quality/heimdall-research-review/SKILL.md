---
name: heimdall-research-review
description: Review research findings for proof completeness, specificity, and verifiability — spot-check citations and flag excessive unverified-claim ratios.
---

# Research Review

## Purpose

Validate that research Workfiles ground every finding in specific, verifiable proof before those findings are consumed downstream. The proof standards under review — source tiers, proof formats per source kind, `[UNVERIFIED]` marking — are the researcher's standing research convention. This skill defines the reviewer-side validation checklist and verdict semantics.

## When to Use

- When reviewing a research Workfile (findings, analysis, investigation output).
- When a review brief asks for proof validation of any findings document.

## Workflow

1. **Understand the research scope.**
    - Read the research brief or stated scope: which sources were in scope, and whether any override applied.
    - Identify the Workfile's claims — each discrete finding is a unit to validate.
2. **Check completeness.**
    - Every finding has a proof reference (file path, URL, key, or timestamp).
    - No findings are missing both a proof and an `[UNVERIFIED]` marker.
    - All `[UNVERIFIED]` claims include an explanation of why verification was not possible.
3. **Check specificity.**
   - Each proof meets the format for its source kind: path + line numbers for files; full, resolvable URL or stable identifier for web/document systems; exact key for trackers; query + retrieval timestamp for data/API sources; dated, attributed reference for ephemeral/human sources.
   - No vague references like "the codebase" or "the docs".
4. **Spot-check proof resolution.**
     - Verify that at least 2 proofs resolve to their claimed sources: paths exist and line numbers are accurate, URLs load, keys are valid.
     - Prioritize proofs backing the Workfile's most load-bearing findings.
5. **Compute the unverified ratio and render the verdict.**
   - Count `[UNVERIFIED]` claims; divide by total claims; flag if the ratio exceeds 25% (more than 1 in 4 claims unverified).
   - **PASS** — proofs are complete, specific, spot-checked, and the unverified ratio is ≤25%.
    - **PASS-WITH-NOTES** — proofs are mostly complete and specific, but minor gaps exist (e.g., one vague citation, unverified ratio at 20–25%). Request clarification or improvement before the Workfile is consumed.
   - **BLOCKED** — critical proof gaps exist (e.g., >25% unverified, multiple vague citations, broken file paths). Reject and request resubmission with complete proofs.

## Quality Criteria

- Every finding in the Workfile was checked for a proof reference or an explained `[UNVERIFIED]` marker.
- Specificity was assessed against the format for each proof's source kind, not a single generic standard.
- At least 2 proofs were actually resolved against their sources — never format-checked only.
- The unverified ratio was computed and stated in the review, not eyeballed.
- The verdict names the specific gaps that drove it, so resubmission is actionable.

## Anti-Patterns

- **Rubber-stamping**: Approving on format alone without resolving any proof against its source.
- **Format-only review**: Checking that proofs look right (shape, syntax) without spot-checking that they resolve.
- **Accepting vague citations**: Letting "the codebase" or "the docs" pass as proof.
- **Ignoring the ratio**: Passing a Workfile where unverified claims dominate because each one is individually explained.
- **Re-doing the research**: Re-investigating the topic instead of validating the presented proofs — the review validates evidence, not conclusions reachable by independent research.
