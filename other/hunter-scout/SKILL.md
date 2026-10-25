---
name: hunter-scout
description: >-
  The Job Scout. Finds the best open roles for the user's profile and ranks
  them by fit: pulls live listings from public job boards that need no login
  (Greenhouse, Lever, Ashby, NVIDIA's Workday board, Netflix's careers search),
  filters by title, place, remote and how recent, scores every listing 0-100
  against hunter/profile.json with the reasons (title, skills, location,
  seniority, pay range, freshness), writes hunter/jobs.json and adds the
  user's picks to the pipeline. Gives the manual route for Google, Meta and
  Amazon, whose careers sites cannot be read by a script. Use when the user
  says "find me jobs", "best listings for me", "scout roles", "what's open at
  Google", "search Software Engineer jobs", "rank these jobs", or "where
  should I apply".
argument-hint: "[company or title]"
---

# hunter-scout

Instead of sending thousands of resumes, send a few to the roles that fit. The
scout reads the job boards companies publish for exactly this purpose, keeps
the listings that match the titles and places you want, and ranks them with a
score you can check line by line.

What the user typed after `/hunter-scout`: `$ARGUMENTS`

Tool in this folder (standard library Python, no keys, no login):

```bash
python3 "${CLAUDE_SKILL_DIR}/jobs.py" --help
```

## What it reads and writes

- Reads `hunter/profile.json`: `target_roles`, `skills`, `locations`, `remote`,
  `relocate`, `exclude_titles`, `years_experience`, `salary_floor`,
  `dream_companies`, `work_authorization`. If it is missing, copy
  `skills/hunter-apply/profile.example.json` (the reel's fictional Jordan
  Reyes) to `hunter/profile.json` and fill it in with the user, one true fact
  at a time.
- Reads `boards.json` in this folder: 44 companies and the board each one
  really uses, every token checked live on 2026-10-15. Add any other company
  with `--board "Name=greenhouse:token"` (or `lever:` / `ashby:`). The token is
  the last part of the company's job board address, for example
  `job-boards.greenhouse.io/discord` is `discord`.
- Writes `hunter/jobs.json`: `{ "as_of", "scanned", "matched", "jobs": [ {"id",
  "company", "title", "location", "url", "source", "posted", "score", "why"} ] }`.
- `pick` adds chosen listings to `hunter/pipeline.json` as roles at stage
  `saved`, which `/hunter-tracker` and the other skills read.

## Which careers sites it can and cannot read

| Company | How | Why |
|---|---|---|
| Greenhouse, Lever, Ashby boards (Stripe, Discord, OpenAI, Ramp, Palantir and 34 more) | automatic | public job board APIs published for job seekers and aggregators |
| NVIDIA | automatic, Workday board | robots.txt allows the career site; the tool never touches nvidia.com, whose terms forbid scrapers |
| Netflix | automatic, careers search | robots.txt on explore.jobs.netflix.net allows /api/apply |
| Google | manual | no public feed, and robots.txt disallows crawling paged job results |
| Meta | manual | Meta's automated data collection terms require written permission |
| Amazon | manual | amazon.jobs links Amazon's Conditions of Use, which exclude robots and data mining |

For a manual company, open its careers search in the user's own browser
(`jobs.py boards` prints the link). Claude in Chrome can read the results
page with the user present, one page at a time, and the user can save the
search or turn on alerts in their own account. Never loop through pages, never
script it.

## The fit score

`score = title 35 + skills 30 + location 15 + seniority 10 + pay 5 + freshness 5`

- Title: 35 when a target role (or a known alias, like Software Development
  Engineer for Software Engineer) is in the title, 30 when every word is,
  less for a partial match. Titles under 15 are dropped unless `--any-title`.
- Skills: the share of the profile's skills found in the posting, full marks
  at six. Feeds without descriptions (Workday, Netflix) get a neutral 10 and a
  note to open the posting.
- Location: 15 for a profile location or remote in the user's country, 8 when
  a move is needed and the user is open to relocating, 0 otherwise.
- Seniority: 10, or 3 when the posting asks for more years than the user has
  (plus one), or 4 for a Senior title under five years.
- Pay: 5 when the posted range clears `salary_floor`, 0 when it does not, 2
  when no range is posted. Freshness: 5 within a week, 3 within 30 days.

Every point comes with a reason in `why`. A score ranks listings against the
profile; it never predicts an offer. Say so when you show it.

## Steps

1. Check `hunter/profile.json` exists and is true. Ask for anything missing
   (target titles, places, salary floor) rather than guessing.
2. Search. Default boards are the profile's `dream_companies`; `--company`
   picks others, `--all` scans every automatic board (about 40 polite calls):

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/jobs.py" search
   python3 "${CLAUDE_SKILL_DIR}/jobs.py" search --company Stripe --company Discord --days 30
   python3 "${CLAUDE_SKILL_DIR}/jobs.py" search --all --remote --min-score 70
   ```

   Other filters: `--title "Backend Engineer"`, `--location "Seattle, WA"`,
   `--limit 25`, `--json`. Exit 1 means nothing passed the filters.
3. Show the top listings with score, why, the posted date and the link, and
   the manual route for any dream company without a feed. Open the top few
   postings and read them before calling one a fit.
4. Ask which ones to pursue, then add exactly those:

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/jobs.py" pick <id> <id>
   ```

5. Suggest the next skills for each pick: `/hunter-research`,
   `/hunter-resume`, `/hunter-linkedin`, `/hunter-connector`.

If a board fails (HTTP 404), the company moved boards: `jobs.py check
--company Name` re-verifies, and the user can pass the new token with
`--board`.

## Example: the reel

Jordan Reyes (fictional) is a Software Engineer at Brightline Labs in
Chicago with three years of Go, Python and distributed systems, open to
relocating. His dream companies are Google, Meta, NVIDIA, Netflix and Amazon.
`jobs.py search` reads NVIDIA's Workday board and Netflix's careers search,
then prints the manual route for Google, Meta and Amazon. Jordan searches
Google's careers site with Claude in Chrome and finds the Software Engineer
role on Google Cloud, Infrastructure in Mountain View. Netflix's "Software
Engineer (L6) - Compute Runtime" (remote, United States) scores 75: title
match, remote, posted 20 days ago, skills to check on the posting. He picks
it and the Google role, and both land in `hunter/pipeline.json` as `saved`.

## What it never does

- Never logs in anywhere, never reads a site whose robots.txt or terms say no,
  and never pages through results a site asks crawlers not to page through.
- Never hammers a server: one request per board, at most a few detail calls,
  a pause between calls, and a User-Agent that says what it is.
- Never invents a listing, a salary or a posting date. Unknown means unknown.
- Never applies. Applying is `/hunter-apply`, and the user submits.
