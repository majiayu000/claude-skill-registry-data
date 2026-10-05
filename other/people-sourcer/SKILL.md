---
name: people-sourcer
description: Use this skill any time the user wants to FIND specific people online and put them in a spreadsheet — recruiting candidates, sales prospects, outreach lists, research participants, journalist sources, podcast guests, influencer lists, lead lists, beta testers, advisors, or hires. Triggers on "find me N people who…", "build a list of contacts who…", "source candidates for…", "I need 50 prospects who…", "scrape Reddit/LinkedIn/X for [persona]", "build a Google sheet of people who…", "prospect list", "lead list", "candidate list", "outreach list", "shortlist of [role]", or any variant where the deliverable is a structured list of named individuals with contact info and personalized notes. Runs iterative BrightData scraping across LinkedIn, Reddit, X, Instagram, TikTok, YouTube, GitHub, forums; uses the worldbuilder lens for per-person commentary and outreach angles; outputs a multi-sheet xlsx (Google-Sheets-compatible). Prefer this over generic web search whenever the deliverable is a list of people.
---

# People Sourcer

A real recruiter, BD person, or research lead doesn't open a CRM first. They start with a question: *who specifically am I trying to reach, and why?* Then they hunt — across whichever platform that tribe actually lives on — and they keep notes. This skill makes Claude work that way, end-to-end, into a spreadsheet the user can act on.

## Core premise

Spam happens when you compile names without context. A list with 200 anonymous LinkedIn URLs is worse than 30 rows where each one has a real signal — *this person posted last week about exactly your problem, here's how to enter their world.*

So the rule is: **never source from zero. Always source from signal.** Find the place where the right people are already self-identifying, scrape that signal, then enrich and personalize. The personalization is what makes the difference between a useful list and noise.

## When to use this skill vs. just Google

Use this skill when the deliverable is a **list of named individuals** with structured fields. Don't use it for:
- Aggregate research ("how big is the X market") — use web search.
- Finding a single specific named person — just web search + verify.
- Company lists without people attached — that's account research.

If in doubt: if the user wants rows in a spreadsheet with names and an outreach angle, this is the skill.

## The workflow

Six phases. Each writes to a scratchpad so context survives long runs.

```
1. Intake          → pin down WHO and WHY
2. Source strategy → pick platforms + queries
3. Discovery       → iterative BrightData scraping
4. Enrichment      → per-person profile + contact pull
5. Personalization → worldbuilder commentary per row
6. Output          → multi-sheet xlsx
```

Skip phases that are already done. If the user hands you a list of profile URLs and just wants enrichment + commentary, jump to Phase 4.

---

## Phase 0: Scratchpad first

Before scraping anything, create a scratchpad so you don't lose the thread mid-run.

```bash
mkdir -p /home/claude/sourcing-work/<project-slug>/raw
touch /home/claude/sourcing-work/<project-slug>/brief.md
touch /home/claude/sourcing-work/<project-slug>/candidates.jsonl
```

- `brief.md` — the persona, query plan, and audience model. See `references/scratchpad-template.md`.
- `candidates.jsonl` — one JSON line per candidate, appended as you find them. JSONL because you'll be writing as you scrape, and a corruption in one line doesn't kill the whole file.
- `raw/` — raw scrapes by source URL, named like `linkedin-search-1.json`, `reddit-r-netsec-1.md`, etc.

Why JSONL for candidates: you'll likely process 30–500 people across multiple rounds. Mid-run failures shouldn't lose progress. Append-only is the right shape.

---

## Phase 1: Intake

Pin down the brief in `brief.md` before doing anything else. The single most expensive mistake in sourcing is scraping the wrong audience well.

Required:
- **Persona** — role/title, seniority, function. Be precise: "senior backend engineer with Rust experience" not "good engineer."
- **Signals** — what publicly-visible behavior identifies them? *They contributed to repo X. They posted about Y last quarter. They list Z certification. They lead a meetup on W.* Without signals, you're guessing.
- **N** — how many do they want? 20 ≠ 200 in workflow shape.
- **Purpose** — recruiting? sales? podcast guests? user research? This determines the "outreach angle" column entirely.
- **Geography / language** — global? specific country/city? English-only?
- **Custom fields** — anything beyond defaults the user wants captured.
- **Output preference** — xlsx (default), Google Sheet via Drive (if connected), or CSV.

If the brief is vague ("find me ML people"), ask 1–2 sharp questions before scraping. Don't ask a wall — ask the ones that actually change the search:
- *"Are you looking to hire them, sell to them, or interview them? It changes who I prioritize."*
- *"Any specific signal — open-source contribs, conference talks, recent job changes — that should weight my search?"*

If the user is decisive ("just find me 50 senior MLEs in Bangalore who post about RAG"), skip the questions and go.

---

## Phase 2: Source strategy

Pick platforms based on where the persona actually lives. See `references/source-matrix.md` for the full decision table; the short version:

| Persona | Primary platform | Why |
|---|---|---|
| B2B/SaaS buyers, execs, recruiters' candidates | LinkedIn | Self-identified work history, public posts |
| Devs / technical talent | GitHub + Reddit + X (formerly Twitter) + LinkedIn | Code is the signal; posts are the noise |
| Indie hackers / founders | X, IndieHackers forum, ProductHunt, LinkedIn | Where they ship and gripe |
| Security / pentesting | Reddit (r/netsec, r/AskNetsec, r/oscp), X infosec, ctftime, conference speaker pages | Tribe is small, vocal, identifiable |
| Researchers / academics | Google Scholar, arXiv, ResearchGate, university pages, Twitter/X | Citations + author pages |
| Creators / influencers | YouTube, TikTok, Instagram, Twitter/X | Platform IS the work |
| Local community / event attendees | Facebook events, Meetup, local subreddits, Eventbrite | Hyperlocal |
| Journalists / writers | Twitter/X, Muck Rack, bylines on outlet sites | Bylines = identity |

Plan your queries in `brief.md` before firing them. Write them out as a numbered list so you can reuse and iterate.

### Tools

These are the BrightData tools you'll lean on — they're deferred, so call `tool_search` first to load them.

| Goal | Tool |
|---|---|
| Find LinkedIn profiles by query | `bd:web_data_linkedin_people_search` |
| Pull a single LinkedIn profile (full data) | `bd:web_data_linkedin_person_profile` |
| Pull LinkedIn posts | `bd:web_data_linkedin_posts` |
| Reddit post + comments | `bd:web_data_reddit_posts` |
| X (Twitter) posts | `bd:web_data_x_posts` |
| Instagram profile / posts / reels | `bd:web_data_instagram_profiles` / `_posts` / `_reels` |
| TikTok profile / posts | `bd:web_data_tiktok_profiles` / `_posts` |
| YouTube profile / videos / comments | `bd:web_data_youtube_profiles` / `_videos` / `_comments` |
| Facebook posts / events | `bd:web_data_facebook_posts` / `_events` |
| Discovery (which subs, which writers, etc.) | `bd:search_engine`, `bd:search_engine_batch`, `bd:discover` |
| GitHub profiles, personal sites, niche forums, anything else | `bd:scrape_as_markdown` (or `bd:scrape_batch` for ≤10 URLs) |

See `references/bd-tool-cheatsheet.md` for parameter examples.

---

## Phase 3: Discovery — iterative scraping

Sourcing is not "one search and done." It's a loop where each round narrows from where-they-are to who-specifically-they-are.

### Round 1 — Locate the watering holes

For each platform you picked, run a discovery query to find the *places* the persona congregates. Use `bd:search_engine_batch` to fire several at once.

Example for "senior Rust backend engineers in EU":
- `"senior rust" engineer site:linkedin.com europe`
- `rust backend site:github.com followers:>200`
- `site:reddit.com/r/rust experience hiring`
- `rusty-days OR rustconf speaker`

Don't scrape candidates yet. Just identify *where* they cluster — the active subreddits, the LinkedIn groups, the conference speaker pages, the GitHub orgs.

Write findings under "Round 1 — Discovery" in `brief.md`.

### Round 2 — Pull candidates from the watering holes

Now actually pull people. Choose the right tool per source:

- LinkedIn search results → `bd:web_data_linkedin_people_search` with structured filters (role, location, current company keywords).
- A subreddit thread of "who's hiring" or "who wants a job" → `bd:web_data_reddit_posts` to get post + commenter usernames + their text.
- A conference speaker page → `bd:scrape_as_markdown` on the speaker URL, then for each speaker name, search their LinkedIn / X.
- A GitHub org or repo's contributors page → `bd:scrape_as_markdown` on `/graphs/contributors`.

Append each candidate as a JSONL line to `candidates.jsonl` immediately:

```json
{"name":"…","handle":"…","platform":"linkedin","profile_url":"…","raw_signal":"posted about RAG eval pipelines on Apr 4","source_query":"senior MLE site:linkedin.com bangalore RAG","seen_at":"2026-04-29"}
```

Don't bother with full enrichment yet — just capture name, primary URL, and the one-line signal that landed them on the list. Enrichment is Phase 4.

### Round 3 — Gap fill

Look at your candidates file. Are you skewed all-LinkedIn? All one country? All male names (a real bias risk)? All from one company? Run targeted rounds to fill gaps.

Stop when you have **roughly 1.5–2× the target N** (you'll lose some to dedup, dead profiles, and bad fits in the next phase).

### Stop conditions

- You hit the 1.5–2× target.
- A round adds < 20% new candidates after dedup → diminishing returns, move on.
- You've hit ~40 BrightData calls and haven't broken N → time to reconsider the persona/signals (probably too narrow), not to keep scraping.

---

## Phase 4: Enrichment + contact discovery

For each candidate in `candidates.jsonl`, enrich with whatever's publicly available. Don't enrich all 100 in parallel — batch in groups of 10–20 to keep the run debuggable.

### What to capture

For each person, fill the default schema (see `references/output-schema.md`):

- Full name (verify against the source — handles ≠ legal names; capture both)
- Current role + company
- Location
- Primary platform + URL
- Cross-platform handles (LinkedIn ↔ X ↔ GitHub ↔ personal site) — found via name + role search
- Public email or contact form URL — only if listed on their public profile/site
- Recent signal (the post/talk/repo that's the reason they're on the list)
- Custom fields the user requested

### Contact discovery — what's OK and what isn't

Read `references/ethics-and-rails.md` before this phase. Short version:

✅ Use emails that the person has **publicly published** on their own profile, GitHub, personal site, or signature.
✅ Use contact form URLs.
✅ Use platform DM as the channel ("reach out via X DM" is a valid row value).
❌ Don't guess emails (`firstname.lastname@company.com` patterns are a guess; treat them as unverified at best).
❌ Don't pull from data brokers, leaked dumps, or paid email-finders dressed as "verification."
❌ Don't extract emails from content that's behind a login the person didn't intend you to see.

If you can't find a public contact, that's fine — record `Public contact: not found; reach via [LinkedIn/X DM/contact form URL]`. The user can handle their own outreach platform.

### Cross-platform stitching

For each person, after pulling their primary profile, run one quick search to find their other handles. Patterns that work:
- `"<full name>" site:github.com` (devs)
- `"<full name>" site:twitter.com OR site:x.com` 
- Look for self-linked URLs on the primary profile (LinkedIn "Contact info," GitHub bio, X bio)

This dramatically lifts the quality of the personalization step — you can pull their X bangers in addition to their LinkedIn corporate-speak.

---

## Phase 5: Personalization (the worldbuilder lens)

This is the phase that separates a real list from a CSV-with-extra-steps. **Read `/mnt/skills/user/worldbuilder-writing/SKILL.md` Phase 0 before this phase.** The principle there is the principle here: writing/commenting is applied psychology, not self-expression.

For each person, write three short fields. None of them generic. Each must reference a *specific* signal from that person's actual scraped data.

### 5.1 — "Why they fit" (one sentence)

The reason they're on the list, anchored in a fact. Not "experienced ML engineer" — that's a description. Try: *"Led RAG eval at Phonepe; posted a teardown of LangChain's evaluators on Apr 4 — directly relevant to your eval-tooling pitch."*

### 5.2 — "Outreach angle" (1–2 sentences)

How to enter THEIR world, not pitch from outside it. Apply worldbuilder Phase 0:
- What's the in-group language they use? (Mirror it, don't translate.)
- What's their atomic unit — what do they already agree with? Open the message there.
- What ONE thing should they believe/feel/do after reading your message?

Examples:
- For a Rust engineer who posted about borrow checker frustrations: *"Open with the specific borrow-checker pattern they're hitting. Don't lead with your product — lead with 'I saw your post about lifetimes in async traits, here's a pattern that worked for us.'"*
- For a CTO who blogs about hiring: *"Reference their 'hiring is broken' post specifically. Atomic unit: the cost of bad hires. Don't mention your tool until paragraph two."*

### 5.3 — "Risk / caveat" (only if applicable)

Public signals that should change how the user approaches this person:
- "Posted about being overcommitted last week" → don't pitch a 30-min call.
- "Just changed jobs" → outreach about their *new* role, not the one your scrape indexed.
- "Posts critically about AI tooling" → lead with substance, not features.
- "Inactive for 6+ months" → low-confidence row, deprioritize.

If there's no risk, leave the field empty. Don't invent risks for symmetry.

### What to NOT do here

- Don't write "this person seems passionate about technology" — that's slop.
- Don't write the same outreach angle twice in a row — if you can't differentiate them, you don't have enough signal; go back and scrape more.
- Don't claim things you didn't see. The personalization is only useful if it's verifiable from the source. The user should be able to click the source URL and see the signal you cited.

---

## Phase 6: Output to spreadsheet

Use the xlsx skill: **read `/mnt/skills/public/xlsx/SKILL.md` before writing the file.** It tells you which library and pattern to use in this environment.

### Sheet structure

Three sheets in one workbook:

1. **People** — one row per candidate. Columns from `references/output-schema.md` plus user's custom fields. Format the header row, freeze it, autosize columns, hyperlink all profile URLs.
2. **Sources** — one row per scrape: query, platform, tool used, candidates yielded, timestamp. This is for the user to audit the list and re-run later.
3. **Outreach playbook** — the persona-level audience model from Phase 2 + a short "how to use this list" note. This is the worldbuilder model the per-row angles are derived from. One page, written like a real briefing memo, not a bulleted FAQ.

### File naming

`people-<purpose-slug>-<YYYYMMDD>.xlsx` — e.g., `people-rust-engineers-eu-20260429.xlsx`. Save to `/mnt/user-data/outputs/` and present via `present_files`.

### Optional: native Google Sheet

If the user explicitly asked for a Google Sheet AND the Google Drive connector is loaded:
1. Build the xlsx as above.
2. Use the Drive connector's `create_file` tool to upload it. Drive will let them open as a Sheet.
3. If the connector isn't available, just deliver the xlsx — Google Sheets opens xlsx natively on upload, so this is not a blocker.

Don't promise Drive integration if the connector isn't connected. Check first.

---

## Phase 7: Hand-off — what to tell the user

When you present the file, give them three things in your message:

1. **The N delivered** — "Here are 47 candidates. I aimed for 50; 3 were dropped at QA for [reason]." Honesty about what didn't work matters.
2. **One paragraph of audience insight** — what you learned about this persona from the scraping. The user's about to do outreach; they need the model in their head.
3. **One concrete next step** — "I'd recommend starting with the 12 marked High confidence and writing your first 3 messages off the Outreach Angle column to calibrate."

Don't dump all 47 names into chat. The file IS the deliverable; the chat is the briefing.

---

## Anti-patterns

- **Scraping for theater.** If the user gave you 30 LinkedIn URLs and just wants enrichment + commentary, don't run 6 rounds of discovery. Skip to Phase 4.
- **Skipping Phase 5.** A list without the personalization columns is just a CSV — the user could've gotten that from any data broker. The worldbuilder commentary is the whole reason this skill exists.
- **Generic outreach angles.** "This person seems active in the AI space" is a tell that you didn't actually read their content. If you can't write a specific angle, you don't have enough signal — go scrape more.
- **Padding the count.** If the persona is genuinely narrow and only 22 real fits exist, deliver 22 and say so. Don't pad with weak matches to hit N. The user will figure out the padding by row 30 and lose trust.
- **Making the spreadsheet pretty before it's right.** Get the data and commentary correct first. Formatting is the last step.
- **Email-guessing.** `firstname.lastname@company.com` is not a contact; it's a guess that lands you in spam folders and can violate anti-spam law in some jurisdictions. Leave the field empty if there's no public email.
- **Pretending you found things you didn't.** If a person's email isn't public, write "not public." Don't invent or guess. The user trusting this list is the only thing that makes it useful.

---

## Example shape of a run

User: *"Find me 30 indie hackers who built B2B SaaS in fintech in the last 18 months. I want to interview them for a podcast."*

Rough flow:

1. **Intake** — clarify: revenue stage? geography? "indie" = solo founder vs. ≤5? Lock the persona. User answers: "any geo, English-speaking, solo or 2-co-founder, MRR > $5k, launched in last 18mo."
2. **Source strategy** — IndieHackers (primary), Twitter/X (founders ship and gripe), ProductHunt (launches in window), LinkedIn (cross-stitch profiles).
3. **Discovery** —
   - Round 1: `bd:search_engine_batch` for `"B2B fintech" launched site:indiehackers.com 2024..2026`, ProductHunt fintech launches in date window, X advanced search for `"just hit $5k MRR" fintech`.
   - Round 2: scrape the IndieHackers milestone posts (`bd:scrape_as_markdown`), the PH product pages (founder names + handles), the X threads. Append candidates to JSONL.
   - Round 3: gap fill — list is too US-skewed; one targeted round on EU/India fintech indie subreddits + r/SaaS.
4. **Enrichment** — for each, find LinkedIn + X + their product's site + their public email or DM. Capture launch date, current MRR (if publicly stated), product link.
5. **Personalization** — for each: why they fit (specific milestone post or PH launch), outreach angle for a podcast invite tuned to *their* origin story (anchor on a specific tweet or IH post), risk if any (e.g., "just had a kid, mentioned bandwidth issues" → flag).
6. **Output** — `people-fintech-indie-hackers-20260429.xlsx`, three sheets, custom column "MRR (public)" added per user request. Hand-off message: 28 delivered (2 dropped — one stealth, one sold the company), here's the audience insight, here's how to start.

That's the full flow. Most real runs are messier — the point is the discipline of (a) scraping signal not noise, (b) personalizing per row, (c) being honest about what you couldn't find.

---

## Related skills

- `worldbuilder-writing` — authoritative on audience modeling and per-person commentary. This skill depends on it.
- `xlsx` — authoritative on spreadsheet generation in this environment. Read before Phase 6.
- `pro-graphic-designer` — the architectural sibling. Same scratchpad-driven, iterative-scraping shape.

Don't reinvent what those skills cover. Read them and dispatch.
