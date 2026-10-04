---
name: earnings-and-filings-teardown
description: Extracts the financially material content from 10-K, 10-Q, and 8-K filings and earnings call transcripts into a structured one page brief with a source location on every number. Triggers when someone asks to tear down a filing or earnings release, summarize a 10-K or 10-Q, pull KPIs guidance and risks from a transcript, or brief the CFO on what a company reported.
---

# Earnings and Filings Teardown

## When to use

Use when the office of the CFO needs the financially material substance of a public disclosure distilled fast and traceably.

- A competitor's or the company's own 10-K, 10-Q, or 8-K landed and needs a read.
- An earnings call transcript needs to be reduced to KPIs, guidance, and risks.
- Pre or post earnings prep, or an audit committee read ahead.
- A benchmarking or planning workstream needs clean, sourced inputs from a filing.

The signal is a filing or transcript in hand and a need for reported KPIs, segment detail, guidance, risks, capital actions, and one time items, each tied to where it was found.

## What it produces

A one page structured brief covering reported KPIs, segment and geography revenue, guidance and outlook changes, key risk factors, capital allocation actions, and notable accounting or one time items. Every extracted figure carries a source traceability tag (document, section, page or paragraph), and each section closes with a "so what for the CFO" line.

## Method

1. Identify the document and period. Record filing type (10-K, 10-Q, 8-K, or transcript), the issuer, the fiscal period, the filing date, and the comparable prior period the document itself uses.
2. Pull the income statement. Extract revenue, gross profit, operating income, net income, and EPS for the period and the stated comparable. Compute the period over period change for each: change = (current / prior) - 1. Tag each figure with its statement location.
3. Extract segment and geography revenue. From the segment footnote and MD&A, capture revenue (and segment profit if disclosed) by reportable segment and by geography. Confirm the segments sum to consolidated revenue and note any reconciling or corporate item.
4. Read MD&A for drivers. Capture management's stated reasons for the changes: volume versus price, mix, FX, acquisitions, and one time effects. Quote or paraphrase the driver and tag the source paragraph. Keep management narrative separate from your own inference and label any inference as such.
5. Capture guidance and outlook changes. Record forward guidance (revenue, margin, EPS, capex, free cash flow) and compare it to prior guidance where available: raised, lowered, reaffirmed, or initiated. Note the explicit assumptions management attached to the range.
6. Extract key risk factors. From the risk factors section (10-K) or updates (10-Q) and any forward looking caveats in the transcript, list the risks that are new, materially changed, or financially significant. Skip boilerplate that is unchanged from prior filings.
7. Capture capital allocation actions. Record dividends declared, buyback authorizations and amounts repurchased, debt issued or repaid, M&A, and material capex commitments. Tie each to its source: the cash flow statement, an 8-K item, or the transcript.
8. Flag accounting and one time items. Identify impairments, restructuring charges, tax true ups, changes in accounting policy or estimate, non GAAP adjustments, and other items that distort comparability. Note the dollar effect and whether it hits the reported or the adjusted figure.
9. Reconcile reported to adjusted. Where the company presents non GAAP measures, show the bridge from the GAAP figure to the adjusted figure so the size of each add back is visible, not buried.
10. Write the "so what." For each section add one line on why a CFO should care: a read through to the company's own plan, a peer signal, or a risk to monitor. Keep interpretation separate from extracted fact.

## Inputs

Gather before extracting:

- The actual filing or transcript text, or a verbatim excerpt of the relevant sections.
- The fiscal period and the issuer.
- Prior period guidance or financials if a comparison is wanted.

If a number is not in the provided document, do not supply it from memory. Mark it "not disclosed in source" and, if it matters, ask the user for the document that contains it. Every figure in the brief must come from the provided text.

## Output format

- Header: issuer, document type, fiscal period, filing date, and comparable period.
- Reported KPIs: small table with metric, current, prior, change percent, and source tag.
- Segment and geography revenue: table with source tags and a tie to total.
- Guidance and outlook: prior versus current versus direction, with stated assumptions.
- Key risk factors: bulleted, new or changed only, each tagged.
- Capital allocation: bulleted actions with amounts and source tags.
- Accounting and one time items: item, dollar effect, and comparability note.
- So what for the CFO: one line per section.

## Quality bar

- Every number carries a source tag: document, section, page or paragraph.
- Segment revenue ties to consolidated revenue, and any reconciling item is shown.
- Reported and adjusted (non GAAP) figures are kept distinct and labeled, with the bridge shown.
- Management narrative and your inference are clearly separated.
- Guidance changes are stated as direction versus prior, not just the new level.
- Nothing is recalled from outside the provided document; gaps are marked "not disclosed in source."

## Example

Input (hypothetical 10-Q excerpt): "Revenue was 1,200 (prior year 1,000). Americas 700, EMEA 350, APAC 150. We now expect full year revenue of 4,900 to 5,000, up from 4,700 to 4,800."

Brief, KPIs row: Revenue 1,200 vs 1,000, +20.0%, source: condensed income statement, p. 4.

Segment tie: 700 + 350 + 150 = 1,200, ties to total, source: segment footnote, p. 11.

Guidance: raised, new FY range 4,900 to 5,000 vs prior 4,700 to 4,800, source: MD&A outlook, p. 18.

So what: the top line beat is broad based and management raised the full year, a positive read for the category and a useful external marker for the company's own plan.
