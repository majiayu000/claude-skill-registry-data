---
name: 00-gtm-router
description: >
  Plan and run the full API-first GTM chain - the orchestrator (step 00) that turns
  an ICP description plus optional budget, volume, and urgency into the right
  discovery -> qualification -> extraction -> signals -> judgment -> email-resolution sequence, with
  per-step cost estimates and rationale, then executes it skill-by-skill after a
  go-ahead. Use whenever a request spans more than one chain step or the user asks
  which tools or skills to use, in what order, or what it will cost - e.g. "plan a
  campaign for this ICP", "build me a list end to end", "we're targeting X, what's
  the play", "what would it cost to go after Y", "new client kickoff", "run the
  whole chain" - or when they hand over an ICP or client brief and want prospects
  with verified emails out the other side. Also use when partial data exists (a
  company list without signals, contacts without emails) to pick the right entry
  point mid-chain. For a true cold start - "first campaign", "never run a
  campaign", "no CRM", nothing to analyze yet - route to run-first-campaign,
  the packaged workflow that sits above the chain. For a single named step alone
  (just scrape one site, just find one email), use that component skill directly.
---

# GTM Router - the orchestrator (00)

Every other skill in this chain wraps a tool. This one wraps the decision: given an
ICP, which chain do you run, in what order, at what depth, and what will it cost.
Tool-routing ("use Firecrawl for scraping") is table stakes; this skill does
methodology-routing - the shape of the ICP picks the discovery path, volume picks
the extraction depth, evidence type picks the signal source, every discovered list
passes the qualification gate (01-icp-qualify) before credits are spent on it, and
everything funnels through judgment (05) before anyone writes an email. Two
model-judgment layers bracket the paid steps: the gate decides who is worth paying
to know more about, the judge decides what to say to them.

The router itself spends nothing. All credits are spent inside component skills,
each of which keeps its own spend gates. The router's job is to make the spend
deliberate: plan first, estimate honestly, execute only after a go-ahead, and
checkpoint between steps.

## Inputs

- **icp_description** (required) - who the client is targeting, in plain English.
- **icp_context** - what the client sells, to whom, and what pain it removes (2-4
  sentences). 05-signal-builder cannot judge without it, so collect it during
  planning, not four steps in. If it's missing, ask once.
- **exclusions** (optional, ask once) - competitors, current customers,
  do-not-contact domains. The gate (01-icp-qualify) enforces them for free;
  discovery skills also apply them as filters where supported.
- **budget_ceiling**, **target_volume**, **urgency** (optional) - shape the plan.
  Missing values don't block planning: assume, label the assumption, and show the
  math so the user can correct it.

## Start where the data runs out

Discovery is only step one if the user has nothing. Route to the first step whose
input is missing:

| User already has | Enter the chain at |
|---|---|
| Nothing yet - no list, no CRM, first campaign ever | run-first-campaign - the packaged cold-start workflow (context -> source of record -> gate -> rank -> drafts -> sheet, owner approval between steps) |
| Nothing but an ICP description | Discovery (01-prospeo-discover, 02, or 04-theirstack discover, by shape below) |
| Example companies to find more of | 01-prospeo-lookalike - the list is **seeds**, not targets |
| A target company list (domains) | 01-icp-qualify first, then 03/04 on the survivors |
| A list with scrape/signal data | 05-signal-builder |
| Named contacts missing emails | 06-resolution-email-person |
| Signals + verified emails | email-writer (the chain is done) |

**A domain list is ambiguous input - resolve it before routing.** The same CSV
routes two opposite ways: a *target* list gets enriched (03/04), a *seed* list
gets expanded (01-prospeo-lookalike). "Here are our 40 closed-won accounts" or
"our competitor's customers" is almost always seeds; a conference attendee
export or a purchased list is almost always targets. When the framing is
genuinely unclear, ask - routing seeds into 03 scrapes the customers they
already have.

Inherited data passes through untouched - the chain contract is additive
(`headless-gtm-shared/CONVENTIONS.md`): every record keeps its upstream fields, keyed by
normalized `domain`.

## Step 1 - classify the ICP shape

| Shape | You'll recognize it by | Discovery route |
|---|---|---|
| **b2b-saas** | Companies a B2B database can filter: industry + size + geo + funding; buyers have titles | 01-prospeo-discover from filters; 01-prospeo-lookalike from seed companies |
| **vertical-smb** | Local or owner-operated: studios, salons, clinics, gyms, restaurants, trades, venues - Maps-addressable | 02-apify-maps-discover |
| **hiring-defined** | The ICP is an event: "companies that just hired X" or "have an open X req" | Open reqs: 04-theirstack-jobs discover, directly. Past joins: 01 superset + 04 filter (see below) |
| **web-scattered** | No database covers them and they're not on Maps: directories, marketplaces, event listings, niche communities | 03-firecrawl-research extract mode on the source sites |

If the shape is genuinely ambiguous, ask one question - "could you find these
companies in a B2B database by industry and size, are they local businesses you'd
find on Google Maps, or are they defined by something that just happened?" - then
commit. Don't run a full interview; one answer plus labeled assumptions beats five
questions.

## Step 2 - assemble the chain

Default chain per shape. Deviate when the modifiers below say to, and say why in
the plan.

| Shape | Chain |
|---|---|
| b2b-saas | 01 (discover from filters, or lookalike from seeds) -> 01-icp-qualify -> 04-crustdata -> 03 (selective) -> 05 `icp_shape=b2b-saas` -> 06 |
| vertical-smb | 02 -> 01-icp-qualify -> 03 -> 05 `icp_shape=vertical-smb` -> 06 |
| hiring-defined | 04-theirstack-jobs discover (open reqs), or 01 bounded superset -> 01-icp-qualify -> 04-theirstack-jobs check / 04-crustdata-signals -> 05 `b2b-saas` -> 06 |
| web-scattered | 03 extract (directories) -> 01-icp-qualify -> 04 where coverage exists -> 05 -> 06 |

The calls that make these chains work:

- **The gate runs before any paid step - and twice.** 01-icp-qualify is free
  (in-session judgment), so it sits between discovery and the first
  credit-spending step in every chain: pass 1 judges fit on discovery fields,
  and only the survivors in its `records.jsonl` get enriched, scraped, or
  resolved. After 03/04 add evidence, its pass 2 re-judges the uncertain rows
  and can demote qualified ones - schedule it before 05 ranks anything. The
  plan hands the gate what it needs: the client profile (icp_context), the
  exclusion list, and the per-company downstream cost from unit-costs.md, so
  its spend-avoided line is a real number instead of a question back to the
  user. Discovery filters match labels; the gate judges fit - don't loosen the
  gate to keep volume up, fix the discovery filters instead.
- **04 is a layer, not one skill.** 04-crustdata-signals covers what already
  happened (funding, joins, headcount); 04-theirstack-jobs covers what's open
  right now (job reqs). Both write the same additive records - 05 merges by
  domain - so run both when the play needs both kinds of evidence. The
  theirstack sizing count (~1 credit against a whole domain list) prices the
  open-req overlay before any commitment, so adding it to any chain is cheap
  to check.
- **01 is a layer too - filters vs seeds.** 01-prospeo-discover builds a list
  from firmographic criteria; 01-prospeo-lookalike builds one from example
  companies. Route on what the client can actually articulate: a described ICP
  ("Series B fintech, 50-200, US") goes to discover, and example logos ("more
  like these 30 closed-won accounts") go to lookalike, which is the better
  starting point when the client's real pattern is tacit - they recognize a good
  fit but can't name the filters. Lookalike's Mode 2 closes the loop: it reads
  the 25 closest matches for their shared pattern, builds an ICP from it, and
  hands that to discover for the broad search. Use Mode 1 when the matches
  themselves are the deliverable, Mode 2 when the seeds are a means to a bigger
  list. One caution worth planning around: a niche seed set often classifies
  under a huge parent industry, so a Mode 2 ICP of industry + size + geo can
  balloon into six figures - the specificity lived in the keywords. Sanity-check
  the count and re-add the recurring keyword before exporting.
- **b2b-saas scrapes selectively.** 04-crustdata's structured signals (funding,
  headcount, hires) cover database-tracked companies well. Scrape (03) only the
  slice that needs page-level evidence - the top decile by 04 signal strength, or
  accounts where 04 came back empty. Scraping all of a 2,000-domain list burns
  credits on companies judgment will score 3/10 anyway.
- **vertical-smb skips 04-crustdata.** Funding/headcount vendors barely cover
  owner-operated businesses; the website and Maps listing are the signal source,
  so the scrape is not optional - it's most of the evidence 05 will get. If the
  client's angle is hiring, a 04-theirstack sizing count is the cheap way to test
  whether postings coverage exists before assuming it doesn't.
- **hiring-defined routes by evidence type.** Open reqs: 04-theirstack-jobs
  discover mode searches "companies with an open X req" directly - its free
  blurred count returns the job AND company yield before any spend (then 1
  credit per job returned), so no superset is needed. Past joins ("just hired
  X"): nothing searches that directly, so build a bounded firmographic superset
  with 01, then filter by 04-crustdata-signals `recent_hires`. Enriching an
  unbounded superset is the dominant cost in this shape - cap the superset in
  the plan, and run the cheaper filter first.
- **web-scattered starts from a proposed source of record.** Propose the 2-3
  places these companies are already listed - a licensing registry, professional
  college, trade association directory, or marketplace, with Maps (02) as the
  general fallback - and confirm with the user before extracting. Don't open by
  asking them to supply URLs: proposing the source is the plan's job, confirming
  it is the user's. 03's "Directory and registry extraction" turns the confirmed
  source into a company list, and the chain proceeds normally from there.
- **Judge before you resolve - by default.** 05's ranking decides which accounts
  deserve per-contact resolution spend, and the signal work is what makes the
  email worth sending. Flip to resolve-first (06 straight after discovery,
  signals only on the emailable set) when the client will email every resolvable
  account regardless of angle, or when per-domain signal spend clearly exceeds
  per-contact resolution spend at the expected coverage. Either order is
  defensible - the plan states which one it picked and why.
- **Free gates shrink paid steps.** 01-icp-qualify is the institutional one -
  always on, right after discovery. Beyond it, look for any other free call that
  disqualifies domains before a paid pass: a free employee scan that shows who
  even has the target function, a count-only size check, a cached prior run.
  Halving a per-domain credit step beats optimizing anything downstream of it.

Modifiers, applied in this order:

1. **Volume** sets extraction depth: under ~200 domains, 03 standard mode; 200-2K,
   standard on the signal-bearing slice and minimal elsewhere; over 2K, minimal
   mode or top-decile-only scraping. Deep mode is for short high-value lists.
2. **Budget ceiling** caps volume: compute max affordable records from
   `references/unit-costs.md` and say plainly if the target volume doesn't fit.
3. **Urgency** trades depth for speed: minimal scrape mode, default enrichment
   windows, skip nice-to-have overlays. It never skips 05 - unjudged lists produce
   the generic copy this whole chain exists to avoid.

**Pilot first, always.** Propose a 100-200 record pilot end-to-end before full
volume (smaller for small targets). Experiments beat opinions: a pilot validates
per-unit cost, the qualification pass rate, hit rates, and signal quality before
the budget is committed. Full volume on the first pass needs an explicit reason.
The pilot also carries the gate's calibration rounds, so the full run inherits an
already-corrected qualification brief.

## Step 3 - estimate cost and time

Read `references/unit-costs.md` - don't estimate from memory - and build per-step
line items: `volume x unit cost`, as a range. Every step after the gate prices on
**post-qualify volume** (discovered x pass rate); the pass rate is a labeled
assumption until the pilot trues it. Flag which numbers are plan-dependent
(credit prices vary by vendor plan) and which steps dominate the total. Estimate
wall-clock time from the rate limits in the same file; enrichment RPM, not scraping,
is usually the bottleneck on large runs.

## Step 4 - present the plan, then stop

```markdown
## Campaign plan: {one-line ICP}
**Shape:** {shape} - {one sentence why}
**Entry point:** {where and why, if not discovery}
**Volume:** {target} · **Budget:** {ceiling or "none given"} · **Pilot:** {size}

| # | Step | Skill | In -> out | Est. cost | Est. time |
|---|---|---|---|---|---|

**Total:** {range} · **Dominant cost:** {step and why}
**Why this chain:** {2-4 bullets - only the non-obvious calls}
**Alternate:** {1-2 lines - what changes if budget or volume moves}
**Assumptions / gaps:** {labeled assumptions; anything to confirm}

Run the pilot ({n} records, ~{cost})?
```

Present the plan and wait. Don't start executing in the same turn - the gap between
plan and execution is where the user corrects the ICP, the budget, or the angle,
and a correction after step 1 has already spent credits is a refund nobody issues.

## Step 5 - execute, checkpointing between steps

On go-ahead:

1. Create a run folder at `./runs/<run-id>/` in the working directory
   (timestamp+slug, e.g. `2026-07-21-00-router-yoga-gta`): the approved
   `plan.md` plus `manifest.json` tracking
   `{step, skill, run_dir, status, est_cost, actual_cost}` per step.
2. Run each step by its own SKILL.md. Every component skill writes into that
   same `./runs/` root under its own step-prefixed run-id; record each path in
   the manifest. Hand the previous step's `records.jsonl` to the next step by
   explicit path - never a reformatted copy, never a guessed sibling folder.
3. Plan approval covers the spends listed in the plan. When a component skill asks
   to confirm a spend within its plan line, proceed; anything above the line, or
   any step not in the plan, stops and asks. 01-icp-qualify's own user gates stay
   live either way - the qualification brief gets approved before judging on a
   first client run, and uncertain rows are never forwarded silently. Those are
   judgment gates, not spend gates; plan approval doesn't answer them.
4. Checkpoint after each step: actual cost and record count vs estimate. Stop and
   re-plan if actual unit cost reaches 2x the estimate, output count lands under
   half of expected, or a step returns empty. A qualification pass rate far below
   the assumption is a discovery-filter problem - tighten the filters and re-run
   discovery rather than loosening the gate. Report the numbers either way - the
   estimate-vs-actual gap is how the unit-costs file gets better.
5. After 06, close out: final `records.jsonl` path, total spent vs estimated,
   count at each stage (discovered -> qualified -> judged -> resolved), the
   gate's spend-avoided total, and the handoff - top signals per account plus
   fallback go to email-writer, which needs the icp_context collected at the
   start.

## When a step can't run

A missing skill or API key doesn't invalidate the route. Keep the step in the
plan, mark it **manual**, name the tool and what to do by hand (e.g. "no
CRUSTDATA_API_KEY - pull funding/headcount manually for the top 50, or add the key
and run 04"). Degrade the plan, don't silently reroute around the methodology.

## Scope boundaries

| Not this skill | Use instead |
|---|---|
| A true cold start - no list, no CRM, first campaign ever | run-first-campaign, the packaged cold-start workflow |
| One named step ("scrape acme.com", "find this person's email") | The component skill directly |
| Qualifying an existing list, nothing downstream | 01-icp-qualify directly |
| Judging an existing evidence bundle | 05-signal-builder |
| Writing the emails | email-writer |
| Classifying replies after send | reply-triage |
| Picking tools for a stack the chain doesn't cover (ads, events, content) | Out of scope - say so |

## References

- `references/decision-tree.md` - the full routing logic as a readable doc:
  shapes, worked examples, the resolution waterfall. Shareable on its own.
- `references/unit-costs.md` - per-step unit costs, rate limits, estimation
  formulas, worked examples. Read before any estimate; update after any run where
  actuals diverged.
- `../headless-gtm-shared/CONVENTIONS.md` - the chain contract: JSONL records, `runs/`
  folders, additive fields, domain as key.
