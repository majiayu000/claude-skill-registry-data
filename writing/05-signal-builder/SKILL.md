---
name: 05-signal-builder
description: >
  Rank a prospect's outbound signals and pick the campaign approach (Pain-led /
  Value-led / Segment fallback) - the judgment layer (step 05) of the API-first
  GTM chain. Takes scraped website markdown (03-firecrawl-research), vendor
  signals like funding / headcount / recent hires (04-crustdata-signals), or
  just a URL or pasted content, and emits ranked provenance-backed signals: the
  exact quotable sentence, source URL, 1-10 score, and recommended approach.
  Use whenever the user wants to score, rank, or prioritize prospects or
  accounts, decide outreach angles, or asks "which of these should we email
  first", "what's the angle for this account", "rank these signals", or "turn
  this scrape into campaign angles" - and whenever a records.jsonl or
  enrichment output is ready for judgment before writing copy. Scoring lives
  here; scraping belongs to firecrawl-research, vendor pulls to
  crustdata-signals, email finding to resolution.
---

# Signal Builder - the judgment layer (05)

Signal vendors sell facts ("company X raised", "company Y is hiring"). Scrapers sell
pages. Neither tells you whether a fact is a Pain-led trigger, a Value-led opening, or noise for
this particular client. That call - which finding matters, how much, and what to do
with it - is this skill. It runs on model judgment alone: no API key, no credits spent.

Two ways in:

| You have | Mode |
|---|---|
| One prospect - a URL, pasted content, or a content file | A - Single prospect |
| Chain output - records.jsonl and run folders from 01/02/03/04 | B - Batch over records |

Both modes need `icp_context`, and both produce the same two outputs: a human report
and chain records.

## icp_context and icp_shape

`icp_context` (required): what the client sells, who they sell to, and what pain it
removes. 2-4 sentences is enough. If it's missing, ask once - accept a pasted
description or a file path. A signal only exists relative to this context: a hiring
spree is a 9 for one client and noise for another.

`icp_shape` picks the calibration catalog:

| Shape | Prospects look like | Catalog |
|---|---|---|
| `b2b-saas` | funded companies, title-based orgs, tech stacks, exec moves | `references/signal-types-b2b-saas.md` |
| `vertical-smb` | local or owner-operated - studios, venues, clinics, restaurants, trades | `references/signal-types-vertical-smb.md` |

If the user doesn't pass a shape, infer it from icp_context (end-customers that are
local, Maps-addressable businesses → `vertical-smb`; otherwise `b2b-saas`) and state
which one you picked. Read the catalog before scanning - it carries the per-shape
scoring adjustments, not just examples. For a vertical neither catalog fits, see
`references/calibration-guide.md`.

## Mode A - single prospect

1. Get content. Pasted or file content: use as-is. URL only: if the
   03-firecrawl-research skill is installed, run its standard mode and use the scan
   output; otherwise fetch the high-signal pages directly (homepage, /about, /careers,
   /pricing, /blog) with whatever fetch tool is available. List any page you couldn't
   get - a missing careers page is a coverage gap to report, not a zero signal.
2. Judge (method below) and write the report. If this prospect is part of a chain run,
   also emit a record (Mode B, step 3).

## Mode B - batch over chain records

`scripts/signal_io.py` is stdlib-only Python - no installs. Paths below are relative
to this skill's directory.

1. **Collect** - assemble one evidence bundle per domain from upstream outputs:

   ```bash
   python3 scripts/signal_io.py collect \
     --records path/to/03-run/records.jsonl \
     --records path/to/04-run/records.jsonl \
     --scrape-run path/to/03-run \
     --crustdata-run path/to/04-run \
     --out runs/2026-07-21-acme-batch
   ```

   `--records` takes any chain `records.jsonl` - 01, 02 (Maps), and 04 run
   folders all emit one.

   Every flag except `--out` is optional and repeatable; pass whatever upstream
   artifacts exist. Records merge by domain (upstream fields are kept, never
   overwritten). Output: `inputs/<domain>.md` bundles, `records_in.jsonl`,
   `tracker.json`, `meta.json`. Re-running collect is safe - done domains stay done.

   Bundles with no page content and no structured signals are flagged `thin` in the
   tracker. For a thin batch, run 03-firecrawl-research first; for 10 or fewer
   domains it's fine to fetch pages yourself as in Mode A and judge from that.

2. **Judge** each pending domain: read `inputs/<domain>.md`, apply the method below,
   write the signal JSON to a temp file, then:

3. **Emit** - validate and append to the chain output:

   ```bash
   python3 scripts/signal_io.py emit --run runs/2026-07-21-acme-batch \
     --domain acme.com --signals-json /tmp/acme-signals.json
   ```

   Emit enforces the record contract (fields, score range, approach enum, non-empty
   sentence and source), merges signals into the upstream record, appends to
   `records.jsonl`, and marks the domain done. On a validation failure it names the
   bad signal and rule - fix the JSON and re-emit. Re-emitting a domain replaces its
   record instead of duplicating it.

4. **Resume / finish**: `python3 scripts/signal_io.py status --run runs/<id>` shows
   done/pending. When all domains are done, write `runs/<id>/report.md` (per-domain
   report sections plus segment-level patterns you noticed) and point the user at
   `records.jsonl` - that file is what 06-resolution and the router consume.

For batches over ~100 domains, judge in passes of 25 and re-check score distribution
between passes (see the honesty threshold below) so drift doesn't compound.

## How to judge

Work one domain at a time with the shape catalog open.

1. **Pull candidates from every source.** Page content: careers/jobs, blog/news,
   pricing, integrations, footer tech clues. Structured blocks: funding rounds,
   headcount and department growth, recent hires, job postings. Enrichment beats
   inference - if a structured block says 12 recent hires, don't re-derive headcount
   from prose.
2. **A structured signal is a fact, not a verdict.** "18 recent hires" becomes a
   signal only when the roles map to the pain the client solves. That mapping is the
   judgment. The same goes in reverse: don't discard a boring-looking fact before
   checking it against icp_context.
3. **Score each candidate 1-10** against the anchors below, adjusted by the catalog.
4. **Assign an approach** per signal (table below).
5. **Provenance, every signal.** Web signal: quote the sentence verbatim from the page
   and cite the page URL. Structured signal: state the fact exactly as the data
   supports it (round, amount, date; name, title, start date) and cite
   `vendor:section:domain`, e.g. `crustdata:funding:acme.com`. A finding you can't
   source isn't a signal - drop it or report it as a gap.
6. **Prefer combinations.** Hiring for the role plus competitor friction outranks
   either alone. Write the combination as one signal: lead sentence and source_url
   from the strongest piece of evidence, the rest in `notes`.
7. **Cap at 5 signals, always end with a fallback.** Downstream copy uses the top 2-3;
   a 12-item list is unranked noise. If nothing clears a 3, say so plainly - the
   fallback is the campaign in that case.

## Scoring anchors

| Score | Means | Typical evidence |
|---|---|---|
| 9-10 | Switching intent or acute pain, now | competitor in place plus visible friction; active job post for the exact role the product replaces or augments; public complaint that maps 1:1 to the value prop |
| 7-8 | One strong behavioral signal | leadership hire in the relevant function; fresh funding aimed at the client's area; JD language describing the exact pain; negative reviews in the problem area |
| 5-6 | Problem-space evidence | adjacent tools in the stack; hiring around (not in) the function; growth or expansion straining the relevant process |
| 3-4 | Contextual fit only | right stage, size, or business model - no behavioral evidence |
| 1-2 | ICP match only | fallback territory |

Score honestly - downstream copy calibrates tone on the number, so an inflated 8 reads
as false familiarity in the email. If more than 40% of a batch scores 8+, re-check
those domains against the anchors before emitting more.

## Approach per signal

| Approach | Use when | Email shape |
|---|---|---|
| **Pain-led** | the signal names a specific, acute pain you can ask about | "Noticed [signal]. Teams in that spot usually deal with [pain]. Is that you?" |
| **Value-led** | you can hand over something genuinely useful tied to the signal before asking for anything | "Put together [artifact] for you - [insight]." |
| **Segment fallback** | moderate or contextual signals; every fallback | lead with the most common pain for the profile, ask if it resonates |

Signals scoring 8+ usually carry Pain-led. Pick Value-led only when a real artifact exists to
give (an audit, a teardown, a list), not a hypothetical one. 4 and under: Segment fallback.

## Output 1 - the report

One section per judged prospect. Keep this structure so reports stay comparable
across prospects and runs:

```markdown
## Signal Scan: {Company}
**URL:** {url} · **Shape:** {icp_shape}
**Summary:** {1-2 sentences: what they do, their situation, the most interesting finding}

### Signal 1: {Name} (Score: X/10)
**Detected:** {the factual finding}
**Implies:** {what their team is dealing with day to day}
**Approach:** {Pain-led | Value-led | Segment fallback}
**Angle:** {one sentence - the core message this signal enables}
**Source:** {url or vendor ref} - "{the quotable sentence}"
**Data points for copy:** {variable}: {value} · {variable}: {value}

### Signal 2: ... (highest score first)

### Fallback (Score: X/10)
**Assumption:** {most common pain for this profile}
**Approach:** Segment fallback
**Angle:** {one sentence}
```

Close the report with the handoff: top 1-2 signals plus the fallback are the campaign
set to pass to email-writer (or whatever writes the copy) - signal 1 drives the lead
campaign, the fallback drives the catch-all.

## Output 2 - the chain record

What 06-resolution and the router parse. One JSON object per domain in
`records.jsonl`: the upstream record with two added fields. Upstream fields
(`company`, `domain`, `person`, `filters_matched`, anything else) pass through
untouched.

```json
{"company": "Acme Corp", "domain": "acme.com", "person": null,
 "filters_matched": ["has_homepage", "has_careers", "Series A $18M"],
 "signals": [
   {"signal_type": "hiring-role-replaced",
    "signal_sentence": "You'll own supplier escalations across email, WhatsApp and phone.",
    "source_url": "https://acme.com/careers",
    "score": 9, "approach": "Pain-led",
    "evidence_date": "2026-07", "notes": "2 open Supply Chain Coordinator roles"}
 ],
 "fallback_approach": {"approach": "Segment fallback",
                       "angle": "Mid-market distributors usually drown in manual PO chasing"}}
```

Field rules (emit enforces them):

- `signal_type` - kebab-case; use the catalog's type name where one fits, free-form otherwise
- `signal_sentence` - the referenceable evidence: verbatim quote for web signals, faithful fact statement for structured signals
- `source_url` - `http(s)://` page URL, or `vendor:section:domain` for structured signals
- `score` - integer 1-10 · `approach` - `Pain-led` | `Value-led` | `Segment fallback`
- signals sorted by score descending, max 5; `evidence_date` and `notes` optional
- `fallback_approach` - always present: `{approach, angle}`

## Failure modes to avoid

- **Embellished quotes.** The signal_sentence for a web signal is copied from the
  page, not improved. If the finding is a composition ("3 roles in 30 days"), the
  composition goes in the report and `notes`; the sentence stays verbatim.
- **Generic signals.** "They're growing" is not a signal. "Posted 3 Supply Chain
  Coordinator roles in the last 30 days" is.
- **Inflated scores.** A 4/10 batch is useful information - it tells the client this
  segment needs a Segment fallback catch-all, not personalization theater.
- **Invented sources.** Never cite a URL you didn't see in the bundle or fetch. If
  coverage was thin, say which pages were missing instead.
- **Editing upstream fields.** The record is additive; you add `signals` and
  `fallback_approach`, nothing else changes.

## Scope boundaries

| Not this skill | Use instead |
|---|---|
| Scrape sites at scale | 03-firecrawl-research |
| Pull funding / headcount / hires from vendors | 04-crustdata-signals |
| Find or verify email addresses | 06-resolution-email-person |
| Write the actual emails | email-writer |

## References

- `references/signal-types-b2b-saas.md` - B2B SaaS calibration catalog
- `references/signal-types-vertical-smb.md` - vertical SMB calibration catalog
- `references/calibration-guide.md` - reply-gym format: calibrate a new vertical from classified reply data
