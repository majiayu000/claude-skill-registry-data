---
name: market-research
description: Conduct market research, competitive analysis, investor due diligence, and industry intelligence with source attribution and decision-oriented summaries. Use when the user wants market sizing, competitor comparisons, fund research, technology scans, or research that informs a business decision. Do NOT use for building the investor-facing documents themselves (investor-materials) or for campaign copy derived from the findings (marketing-campaign).
origin: ECC
---

# Market Research

Produce research that supports decisions, not research theater.

## When to use

- researching a market, category, company, investor, or technology trend
- building TAM/SAM/SOM estimates
- comparing competitors or adjacent products
- preparing investor dossiers before outreach
- pressure-testing a thesis before building, funding, or entering a market

**When NOT to use:**

- the deliverable is the deck, memo, or model — that is `investor-materials`; this skill feeds it
- the deliverable is campaign copy — that is `marketing-campaign`
- no sources are reachable (offline, no web access, paywalled). Research written from model
  memory is indistinguishable from fabrication and carries no evidence tag — say so and stop

## Inputs

Required before writing a single finding — **absent input = stop, never fill the gap from memory**:

1. **The decision the research serves.** "Should we enter X", "is fund Y a fit", "do we build or
   buy". Without a decision, the output is a summary, not research.
2. **Reachable sources.** Every important claim needs one. Use web search / Exa / vendor docs and
   record the URL and the retrieval date. A claim whose source cannot be opened is deleted or
   relabelled as an assumption.
3. **Internal facts, from the SOT** — for SkyyRose sizing or competitive positioning, product and
   price reality comes from `wordpress-theme/skyyrose-flagship/data/skyyrose-catalog.csv`, never
   from recollection.
4. **A stated as-of date.** Data ages; the reader needs to know how stale.

## Procedure

1. State the decision, then the questions that would change it.
2. Gather sources. For each mode, collect:
   - **Investor / fund diligence** — fund size, stage, typical check size; relevant portfolio
     companies; public thesis and recent activity; fit and non-fit reasons; red flags.
   - **Competitive analysis** — product reality (not marketing copy); funding and investor
     history if public; traction metrics if public; distribution and pricing clues; strengths,
     weaknesses, positioning gaps.
   - **Market sizing** — top-down from reports or public datasets, bottom-up sanity check from
     realistic acquisition assumptions, and an explicit assumption for every leap in logic.
   - **Technology / vendor** — how it works; trade-offs and adoption signals; integration
     complexity; lock-in, security, compliance, and operational risk.
3. Label every line as **fact** (sourced), **inference** (reasoned from facts), or
   **recommendation**. Append `(Source: <url or dataset>, <date>)` to every number as you write
   it, so the sourcing check below runs mechanically.
4. Include contrarian evidence and the downside case. A brief with no counterargument was not
   research.
5. Write the output in this structure: executive summary · key findings · implications · risks
   and caveats · recommendation · sources.
6. Run the Verification checks on the brief file before delivering.

# Verification

Run against the written brief. A check that errors on a bad path exits 2 — a dead gate, not a
pass (bug-230).

1. **Every number carries a source** — the check that separates research from assertion:

```bash
grep -nE '[0-9]+(\.[0-9]+)?%|\$[0-9]|[0-9]+(\.[0-9]+)?[BMK]\b' research-brief.md | grep -v 'Source:'
```

   **PASS:** exit 1, no lines returned. Acceptable labels include
   `(Source: <url>, <date>)` and `(Source: operator-supplied; unverified)` —
   an unlabelled number is deleted or relabelled, never left standing. `[repro]`

2. **Every cited URL actually resolves** — a citation that 404s is worse than no citation:

```bash
grep -ohE 'https?://[^ )]+' research-brief.md | sort -u | while read -r u; do
  printf '%s -> ' "$u"; curl -s -o /dev/null -w '%{http_code}\n' --max-time 15 "$u"
done
```

   **PASS:** every line ends in `200` (or a documented `301`/`403` for known paywalls, called out
   in the brief). Any `000` or `404` — remove the claim or find a live source. `[live]`

3. **The required structure exists** — a brief missing risks or a recommendation is a summary:

```bash
grep -ciE '^#+ .*(executive summary|key findings|implications|risks|recommendation|sources)' research-brief.md
```

   **PASS:** prints `6`. Fewer means a required section is missing — most often "risks and
   caveats", which is exactly the section that makes the brief falsifiable. The `-i` is
   load-bearing: without it the pattern never matches a `## Executive summary` heading and the
   check silently prints `0` for every input, which is a dead gate, not a finding. `[repro]`

Checks 1 and 3 were both proven able to fail before being trusted (rule 3) — see the worked
example for check 1, and check 3 was run against a brief with the risks section removed, which
printed `5` instead of `6` `[repro]`.
**A SKIP is not a PASS:** whether the recommendation actually follows from the evidence is a
human judgment no command grades — state it as open and name the decision-maker who closes it.

## Worked example

Real run, 2026-07-28. Brief drafted to the session scratchpad as `research-brief.md` with three
findings. First pass, the sourcing gate went **red** — proving it can fail:

```bash
$ grep -nE '[0-9]+(\.[0-9]+)?%|\$[0-9]' research-brief.md | grep -v 'Source:'
3:- Average luxury-streetwear AOV is $240
```

The other two lines already carried `(Source: ThredUp 2025 Resale Report)` and
`(Source: Morning Consult, 2025)` and were not returned. After relabelling the AOV line
`(Source: operator-supplied; unverified)` — the honest label, since no external source backed
it — the same command exits 1:

```bash
$ grep -nE '[0-9]+(\.[0-9]+)?%|\$[0-9]' research-brief.md | grep -v 'Source:'; echo "exit=$?"
exit=1
```

Both states observed this session `[repro]`. Note what the fix was: the number was **relabelled
as unverified**, not silently kept. That is the difference between the gate working and the gate
being gamed — and the AOV figure now carries `[inferred]` scope, so it cannot support a severity
claim in any downstream deck.

## Failure modes

| Failure | What it looks like | Rule |
|---|---|---|
| Numbers from model memory | a plausible market size with no citation | Indistinguishable from fabrication. Check 1 catches unlabelled numbers; a fabricated *label* is caught by check 2 |
| Dead citations | source URL 404s or was never opened | Check 2 `[live]`. Remove the claim or replace the source |
| Stale data presented as current | a 2019 report cited without a date | Always state the as-of date and flag stale data explicitly |
| Fact / inference / recommendation blurred | an inference reads as a finding | Label each line. `[inferred]` never carries severity (bug-287) |
| No counterargument | every finding supports the desired conclusion | Include contrarian evidence and the downside case, or the brief is advocacy |
| Summary instead of decision | reader still cannot act | Check 3 requires implications, risks, and a recommendation |
| Mechanical greens read as a full pass | "research verified" with no human judgment on the logic | A SKIP is not a PASS — name the open judgment and its owner |
| Internal facts from recollection | SkyyRose price or SKU quoted from memory | The catalog CSV is the SOT; plausible ≠ sourced (bug-096 shape) |

## Related skills

`investor-materials` (turning findings into deck/memo/model) · `marketing-campaign` (Phase 1
research brief) · `seo` (keyword and competitor search-visibility data)
