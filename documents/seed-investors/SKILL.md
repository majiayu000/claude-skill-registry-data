---
name: seed-investors
description: >-
  Investor Finder. Researches the best investors for your idea from public
  sources only (the firm's own site, public profiles found through web
  search, SEC EDGAR Form D filings, the press) and ranks them by fit, 0 to
  100, with the reasons and a source link on every row: stage, sectors,
  check size against your ask, geography, how recent their last relevant
  deal is, and a warm intro. Reads SEC Form D filings to see who in your
  space raised, how much and when. Writes seed/investors.json for the
  Closer and the Pitch Coach. Use when the user says "find investors",
  "who should I pitch", "which VCs invest in pet tech", "build my investor
  list", "rank these investors", "who funded companies like mine", "Form D",
  or after /seed-plan, before /seed-closer.
argument-hint: "[\"your space in a few words\"] [--since YYYY-MM-DD]"
---

# seed-investors

The Investor Finder builds the list you will actually email. A good list is
short and specific: people who invest at your stage, in your space, with a
check that fits your round, who did a relevant deal recently. Claude does the
research on the open web, writes one row per investor with the links it
read, and this tool ranks the rows the same way every time and says why.
Every fact keeps its source, so you can check it before you lean on it.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/investors.py" formd --q "pet care" --since 2025-01-01      # who raised, how much, when
python3 "${CLAUDE_SKILL_DIR}/investors.py" import seed/research.csv                     # rows from public research
python3 "${CLAUDE_SKILL_DIR}/investors.py" add --name "Maya Chen" --firm "Northlight Ventures" \
    --stage seed --check 250K-1M --sectors "pet care; consumer marketplaces" --geo US \
    --last-deal "led a pet-care seed round" --last-deal-date 2026-04-13 --source URL --source URL
python3 "${CLAUDE_SKILL_DIR}/investors.py" rank --write                                 # fit 0-100 with reasons
python3 "${CLAUDE_SKILL_DIR}/investors.py" show                                         # the ranked list
python3 "${CLAUDE_SKILL_DIR}/investors.py" show maya-chen                               # one row, every source
```

`investors.example.csv` in this folder is the format (the reel's six
investors, all fictional, with `.example` addresses). `rank` takes `--stage
--sectors --geo --ask --check` the first time, or reads them from
`seed/config.json` (`startup.stage`, `sector`, `geography`, `raise`).

## What it reads and writes

| file / feed | what |
| --- | --- |
| your research, as CSV or JSON | name, firm, role, email, stage, check, sectors, geo, last_deal, last_deal_date, sources, warm_intro, personal_line, notes |
| `seed/config.json` | your stage, sectors, geography and raise; `sec_user_agent` for SEC |
| SEC EDGAR full-text search | `efts.sec.gov/LATEST/search-index?q=...&forms=D`: Form D filings in your words and dates |
| each Form D `primary_doc.xml` | amount offered and sold, number of investors, securities (equity, SAFE, debt), date of first sale, the names and roles of officers and directors |
| `seed/investors.json` | `import` and `add` write it; `rank --write` adds `fit` and `reasons`. `/seed-closer` drafts from it, `/seed-coach` preps calls from it |
| `seed/formd.json` | `formd --write`: the filings, the links, the summary |

## How fit works

| part | points | how |
| --- | --- | --- |
| stage | 25 | they invest at your stage; 12 if one stage off (pre-seed, seed, series a, series b, growth) |
| sectors | 25 | two or more of your sectors match theirs; 15 for one. "pets" matches "pet care", "carpet" does not |
| check | 20 | their range overlaps the check you want (default 5% to 50% of the ask); 10 within a factor of 2; 0 if their smallest check is bigger than your whole round |
| recency | 15 | their last relevant deal: 15 x (1 - days ago / 730), rounded half up |
| geography | 10 | they invest where you are, or globally |
| warm intro | 5 | someone can introduce you |

Each part prints its reason, like "checks of $250K-$1M fit the $75K-$750K
you want (+20)". A row without a public source URL is refused and never
ranked.

## Rules

- **Public sources only.** The firm's own site, public Crunchbase, AngelList
  or LinkedIn pages that a web search turns up, SEC EDGAR, the press. Never
  log in anywhere, never scrape behind a login, never scrape LinkedIn: open
  what a search result shows, and nothing else.
- **A source on every row.** `import` and `add` refuse a row without an
  https link; `rank` refuses one that lost it.
- **Never collect phone numbers or home addresses.** Such columns are dropped
  with a note, and a row with a phone number in its text is refused. Use the
  email a firm publishes for pitches; the tool warns on personal-style
  addresses.
- **Form D is a lead, not a list of investors.** It names the company that
  raised, the amount, the date and its officers and directors. A director who
  is not an officer often holds an investor's board seat: look them up in the
  press. A pooled fund's Form D (a venture capital fund raising money) is an
  investor to research. Form D has no business description, so search the
  words founders put in company names.
- **SEC asks who is asking.** `sec_user_agent` in `seed/config.json` (or
  `SEC_USER_AGENT`) must be your real name and email. Without it `formd`
  refuses. It pauses between requests, far under SEC's limit.
- **No promise of a check.** A high fit means worth a careful email, nothing more.

## Steps

1. Make sure `seed/config.json` has the startup's stage, sector, geography
   and raise (from `/seed-plan`), and a real `sec_user_agent`.
2. Run `investors.py formd --q "<a word in your space>" --since <18 months
   ago>`. Read who raised and how much: it is your comparable set, and the
   press coverage of those rounds names the investors who led them.
3. Research on the open web, from those leads and from searches like "seed
   investors <your space>", "<firm> portfolio <space>". For each investor,
   write a row with the facts and the URLs you read. Write the
   `personal_line` from something real they did or wrote, with its source.
4. Save the rows as CSV and run `investors.py import FILE.csv`. Fix every
   refusal (a missing source, a phone number) by fixing the research.
5. Run `investors.py rank --write` (with `--stage --sectors --geo --ask` the
   first time if the config is empty). Read the top ten with their reasons
   and check each fact you will quote.
6. Show the user the ranked list with fits, reasons and links, and ask which
   ones to approach.
7. Hand off to `/seed-closer`, which drafts one email per approved investor
   from `seed/investors.json` and sends nothing without the user's yes.

## Example: the reel

Leashly (made up) is raising a $1.5M seed for a US dog-walking marketplace.
The six investors are fictional too (`investors.example.csv`). `investors.py
rank --stage seed --sectors "pet care; marketplaces; local services;
consumer" --geo US --ask 1.5M --today 2026-10-26 --write`:

```
Investor fit for a $1.5M seed round in US, sectors pet care, marketplaces, local services, consumer; checks of $75K-$750K wanted
  fit  name             firm                   check        stage            id
   96  Maya Chen        Northlight Ventures    $250K-$1M    pre-seed, seed   maya-chen
   93  Daniel Okafor    Harbor Seed Fund       $100K-$500K  seed             daniel-okafor
   91  Priya Raman      Kite Hill Capital      $500K-$2M    seed, series a   priya-raman
   89  Sam Whitaker     Angel investor         $25K-$100K   pre-seed, seed   sam-whitaker
   87  Elena Brooks     Bluebell Ventures      $250K-$750K  seed             elena-brooks
   85  Marcus Lee       Copperline VC          $100K-$400K  seed             marcus-lee
```

Maya's 96 is 25 (seed) + 25 (pet care, marketplaces, consumer) + 20 (her
$250K-$1M checks fit the $75K-$750K Leashly wants) + 11 (her latest pet-care
seed round, 196 days ago) + 10 (US) + 5 (a warm intro). Her personal line,
"Saw you led two pet-care seed rounds, so you know the 20% fee problem
better than anyone.", goes to `/seed-closer` with her row.

## What it never does

It never invents an investor, a deal or an email address, never guesses a
check size it did not read, never logs in, never stores a phone number or a
home address, and never contacts anyone. Not investment advice.
