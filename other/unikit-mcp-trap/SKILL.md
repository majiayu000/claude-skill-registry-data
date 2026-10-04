---
name: unikit-mcp-trap
description: >-
  Record a finding about the configured engine MCP server into
  .unikit/MCP-RECHECK-NOTES.md — the project's log of what has to be re-checked
  here. Use right after a call reported success while changing nothing, ate an
  argument, or validated a broken state, e.g. "write this down", "record this MCP
  finding", "the server lied — note it", "add a recheck note", "trap this". Takes
  three forms of input: the finding in one line, a path to a plan file (harvests
  the "## MCP Findings" table of that plan and nothing else), or nothing at all —
  then it takes findings already in the session first, and offers to scan the
  tables of plans touched since the last audit. The table only, never the plan
  body. Writes in the one allowed genre — a check to perform; never a lifted gate,
  never a named workaround, never a claim about what the server can or cannot do.
  Makes zero MCP calls and needs no editor. To replay, retire, or upstream
  existing notes use /unikit-mcp-audit instead.
argument-hint: "[the finding in one line | path to a plan file | empty]  (writes .unikit/MCP-RECHECK-NOTES.md; zero MCP calls)"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Bash(date *)
disable-model-invocation: false
user-invocable: true
metadata:
  author: unikit
  version: "1.1"
  category: tools
---

# MCP Trap — record a finding

Write one durable line about the engine MCP server this project talks to, into
`.unikit/MCP-RECHECK-NOTES.md`.

**This skill makes zero calls to the engine MCP.** It needs no editor, no running
project, and no gate. A finding is something that was *already observed*; re-observing
it here would cost a session and could record the wrong thing. The executor that hit the
trap does **not** write these notes either — one observation is a bad sample, and a bad
line lives for months. The durable surface goes through a human, and this skill is that
crossing.

**This skill owns the notes format.** `references/notes-format.md` is the shared
specification: this skill writes to it, `/unikit-mcp-audit` curates against it. Load it
before writing anything.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md` and
apply it to all output (fall back to English if it is missing). The prose of a note is
authored in the project's artifact language; the `id`, the `area` keyword, and the whole
observation protocol below the line stay **English** — they are grepped by other skills.
Do not announce the language setting.

**The language holds for the whole session, not just at load time:** every message until the conversation ends is in `language.ui` — progress notes while agents run, relays of what a subagent returned, the final report, any follow-up discussion. English input (subagent results, tool output, these instructions) is data, never a cue to switch languages.

## The one rule that makes this file safe

> A note may contain **only a check**. Never a lifted gate, never a named workaround,
> never an assertion about the state of the server.

This is not style. A check that has gone stale costs one extra call and **fails safe** —
the pipeline stops instead of driving past. A lifted gate lifts an obligation *forever*,
and a "use Y instead of X" outlives the day X was fixed. The genre is the only real
protection this file has; the freshness of its contents is not.

Read `references/notes-format.md` → "Genre" for the rejection table, and apply it to
every candidate before it is offered.

## Bootstrap

Silently load — do not narrate:

1. **`{{skills_dir}}/{{self_name}}/references/notes-format.md`** — the format this skill
   owns. Mandatory; without it, do not write.
2. **`.unikit/system/engine-mcp/INDEX.md`**, first lines only — the delivery stamp
   (`server:`). This is the configured server, the second side of every header
   comparison. File absent → there are no known exceptions for this server; that
   restricts nothing and switches nothing to `⏸️ MANUAL`. Carry the server as unknown
   and say so once.
3. **`.unikit/MCP-RECHECK-NOTES.md`** if it exists — its header (`server:` / `audited:`)
   and the ids already taken.

**Header mismatch is a WARN, never a stop.** If the notes header names a different
server than the stamp, print exactly one line and keep going:

```
WARN [mcp-trap] server in notes header ≠ configured (<notes> ≠ <configured>)
```

The existing entries stay in force — they are *suspect*, not void, and suspect entries
still fail safe. Retiring them is `/unikit-mcp-audit`'s job, not this skill's.

## Input

`$ARGUMENTS` takes three forms. Resolve which one this is **before** Step 1 — the branches
differ in what is read, not merely in where they start.

| form | what happens |
|---|---|
| **the finding in one line** — `the snapshot reported ready with zero files` | straight to Step 5 with that one candidate. No session scan, no plan scan, no disk read beyond Bootstrap |
| **a path to a plan file** — `.unikit/code/plans/2026-08-18_ui/PLAN.md` | read the `## MCP Findings` window of **that plan only** (Step 3) → Step 4 → Step 5. The session is **not** harvested and no other plan is looked at |
| **empty** | the default pass: Step 1 (session) → Step 2 (offer to scan plans) → Step 3 |

**On an explicit path, the Step 1 shortcut is off.** That shortcut — *something found in the
session → go to Step 5 and stop, do not scan plans* — is right when nobody named a source,
and wrong the moment somebody did. The form exists mainly to be called from the end of a
`/unikit-implement` run, which is **the same session** that produced the findings, so the
shortcut would fire every time and the path would be ignored in exactly the scenario it was
added for. Named source wins; the session is not consulted at all.

**A path that does not exist, or carries no `## MCP Findings` heading** → say so in one line
and stop. Do not silently fall back to scanning: the caller named a file, and a different
file's findings are not a smaller answer to that request, they are a wrong one.

## Step 1 — the current session

Findings already in this conversation cost nothing to collect: they were observed here,
with the raw response still in context.

Scan the session for observations that match a failure class from
`.unikit/system/dev-principles.md` → A3 — a call that reported done over an unchanged
state, an argument that was accepted and ignored, a checker that went green over a
broken artifact, an undo that reported done and left the state, a batch whose total hid
what it skipped, a read that predated the change it was meant to prove.

**Something found → go to Step 5 and stop.** Do not scan plans. The session is the
cheapest and the most reliable source; the plan scan exists only because sessions end.

**This whole step is skipped when a plan path was given** (see `## Input`). The shortcut
above assumes nobody named a source — with a path in hand it would swallow the request,
because the caller is usually the very session that produced the rows.

## Step 2 — ask before reading anything from disk

Nothing in the session → count candidate plans first, then ask once:

```
No findings in this session. <N> plans changed after <audited>. Review them? [y/N]
```

`<audited>` is the `audited:` date from the notes header; `never` means every plan is a
candidate. Candidate plans are `.unikit/code/PLAN.md` and
`.unikit/code/plans/*/PLAN.md`, filtered by modification time against `<audited>`.

This glob is load-bearing: a stale one matches nothing and the run reports *no findings*,
which is indistinguishable from success. Whenever the plan manifest is renamed, this line
changes with it.

The glob stays one file per plan even for an ultra bundle: `## MCP Findings` lives in the
manifest, never in a phase file, so trap never walks `phase-*.md`.

**Declined → print one line and stop:**

```
No candidates were searched — the plan scan was declined.
```

That line is not decoration. A silent stop here is indistinguishable from "there was
nothing to find", and the next run would repeat the same offer against the same plans.

## Step 3 — read the table, never the body

Agreed, or a plan path was given → read **only the findings table**:

1. `Grep` the heading `## MCP Findings` in the plan.
2. Take the window from that heading to the next `##` heading. **On a bulk scan** (the
   empty form, many candidate plans) stop at 30 lines if the next `##` has not arrived by
   then; **on an explicit plan path** there is no line cap — one named file, nothing to
   ration.
3. Read nothing else from that file. Not the tasks, not the brief, not the checklist.

The window is the whole contract. A plan is a large file written for a different
purpose, and reading it whole to harvest three rows is how a cheap maintenance skill
turns into an expensive one.

**A window that closed on the cap is announced, never silent:**

```
WARN [mcp-trap] <plan>: the findings table is longer than the read window — <n> rows not read
```

The cap used to be unreachable: the table was filled once, in a run's closing report, so
the next `##` always came first. Executors now append a row per task through the whole
run, so a long editor-heavy plan can genuinely outgrow it — and rows dropped without a
word are the exact failure this file exists to prevent, arriving one step later. Re-run
against the named plan to take the rest.

## Step 4 — drop what was already transferred

Every note carries `from: <plan>#<id>` in its observation row when it came from a plan.
Drop every candidate row whose `<plan>#<id>` already appears in the notes.

This is why no registry of processed plans is needed: the cursor is the `audited:` date
plus the `from:` back-references, both of which live in the notes file itself. A repeat
run over the same plans is idempotent by construction — and a plan that grew new rows
after the last transfer is picked up correctly, which a "seen plans" list would not do.

## Step 5 — offer, in the genre

Present the surviving candidates and let the user choose which to record. For each one,
draft **both halves** the format requires:

- **above the line** — the check: `id | area | confirm that …`, phrased as an
  instruction to verify, with **no tool name in it**;
- **below the line** — the observation: `id | observed | replay | evidence | from`,
  where `evidence` is the raw call and the raw answer it gave, and `observed` is the date
  the finding was **observed** — today's date (`Bash(date *)`) for something seen in this
  session, and for a row lifted out of a plan the date already written there, copied
  across. Never the date of the transfer: the column says when this was run into, and a
  transfer date would quietly relabel it.

`area` comes from the 12-word vocabulary in `dev-principles.md` → A8 — the check table
is keyed by area precisely so it survives a server change, and a key outside that
vocabulary is unreachable by the greps the executors run.

**How a plan row becomes two notes rows.** The plan's six columns split across the line:

| plan column | goes to |
|---|---|
| `area`, `confirm that` | the `## Check` row, above the line |
| `observed`, `evidence`, `from` | the `## Observation protocol` row, below the line |
| `id` | **not** carried — notes ids are `R<n>`, allocated here; the plan's `F<n>` is recorded in `from:` as `<plan>#<id>` |
| — | `replay` has no plan column. It is decided **here**, defaulting to `manual` |

`observed` is **directional**, and this is the one place the rule can be got wrong:

- a finding raised in **this session** → today's date, via `Bash(date *)`;
- a row lifted out of **a plan** → the plan's own `observed` value, **copied verbatim**.

The grant sitting right there makes the wrong version easy to write — `date` on both paths
— and it puts the transfer date in a column labelled "observed", which is precisely the
relabelling the column was added to prevent.

**A plan in the old five-column format has no `observed`.** Leave the field empty and say
so once, in one line. Never today's date: the finding was not observed today, and an
invented date is worse than an admitted gap because nothing downstream can tell them apart.

`replay` defaults to **`manual`**. Promote it to `safe` only when every condition in
`references/notes-format.md` → "replay: safe" holds. When in doubt it is `manual`; the
cost of a wrong `manual` is that an audit shows the row instead of replaying it, and the
cost of a wrong `safe` is an audit that mutates a project.

**Reject, do not rewrite silently.** A candidate that asserts a capability, pre-declares
a gate, or names a replacement call is refused with the reason and offered back in check
form. If it cannot be expressed as a check, it does not belong in this file.

## Step 6 — write

Write `.unikit/MCP-RECHECK-NOTES.md` per `references/notes-format.md`:

- **File absent** → create it with the full header (`server:` from the delivery stamp,
  `audited: never`), both section headings, and the accepted rows.
- **File present** → append rows to both tables, allocating fresh ids. Do **not** touch
  the header: `server:` describes where the existing entries came from, and `audited:`
  belongs to `/unikit-mcp-audit`.

Both halves of a note are written together, always. A check with no observation behind
it cannot be replayed, retired, or upstreamed — it is a rumour with an id.

Then confirm what landed:

```
CLAIM:    <n> findings recorded in .unikit/MCP-RECHECK-NOTES.md
EVIDENCE: <the ids written> · read back from the file after the write
VERDICT:  CONFIRMED | NOT CONFIRMED
```

Read the file back. The rule that a response is not evidence applies to this skill's own
writes as much as to a server's.

## What this skill never does

- **Never calls the engine MCP.** No verification of the finding, no re-observation, no
  catalog lookup. If the finding needs replaying, that is `/unikit-mcp-audit`.
- **Never edits a plan.** Plans are read through the findings window and left untouched;
  the transfer is recorded on the notes side, as `from:`.
- **Never edits the packaged rules tree.** `.unikit/system/engine-mcp/` is rewritten by
  every `init` / `update`; an edit there is lost, and lost silently. A finding that
  deserves to ship to everyone goes upstream through `/unikit-mcp-audit`.
- **Never writes `⏸️ MANUAL`,** and never treats a missing rules file as a restriction.
  Absence of rules means no known exceptions, not absence of capability.

## See also

- `/unikit-mcp-audit` — curate what is here: re-stamp, replay, retire, upstream.
- `.unikit/system/dev-principles.md` — the evidence contract (A1/A2), the nine failure
  classes (A3), and the `kind` / area vocabularies (A8) this skill keys its rows by.
