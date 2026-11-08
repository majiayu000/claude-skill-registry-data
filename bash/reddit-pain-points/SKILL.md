---
name: reddit-pain-points
description: >-
  Mine a niche's subreddits for the complaints that keep coming back, and return a
  ranked table: each pain, how many distinct threads and authors raised it, the date
  spread, and 2-3 short verbatim quotes with permalinks. Use for "what are the biggest
  pain points for X", "what do restaurant owners complain about", "find problems
  worth solving in Y", or before building a product for a trade.
compatibility: >-
  Python 3, standard library only. Network access to one host:
  arctic-shift.photon-reddit.com (the public Arctic Shift Reddit archive). No key, no login.
allowed-tools: Bash(python3:*) Read Write
metadata:
  network-hosts: "arctic-shift.photon-reddit.com"
  network-purpose: "read public Reddit posts and comments from the Arctic Shift archive"
  version: "1.0"
---

# Reddit pain points

The deliverable is a **ranked pain table**, not a summary of vibes: every row is a
complaint that recurs across distinct threads and people, counted by a script, with
the words people used and a link to each.

## Method

**1. Pick where the operators talk.** One to four subreddits of people who *have* the
problem (r/restaurateur, r/HVAC, r/smallbusiness), not people who sell to them. Twelve
months is a good default window.

**2. Pull the whole corpus, not a keyword slice**, so counts aren't shaped by your guesses.
Add `--queries` only when the sub is general and you need to narrow it to a trade.

```bash
python3 scripts/reddit_pull.py --subreddits restaurateur \
  --after 2025-11-01 --before 2026-11-01 --top 0 --comments 15 --comments-for 60 \
  > pull.json 2> pull.log
```

**3. Discover candidate pains** from sentences that carry complaint words:

```bash
python3 scripts/reddit_tally.py phrases pull.json --near-preset pain --min-threads 3 --top 40
```

**4. Write `themes.json`**: 6-15 pains, named in the operators' words, each a list of
regexes. Read the phrase table and a sample of pain sentences, then group:

```json
{"Staffing: no-shows and quitting": ["no.?show", "quit", "call(ed|s)? out", "can't find (good )?(staff|cooks|help)"],
 "Food and supplier costs":        ["food cost", "price of (beef|eggs|chicken)", "supplier", "sysco"]}
```

**5. Count, then refine.** Check what the themes missed, add or split themes, re-run:

```bash
python3 scripts/reddit_tally.py themes pull.json --themes themes.json --near-preset pain --show-unmatched 30
python3 scripts/reddit_tally.py themes pull.json --themes themes.json --near-preset pain --quotes 3
```

The table has two counts that answer different questions: **threads** (how often the
topic comes up at all) and **in a complaint sentence** (threads where it sits next to a
pain or complaint word). Report both. `--near-preset pain` restricts the whole count to
complaint sentences; it is strict, because people describe pain without saying "frustrating".

## The deliverable

1. The corpus line and the in-scope / matched / unmatched line, verbatim from the tally.
2. The ranked table: pain, threads, authors, first, last, months active.
3. Under each of the top pains, 2-3 verbatim quotes with permalinks.
4. One line per pain on what it is, in plain words. Analysis is yours; numbers are not.

Rank by distinct threads, then authors. A pain raised in 40 threads by 38 people over
11 months is a pattern; one raised 40 times by 3 people in one week is a flame war.
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

r/restaurateur, 2025-11-01 to 2026-11-01, whole corpus pulled (no `--queries`), 12 themes.

```
Corpus: 2,027 documents (1,143 posts, 884 comments) in 1,145 threads by 1,420 authors, r/restaurateur, 2025-11-02 to 2026-10-31. Dropped as vendor pitches / market research: 94 posts (+7 of the pitche…
In scope: 2,020 documents. Matched at least one theme: 699. Matched none: 1,321.
```

| # | theme | threads | in a complaint sentence | authors | mentions | first | last | months active |
| 1 | Staffing: hiring, no-shows, turnover | 146 | 9 | 189 | 202 | 2025-11-06 | 2026-10-31 | 12 |
| 2 | Reviews and marketing | 89 | 2 | 118 | 128 | 2025-11-11 | 2026-10-30 | 12 |
| 3 | Food and supplier costs | 71 | 4 | 78 | 87 | 2025-11-05 | 2026-10-30 | 12 |
| 4 | Cash flow and profitability | 70 | 5 | 84 | 94 | 2025-11-17 | 2026-10-29 | 12 |
| 5 | Card processing, POS and chargebacks | 69 | 6 | 87 | 103 | 2025-11-03 | 2026-10-31 | 12 |
| 6 | Payroll, tips and wages | 62 | 4 | 91 | 102 | 2025-11-02 | 2026-10-20 | 12 |
| 7 | Delivery apps and third-party fees | 53 | 3 | 66 | 72 | 2025-11-29 | 2026-10-20 | 12 |
| 8 | Equipment and repairs | 51 | 9 | 63 | 66 | 2025-11-04 | 2026-10-20 | 11 |
| 9 | Inventory, waste and ordering | 47 | 3 | 51 | 52 | 2025-11-17 | 2026-10-24 | 12 |
| … | (4 more rows) | | | | | | | | |

**Staffing: hiring, no-shows, turnover**
- "Menu printing and updating is a major non-productive time suck for a staff person." (2026-01-09, https://reddit.com/comments/1q87xuw/_/nylk2q4)
- "Finding and holding good staff is always and will always be the hardest part." (2026-10-02, https://reddit.com/comments/1wvpzjl/_/pdhbnmu)

**Food and supplier costs**
- "January data (per NRN's article, "Menu inflation moderated in January") shows menu price increases slowing month-to-month." (2026-02-18, https://reddit.com/comments/1r8areq)
- "I thought the hardest part of running a food business would be labor, food cost, equipment breaking… but honestly?" (2025-11-22, https://reddit.com/comments/1p3ydjp)

**Slow sales and foot traffic**
- "Now heading into summer, the slow season for hotpot." (2026-06-09, https://reddit.com/comments/1u1anag)
- "Struggling with foot traffic for my small restaurant" (2026-10-20, https://reddit.com/comments/1xaicdi)

Reading it: staffing is the most-discussed topic (146 threads, 189 authors), but "Slow sales and foot traffic"
has the highest share of threads where the mention sits in a complaint sentence
(6 of 18, against 9 of 146 for staffing). The two columns separate what owners *talk about* from what they
*complain about*; report both. 94 posts were dropped as vendor pitches before counting.
