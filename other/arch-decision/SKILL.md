---
name: arch-decision
description: Run a structured 7-stage architecture decision loop on any technical choice — vendor evaluation, build-vs-buy, infra strategy, schema change, ADR. Produces a scored decision memo with a binary verifier verdict. Good triggers include "should we use X or Y", "help me think through our options", "we need to decide", "evaluate approach", "technical trade-off", "which is better for our stack", "options for", "design decision", "ADR", "architecture decision".
---

# arch-decision

A structured 7-stage loop for any architecture, vendor, infra, or build-vs-buy question. The skill provides the process; you make the final call.

**For non-technical decisions (people, process, policy):** evidence in Stage 3 may include interviews, budget documents, policy files, and performance records. Stage 4 criteria must include legality, fairness, and privacy where applicable.

## How to start

Paste your question in plain language. Example: "Decide whether to build our own webhook delivery system or buy one." The skill runs Stages 1–3 automatically, then stops for your input before scoring.

---

## Stage 1: Framer

**Tool restriction: NO tools. Input only.**

Turn the question into a single sentence ending with `?`, labelled `Decision question:`. Write one measurable line labelled `Success criterion:` that defines done.

**MUST NOT:** express preference, list options, or suggest an approach.

**End-of-stage self-check:** "I have not expressed preference. I have not listed options. I have one decision question and one success criterion."

**Double-review:** Review once as "did I stay neutral?" then once as "is the success criterion actually measurable?". Each pass must output at least one concrete objection OR an explicit "No objection because [specific reason]". If an objection is found, show the specific revision made before continuing. Declaring a review passed without visible output is invalid.

---

## Stage 2: Option Widener

**Tool restriction: NO tools. No web search, no file reading.**

Enumerate ALL options before ANY comparison.

**MUST include:**
- `Do nothing / Status quo` with a non-empty `Cost/consequence:` line
- At least one option marked `Not in original brief`
- The most reversible option identified with `Most reversible: yes`

**MUST NOT:** score, rank, compare, or express preference.

**`Cost/consequence:` must name a specific impact, the affected party, a timeframe, and a measurable magnitude — or explicitly label missing data as `GAP:`. Vague adjectives ("some disruption", "increased risk") fail Check 2.**

**End-of-stage self-check:** "Do nothing is present with a cost. I have at least one option not in the original brief. No scores or rankings appear."

**Double-review:** Review once as "have I genuinely widened, or just listed what was asked?" then once as "is the do-nothing cost honest or vague?". Each pass must output at least one concrete objection OR an explicit "No objection because [specific reason]". If an objection is found, show the specific revision made before continuing. Declaring a review passed without visible output is invalid.

---

## Stage 3: Evidence Analyst

**Tool restriction: Web search, file reading, Deep Research ONLY. No scoring, no recommendations.**

Record the instinctive leading option (the one that looks best after Stage 2) at the top of this stage before any research begins.

For each option, gather evidence. Maintain an **Evidence ledger** table:

| ID | Claim | Source/GAP | Favours option |
|----|-------|------------|----------------|

**MUST:** actively hunt for evidence AGAINST the instinctive leading option.

Every claim must have a URL, file path, doc reference, or explicit `GAP: [description]` in Source/GAP.

**MUST NOT:** recommend, score, or imply a winner.

**End-of-stage self-check:** "Every row in my evidence ledger has a non-empty Source/GAP. I have searched for evidence against my instinctive leading option."

**Double-review:** Review once as "are there claims in my prose not in the ledger?" then once as "did I actually look for counter-evidence?". Each pass must output at least one concrete objection OR an explicit "No objection because [specific reason]". If an objection is found, show the specific revision made before continuing. Declaring a review passed without visible output is invalid.

---

## Stage 4: Numbers Analyst

> ⚠️ **HUMAN GATE — STOP BEFORE THIS STAGE** ⚠️
>
> Output the block below and wait for a SEPARATE human reply. Do NOT proceed until the human responds.
> **Assistant-authored weight confirmations are invalid. Copy the human's reply verbatim into the memo before any scoring begins.**

```
AWAITING WEIGHTS FROM HUMAN

Please confirm or edit the criteria weights before I score anything.
Proposed criteria (total must sum to 100):
- [criterion 1]: [weight]
- [criterion 2]: [weight]
...
Reply with your confirmed weights and I will proceed.
```

**Tool restriction: No web search. Use only the Stage 3 evidence ledger and any uploaded files.**

Build a scoring matrix using ONLY the human-confirmed weights.

**MUST write** immediately before the matrix:
`Weights locked before scoring: LOCKED BEFORE SCORING — [list each criterion:weight]`

**Every score cell must cite at least one evidence ledger ID (e.g. [E3]) or `GAP:` label. Unledgered reasoning is inadmissible — if you cannot cite a ledger entry for a score, add a `GAP:` row to the ledger first.**

**MUST NOT:** re-score after seeing results, adjust weights retroactively.

**End-of-stage self-check:** "The weights locked line appears before any scores. I used only the human-confirmed weights. Every score cell cites a ledger ID or GAP:."

**Double-review:** Review once as "did I sneak in any retroactive weight adjustment?" then once as "are all scores defensible from Stage 3 evidence?". Each pass must output at least one concrete objection OR an explicit "No objection because [specific reason]". If an objection is found, show the specific revision made before continuing. Declaring a review passed without visible output is invalid.

---

## Stage 5: Red Team

**Tool restriction: NO tools. Pure argument only.**

For each option NOT recommended by the matrix, write its strongest steelman. Then write a pre-mortem for the winner.

Each steelman must: (a) argue why that option should WIN, not merely why it is reasonable; (b) cite at least one evidence ID from Stage 3; (c) identify the winner's strongest vulnerability. A steelman a genuine advocate would reject as inadequate must be revised.

**Format:**

`Steelman — [Option name]:` paragraph

`Pre-mortem — [Winner]:` paragraph starting "If we chose [winner] and it failed..."

**End-of-stage self-check:** "Each steelman argues for a win, cites evidence, and names the winner's vulnerability. My pre-mortem names a specific failure mode, not a generic risk."

**Double-review:** Review once as "would a genuine advocate recognise this as their best argument?" then once as "is the pre-mortem specific enough to act on?". Each pass must output at least one concrete objection OR an explicit "No objection because [specific reason]". If an objection is found, show the specific revision made before continuing. Declaring a review passed without visible output is invalid.

---

## Stage 6: Recommender

**Tool restriction: NO new research. Synthesise from Stages 1–5 only.**

Write a one-page decision memo:

1. `Recommendation:` one sentence naming the option and the success criterion it serves
2. `Rationale:` 2–3 paragraphs citing evidence IDs from Stage 3
3. `Strongest counter-argument:` must (a) quote or paraphrase the Stage 5 steelman's strongest claim; (b) cite the evidence IDs that support it; (c) explain exactly why the recommendation still holds despite it
4. `Pre-mortem mitigation:` "If [failure mode from Stage 5], then [specific mitigation]"
5. `Day-one delta:` one sentence — what changed vs the instinctive answer recorded at the start of Stage 3
6. `What we don't know:` bullet list of GAPs from Stage 3 that could change this recommendation

**MUST NOT:** introduce new evidence, revisit weights.

**End-of-stage self-check:** "I have addressed the strongest counter-argument with a quote or paraphrase and evidence IDs. My pre-mortem mitigation is in If/then form. I have named a specific day-one delta."

**Double-review:** Review once as "does someone who disagrees know exactly which evidence to challenge?" then once as "is the day-one delta specific or generic waffle?". Each pass must output at least one concrete objection OR an explicit "No objection because [specific reason]". If an objection is found, show the specific revision made before continuing. Declaring a review passed without visible output is invalid.

---

## Stage 7: Verifier

**Tool restriction: NO tools. Fresh-eyes read of the memo only.**

Run all 5 checks. Return PASS or FAIL with per-check results.

**The 5 checks:**

1. Does the opening block contain one line starting `Decision question:` ending with `?` and a separate non-empty line starting `Success criterion:`? (NO = missing decision target or success criterion)
2. In `Options considered`, are there ≥3 named options including `Do nothing`/`Status quo` with a `Cost/consequence:` line naming a specific impact, affected party, timeframe, and measurable magnitude or `GAP:` — AND a different option marked `Not in original brief`? (NO = option set brief-biased or do-nothing cost too vague)
3. Does every analytical paragraph/table row cite an evidence ID or `GAP:`, does every ledger row have a source or `GAP:`, does each option have ≥2 ledger rows with at least one non-GAP source (unless all unavailable), and does every score cell cite a ledger ID? (NO = unsourced claim, under-evidenced option, or unledgered score)
4. Does `Weights locked before scoring:` listing each criterion and weight appear before the first scoring marker? (NO = scoring may have preceded weight-locking)
5. Does the `Recommender` section include `Strongest counter-argument:` naming a non-recommended option and `Pre-mortem mitigation:` in `If ... then ...` form? (NO = memo does not engage the strongest opposing case with an actionable mitigation)

**Output format:**

```
VERIFIER RESULT: [PASS / FAIL]

Check 1: [YES/NO] — [one line]
Check 2: [YES/NO] — [one line]
Check 3: [YES/NO] — [one line]
Check 4: [YES/NO] — [one line]
Check 5: [YES/NO] — [one line]

[If FAIL: "The memo does not count until all checks return YES. Return to Stage [N] and fix: [specific issue]."]
[If PASS: "Memo is valid. The human may now act on this recommendation."]
```

---

## Worked example (EKS upgrade)

**Input:** "Decide how to upgrade our EKS platform version with minimal risk to partner-facing APIs."

**Stage 1 output:**

`Decision question:` Which EKS upgrade strategy minimises downtime and rollback risk for partner-facing APIs while reaching a supported platform version within 60 days?

`Success criterion:` Zero partner-facing API errors during cutover, rollback achievable within 30 minutes, target version reached by deadline.

**Stage 2 options:**

| Option | Most reversible? | Notes |
|--------|-----------------|-------|
| Do nothing / accept security risk | — | `Cost/consequence:` Unsupported version; growing CVE exposure; AWS support unavailable for incidents affecting ~N partner API calls/day until resolved |
| In-place managed node group rolling upgrade | — | Standard path; lower ops overhead |
| Blue-green parallel cluster | yes | `Most reversible: yes` — traffic can shift back instantly |
| Upgrade staging first, then prod with canary traffic shift | — | `Not in original brief` — adds a rehearsal gate before prod |
