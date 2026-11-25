---
name: job-board-scout
description: Build a deduplicated, ranked queue of new job postings from public job feeds and public Ashby, Greenhouse and Lever boards, filtered by rules you write down. Use when asked to watch job boards, track new roles for a search, build a job review queue, or find remote postings matching specific titles and locations.
---

# Job Board Scout

Discovery, not application. The script reads public job endpoints, applies filters
you declare in a config file, deduplicates against a state file, and writes a
markdown review queue. It has no credential, sends nothing, and cannot apply to a
job or message anyone.

## Prerequisites

Python 3.9 or later, standard library only. No API key, no account, no secret.
Outbound HTTPS to the endpoints you list in the config.

## Before the first run: write the config

There is no default search. `filters.title_terms` is required and the script exits
2 if it is missing, because a scout that guesses what you want is a scout that
wastes your review time. Start from [`examples/recruiting.json`](examples/recruiting.json)
and replace the lists with the user's own.

Ask the user for, and write into the config:

1. **Titles** (`filters.title_terms`). Substrings matched against the posting title,
   casefolded. Prefer stems (`talent sourc`) over full words.
2. **Disqualifiers** (`filters.exclude_terms`). Matched across title, description,
   tags and employment type. This is where hourly work, unpaid work, and
   near-miss titles go.
3. **Remote requirement** (`filters.require_remote`, `filters.non_remote_terms`).
4. **Geography** (`filters.geography`). This filter reads the location restriction
   the posting states. It is a filter over posting text, not a claim about anyone's
   right to work anywhere. `allow_unstated: false` fails closed: a posting that says
   nothing about location is dropped rather than assumed to be open.
5. **Sources**. Four feed adapters (`arbeitnow`, `himalayas`, `jobicy`, `remotive`)
   plus a watchlist of public ATS boards. See
   [references/sources.md](references/sources.md) for how to find a board name and
   how to confirm it before adding it.
6. **Scoring** (`scoring`). Ordering only, never filtering. Title tiers are
   evaluated in config order and the first match wins; signal terms all accumulate.

## Running it

```
python scripts/job_board_scout.py --config myconfig.json --state .scout/state.json --out out
```

`--dry-run` runs the whole pipeline without recording anything as seen, so you can
tune filters against real data and still get the same roles on the real run.
`--json` prints the run summary for a wrapper to read. `--max-new N` overrides the
config for one run.

Schedule it with cron or any scheduler. Nothing in the script needs a daemon.

## Reading the result

`out/queue.md` carries the roles, then three sections that matter more than the
roles when you are tuning:

- **Source status** — `ok (N records)` or `failed (ExceptionName)` per source. A
  source that has been failing for a week is a dead board name, not a quiet market.
- **Filter counts** — how many postings each rejection reason removed. If
  `title does not match filters.title_terms` is eating everything, your terms are
  too narrow.
- **Coverage warnings** — a source returned records but zero title fits. Usually
  the wrong board or the wrong vocabulary for that market.

## Boundaries

- Read-only. Public GET requests to the configured endpoints and nothing else.
- If every configured source fails, the run exits 1 rather than writing an empty
  queue. An empty queue must mean "nothing new", never "the network was down".
- Deduplication is by company + title + location, not by URL, so one posting
  syndicated to three feeds is queued once. State is capped at 5000 keys.
- Never present a score as a judgement of the role. It is a review order, and
  every point in it is printed with the rule that produced it.
- Do not add a board to the watchlist without fetching its endpoint once first.
