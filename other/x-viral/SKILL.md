---
name: x-viral
description: >-
  The virality engine. Find the posts that are actually outperforming in the
  user's niche on X, rank them by how far each beat its own account, break
  each one down into hook, structure and format, then recreate the winners in
  the user's own voice for their audience. Use when the user says "find viral
  posts", "what's working on X right now", "what are people posting in my
  niche", "reverse engineer this account", "build me a swipe file", "why did
  this tweet blow up", "recreate this post for me", or has nothing to post and
  no evidence to decide with.
---

# x-viral

The research skill. Everything else in this pack writes; this one goes and
looks first, and then writes from what it found. Run it monthly, not daily.
Formats on X last a season.

Two tools live in this folder and both run:

```bash
python3 pull.py urls.txt > swipe.tsv                      # URLs you picked -> exact text, format, date
python3 swipe.py swipe.tsv --out ~/.claude/x/swipe.md     # rank, break down, write the swipe file
```

## The one idea that makes this worth doing

**Raw numbers are not evidence.** An account with 900,000 followers doing
400,000 views had an ordinary Tuesday. An account with 6,000 followers doing
400,000 views found something, and that something is copyable.

So everything ranks on the **outlier multiple**: a post's views divided by
that account's own median. Above 3x is a signal. Under 1.5x is that account's
normal day, and it teaches nothing however big the number looks.

## Step 1: pick the accounts

Ask the user for 6 to 10 accounts, or propose them and get approval:

- **4 direct**: same niche, same audience, somewhat ahead of the user.
- **3 adjacent**: different niche, same audience. Formats arrive here first.
- **2 or 3 outsized**: much bigger, for format only. Never for cadence or tone.

Also ask for the user's own **Bookmarks**. It is the most relevant corpus
there is and it is already filtered by their taste.

## Step 2: collect, by hand, in order

For each account, the **last 10 to 15 posts in order**, the dull ones
included. Not the hits. The median is computed from these rows, and a sample
of only the bangers inflates it and hides the outliers you came for.

Copy each post's link, and read its **view count** off the post (it is public
on every post, under the text). Likes, replies and reposts too, if they are
easy to see.

The user can do this in their own browser in about ten minutes. If this
session has a browser tool connected to the user's own logged-in browser, you
can open the profiles and read them with the user present, at human speed.
Rules that are not negotiable:

- **Never log into X on the user's behalf, never ask for a password,** never
  use their session for anything but reading the pages they asked about.
- **This is reading, not scraping.** Ten accounts, a dozen posts each. X's
  Terms prohibit crawling or scraping "in any form, for any purpose" without
  written consent, and name damages for bulk access. No crawler, no scraping
  service, no loops in the background, no search-results harvesting.
- **Copy the shape, never the words.** Hook formula, structure, format,
  length. Not their sentences. Attribute every row to its account.

## Step 3: fill the sheet

```bash
python3 pull.py urls.txt > swipe.tsv
```

`pull.py` calls X's documented oEmbed API, the one that exists so websites
can embed a post from its URL. It fills in the exact text with its line
breaks, the account, the date and the format (text / media / link / long).
One request per second, capped at 100 a run. It does not fetch counts,
because oEmbed does not carry them, so fill in the `views` column (and likes,
replies, reposts if you have them) from what is on screen.

## Step 4: rank and break down

```bash
python3 swipe.py swipe.tsv --out ~/.claude/x/swipe.md
```

For every post it computes the outlier multiple over that account's own
median, then the breakdown:

| | what it names |
| --- | --- |
| **hook** | the formula from `../x-post/hooks.json` (21), and the hook's score |
| **structure** | one line, one paragraph, short lines, a list, a long post, a thread |
| **format** | text, media, link, long |

Then it compares the top third with the bottom third on all three. Accounts
with fewer than 5 posts collected are skipped rather than ranked on noise.

## Step 5: say what it means, carefully

Report three things and no more:

1. **Which hook formulas over-index** in the top third, with counts. Two
   formulas appearing four times each across six accounts is a finding. One
   appearing twice is not.
2. **What the top third share structurally** that the bottom third do not:
   first-line length, one line vs a list, media vs text, link or no link.
3. **The unclassified hooks.** Every hook the classifier could not name is
   either noise or a formula `hooks.json` does not have yet. Read them by
   hand. This is the most valuable part of the output.

Then state the sample size in plain words. Forty posts across six accounts
supports a claim. Twelve does not, and saying so is the difference between
research and horoscopes.

## Step 6: recreate them for the user

For the top three, write **the user's version**: their own story, their own
number, their audience, in the shape that is working. Read `voice.md` first.
Each one:

```
FOUND   @someaccount · 6.4x · #7 The Hottest New · one line · text
        "The hottest new design tool is a text file."
SHAPE   The hottest new {familiar category} is {unexpected thing}.
YOURS   The hottest new marketing hire is a skill file.
```

Keep the found post's structure and none of its words beyond the frame. Run
each through `/x-post` (count, hook score) and `/x-human` before showing it.
Never hand back "make a post like this one". Hand back a post they could put
up tomorrow.

## Output

The ranked list, the three findings, the unclassified hooks, and three
recreated posts. The swipe file goes to `~/.claude/x/swipe.md`, where
`/x-post` and `/x-plan` read it, so after this runs once the rest of the pack
is working from the user's niche instead of from defaults.

Nothing is posted, liked, followed or messaged by this skill. It reads.
