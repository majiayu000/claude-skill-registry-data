---
name: cs-research
version: 1.0.0
description: Research a customer question across docs, changelogs, and past tickets, then answer with source attribution, a confidence rating, and honest gaps.
author: matrixx0070
tags: [customer-support, research, knowledge-base, attribution, accuracy, verification]
capabilities: []
---

## When to use

Use this when a customer asks something you cannot answer from memory — how a feature behaves, whether a limit exists, if a bug is known, or what changed in a release. Build a cited answer instead of guessing.

**Not for:** questions you already know cold (just reply), turning a solved issue into docs (cs-kb-article), or open-ended web research unrelated to the product. If no internal source can settle it, escalate rather than infer.

## Method

1. Restate the question with the customer's plan, version, and platform pinned. A "does X work" answer often depends on these.
2. Search authoritative sources in order: official docs/help center → changelog/release notes → engineering tickets and known-issue lists → prior resolved tickets. Prefer newest and most authoritative.
3. Cross-check each claim against at least two sources. **Decision point:** if sources conflict, favor the one closest to current product state (dated release notes beat old docs) and note the conflict.
4. Label each finding as documented behavior or observed/anecdotal, with source and date.
5. **Decision point:** if no source confirms it, mark "unconfirmed — needs eng verification" and stop — do not reason your way to an answer.
6. Draft for the customer's level, then attach the internal source trail so a teammate can re-verify.

## Example

> **Q:** Can Business-plan users export more than 10k rows? (v3.2, web)
> **A:** Yes — the 10k cap was raised to 100k for Business and above.
> **Confidence:** High.
> **Sources:** Changelog 2026-05-12 "Export limit raised to 100k (Business+)"; Docs → Exports → Limits (updated 2026-05-14). Both agree.
> **Gap:** none.

## Pitfalls

- Answering from one source — a single stale doc is how wrong answers ship.
- Blending documented and anecdotal behavior without labels.
- Guessing to avoid saying "unconfirmed" — a wrong confident answer costs more than a delay.
- Dropping the source trail, so no one can verify or reuse your work.

## Output format

```
Question: <restated + plan/version/platform>
Answer: <concise, customer-ready>
Confidence: High / Medium / Low
Sources:
  - <claim> → <title, date, link>
Conflicts / gaps: <or "none">
Next step if unconfirmed: <who verifies>
```
