---
name: delivery-stats
description: "Collect delivery statistics for a finished epic and every ticket under it: tokens by model, cache efficiency, estimated cost, subscription window and code volume."
disable-model-invocation: true
---

# Delivery stats

**Objective:** After an epic and its child tickets are done, report what the delivery actually cost —
as a standalone HTML dashboard plus a short summary in this session.

Read-only. It reads local session transcripts, this repository's git history and the issue tracker,
writes one HTML file, and sends nothing anywhere.

## Route

The tool ships with the harness at `.harness/reporting/delivery_stats.py`. If it is absent, this
project did not install the capability that provides it — say so instead of reimplementing it here.

```bash
python .harness/reporting/delivery_stats.py --repo . --epic <номер> \
  --html .harness/.sandboxes/reports/delivery-stats/epic-<номер>.html
```

Add `--json` when the developer wants the raw numbers rather than the summary. `--rates <file>`
overrides the rate card; `--base <ref>` overrides the diff base.

Save a versioned baseline after a completed, comparable epic, then pass it when reporting the next
one. The comparison appears in both the terminal/JSON report and the HTML dashboard:

```bash
python .harness/reporting/delivery_stats.py --repo . --epic <baseline-epic> \
  --save-baseline .harness/.sandboxes/reports/delivery-stats/epic-<baseline-epic>.baseline.json
python .harness/reporting/delivery_stats.py --repo . --epic <current-epic> \
  --baseline .harness/.sandboxes/reports/delivery-stats/epic-<baseline-epic>.baseline.json \
  --html .harness/.sandboxes/reports/delivery-stats/epic-<current-epic>.html
```

## Procedure

1. **Resolve the epic.** The developer names it. If they name a child ticket instead, run it on that
   ticket anyway — the tool treats a ticket with no sub-issues as a scope of one — and say that is
   what you did.
2. **Check the rate card before promising money.** Cost appears only when
   `.harness/reporting/rates.json` exists and prices the models that were used. There is no built-in
   price list, by design: prices depend on the plan and change over time. If it is missing, copy
   `.harness/reporting/rates.example.json`, tell the developer to fill in their own rates, and report
   everything else meanwhile — do not invent a number, and do not quote a price you did not read from
   that file.
3. **Save or compare a baseline when useful.** Save only a completed epic that is comparable to the
   one being assessed. The comparison preserves `exact` or `estimated` attribution for each provider
   on both sides; a delta appears only when telemetry exists for both sides.
4. **Run the tool** and write the dashboard under `.harness/.sandboxes/reports/delivery-stats/`.
5. **Report the summary** in this session: tickets closed, code volume, tokens by model, cache split,
   cost if priced, and the path to the HTML.
6. **Carry the caveats through, do not smooth them over.** They are the point of the report:
    - Claude Code work is attributed **exactly** — every transcript record carries its branch.
    - Codex work is attributed **approximately** — its logs carry no branch, only a working directory
      and a timestamp, so its totals cover this repository inside the epic's activity window and can
      include unrelated work from the same period. Always say "оценка" when quoting it.
    - Anything the tool could not source reads `нет данных`. Repeat it as missing; never round it to
      zero and never fill it from memory.
    - An ADR counts as added only when the commit that first added the file belongs to one of the
      epic's pull requests, so a squash-merged pull request undercounts. Mention it only if the
      developer asks why a number looks low.
7. **Offer to attach it.** The dashboard is a local file; posting it to the epic is the developer's
   call, not an automatic step.

## Boundaries

Do not edit the transcripts, the rate card or the git history to make a number look better. Do not
add prices, models or tickets the tool did not report. If the tool exits non-zero, show its stderr
and stop — a partial statistic presented as complete is worse than none.
