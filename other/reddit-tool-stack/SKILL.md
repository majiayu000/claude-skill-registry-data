---
name: reddit-tool-stack
description: >-
  Find out what tools people in a role actually use, which they switch from and to, and
  why, from their own Reddit threads. Returns a tool x threads / authors / praise /
  complaint / switched-to / switched-away table, a from-to switch table, and linked
  verbatim quotes. Use for "what software do HVAC companies use", "what's the stack
  for X", "what do bookkeepers switch to", or before picking or building a tool for a trade.
compatibility: >-
  Python 3, standard library only. Network access to one host:
  arctic-shift.photon-reddit.com (the public Arctic Shift Reddit archive). No key, no login.
allowed-tools: Bash(python3:*) Read Write
metadata:
  network-hosts: "arctic-shift.photon-reddit.com"
  network-purpose: "read public Reddit posts and comments from the Arctic Shift archive"
  version: "1.0"
---

# Reddit tool stack

The deliverable is a **tool table** for one role: which tools come up, among how many
distinct people, how often in a praising or complaining sentence, and which way people
move between them. The answers to "what do you use" live in the **comments**, so this
skill always pulls them.

## Method

**1. Pull the role's subreddits with tool-shaped keywords and their comments.**

```bash
python3 scripts/reddit_pull.py --subreddits HVAC hvacadvice \
  --queries software " app" crm "what do you use" servicetitan housecall jobber \
  --after 2025-11-01 --before 2026-11-01 --top 0 --comments 25 --comments-for 50 \
  > pull.json 2> pull.log
```

Matching is a raw substring test, so `" app"` also matches "apply" and "appreciate"
(it pulled 2,659 of 14,928 posts on r/hvacadvice); prefer `" app "`, `" apps "`. Seed `--queries` with generic words (software, app, crm, "what do you use") plus the two
or three tools you already know; the comments will name the rest.

**2. Discover the names you didn't know:**

```bash
python3 scripts/reddit_tally.py tools pull.json --discover --min-authors 3
```

This prints capitalised mid-sentence tokens by distinct authors. It is a candidate list,
not a count: most entries are ordinary words. Pick the products.

**3. Write `tools.json`**: one entry per product, every alias people use for it.

```json
{"ServiceTitan": ["servicetitan", "service titan", "ST"],
 "Housecall Pro": ["housecall pro", "housecall", "hcp"],
 "Jobber": ["jobber"]}
```

Short aliases (`ST`, `HCP`) are matched as whole words, case-insensitive; drop one if
it collides with ordinary text in this trade.

**4. Count:**

```bash
python3 scripts/reddit_tally.py tools pull.json --tools tools.json --quotes 2 --quote-rows 8
```

## Reading the columns

- **praise / complaint**: documents with a sentence naming the tool and a praise word (or a
  complaint word), never both. A rough sentiment proxy; read the quotes before you trust it.
- **switched to / switched away**: a switch verb in the same sentence, direction read from
  "from X" / "to X" / "replaced X with Y". The from-to table pairs them; `?` means the other
  side was not in your tools file, which usually means you missed a tool.
- A tool with many authors and few switches is the default; one with switches *to* it
  and complaints about the incumbent is the challenger. Say which is which, with numbers.

## The deliverable

The corpus line, the tool table, the switch table, and per top tool one praise and one
complaint quote with links. Then the "why" in your words, each claim pinned to a quote.
## Ground rules (every skill in this series)

- **Every number comes from `reddit_tally.py`.** Threads, authors, counts, dates, rates:
  paste them from its output. Never estimate, round up, or count by reading.
- **Every quote is verbatim, short (25 words or fewer), and carries its permalink.**
  The tally prints them that way; don't paraphrase inside quote marks.
- **Print the corpus line.** The tally's first line (documents, threads, authors,
  subreddits, dates) goes at the top of the deliverable, so a reader knows the sample.
- **The keywords shaped the corpus.** A count is a property of *your pull*, not of the
  subreddit: "41 of the threads I pulled" is honest, "41% of r/X" is not.
- **Absence is not proof.** The archive lags live Reddit and has gaps; a zero is
  reported as a zero for this window and these subreddits, nothing wider.
- **Vendor pitches are dropped before counting.** Owner subreddits are full of "I built
  a tool for X, what's your biggest pain?" posts; the tally drops them (and the pitcher's
  own replies) and prints how many (`digest` keeps everything). `--keep-pitches` turns that off.
- Archive quirks (silent truncation, why server-side search is useless, the dead
  alternatives) live in the `reddit-mining` tool skill. Read it if a pull looks thin.

Nothing here bundles, hosts or resells Reddit data: the scripts query the public
Arctic Shift archive from your own machine, and Reddit's terms (and Arctic Shift's)
govern what you do with what you pull.

## Setup

The scripts sit in `scripts/` beside this file: `reddit_pull.py` (fetch) and
`reddit_tally.py` (count). Python 3, standard library only, no key, no login. Pulls
over a busy subreddit take minutes: run them in the background and write to a file.
Part of a set: `reddit-mining` (the tool skill), `reddit-pain-points`,
`reddit-demand-check`, `reddit-tool-stack`, `reddit-competitor-chatter`,
`reddit-customer-language`, `reddit-thread-digest`.

## Example (real run, trimmed)

r/HVAC, 2026-05-01 to 2026-11-01, keyed on software / app / crm / "what do you use" plus
three known products, comments on the 25 most-discussed threads.

```
Corpus: 1,456 documents (464 posts, 992 comments) in 465 threads by 984 authors, r/HVAC, 2026-05-01 to 2026-10-31. Dropped as vendor pitches / market research: 19 posts (+8 of the pitcher's own commen…
```

| # | tool | threads | authors | praise | complaint | switched to | switched away | top thread |
| 1 | Daikin | 14 | 24 | 0 | 1 | 0 | 0 | https://reddit.com/comments/1x4zwqz |
| 1 | Daikin | 14 | 24 | 0 | 1 | 0 | 0 | https://reddit.com/comments/1x4zwqz |
| 2 | Trane | 22 | 21 | 1 | 1 | 0 | 0 | https://reddit.com/comments/1wxj7q6 |
| 3 | ServiceTitan | 14 | 18 | 0 | 2 | 0 | 1 | https://reddit.com/comments/1ue17tk |
| 8 | Housecall Pro | 8 | 8 | 0 | 0 | 0 | 0 | https://reddit.com/comments/1tkdeyo |
| 10 | Rilla | 3 | 5 | 0 | 0 | 0 | 0 | https://reddit.com/comments/1ue17tk/_/otgnxhi |
| 12 | Jobber | 3 | 3 | 1 | 0 | 0 | 0 | https://reddit.com/comments/1v7jx3d |
| 14 | FieldEdge | 1 | 1 | 0 | 0 | 0 | 0 | https://reddit.com/comments/1tkdeyo |
| … | (8 more rows) | | | | | | | |

| from | to | documents | example |
|---|---|---|---|
| ServiceTitan | ? | 1 | "Left ServiceTitan after 18 months — here's what I learned" (https://reddit.com/comments/1txwwfh) |

- ServiceTitan, complaint: "ST is so expensive that our wages suffered." ([link](https://reddit.com/comments/1ue17tk/_/otgym4e))

Reading it: r/HVAC is mostly technicians, so equipment brands outnumber business software
(Daikin 24 authors, ServiceTitan 18, Housecall Pro 8, Jobber 3). Software is discussed
thinly here, and mostly with complaints (ServiceTitan 2, praise 0). For the owner's
office stack, rerun on the subs where owners post (r/smallbusiness, r/sweatystartup with
`--queries hvac`) before drawing a conclusion, and say "thin" when the tally is thin.
The one switch row is a post whose only reply is a moderator removing it as software
marketing (`--thread 1txwwfh` shows it): open a switch thread before citing it.
