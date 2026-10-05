---
name: cyclotic
description: |
  Checks how well a Linear cycle is prepared. Reports per-person load in
  working days against available days, tickets with no estimate, tickets
  nobody is assigned to, oversized tickets that need splitting, work that
  did not finish last cycle, on-call rotation cost, and how groomed the
  backlog behind the cycle is. Invoke when the user says "cyclotic",
  "cyclotic prep", "cyclotic prep next", "cyclotic review", "cyclotic init",
  "cyclotic configure", "cyclotic for" a person's name, "cyclotic show
  cards", "cyclotic list tickets", "cyclotic explain" a person's name, or
  adds "-v" or "verbose" to any of those. Also invoke when the user asks
  whether a cycle or sprint is ready, who is over or under capacity, what
  carried over from last cycle, which tickets still need estimates, how the
  backlog looks going into planning, what is in the cycle and at what sizes,
  or how one person's load adds up. Read-only against Linear.
license: MIT
compatibility: |
  Requires Linear MCP installed and authenticated. Optional: incident.io MCP
  for on-call rotation lookup. Without it, rotation days are not deducted and
  the footer says so.
metadata:
  author: xornivore
  version: "1.0.0"
---

# cyclotic

Read a scoped slice of a Linear workspace and report how well a cycle is
prepared. Two modes: `prep` asks how well a cycle about to be worked **is**
prepared, while there is still time to change it. `review` asks how well the
cycle that just closed **was** prepared, and what it left behind.

Read-only against Linear. The only file this skill writes is its own config
under `~/.config/cyclotic/`.

## Install

```bash
npx skills add xornivore/skills@cyclotic --agent claude-code -y
```

Requires Linear MCP:

```bash
claude mcp add linear --transport sse https://mcp.linear.app/sse
```

On-call deduction additionally requires incident.io MCP, which is optional:

```bash
claude mcp add incident-io --transport http https://mcp.incident.io/mcp
```

Without it the report still runs, no rotation days come off anyone's available
days, and the footer says rotations were not checked — see
[ingest.md](./references/ingest.md).

## When to use

Invoke when the user:

- Uses an explicit phrase: `cyclotic`, `cyclotic prep`, `cyclotic prep next`,
  `cyclotic review`, `cyclotic init`, `cyclotic configure`.
- Adds a person filter: `cyclotic prep for avery`, `cyclotic review for avery`.
- Asks for detail: `cyclotic prep -v`, `cyclotic show cards`,
  `cyclotic list tickets`, `cyclotic explain chen`, `cyclotic why chen`.
- Asks a planning question: "is this cycle ready", "who is overloaded this
  sprint", "what carried over from last cycle", "which tickets still need
  estimates", "is the backlog groomed enough to plan from", "show me the
  tickets with their sizes", "how does Chen's load add up".

Do not invoke for:

- Writing to Linear. This skill never creates or edits issues, and never
  changes estimates or assignees.
- Judging a person's output. See [hard rule 5](#5-judge-the-plan-never-the-person).
- Velocity trends, estimate-accuracy tracking, or anything that needs a
  person's history across several cycles.

## Mode routing

Parse the user message into a mode plus an optional person filter:

| User phrasing | Mode | Target cycle |
| --- | --- | --- |
| `cyclotic prep` | prep | active cycle |
| `cyclotic prep next` | prep | next upcoming cycle |
| `cyclotic prep for avery` | prep, filtered | active cycle |
| `cyclotic review` | review | most recently completed cycle |
| `cyclotic review for avery` | review, filtered | most recently completed cycle |
| `cyclotic init` | setup | — |
| `cyclotic configure` | setup (alias of `init`) | — |

Bare `cyclotic` with no mode word routes to `prep`.

Three modifiers compose with any mode above. Each has its own layout in
[verbose.md](./references/verbose.md), loaded only when one is present:

| Modifier | Phrasings | Adds |
| --- | --- | --- |
| verbose | `-v`, `--verbose`, `verbose`, `in detail` | ticket inventory and per-person arithmetic, after the normal report |
| inventory | `show cards`, `list tickets`, `list cards`, `with sizes` | the ticket inventory alone |
| explain | `explain avery`, `why avery`, `break down avery` | one person's arithmetic alone |

So `cyclotic review -v` is a verbose review and `cyclotic show cards for next`
lists the next cycle's tickets.

Match the person filter on first name or full name, case-insensitively,
against the config roster. When one first name matches two roster members,
ask which one — never guess. When nothing matches, exit with a one-line
message listing the roster. Never fall back to an unfiltered run.

## Pipeline

When invoked in any non-setup mode, do these in order:

1. **Resolve scope.** Read `~/.config/cyclotic/GROUP.toml`, where GROUP is the
   working-group name. When no config exists and the session is interactive,
   route to the init flow ([init-flow.md](./references/init-flow.md)). When no
   config exists and the session is non-interactive, exit with
   `no scope configured; run "cyclotic init"` and stop.
2. **Ingest.** Run every Linear and incident.io read in one phase per
   [ingest.md](./references/ingest.md), and land the results in a fact sheet
   ([assets/factsheet-template.yaml](./assets/factsheet-template.yaml)).
   Cycle dates and working days come from Linear on every run, never from
   config.
3. **Compute capacity.** Pure arithmetic over the fact sheet per
   [capacity.md](./references/capacity.md). No queries.
4. **Fire flags.** Evaluate each flag against the fact sheet per
   [flags.md](./references/flags.md).
5. **Render.** Emit sections in the order set by
   [presentation.md](./references/presentation.md). Plain text only. When the
   run carries a verbose, inventory, or explain modifier, also load
   [verbose.md](./references/verbose.md).
6. **Footer.** State every blind spot accumulated during ingest, one line
   each, and only when true.

Never query Linear or incident.io after step 2 finishes
([hard rule 3](#3-never-re-query-after-ingest)).

## Hard rules

### 1. Read-only against Linear

Every Linear MCP call is a read. The only file this skill writes is
`~/.config/cyclotic/GROUP.toml`, and only from `init` or `configure` after
showing the rendered result and getting a yes.

Every flag needs human judgment — the right estimate, who takes the project,
how to split an oversized ticket. There is no mechanical fix to offer, so a
write path would add risk and buy nothing.

Correct: report that `ENG-201` has no estimate.

Wrong: set `ENG-201` to `M` because the sibling tickets are `M`.

**Audit:** no Linear MCP write tool appears in any run; no `Edit` or `Write`
targets a path outside `~/.config/cyclotic/`; no `Bash` call mutates the
user's repos.

### 2. Never run unscoped

No config plus an interactive session routes to the init flow. No config plus
a non-interactive session exits with `no scope configured; run "cyclotic init"`.
Never enumerate the workspace.

Correct: `list_issues` carrying `team` from config, or an explicit project-id
set derived from config.

Wrong: `list_issues` with no team and no project, to "see what is there."

**Audit:** every ingest query carries either a team filter or an explicit
project-id set derived from config.

### 3. Never re-query after ingest

When rendering needs a fact that is not in the fact sheet, that is an ingest
bug. Fix it in ingest rather than reaching for another query.

This holds after the report too. Keep the fact sheet for the rest of the
conversation and answer follow-up questions from it — it carries every ticket's
project, status, timestamps, and day value, which is far more than any layout
renders. Answer in a sentence or a few rows rather than re-rendering the report.

A question the fact sheet cannot answer is a **new run**, not a new query. Name
the mode that would answer it and offer to run it.

Correct: asked mid-conversation "what project is `ENG-233` in?", answer from the
fact sheet.

Correct: asked "what did Chen finish last cycle?" during a `prep` run, say the
run holds only the active cycle and offer `cyclotic review`.

Wrong: querying the previous cycle mid-conversation to answer it, which mixes
two ingest passes in one thread with nothing marking the seam.

**Audit:** [presentation.md](./references/presentation.md),
[capacity.md](./references/capacity.md),
[flags.md](./references/flags.md), and
[verbose.md](./references/verbose.md) contain no instruction to call Linear or
incident.io MCP.

### 4. Unestimated work never reads as spare capacity

Linear counts a ticket with no estimate as one point. This skill does not — it
contributes zero days and is reported as unknown. A load figure computed over
unestimated tickets understates reality, and rendering it bare invites the
reader to hand that person more work.

For any person holding unestimated tickets, render load with a trailing `+`,
suppress the signed delta, and put the count in the notes column. Their verdict
is never a bare `UNDER` and never `full`: below available it is `UNDER?`, and at
or above it, `OVER` — unknown work can only push a full cycle further over.

Correct: `Chen   6.0d+   10.0d           UNDER?   3 unestimated`

Correct: `Dara  14.5d+   10.0d           OVER     2 unestimated`

Wrong: `Chen   6.0d    10.0d    -4.0   UNDER`

Wrong: `Avery 10.0d+   10.0d            full     1 unestimated`

A ticket sized `-` (Linear's explicit zero estimate) is **sized**, not
unestimated. It contributes zero days and triggers none of this.

**Audit:** for any person whose `unestimated` count is above zero, the
rendered load ends in `+`, no signed delta appears on that row, and the
verdict is not a bare `UNDER`.

### 5. Judge the plan, never the person

Flags describe tickets, load, and sizing. Statements about the plan are in
scope. Verdicts about a person are not.

Correct: `Dara's cycle holds 14.5d against 10.0d available.`

Wrong: `Dara is overcommitted.` / `Dara is slow.` /
`Dara completed 58% of their estimate.`

No scores, no percentages of a person's output, no ranking of people against
each other, no tracking of an individual across cycles. `review` keeps
completion totals at team level so there is no per-person figure to rank.

Without this rule a capacity tool turns into a performance-review instrument.
It is also the rule that constrains this skill's main feature, which makes it
the one most likely to get quietly dropped. Do not drop it.

**Audit:** grep **rendered output** for a roster member's name adjacent to any
of `slow|behind|underperform|overcommitted|%`. Any hit outside a day-count
context is a violation. Run this against a report, never against this file —
the `Wrong:` lines above are deliberate counter-examples and will match.

### 6. State blind spots once

The footer names, in one line each and only when true: rotations not checked;
tickets excluded from day totals for having no estimate; the backlog query
truncated at the page cap; roster names that never resolved to a Linear user;
carried-over work the cycle's own totals imply but that cannot be attributed
to a named ticket.

A reader who is not told about a gap assumes there was none.

Correct: `rotations not checked (incident.io MCP not installed); available
days may be overstated.`

Wrong: rendering a full capacity table with no note, when no rotation data
was fetched at all.

**Audit:** when `oncall.schedules` is empty or incident.io MCP is absent, the
footer contains the rotations-not-checked line.

### 7. Plain text only

Output renders as markdown. No ANSI escapes, no emoji, no image export, no
palette, no theme, and no `[render]` config section. Signal is carried by
words, structure, and column alignment.

Tables use markdown table syntax. Use fixed-width blocks only where column
alignment carries meaning, such as the capacity table.

**Audit:** rendered output contains no `\x1b[` sequence and no character in
the Emoji property range.

## Reference index

| Pipeline step | Files pulled |
| --- | --- |
| Init flow (interactive) | [init-flow.md](./references/init-flow.md), [assets/config-template.toml](./assets/config-template.toml) |
| Ingest | [ingest.md](./references/ingest.md), [assets/factsheet-template.yaml](./assets/factsheet-template.yaml) |
| Capacity math | [capacity.md](./references/capacity.md) |
| Flags | [flags.md](./references/flags.md) |
| Render | [presentation.md](./references/presentation.md) |
| Render, when verbose or `show cards` or `explain` | [verbose.md](./references/verbose.md) |

All references are one level deep from `SKILL.md`.

Fixtures for checking the arithmetic and flag conditions without a live
workspace live under `tests/fixtures/`. They are agent-verifiable scenarios,
not an automated suite — see [flags.md](./references/flags.md) for the
expected verdicts.

## Design history

Design spec:
[`2026-08-03-cyclotic-design.md`](../../docs/superpowers/specs/2026-08-03-cyclotic-design.md).
