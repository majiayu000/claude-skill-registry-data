---
name: advisory-review
description: Final critic gate before report emission. Use after detection to verify evidence and thresholds, enforce sample sufficiency and claim-level severity, remove false positives, merge duplicate root causes, and reject causal prescriptions as findings. Adds separately labeled proactive recommendations.
license: MIT
---

# Advisory Review (the in-loop critic)

Detectors are optimistic by construction: each one looks for its own failure
mode and finds it. Nothing in a detector's own logic asks "would a careful
reviewer accept this?" That question is this skill's entire job, and it holds
the authority to **drop and downgrade**, not merely annotate.

The marketplace is graded on unseen sites. On an unseen site the expensive
mistake is not a missed finding — it is a confident, wrong one. This skill is
the component that trades a little recall for a lot of precision.

## When to use

After every detection layer has run, before the report is composed. Run it
standalone to review a completed run without re-crawling.

## Inputs

- **Required** — a run workspace already holding every detection layer's output
  (`url-validation`, `crawl-reachability`, `structured-data-identity`,
  `evidence-density`, `freshness-corroboration`, `engagement-audit`) plus the
  `AuditConfig` those layers agreed on.
- **Optional** — `--strict` to also drop findings that pass the five gates but
  rest on the thinnest evidence.
- **Not consumed** — no network access, no page re-fetch. The critic reasons
  over the candidate findings alone, which is what makes it cheap enough to run
  in-loop and repeatable.

```
python3 scripts/advise.py [--workspace PATH] [--strict] [--json]
```

## Procedure

Deterministic, in this order, and idempotent: one pass over the candidate
findings, then one deduplication pass, then the proactive layer. Re-running it
on its own output does not change either the count or the wording.

1. **Load every detection layer's findings.** Keep each finding's layer, check
   id, claim level, observed value, expected value and affected URLs.
2. **Apply the five gates in order** — evidence sufficiency, threshold
   coherence, sample sufficiency, claim-level discipline, false-positive traps.
   A failure is recorded with its reason rather than silently dropped.
3. **Downgrade where severity outran the evidence.** A demotion also caps
   `suggested_action.priority` at the new severity, so the action never
   outranks the claim it serves.
4. **Deduplicate and merge** findings describing one upstream root cause,
   recording the absorbed titles as `consequences`.
5. **Add the proactive layer** — improvements that hold where no defect was
   found, labelled claim level 4 and marked as hypotheses. These are the only
   place a causal prescription may appear.
6. **Emit the audit trail** — what was dropped, downgraded and merged, and why,
   so the published report can show its own reviewer's reasoning.

## The five gates

Every finding must pass all five. Each rejection is recorded with its reason,
so the audit trail shows what was removed and why.

After the gates, one alignment pass runs over every survivor:
**priority alignment.** `suggested_action.priority` may sit below severity (a
medium defect with a one-line fix legitimately jumps the queue) but never
above it. A downgraded severity with an untouched `critical` action priority
reads as a contradiction — the report would assert the claim was too weak to
keep its severity while demanding top-of-queue action on the same claim — so
the critic caps priority at the downgraded severity and records the change in
the downgrade trail under the `priority_alignment` gate.

### 1. Evidence sufficiency

A finding must carry a concrete observed value **and** at least one real URL.
"The site lacks structured data" is rejected; "8 of 11 sampled pages (e.g.
`https://example.com/products/x`) contain no JSON-LD block" passes. A finding
whose evidence string contains no digit and no URL is almost always a detector
asserting rather than observing.

### 2. Threshold coherence

The observed value must actually breach the stated expectation. A detector that
reports "median response 1,400 ms" against an expectation of "under 3,000 ms"
has fired incorrectly, and the finding is dropped rather than reworded. This
catches inverted comparisons and off-by-one threshold bugs at the report
boundary, where they would otherwise be invisible.

### 3. Sample sufficiency

A claim about the population needs enough of the population. A finding phrased
as "N of M pages" where M is below the configured minimum is either dropped or
demoted to a single-page observation with its severity reduced. This is what
stops a one-page crawl from producing site-wide verdicts.

### 4. Claim-level discipline

From the identification map in arXiv:2604.25707 §5.5:

| Level | Kind | Ceiling | Treatment |
|---|---|---|---|
| 1 | Direct observation | `critical` | May be asserted flatly |
| 2 | Descriptive contrast | `high` | Must read comparatively |
| 3 | Mechanism interpretation | `medium` | Must stay hedged |
| 4 | Causal prescription | — | Never a finding; moved to proactive as a hypothesis |

The paper is explicit that its dataset supports counting and contrast, and does
not support statements of the form "changing X will cause Y citations". A
finding claiming Level 1 while using causal language is re-levelled and
re-capped.

### 5. False-positive traps

A documented list of patterns that look like defects and are not. The full list
with rationale is in `references/false-positive-traps.md`. Representative
entries:

- `noindex` on a search-results, filter, pagination or staging-preview URL is
  correct behaviour, not a defect.
- Missing `Product` schema on a legal, about or contact page is expected.
- A hub or category page being short is its function, not thin content.
- A privacy policy with no comparison content is not an absorption failure.
- A page with no date is only stale-looking if its type implies recency.
- Marketing hedges on a homepage hero are conventional; the finding requires
  hedges to dominate *and* evidence to be absent.
- A single affected page out of many is not a site-wide critical.

## Deduplication

The same root cause surfaces in several layers. A JavaScript-rendered page
produces a render fault in reachability, missing structured data in selection,
and thin content in absorption — three findings, one cause. The advisor merges
these into the upstream finding and records the downstream symptoms as
consequences, so the report says "fix this one thing" rather than presenting
three independent problems.

## Proactive layer

After verification, the advisor adds recommendations that strengthen the brand
where no defect was detected. These are held to a higher bar than findings:
each must name its evidentiary basis and be non-obvious. Generic advice
("publish more content", "add an FAQ") is explicitly disallowed — the FAQ case
because the paper measures it at negative influence.

## Output

`07-advisory-review.json`:

```json
{
  "input_findings": 23,
  "output_findings": 17,
  "dropped": [ { "title": "...", "gate": "evidence_sufficiency", "reason": "..." } ],
  "downgraded": [ { "title": "...", "from": "high", "to": "medium", "reason": "..." } ],
  "merged": [ { "kept": "...", "absorbed": ["..."], "reason": "..." } ],
  "proactive_recommendations": [ ... ],
  "verdict": { "precision_actions": 6, "confidence": "..." }
}
```

## Guardrails

Read-only; consumes layer artefacts only and issues no network requests. It
never invents a finding — it can only remove, demote, merge or annotate what
the detectors produced. New material appears solely as clearly-labelled
proactive recommendations.

## Grounding

The claim-level model is the paper's identification map (§5.5), which separates
Level 1 direct counts from Level 4 causal optimisation prescriptions and warns
that "it is tempting to translate every correlation into a content tactic",
noting such translation is a hypothesis-generation tool rather than a
scientific law. An audit report is precisely where that temptation does damage,
which is why the discipline is enforced mechanically here rather than left to
the detectors' good intentions.
