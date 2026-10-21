---
name: daily-report
description: >
  Use for the daily report, morning brief or dashboard, what needs attention today, or a cross-wiki what's-new; also to redesign the brief. Plain digest: use /llm-wiki:wiki-report.
argument-hint: "[date|focus|setup]"
---

# Daily-report — the profile-aware morning synthesis

Writes the day's report pages, a narrow set of wiki promotions, and — only
with an operator at the keyboard — the first-run seeds. Judgment-heavy: for a
top-tier model.

Scope: `$ARGUMENTS` — a date to report as, or a focus. Default: today,
everything since the last report. `setup` alone runs the interview instead
(§8); words after it make the whole a focus. A job's scheduled run is
`<args…> ticket=<id> stage=routine`, the words before `ticket=` its date or
focus, with nobody to answer. Under `ticket=` a leading `setup` is never the
interview: the run reports, noting that setup needs an operator.

One run is one op: `daily-report`, opened in §1 and closed at the end of §7,
or on the setup path `grill` alone (§8). Never `git commit`: the close
commits what the run wrote, by hand or at a scheduled run's landing
(`llm-wiki-ops reference operations`).

Dream analyzes; this skill formats. It never needs operator input mid-run —
open questions land in the report for the next `/llm-wiki:grill`.

## This wiki

!`llm-wiki-ops whereami skill=daily-report || echo "whereami failed with exit $?: this directory may not be a wiki — stop and tell the user"`

Every command below acts on this wiki. Asked to run against a different one?
`llm-wiki-ops reference cross-wiki` says how.

## 1. Compose the overlay, then open the run

```sh
llm-wiki-ops policy get daily-report daily-report-setup
```

The `daily-report` overlay extends this procedure — section plan, tone,
cross-wiki list, tighter promotions. Both scopes, wiki first, later text
winning; an empty answer is stock alone.

**Setup pending** — a `daily-report-setup` row came back: this wiki still
runs on the overlay its preset seeded. With an operator at the keyboard, go
to §8, which is where this wiki's own answers replace it and the only place
the marker is retired. With nobody to answer, do what the row says: follow
the seeded overlay, leave the marker exactly as found, and say in the report
that one pass with a person answering would tailor it. The marker pattern is
`llm-wiki-ops reference policy-overlays`.

The read writes nothing, so it needs no op. Bound for §8 — `setup` by hand,
or the row with an operator — open nothing here: that run ends at §8's
close. Otherwise:

```sh
llm-wiki-ops op open daily-report
```

## 2. Fix the window

```sh
llm-wiki-ops op latest daily-report filter=outcome:ok
```

The window opens at that run's commit. A `partial` or `failed` run HOLDS the
window — the days behind its shortfall are still unreported — so the span
keeps growing until an `ok` covers it.

`found: false` → open at the newest run of any outcome:

```sh
llm-wiki-ops op latest daily-report
```

Still nothing → cover the last three days. The marker never comes from
report filenames on disk.

## 3. Gather — read-only

A failed input is a one-line note in the report, never an abort.

```sh
llm-wiki-ops git changed research sources filter=since:<the marker>
llm-wiki-ops op since filter=since:<the marker>
llm-wiki-ops page lint
llm-wiki-ops page ls filter=under:wiki/profile
llm-wiki-ops page ls filter=under:research/reports
llm-wiki-ops page ls filter=under:research/channels
```

- **Channel ledgers** — a channel job's `dest` is
  `research/channels/<slug>`, one page per day. Read the ledger pages inside
  the window and nothing else: never a sibling raw capture
  (`llm-wiki-ops reference channel-ledger`). With an operator at the
  keyboard, `llm-wiki-ops jobs ls` also names a channel job not
  pulled here, which has no ledger for the gap days — note and skip. A
  scheduled run cannot list jobs, so it reports the ledgers it found.
- **This wiki's ops digest** — the newest `research/reports/` page inside the
  window, read with `llm-wiki-ops page read <path>`. The `ops-morning` job
  `requires` a `wiki-report` run within the day, so under the schedule there
  is always one to read; a by-hand run may find none — note the gap and
  continue. Take it as given, never re-derive it.
- **What the wiki did** — `op since` is the runs, `git changed` the files.
- **Lint delta** — `page lint` against the previous report's `lint:`
  frontmatter.
- **Operator profile** — `wiki/profile/`, the lens for everything else.
  Absent: proceed impersonally and note that `/llm-wiki:grill` would
  personalize the wiki.
- **Cross-wiki what's-new — OPT-IN, off by default.** Runs only for wikis the
  overlay names. Per named wiki, `llm-wiki-cli machine config get wikis.<name>.path`,
  then read its `wiki/log.md` and recent reports with your own file tools.
  Never fan out across the registry, never write to another wiki, and never
  quote one the overlay did not name. A denied peer read under a confined run
  is noted and skipped.

## 4. Synthesize through the profile

What moved the operator's goals; what needs attention today and why, in their
terms; what is coasting; what contradicts the profile's current picture.
Surface contradictions — never resolve them. Dream owns that.

## 5. Promote — narrow, and every write logged

May write exactly: timeline entries on **existing** pages; dated or pointer
facts on **existing** pages; entity stubs for genuinely new recurring actors.

```sh
llm-wiki-ops page edit wiki/entities/<Name>.md --stdin
llm-wiki-ops page create title="<Name>" dest=wiki/entities type=entity --stdin
```

Never: topic or concept pages, restructuring, contradiction resolution,
staleness downgrades, `sources/`, staged-page frontmatter, or another wiki.
Each promotion gets a `report`-prefixed `wiki/log.md` bullet and appears in
the report's Promotions section. The overlay may tighten this list, never
widen it.

## 6. Write the markdown record

`wiki/reports/YYYY-MM-DD.md`, the durable record:

```sh
llm-wiki-ops page create title="2026-09-05" dest=wiki/reports type=report --stdin
llm-wiki-ops page edit wiki/reports/2026-09-05.md --stdin
```

Frontmatter carries `date`, `dashboard:` — a relative link to the sibling
HTML — and `lint: {errors: N, warnings: N}` in that inline form. It also
carries the lead's first sentence as `lede`, and `attention`: the items the
body's attention section names, at most five, most pressing first, as ONE
JSON list:

```sh
llm-wiki-ops page edit wiki/reports/2026-09-05.md 'lede=<the lead’s first sentence>' \
  'attention=[{"title": "…", "detail": "…", "severity": "attention", "source": "Gmail · clients", "page": "wiki/…/….md", "action": "…"}]'
```

`severity` is `info`, `attention` or `failing`; `source` is the channel or
page the item came from; `page` is a wiki-relative path that exists, or
omitted; `action` is the one next step. Write each for the operator, the way
the body says it. Both values are single-quoted, so an apostrophe in either is
written `’`. Nothing needs attention: clear the key with `attention=`, or a
same-day rerun keeps the earlier list.

Body, empty sections omitted: the lead in three to five sentences; what
needs attention; channel summaries; cross-wiki findings; what the wiki did,
with the lint delta; promotions with their log lines; open questions (§9).

If the newest `dream` run is older than a day or absent —
`llm-wiki-ops op latest dream` — say so in a header note. A same-day rerun
overwrites. `wiki/index.md` gets ONE directory-level line for
`wiki/reports/`, never a line per day.

## 7. Author the day's brief

Run `llm-wiki-ops reference daily-report/setup` first (it prints `references/setup.md`) — the
template, the three hard rules, and who owns which concern.

`wiki/reports/YYYY-MM-DD.html` is standalone HTML, authored fresh from that
day's story. `wiki/reports/_template.html` supplies the design language and
is a working sample, never a form. Absent, with an operator at the keyboard:
seed it from `references/dashboard-template.html`. With nobody to answer do
NOT seed — render from that reference copy read-only and note the missing
template.

Content bar: written for the operator in their terms; every actionable item
carries why it matters, a next step, and a copyable draft where a reply IS
the next step; every claim carries its receipt; no wiki operations on the
glass; self-contained.

Then close the run's one op, the last thing it posts:

```sh
llm-wiki-ops op close daily-report outcome=ok summary="daily report 2026-09-05: <one line>"
```

`outcome` is what moves the window: `ok` only when it all landed — the
report, its promotions and the brief — `partial` when some of it did — say
what fell short — `failed` when none did.

Then, only when `whereami` reports `sandbox.jail: none` — a sandboxed session cannot
reach the search service, and the runner indexes after this session exits:

```sh
llm-wiki-ops search index
```

Fail-open, and it indexes the markdown only. Never index the HTML.

## 8. Setup — the one interactive mode

`setup` as the argument, or §1 finding the `daily-report-setup` marker with
an operator at the keyboard. Follow
the interview `llm-wiki-ops reference daily-report/setup` prints (`setup.md`): inventory what is connected, ask what they
care about seeing each morning, cut sections nothing feeds, personalize the
template, fold the section plan and tone into the overlay on the operator's
yes, retire the marker when §1's read returned it — a redesign on a wiki
that already ran setup got no row and skips that step — and close under the
`grill` op, never `daily-report`, which would advance the window cursor.
The run ends at that close; the report waits for the next invocation.

## 9. Open questions — the grill loop

Plain bullets, optionally naming the profile page each would fill
(`- Is the Q3 pricing goal still alive? → goals`). Grill reads this section of
the newest report as top-priority gaps. When a question persists across
reports, print the instruction in the report and on the brief: **type
`/llm-wiki:grill`**.

## Never

- Write outside the report's markdown and HTML, the interactive-only first-run
  seeds, the promotion list, and the `wiki/log.md` and `wiki/index.md`
  entries.
- Read a raw channel capture, or touch another wiki in any writing way.
- Resolve contradictions, merge topic or concept pages, or downgrade stale
  facts — dream owns all three.
- Ask the user anything mid-run; §8 is the sole exception.
