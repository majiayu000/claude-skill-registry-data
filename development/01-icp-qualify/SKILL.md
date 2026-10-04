---
name: 01-icp-qualify
description: >-
  The qualification gate of the GTM chain - judges every discovered company
  against the client's ICP before any paid enrichment, so credits are spent only
  on companies that could actually buy. Works for any client and any vertical:
  it studies the client first, then compiles client-specific qualification
  criteria and applies them. Use whenever a prospect list needs cleaning before
  outreach or enrichment - "qualify this list", "remove non-ICP companies",
  "which of these fit the ICP", "filter this lead list", "clean the list before
  enriching" - and always between discovery and any credit-spending skill when
  running as part of the chain. Also use when the user has a CSV/JSONL of
  companies and asks which ones are worth pursuing, even if they never say the
  word "qualify". Runs on model judgment by default - no API keys required.
---

# ICP Qualify - the gate

Discovery filters match **labels** (industry codes, size bands, locations as a
database recorded them). This skill judges **fit**: would this specific company
plausibly buy from this specific client? The two questions diverge constantly -
acquisitions, competitors, stale headcounts, and shell listings all pass label
filters and then waste enrichment spend downstream. The gate exists so every
credit spent after discovery goes to a company that could actually buy.

The skill is **general-purpose by construction**: nothing client-specific is
hardcoded. It first understands the client, then compiles a client-specific
**qualification brief**, gets it approved, and only then judges prospects.

## Phase 1 - understand the client

Detect the operating mode; never ask for what is already available.

- **Package mode** - running inside the chain: inherit the client profile
  (what they sell, ICP bounds, exclusions) from the chain's client-profile
  artifact or the router's plan. Ask nothing.
- **Standalone mode** - invoked directly: the user names the client company
  and provides whatever they have - ICP description, firmographic bounds,
  competitor names, exclusion list. **Proceed with whatever exists.** Missing
  information never blocks a run.

**Research fallback (bounded).** If the client's business or ICP is still
unclear, read the client's own website - homepage, about, product pages, at
most ~5 pages - and draft the missing understanding. Cache everything learned
into the client profile so research runs once per client, not once per run.

## Phase 2 - compile the qualification brief

From the client understanding, write the criteria that will judge every
prospect. The brief has two mandatory checks, one universal check, and
client-specific dynamic checks:

1. **Business nature (primary).** What does the prospect actually do, judged
   from its description - and does that match who the client sells to? This is
   also where competitors are caught: a prospect in the client's own product
   category is never a lead.
2. **Firmographics.** Headcount band, geography, industry bounds from the ICP.
   Cheap, rule-based - and applied with the wide-tolerance rule below, because
   discovery data is often stale.
3. **Independence and liveness (universal).** Is this still an operating,
   independent business? Acquired, merged, dormant, or shell companies are not
   buyers regardless of fit. This check is client-independent and always on.
4. **Dynamic checks (client-specific).** Derive 1–3 checks from this client's
   reality that the generic checks can't know - e.g. for a QA-automation
   client: "does the prospect ship software?"; for a payroll client: "does the
   prospect have employees in the covered countries?". These are generated
   fresh per client, from the profile and research.

**The brief is an artifact, not a thought.** Write it out (see
`references/brief-template.md`), show it for approval before judging anything,
then save it to the client config. Later runs **reuse the saved brief** -
regenerate only when the user asks for a refresh, when calibration amends it,
or when a run's disqualification rate departs sharply from the client's history
(suggest a refresh; never regenerate silently). The brief records which model
it was calibrated with; a model change re-triggers the acceptance check below.

## Phase 3 - judge every prospect

Read `references/dq-catalog.md` before judging - it defines every
disqualification category and the evidence each requires.

Apply the checks in cost order: exclusion list first (free), firmographic
screen next (rules on existing fields), then business-nature and the remaining
judgment checks.

**Three verdicts, asymmetric on purpose:**

- **`qualified`** - fits the brief; no DQ category applies.
- **`disqualified`** - a DQ category applies **with quotable evidence** (a
  sentence, a redirect, a number, a list entry). Name the category and the
  evidence, always.
- **`uncertain`** - fit can't be confirmed, but no DQ can be proven.
  **Uncertainty is never a disqualification.** The two mistakes cost
  differently: wrongly qualifying wastes a few credits; wrongly disqualifying
  throws away a real buyer. When in doubt, `uncertain`.

**The wide-tolerance rule for firmographics.** Discovery data lies about size
and location often enough that near-misses must not hard-fail: outside the
band but within roughly 2× of the ceiling or half of the floor → `uncertain`,
resolved later by fresher evidence. Beyond that → `disqualified` (no data
error is that large). Missing data → proceed; absence is never evidence.

**Description sourcing.** Business-nature judgment needs a description. When a
record has none (common for Maps-sourced rows), fetch the prospect homepage's
title and meta-description with a plain HTTP request - free, no scraping
service - and judge from that. If the fetch fails, the verdict is `uncertain`
with the gap noted.

**Two passes.** Pass 1 runs pre-spend on discovery fields. Pass 2 re-runs
after scrape/signal skills have added evidence: re-judge every `uncertain`,
confirm every `qualified` (evidence can also demote - an acquisition surfaced
by a scrape moves a qualified row to disqualified). Verdicts update in place
with `pass: 2`; rows move between output files to match their new verdict.

## Execution engines

- **Default:** judgment runs in-session. No API key, no per-company cost.
- **Scale option:** for large lists, an external model may do the judging via
  an OpenAI-compatible endpoint - any vendor. Configuration:
  `QUALIFY_LLM_BASE_URL`, `QUALIFY_LLM_API_KEY`, `QUALIFY_LLM_MODEL`. Missing
  configuration → in-session, silently.
- **Acceptance check:** a newly configured model must first pass the chain's
  evaluation set (`_evals/01-icp-qualify/`) before judging a real list, and its
  false-disqualification rate is the number to watch - that's the expensive
  mistake. A model that fails falls back to in-session judgment.
- External judgments return structured JSON matching the record contract;
  invalid responses are retried once, then that record becomes `uncertain`.

## Calibration (first run per client, and per model)

1. Judge the first 10 records; show a compact table: company · verdict ·
   category · one-line reason.
2. Take corrections. Every correction becomes a rule written into the brief
   (e.g. "hybrid manufacturers with named product lines qualify").
3. Repeat in batches of 10. After **two consecutive clean rounds**, run the
   remainder without check-ins.
4. Same client + same model later → skip calibration. Model changed → run the
   acceptance check, then one abbreviated calibration round.

## Output contract

Three files per run, under `runs/<run-id>/` per `headless-gtm-shared/CONVENTIONS.md`:

- **`records.jsonl`** - what flows downstream: all `qualified` rows, plus
  `uncertain` rows **only if the user opts them in** (see the gate below).
  Every row keeps all upstream fields and carries its `qualification` object,
  so a later pass can re-find and re-judge the uncertain ones.
- **`uncertain.jsonl`** - the review queue, when uncertain rows are withheld:
  each with its open question. Nothing here is lost; it waits for pass 2 or a
  human decision.
- **`disqualified.jsonl`** - the audit trail: every rejection with category,
  reason, and quoted evidence. Downstream skills never read this file; the
  client conversation about "why did the list shrink" starts here.

Because disqualified rows are physically absent from `records.jsonl`,
**downstream skills need no changes** - they read the forwarded file exactly
as they always have.

The `qualification` object on every row:

```json
{"qualification": {
  "verdict": "disqualified",
  "dq_category": "acquired",
  "reason": "Operates as a division of a larger vendor",
  "evidence": "https://example.com - 'Example is now part of BigCo'",
  "flags": [],
  "pass": 1,
  "confidence": 90}}
```

**The uncertain gate.** After judging, report the counts and ask one question:
"Qualification complete - N qualified, M uncertain, K disqualified. Forward
the uncertain ones too? (yes/no)" - with the uncertain list summarized so the
choice is informed. Never forward them silently; never drop them silently.

**Run summary.** Close every run with: total in · qualified / uncertain /
disqualified · DQ breakdown by category · flags raised · and **downstream
spend avoided** (disqualified count × the per-company cost of the chain's paid
steps) - the gate's ROI, stated every time. In standalone mode with no cost
sheet available, say so and ask for a per-company figure rather than invent
one.

## What never to do

- Never delete a record - every row lands in exactly one of the three files.
- Never disqualify on uncertainty, missing data, or a label alone.
- Never qualify a company in the client's own product category.
- Never judge prospects before the brief exists and has been approved.
- Never let a calibration correction go unrecorded in the brief.
- Never end a run without the summary and its spend-avoided line.
