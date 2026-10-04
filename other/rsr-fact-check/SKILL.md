---
name: rsr-fact-check
version: 1.0.0
description: Verify one specific claim against primary sources and return a verdict with evidence.
author: matrixx0070
tags: [research, fact-check, verification, claims, primary-source]
capabilities: []
---

# Fact Check

## When to use
Reach for this when there's a single discrete claim on the table and you need to know if it's true — a statistic, a quote, an attribution, a date, a "study shows" assertion. Output is a verdict backed by the primary source, or an honest "unverifiable."

**Not for:** answering an open question (use rsr-deep-dive); rating a source overall (use rsr-source-eval); reconciling many sources into a narrative (use rsr-synthesis). This targets exactly one claim.

## Method
1. **Isolate the claim.** Restate it as a single checkable proposition. Split compound claims — "sales doubled and profits rose" is two checks. *Decision:* if it's a matter of opinion or prediction, stop and label it non-factual.
2. **Identify what would confirm or refute it.** What primary evidence would settle it — the original study, the filing, the transcript, the dataset?
3. **Trace to the primary.** Follow citations upstream past the article to the original source. *Decision:* if you can only find restatements and never the primary, that itself is a finding (verdict: unverified).
4. **Compare against the primary.** Does the primary actually say this? Watch for numbers stripped of context, quotes trimmed to flip meaning, and correlation reported as cause.
5. **Check currency.** Was it true once but since superseded?
6. **Rule.** Assign True / Misleading / False / Unverifiable, quote the decisive evidence, and cite the primary.

## Example
Claim: "A Harvard study found coffee cuts heart-disease risk by 50%." Isolate: single stat, attributed. Trace: the article cites a news piece citing an observational study. Primary: the study reports a ~15% *association* in the highest-consumption group, not causation, not 50%. Verdict: **False** — the 50% figure and the causal framing are unsupported; the real finding is a modest correlation. Evidence quoted from the study abstract, cited.

## Pitfalls
- Stopping at a secondary source that "confirms" it without reaching the primary — you've verified an echo.
- Missing that a real number was quoted stripped of its qualifier (per-year vs. lifetime, relative vs. absolute).
- Calling a claim False when it's merely unverifiable — absence of evidence is its own verdict.
- Fact-checking an opinion or forecast as if it had a truth value.

## Output format
```
Claim: <single proposition, verbatim>
Verdict: <True | Misleading | False | Unverifiable>

Primary source: <title / publisher> — <date> <link>
Decisive evidence: "<quote from primary>"
What the claim got wrong (if any): <e.g. dropped qualifier, correlation→cause>
As of: <date checked>
```
