---
name: audit-usage
description: >
  Reads the execution trail the `audit` hook writes into `.claude/audit-usage/` and
  consolidates it across runs — billable tokens per skill and agent, duration, failure
  rate, permissions granted, and which report to open next. Answers "how many tokens has
  this project spent so far", which no single report answers. Explicit invocation only.
argument-hint: "[empty for the consolidated view | last | <skill or agent> | <report name fragment>]"
disable-model-invocation: true
allowed-tools: Read, Bash(java:*), Bash(ls:*), Bash(grep:*)
model: sonnet
effort: low
---

## Consolidated trail

!`java "${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/ArchHook.java" audit summary 2>&1`

---

Everything below reads. This skill never writes into `.claude/audit-usage/` and never
edits project code — the trail is written by `ArchHook.java audit`, at `Stop`, and by
nothing else.

Answer in English, the language of the reports themselves, so the consolidated view and
the per-run report read as one document. Reports and ledger rows written by an older
hook are in Portuguese (`✅ sucesso`); quote them as they are, never translate a number or
a status out of them. Reports written before decision 0134 also carry a cost in USD; quote
it only from that report, never as a figure of the trail.

## When the block came back empty

The trail is off: `.claude/audit-usage/` does not exist, and `audit summary` prints
nothing at all. That is the switch, not a failure. Say so, and give the two commands that
turn it on — creating the directory is enough, the hook is already wired in
`.claude/settings.json`:

```bash
mkdir -p .claude/audit-usage
printf '.claude/audit-usage/.state/\n' >> .gitignore
```

Then stop. Do not create the directory yourself: switching a versioned audit trail on is
the user's decision, not a side effect of asking what it holds.

If the block says `closed runs: 0`, no run has **finished** yet. Any report listed
under `⏳ No ledger line` is from a run in progress — report it as such and say the
ledger line is written only when the run closes.

## What the block already did

`ArchHook.java audit summary` reads `history.jsonl` (one line per top-level run) and
`nodes.jsonl` (one line per skill or agent that run chained) and does the arithmetic:
totals, spend per piece without double counting, failure rate, and the reports worth
opening. The aggregation is Java on purpose — the ledgers grow without bound, and
injecting them raw would cost tokens on every read and leave the sums to you.

**Never recompute a number the block printed, and never read the `.jsonl` files to
re-derive one.** Your job is rendering and judgment, not arithmetic.

What the block's vocabulary means:

- **Piece** — a skill (`📘`) or an agent (`🤖`) of this project. Plugin skills and runtime
  agents are not recorded.
- **Origin** — `user` typed `/<skill>`; `model` invoked the piece on its own, with no
  run open.
- **Model** — the model the run billed on, or a comma-separated list when a subagent ran
  on another one. `—` means the run was recorded before the column existed, not that the
  model is unknown. It is the first thing to read before comparing two runs of the same
  pipeline: the trail counts tokens only, and a token weighs more on a larger model — on
  the bill and on the plan — so the same token count is not the same spend.
- **root · nested · preloaded** — the piece opened its own run; it was chained
  inside another run; or it was loaded through an agent's `skills:` frontmatter (no
  tokens of its own — they are its agent's).
- **own tokens** — a piece's own spend. A run's total minus its chained pieces is
  the root's own; that is why the per-piece bars add up to the totals instead of
  exceeding them.
- **Calls** — tool calls counted from the transcripts' `tool_use` blocks, attributed to
  pieces like the tokens. `—` means the run was recorded before the column existed.
- **Peak** — the largest single request a piece sent (input + cache read + cache write):
  how much context one turn carried. An absolute number: never turn it into a percentage
  of a context window you would have to state from memory.
- **Plan windows** — how many runs of a piece fit a plan's 5-hour and weekly windows, as
  if nothing else ran: the Pro budget in `.claude/audit-usage/plan-limits.json` × the plan's
  multiplier ÷ the piece's mean billable tokens, capped by the window's hours ÷ its mean active
  duration. Model-blind, like every number of the trail.
  `budget` or `time` says which limit binds. Max 5x and 20x are multiples of Pro on 5 hours,
  the only multiplier Anthropic publishes; Max weekly has no column. A root row counts the
  whole run, what typing that command spends; a `(chained, own)` row only that piece's share.

## Procedure

### 1 · Route on the argument

| Argument | Do this |
|---|---|
| empty | § 2 — consolidated view |
| `last` / `último` | § 3 for the `most recent` report the block names |
| a skill or agent name (`new-feature`, `java-spring-boot-developer`, …) | § 2 reduced to that piece's line, then § 3 for its newest report: `ls -1t .claude/audit-usage/*--<name>.md` when it ran as a root; otherwise the newest `run` of its line in `grep '"skill":"<name>"' .claude/audit-usage/nodes.jsonl` — a chained piece's report is its parent's |
| any other text | treat it as a fragment of a report filename (`ls -1t .claude/audit-usage`); § 3 for the single match. Two or more matches: list them and ask which |

### 2 · Consolidated view

Present the block, in its order, keeping its tables and the `text` bar chart intact —
bars are proportional to billable tokens, not to duration, which is wall-clock and
includes time the user spent thinking. Then add what the block can't:

1. **One line of reading** above the tables — where the tokens went, in words.
2. **Where it went** — from the `Where the pieces spent` block, the piece whose calls
   are dominated by one tool, or whose peak stands out from the rest. Name the tool and
   the number; that is what points at the step to trim.
3. **Health** — name the piece with the worst failure ratio. A piece that fails
   repeatedly is a bad spec, not bad luck.
4. **What to read next** — the single most relevant report, and the exact
   `/audit-usage <fragment>` that opens it.

If the plan windows say `not configured`, say so and point at
`.claude/audit-usage/plan-limits.json` — `{"pro": {"five_hour_tokens": <n>, "weekly_tokens": <n>}}`,
the billable tokens the person saw a Pro window hold (the audit's total when `/usage` reached
100%). Never suggest a budget: Anthropic publishes none, and one written from memory looks as
authoritative as a measured one. Never convert anything to a currency either: the trail prices
nothing, and a rate written from memory is wrong the day after it changes.

### 3 · Single run

`Read` the `.md` file. It is already a finished, icon-rich report — **do not re-render
it and do not paste it back in full.** Summarize in at most six lines: what was run, the
outcome, its billable tokens, the longest step, where it spent (from `🔎 Where the run spent`:
the dominant tool, the costliest turn, the peak context), and anything that deserves
attention (`⏳ in progress`, compaction incidents, permissions added, repeated tool
failures — quote the error's first line the report already redacted, never more).
Then give the path so the user can open the whole thing.

Point out `⏳ in progress` when you see it: it means the run never closed — the session
was killed, or it is still open right now.

## What this skill will not do

- **Never edits or deletes anything under `.claude/audit-usage/`.** Pruning old reports
  is the user's call; if they ask, show the command and let them run it.
- **Never prices the trail.** The numbers come from `audit summary`, in tokens; a cost
  computed from them needs a rate, and a rate written from memory is wrong the day after it
  changes while looking exactly as authoritative as a correct one. Asked for money, point at
  the runtime's own `/cost` for the session (decision 0134).
- **Never reads `.state/`.** Those are the hook's open append-only logs; the rendered
  `.md` is the readable form.
- **Never quotes a redacted value.** The reports blank credential-shaped text on the way
  in. If something still looks like a live secret in a report, say so and point at
  `.claude/schemas/extensions.json`'s `audit.redact` block — a pattern is missing there.

## Why this is a skill, and why the hook ignores it

The hook already answers "what happened in **this** run", and `audit summary` does the
sums across runs. Nothing turns that into "which piece is eating the budget, and which
report should I open" — judgment over data, routed by an argument, which is a procedure,
not a norm and not enforcement.

`audit-usage` is one of the skills the trail does **not** record — the observers: its
class, `observer` in `skill_classes` of `.claude/schemas/extensions.json`, declares
`audited: false`, and `arch-doctor` sits in the same class. Without that, reading the trail would append a report about reading the
trail, and every later read would be mostly reads.

Invoking it still **closes** whatever run is open, and that is the useful half: within a
single session a report stays stamped `⏳ in progress` until something ends the run, so
asking for the report is what finalizes it.

`arch-adopt` is never recorded either — fixed in its own class override. Any other piece
can be switched per project in `.claude/audit-usage/audited.json` (`{"skills": {"<name>":
false}, "agents": {}}`), the one file of `.claude/` the project owns and `/arch-adopt` never
overwrites; `doctor`'s `Audit overrides` line validates it.

Runs on `sonnet` with `effort: low`: `audit summary` already did the sums, and what is
left is ranking and rendering (`@.claude/decisions/0080-procedural-skills-on-sonnet.md`).

## Contract

- **Class:** observer — the territory is `skill_classes.observer` in
  `@.claude/schemas/extensions.json`, and it is **empty**: this skill writes no file. The
  reports under `.claude/audit-usage/` are written by the `audit` hook, not by whoever reads
  them. `ArchHook.java guard` enforces it.
- **Reads** — the output of `ArchHook.java audit summary`; `.claude/audit-usage/*.md`;
  `.claude/audit-usage/nodes.jsonl` only to find the report of a chained piece
- **Writes** — nothing
- **Handoff** — none. Terminal skill: it reports and stops
