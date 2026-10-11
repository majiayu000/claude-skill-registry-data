---
name: check
description: 'Validate the spec and the documents, report where the project stands and what to run next, or audit the implementation against the documents Arguments: --docs | --code | --new | (empty = spec + documents + dashboard).'
---

Read-only in every mode. Nothing here writes to the spec or to a client document.

**Empty** — `macstack-dev:lint`, all three passes, then the status screen. One engine,
two ways of printing it: the dashboard is the lint findings ordered by cost of ignoring
them, not a second set of predicates with its own opinion.

The dashboard also reports **task statuses that disagree with the audit** — read-only,
no `--apply`:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/planning/references/task_status.py" macstack
```

Both directions, and the second is the one worth reading first: a task standing `done`
whose case the newest verdict found `absent`. A work list that looks shorter than the
truth is one nobody goes looking behind. Print the moves it proposes and name
`/macstack-dev:update` as what applies them — this command never writes.

**`--docs`** — pass 3 and the judgment checks only. Use it after editing documents and
before handing anything to a client.

**`--code`** — `macstack-dev:conformance`. Starts from a **case id**: does the
implementation do what this case promises? Writes one `audit` row per case into
`history/ledger.jsonl`. Those verdicts are what `/macstack-dev:plan` reads to tell real
work from a document nobody has checked — without them a gap report counts every case
the team already built.

**`--new`** — `macstack-dev:code-audit`. Starts from a **file** and asks the opposite
question: what is in the code that no document mentions? Enumerates the code by the
conventions the spec declares, then sorts every candidate into one of three lists —
not in the documents · not in the code · contradicts. Output is a proposal, never an
edit: what to do about a contradiction is the owner's ruling, and it is applied through
`/macstack-dev:intake`.

Both read the source tree and neither writes to it. Run `--code` when you want to know
whether the promises hold; `--new` when you suspect the code has moved on without the
documents. On a folder nobody has audited in months, run `--new` first: a verdict on a
case the documents never described is a verdict on the wrong question.

**When the answer is "both have moved"**, this command is the wrong one — it reports and
stops by design. `/macstack-dev:reconcile --master=code|docs` is what closes the
distance, and it makes you say which side is right before it touches anything.

Report errors before warnings, and end with the single next command. If the spec fails
lint, say plainly that it must not be scaffolded from.