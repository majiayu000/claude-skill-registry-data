---
name: run-first-campaign
description: >
  The packaged cold-start campaign workflow - takes an owner with no list, no
  CRM, and no outbound history from a plain-English business description to an
  approved campaign sheet in one supervised pass: business context, a proposed
  source of record (a public directory - registry, professional college, trade
  association, marketplace, Maps - for local or licensed businesses, or a
  firmographic pull - 01-prospeo-discover, 01-prospeo-lookalike,
  04-theirstack-jobs - for B2B), free ICP qualification, signal ranking, a
  drafted 3-email sequence, and a HubSpot-import-shaped CSV. Use when someone
  says "first campaign", "never run a campaign", "no CRM", "I need customers
  but have nothing to analyze", or wants outbound started from zero existing
  data. Nothing sends - the deliverables are drafts and files, and every paid
  step is cost-approved before it runs. For a campaign on an existing list or
  CRM data, use 00-gtm-router directly.
---

# Run your first campaign

The cold-start workflow: an owner or founder with no list, no CRM, and no
campaign history, taken from "here's my business" to an approved campaign sheet.
It chains existing skills in a fixed order with an explicit owner approval
between steps. Nothing in this repo sends email - the end state is a drafted
3-email sequence plus a campaign sheet (owner-readable Markdown and a
HubSpot-import-shaped CSV) the owner approves on screen.

Chain mechanics follow the router's conventions: each component skill runs by
its own SKILL.md, writes into `./runs/` under its own step-prefixed run-id, and
hands `records.jsonl` to the next step by explicit path.

## Step 1 - Business context

Check for `context/offer.md` and `context/icp.md`. If both exist, summarize
them in two sentences and confirm they still describe the business. If either
is missing, offer two paths: the closest vertical preset from
`reference/presets/` (fastest - adopt the archetype, then adjust it together)
or the full `gtm-context` interview. Write the result to `context/`. Wait for
the owner to confirm the context before anything else runs.

## Step 2 - Source of record

Where these buyers are already listed depends on the ICP. Read the confirmed
context and propose the matching source, by name:

- **Local, licensed, or physical-presence businesses** (contractors, clinics,
  dealerships, brokerages, restaurants) live in a public directory - a
  licensing registry, a professional college, a trade-association "find a
  member" directory, a marketplace, with 02-apify-maps-discover as the fallback
  when no structured source exists. These extract via 03 (below).
- **Firmographic B2B** (software, agencies, funded or hiring companies) has no
  directory to scrape - the buyer is defined by what the company is. Pull the
  list instead: 01-prospeo-discover for an ICP-filtered pull,
  01-prospeo-lookalike when the owner can name a few good-fit companies, or
  04-theirstack-jobs when a hiring signal defines the buyer.

Offer 2-3 candidate sources with a one-line reason each; the owner picks or
corrects. Don't open by asking the owner to supply URLs, and don't pull or
extract anything before they confirm the source and the cost.

On confirmation, run the matching source skill. For a directory, that is
03-firecrawl-research extract mode with the listing-row schema (03's "Directory
and registry extraction" section). Firecrawl bills extraction by tokens
(1 credit = 15 tokens), so cost scales with page size: extract the first
listing page alone, read the actual charge, and use it as the per-page figure
before extracting the rest. For a firmographic pull, that is the discovery
skill's own metered call. Either way, state the cost estimate first, follow
the source skill's own confirmation thresholds, report the result (N records,
credits used), and wait for an acknowledgment before Step 3.

## Step 3 - Qualify, free

Run 01-icp-qualify on the extracted records against the confirmed context. This
step costs nothing. Report the counts - N qualified, M uncertain, K
disqualified - and ask 01's uncertain-gate question: forward the uncertain rows
too, or hold them? Wait for the answer.

## Step 4 - Rank

Run 05-signal-builder with the vertical-smb calibration on the qualified set:
targets ranked, one angle per account, verbatim provenance on every signal.
Present the top targets and the segment pattern; wait for the owner to approve
the top segment before anything gets written.

## Step 5 - Write

Run email-writer for the approved segment: a 3-email sequence built on the top
signals and the fallback angle. Drafts only - present them for edits and wait
for "drafts approved" before building the sheet.

## Step 6 - Campaign sheet and final approval

Run 07-campaign-sheet on the final `records.jsonl`: `campaign-sheet.md` (who to
contact first and why, signal and approach per row) plus `campaign-sheet.csv`
with HubSpot default import headers. Present both and stop - nothing is
send-ready until the owner approves the sheet on screen.

Optional branch, only when the owner wants send-ready addresses: run
06-resolution-email-person on the approved rows (cost-gated - state the
estimate first), then regenerate the sheet with the email column filled.

## Approval gates (must hold)

- **Never send anything.** Nothing in this repo sends email. If asked to "just
  send it", say that plainly and point at the approved sheet and drafts.
- **Never spend above the approved estimate.** Every paid step re-states its
  estimate before running; anything above the approved line stops and re-asks.
- **Never auto-progress between steps.** Every step ends at an owner wait.
- A missing API key stops the affected step: name the layer being skipped and
  offer the no-key path (a smaller manual pull, or qualify / rank / write on
  whatever data already exists).

## Output

End the run with a one-paragraph recap: the source of record used, N found ->
M qualified, the top 3 targets with one-line angles, the sheet path, and
elapsed time from context confirmation to sheet.

## Reference

- `reference/presets/` - vertical context presets (offer.md + icp.md pairs)
- `reference/gotchas.md` - failure patterns from real cold-start runs
- `reference/examples/happy-path.md` - one full worked run, from preset to sheet
