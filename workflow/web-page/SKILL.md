---
name: web-page
description: One page, by url — the plain-url harvester behind a job that names no channel unit.
argument-hint: "ticket=<id>"
---

# web-page

You are the plain-url harvest ticket's unit. Unlike every channel unit,
your one stage runs with no model session at all: the pass starts
`scripts/fetch.py` directly — `llm-wiki-ops run ops/skills/web-page/scripts/fetch.py
ticket=<id>` (G2) — in the harvest stage's jail, and that script reads the
ticket, fetches, and posts `tickets update` itself. There is no hand-run
form: the script runs only through the runner, and `tickets run <id>
spawn=self` is refused for this unit's ticket.

## Running a ticket

```sh
llm-wiki-ops --json jobs run job=<slug> wait=<s>
llm-wiki-ops --json tickets run <id> wait=<s>
```

Either starts the stage jailed. The host's `close` (`tickets close <id>`) reads whatever `tickets update` the
script posted and routes it: `ok` mints the process ticket the plugin's own
`scripts/extract.py` runs; `failed` with attempts left re-queues; `gone` (a
refresh only) lands the page as gone. The script never closes its own ticket.

## What it does

`fetch.py` fetches the ticket's own `target` — only `http`/`https` — and
writes `capture.json` (`slug`, `item`, `title: null`, `body`,
`content_type`, `fetched_at`) beside the body, the whole of what the
plugin's `extract` reads. A target already in `known[]` is `ok` with nothing
captured and a reason naming `known`; a refused host, a timeout, an auth
wall or any other failure is `failed` with `missing=<host>,<url>,<why>`; a
refresh whose source answers 404 or 410 is `gone`. See `scripts/fetch.py`
for the full rule set — denial classification, the one retry, and what a
refresh does differently.

## Reference

`llm-wiki-ops reference pipeline-ticket` for the worker loop and the
report every worker leaves.
