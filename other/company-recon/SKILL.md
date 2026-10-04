---
name: company-recon
description: Runs a full due-diligence investigation on a company (optionally for a specific role) before the user applies, interviews, or accepts an offer there. Pulls together the tech stack, engineering culture, work-life balance, toxicity/red-flag signals, interview process, and compensation signal by researching the company's official site/careers page/engineering blog, LinkedIn, Glassdoor, AmbitionBox, Blind, Reddit, and current open job postings. Trigger this whenever the user names a company and asks to "research", "investigate", "look into", "check out", "vet", "do a background check on", or wants to know "what's it like to work at" a company, wants a "culture check" or "red flag check", or wants tech-stack/culture info before applying or interviewing. Also trigger for phrases like "grill me on [company]" or "should I even apply to [company]".
---

# Company Recon

A due-diligence workflow for investigating a company (and optionally a specific role/team there) before the user spends time applying, interviews, or considers an offer. Produces one consolidated report covering tech stack, culture, red flags, interview process, and a verdict.

Built for a job-seeking software engineer — assume the reader wants the unvarnished truth, not corporate marketing copy. Skepticism toward the company's own PR is a feature, not rudeness: an official careers page and a Glassdoor 2-star review are both "sources", but they're not equally reliable for the same claims (see Weighing Evidence below).

## Inputs

- **Company name** (required).
- **Role / team name** (optional) — e.g. "backend engineer", "SDE-2 in the platform team". Narrows the tech-stack and interview-process sections to that role where possible.
- If the user gives neither an explicit company nor enough to search on, ask once for the company name — don't guess.

## Workflow

Work through these in order. Use `web_search` for discovery and `web_fetch` to pull full pages once you have a promising URL — snippets are too thin for this kind of investigation. Budget roughly 15–25 searches/fetches total for a thorough pass; this is a research-heavy task, not a quick lookup.

### 1. Official sources (baseline, not truth)
- Company official site, "About"/"Engineering"/"Tech Blog" pages if they exist.
- Careers page: current open roles (all of them, not just the one the user named) — this is your best live signal for tech stack, team structure, and how fast they're hiring (mass hiring across many roles can mean growth *or* high attrition backfilling — flag it, don't assume which).
- LinkedIn: company page (headcount, headcount trend if visible, recent posts), and search for people who list this company + the target role/title to see real tech-stack mentions in their profiles/posts. Also search LinkedIn for ex-employees' posts about leaving, if any surface.
- If the user gave a role, search for that role's actual job posting(s) — current or recently expired — and extract the full stated stack, not just headline languages.

### 2. Review platforms (the "what's it actually like" layer)
Search each of these by name + company; fetch the actual review pages, not just search snippets:
- **Glassdoor** — overall rating, CEO approval, "Pros/Cons" patterns across multiple reviews (not just the top one), interview reviews and difficulty/experience, salary reports if visible.
- **AmbitionBox** — especially important for India-based or India-founded companies; often has more candid, higher-volume reviews than Glassdoor for these.
- **Blind** (teamblind.com) — anonymous and often the most candid/critical source; search Blind + company name for compensation threads, layoff rumors, management complaints. Note: Blind skews toward complaints/venting, so treat volume of complaints as a signal, not gospel.
- **Comparably** and **Kununu** (Kununu especially if the company has any EU presence) if they surface — quick secondary confirmation.

### 3. Reddit deep-dive
- Search Reddit for `<company> review`, `<company> interview`, `<company> layoffs`, `<company> toxic`, `<company> wlb`, `<company> reddit` — and relevant subreddits (r/cscareerquestions, r/ExperiencedDevs, a country/company-specific sub if one exists, e.g. r/developersIndia for Indian companies).
- Fetch actual threads, not just the search result list — the real signal is in the comments, not the post title. Pull specific, attributable claims (team-specific if possible) rather than one angry outlier.
- Note recency: a scathing thread from 2019 matters less than one from the last 12 months. Prioritize recent threads and flag if everything you find is old (could mean things changed, or could mean it's just not discussed much).

### 4. Synthesize into the report

**Output mode**: default to writing a single Markdown **file** (via the file-creation tools, saved to the outputs directory and presented to the user) — not a chat wall of text. Only respond inline in chat if the user's message includes `--inchat` (anywhere in the message). Either way, the content and structure below are the same — only the delivery channel changes.

Keep it simple and minimal — this is a scannable brief, not a research paper. Write every bullet in **ultra-terse mode** (caveman-ultra style): minimum words that carry full meaning, zero degradation of information. Concretely:
- Drop articles (a/an/the), filler (just/really/basically/simply/notably), hedging, pleasantries.
- Fragments over full sentences. Arrows for causality/sequence (e.g. "6 rounds → comp discussed last → matches disorg complaints").
- Short synonyms over long phrasing (big not "extensive", cut not "eliminate").
- Never abbreviate: company/platform/product/person names, tech names, exact figures, dates, URLs, direct source tags. Abbreviate common nouns only (co., mgmt., yrs, WLB).
- One bullet = one fact/claim. No bullet restates another.
- Every claim still gets a bracketed source tag, e.g. `[Glassdoor, 2025]`, `[Reddit r/cscareerquestions, 2024]`, `[careers page]` — the tag itself stays exact, never compressed into ambiguity.
- Sections with nothing to report get one line saying so, not padding.

Example of the target density — not "Multiple reviews on Glassdoor and Blind, spanning 2024 to 2025, mention that employees are frequently expected to work unpaid overtime, especially during release crunches" but instead "Unpaid overtime during release crunch, recurring 2024-25 [Glassdoor, Blind]."

Sections, in order:

1. **Snapshot** — 2-3 lines: what the company does, size, founded, funding/public status if relevant.
2. **Tech stack** — what they actually use, broken down by team/role if the user specified one or if postings reveal a split (e.g. backend vs. platform vs. data). Source-tag each stack claim (postings are most reliable for "current"; blogs can be stale marketing).
3. **Culture & work-life balance** — synthesized pattern across sources, not a single quote. Only include a theme if it recurs (e.g. "unpaid overtime mentioned across multiple 2024-25 reviews" is a real signal; one bad review is not).
4. **Red flags** — layoffs, attrition/backfill patterns, management complaints, pay delays, legal/labor issues — anything that recurred across ≥2 independent sources. Be direct and unhedged here.
5. **Interview process** — typical rounds (screen → phone/coding → onsite/panel → offer, or whatever their actual pipeline is), what's asked at each round (DSA/system design/take-home/behavioral mix), reported difficulty, reported timeline (fast vs. weeks of silence), and any recurring complaints about the process itself (ghosting, too many rounds, lowball offers after multiple rounds).
6. **Referrals** — see dedicated guidance below.
7. **Analyst notes** — cross-cutting observations that don't fit neatly in one section above but change how the user should read the rest. This is for signal *correlations*, not new raw facts. Examples of what belongs here:
   - Interview-loop shape as its own tell: e.g. "6+ rounds with comp discussed only at the very end" often co-occurs with the same disorganization/toxicity complaints seen in the culture section — flag that link explicitly rather than leaving the reader to notice it.
   - Whether a referral actually matters *here*: some companies' bottleneck is the resume screen (referral helps a lot); others bottleneck at a specific late round or a slow HR/comp-approval stage (referral barely moves the needle) — say which, if the evidence points either way.
   - Any other pattern connecting two sections (e.g. "the same 'mandatory unpaid overtime' complaint appears in both the culture reviews and the interview-process reviews, describing unpaid take-home assignments").
   - If nothing cross-cutting stands out, say so in one line rather than forcing an observation.
8. **Compensation signal** — rough range if visible (Glassdoor/AmbitionBox/Levels.fyi-style), explicitly caveated as self-reported and noisy.
9. **Verdict / checklist** — a short, opinionated bottom line: green flags, red flags, and 3-5 concrete questions to ask the interviewer to pressure-test the specific red flags found (e.g. if attrition is flagged: "what's this team's average tenure?").

### Referrals (section 6 detail)
A referral is usually the single highest-leverage thing the user can do, so treat this as more than a footnote:
- Check whether the company has a formal **employee referral bonus** — search `<company> employee referral bonus` — a generous/actively-promoted bonus usually means referrals are taken seriously in their hiring funnel (worth pursuing), vs. companies where it's a token gesture.
- Search LinkedIn for people who list the target role/team at that company, especially alumni of the user's own university or people who've posted about the company being open to reaching out — these are realistic cold-referral targets.
- Check Blind/Reddit for "how to get a referral at X" threads — sometimes people post their own referral contact or describe what worked.
- If the company runs an official careers-page "refer a friend" portal or has a public referral-request form/Slack/Discord community, note the link.
- Give 1-2 concrete next actions, not just "network more" — e.g. "search LinkedIn for '<university> <company>' and send a short connect note referencing the specific team."

### Weighing evidence
- A claim repeated independently across ≥2 platforms (e.g. Glassdoor *and* Reddit *and* Blind) is much stronger than a single review.
- Distinguish company-wide patterns from team-specific ones when the source lets you (e.g. "the sales org gets criticized far more than engineering" is more useful than a flat rating).
- Recency matters — leadership, culture, and stack all change. Weight anything in the last 12-18 months over older material, and say so when the evidence is stale.
- The official site/careers page is a source for "what they say", not for "what it's like" — never let it stand in for the culture verdict.

## Other useful signals (mention if relevant, don't force all of them)
- **GitHub org** — public repos reveal real stack/quality/activity if the company open-sources anything.
- **StackShare / BuiltWith** — quick automated tech-stack cross-checks.
- **Levels.fyi** — for US-headquartered or US-office roles, better comp data than Glassdoor.
- **Fishbowl** — another anonymous professional-network source, similar niche to Blind.
- **X/Twitter** — engineers at the company sometimes post about stack or culture directly.
- **Company's own engineering blog / conference talks** — good for genuine tech-stack depth (as opposed to marketing), but still skewed positive — treat as "what they're proud of", not "what it's like day to day".

## Output notes
- Default: write and present a Markdown **file**. If the user's message contains `--inchat`, respond in chat instead — same content, no file.
- Ultra-terse throughout (see density rule above) — headers + fragments, zero walls of prose, zero info loss.
- Always source-tag claims (platform + rough recency), tags stay exact/uncompressed.
- If a section has genuinely little to no data (e.g. tiny/stealth company with no reviews), say so plainly rather than padding it — "No Glassdoor/Blind/Reddit presence — too new/small" is a useful finding.
- End with the verdict/checklist section every time — that's the actual decision-support payload.
