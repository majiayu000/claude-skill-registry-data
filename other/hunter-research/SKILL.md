---
name: hunter-research
description: >-
  The Company Researcher. Researches each company the user is applying to and
  writes a one-page brief in hunter/companies/: the business from its own SEC
  filings (latest 10-K, 10-Q, recent 8-Ks with what each one is about), news
  from the company's own blogs, the culture in the company's own words, the
  team the user would join, and the interview loop with a source on every
  line (official prep pages for Google, Meta, NVIDIA, Netflix and Amazon,
  everything else marked community-reported). Use when the user says
  "research Google", "tell me about this company", "company brief", "prep me
  for Meta", "what's their interview process", "what does this team do", or
  before a coffee chat or interview.
argument-hint: "[company] [role]"
---

# hunter-research

Walking into a coffee chat or an interview knowing the business, the latest
news and how the loop works is the cheapest edge there is. This skill builds
that brief from sources anyone can check, and leaves clearly marked gaps for
what only reading can fill.

What the user typed after `/hunter-research`: `$ARGUMENTS`

Tool in this folder (standard library Python):

```bash
python3 "${CLAUDE_SKILL_DIR}/brief.py" --help
```

## What it reads and writes

- `companies.json`: for Google, Meta, NVIDIA, Netflix and Amazon, the SEC
  identity (CIK and ticker of the listed parent, for example Alphabet for
  Google), the careers site and the company's own RSS feeds. Any other
  company works with `--ticker` and `--feed URL`.
- `loops.json`: each company's interview loop. Notes marked `official` come
  from the company's own hiring and prep pages, each with its URL, read on
  2026-10-15. Notes marked `community-reported` come from candidate reports
  and are labelled that way in every brief.
- `brief.template.md`: the brief's sections.
- Writes `hunter/companies/<company>.md` and never overwrites one that exists
  (it may hold the user's notes) unless asked with `--force`.

## The rules

- **Every fact has a source.** A line in the brief either links a filing, a
  feed item or a company page, or it says "(fill in)". Fill those lines only
  from sources you open and read, and add the link.
- **Numbers come from filings.** Revenue, growth and headcount come from the
  10-K, 10-Q or the 8-K results exhibit, quoted with the period. Never from
  memory.
- **Official vs community.** Keep the label on every interview note. If a
  recruiter's description differs, the recruiter wins.
- **AI in interviews.** Google, Meta and NVIDIA say AI tools are not allowed
  during interviews (NVIDIA: it disqualifies the candidacy). Prepare with
  Claude, never use it in the interview, and tell the user so.
- **People.** The brief covers the company and the team. Research on a
  person (the hiring manager) belongs to `/hunter-connector` and uses public
  professional information only.

## Steps

1. SEC asks scripts to identify themselves. Ask the user once for a name and
   email for the User-Agent and save it as `"sec_user_agent": "Name email"` in
   `hunter/profile.json` (or pass `--user-agent`). Without it the brief skips
   filings and says so.
2. Build the brief:

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/brief.py" build --company Google --role "Software Engineer" --team "Google Cloud, Infrastructure"
   python3 "${CLAUDE_SKILL_DIR}/brief.py" build --company "Acme Corp" --ticker ACME --feed https://acme.example/blog/rss
   ```

   Pieces on their own: `brief.py loop --company Meta`, `brief.py sec
   --ticker NFLX`, `brief.py feeds --company NVIDIA --days 14`.
3. Read the sources and fill the "(fill in)" lines: Item 1 of the 10-K in a
   few plain lines, what the news means for the team, the team's work from
   the posting and its public engineering posts, and the user's angle from
   their real resume.
4. Show the user the brief and the three things most worth knowing before a
   chat: what the team does, one recent event, and how the loop works.
5. Suggest `/hunter-connector` for the hiring manager and `/hunter-interview`
   for mock rounds built from the loop.

## Example: the reel

Jordan Reyes (fictional) targets the Software Engineer role on Google Cloud,
Infrastructure. `brief.py build --company Google` finds Alphabet Inc. (GOOGL,
GOOG on Nasdaq) with headquarters on file with the SEC at 1600 Amphitheatre
Parkway, Mountain View, CA; the 10-K for 2025 filed 2026-02-05; the Q2 10-Q
filed 2026-07-23; and the 8-K of 2026-07-22 with item 2.02 (earnings
results), whose exhibit is where revenue gets quoted from. It lists the
latest Google Cloud Blog posts, and the loop: Google's own hiring page
describes recruiter conversations, possible assessments such as a coding
exercise, a panel of structured interviews scored on the same rubrics, no
brainteasers and no AI tools, roughly 6 to 8 weeks; the coding, system design
and "Googleyness and Leadership" split is labelled community-reported. Jordan
fills in what the infrastructure team builds from the posting and the Cloud
blog, then moves on to the connector.

## What it never does

- Never states a fact without a source, and never fills a gap with a guess.
- Never researches individuals beyond public professional information, and
  never anyone's private life.
- Never fetches what a site asks scripts not to: SEC with an identifying
  User-Agent and a pause between calls, each company feed once, nothing behind
  a login.
- Never promises an interview outcome. A brief helps the user prepare; it does
  not predict an offer.
