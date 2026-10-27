---
name: scan-data-sources
description: >
  Sweep for sources that could answer an indicator and vet each on licence and
  coverage. Use when data is thin or a note needs rescanning.
disable-model-invocation: false
---

# Scan Data Sources

Finding out what could answer an indicator is the expensive half of targeting
work, and almost none of it survives the session that did it. This skill makes
the sweep repeatable and makes its output durable: a scan ends by writing a
research note that the next session reads instead of starting again — including
the sources it ruled out, which is the part nobody writes down and everybody
re-derives.

A scan is not the same as a check. The stored checks on a note confirm that what
we found still holds. Only a scan can tell you whether something better has been
published since. Run one when a note reports `rescan_due`, when an indicator's
coverage is embarrassing, or when a funder question depends on a figure the
current source answers thinly.

## Inputs

| Source | Artifact | Used for |
|---|---|---|
| The request | indicator, or the gap that prompted the scan | what to sweep for |
| Connect Labs MCP | `targeting_research` | what was already ruled in or out, and when |
| Connect Labs MCP | `targeting_indicators` | current coverage and which methods answer |
| Connect Labs MCP | `targeting_admin_levels` | the geography the source would have to match |

## Products

- A research note written back via `targeting_research_write`, carrying the
  verdict, the alternatives table, and `scanned_now: true`
- `<phase>/scan-data-sources_summary.md` — the sweep, for a human reader
- Optionally a loader in `connect_labs/labs/indicators/sources/`, when a source
  is adopted

## Process

1. **Read the existing note before searching anything.** `targeting_research`
   for the indicator. A prior scan's rejected list is the most valuable thing in
   it: re-litigating a source that was ruled out on licence wastes the scan.
   Note its `scan_age_days` — what you are doing is refreshing that clock.
2. **State what would have to be true for a new source to win.** Coverage of
   more units, a more recent vintage, a count where we only have a rate, or a
   licence that unblocks something. A scan without this becomes a list of links.
3. **Sweep the four families that actually publish at this scale.** Household
   surveys (DHS, MICS); UN and agency series (IGME, WHO GHO, UNICEF SDMX);
   modelled geospatial surfaces (MAP, WorldPop, GHSL/DEGURBA, Weiss et al.
   accessibility); and humanitarian aggregators (HDX HAPI). Most gaps are filled
   by the third family, because only a modelled surface has a value everywhere.
4. **Check the licence before the data.** This is the step that gets skipped and
   it is the one that invalidates the work. Find the actual licence page and
   quote it — do not infer a licence from a site being free to browse. A
   non-commercial licence (IHME, WHO GHO) means the source can serve as an
   external cross-check but must not be carried into a commercially-framed
   deliverable.
5. **Test the access path for real before believing it exists.** Fetch one
   country, or one boundary, and look at the numbers. An OGC endpoint that
   answers GetCapabilities may still refuse GetCoverage; an API may return a
   styled image instead of the data band. A source is not available until you
   have held a value from it in your hand.
6. **Validate against something external.** A new source's national total
   against a published figure — WHO, a national statistical office, the World
   Bank. Agreement within a few percent is the evidence that adoption is safe;
   a large gap is not automatically disqualifying, but it has to be named and
   carried forward into the methodology.
7. **Decide the aggregation before adopting.** A count sums; a rate needs a
   declared weight. A rate aggregated by area mean lets empty land vote and is
   frequently indefensible — if there is no population grid to weight by, say so
   and consider deferring rather than shipping a weak number that looks strong.
8. **Write the note back** with `targeting_research_write` and
   `scanned_now: true`. Include every source considered with its verdict
   (`adopted`, `rejected`, `candidate`) and the *why*. Give the note checks that
   would fail if the conclusion stopped holding.

## MCP Tools Used

**connect_labs** (remote HTTP, PAT auth)
- `targeting_research` — built
- `targeting_research_write` — built
- `targeting_indicators` — built
- `targeting_admin_levels` — built

## Writing checks that are worth having

A check earns its place by being able to fail. Four kinds exist:

- `coverage` — how many units carry the indicator at a level. Passes if coverage
  has since *grown*, because a backfill is not drift.
- `value` — the figure you reasoned from, for one country, within a tolerance.
- `source` — whether a named source still supplies the indicator at all.
- `measure` — whether the indicator still has the shape you assumed. This is the
  one that catches the nastiest drift: prose reasoning about a rate after
  somebody redefined it as a count.

Record the figure your argument *rests on*, not a figure that happens to be
handy. If your note says "MAP's national total tracks WHO", the check is MAP's
national total.

## Verdicts, and what they oblige

- **adopted** — in use. Say how it is aggregated and what it was validated
  against.
- **rejected** — say whether it failed on licence, coverage, vintage, or
  quality, and never imply a licence rejection is a quality judgement. IHME is
  excluded because its terms exclude us, not because it is worse.
- **candidate** — good, and blocked on something nameable. Say what would
  unblock it, so the next scan can pick it up rather than rediscover it.

## Mode Behavior

- **Auto:** run the sweep, write the note, notify the admin group with the
  verdict and any adopted source's validation gap.
- **Review:** present the alternatives table and the recommendation for approval
  before adopting a source or writing a loader.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-08-29 | Initial version — sweep procedure, licence-first vetting, verdict vocabulary, check design | ACE team |
