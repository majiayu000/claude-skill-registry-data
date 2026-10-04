---
name: job-opening-finder
description: Given a company name (and the user's resume/background), compiles an exhaustive, verified list of that company's currently-open job postings that fit the user, across the company's official careers page, LinkedIn Jobs, Indeed, Naukri, and common ATS platforms (Greenhouse, Lever, Workday, Ashby, SmartRecruiters). Trigger this whenever the user asks to "find openings at", "what roles are open at", "compile positions at", "find me a job at", or wants "all the current openings" or "matching roles" at a named company. Always ask clarifying questions (location/remote preference, role level or track, visa/sponsorship needs, and anything else ambiguous) BEFORE searching, using the ask_user_input_v0 tool — narrowing first prevents wasted, over-broad results. Do not confuse this with company-recon (which investigates culture/tech-stack/interview-process at a company) — this skill's job is finding and listing actual current openings.
---

# Job Opening Finder

Given a company and the user's resume, finds every currently-open role at that company worth the user's attention — not a curated top-3, an exhaustive and verified list.

## Step 1 — Get the resume
- Check whether the user's resume/background is already available (memory, an uploaded file, or earlier in the conversation). If so, use it — don't make the user repeat themselves.
- If no resume/background is available anywhere, ask for it (paste, upload, or a quick summary of role/level/stack) before proceeding. You cannot judge "fit" without it.

## Step 2 — Ask clarifying questions FIRST (before searching)
Always use `ask_user_input_v0` for this — don't just write prose questions, and don't skip this step even if the request seems simple. Narrowing first avoids burning search budget on an overly broad pass. Cover whatever is actually ambiguous, typically:
- **Location / work mode** — specific countries/cities the user is open to, or remote-only, or "onsite is fine anywhere they have an office." If the user's profile already states relocation preferences, pre-fill that as the likely default option rather than asking from scratch.
- **Role / track**, if the resume spans more than one plausible track (e.g. backend vs. full-stack vs. DevOps, or IC vs. anything else) — ask which track(s) to include.
- **Level**, if ambiguous from the resume (new-grad/entry vs. 1-3 YOE vs. senior) — don't guess if the resume could plausibly straddle two levels.
- **Visa/sponsorship need**, if the user's location and the company's likely office locations don't obviously match — this changes which postings are even viable and is worth one question rather than an assumption.
- Skip any question whose answer is already obvious from the resume or from what the user already said — don't ask things you can infer.

Only proceed to Step 3 once you have answers.

## Step 3 — Exhaustive search
Search all of the following for the company — don't stop at the first source that returns results, since companies often split postings across several of these and no single one is complete:

1. **Official careers page** — the primary, most authoritative source. Search `<company> careers` and also check if they use a hosted ATS (very common): search `site:boards.greenhouse.io <company>`, `site:jobs.lever.co <company>`, `site:jobs.ashbyhq.com <company>`, `<company> workday jobs`, `<company> smartrecruiters`. Many companies' "real" job board lives on one of these even if their marketing site links elsewhere.
2. **LinkedIn Jobs** — search `<company>` on LinkedIn Jobs; this often surfaces postings not yet indexed elsewhere, and shows applicant counts/posting age.
3. **Indeed** and, for India-based searches or India-founded companies, **Naukri** — both frequently have postings mirrored from the ATS but occasionally have exclusives or better date-stamps.
4. **Wellfound/AngelList** if the company is a startup.
5. Any company-specific job board mentioned on their engineering blog or Twitter/X (some companies post engineering-specific openings there first).

For each posting found, fetch the actual page (not just the search snippet) to confirm:
- It is still open (not expired/filled — check for "no longer accepting applications" or a stale posted-date with no application deadline extension).
- The real requirements/location/team, since titles alone are often misleading.
- Note the **last-verified timestamp** for each (i.e., when you actually fetched and confirmed it) — this list can go stale within days, so the date matters.

If a listing turns up in search but you cannot fetch/confirm it's still live, include it in a clearly separate "unverified" bucket rather than dropping it or silently treating it as confirmed.

## Step 4 — Match against the resume and preferences
For each verified opening:
- Filter out roles that don't fit the location/track/level answers from Step 2.
- For the remaining set, note *why* it fits (or is a stretch) — specific overlaps between the posting's requirements and the resume (shared languages/frameworks, relevant project type, years-of-experience match), not just "seems related."
- Keep the list exhaustive within the filtered criteria — the goal is completeness, not a top-3 curation. If 15 roles match, list 15.

## Step 5 — Output
Default to a Markdown **file** (write + present it), same convention as company-recon: add `--inchat` anywhere in the user's message to get it inline in chat instead.

Write in **ultra-terse mode** (caveman-ultra style) — minimum words, zero information loss:
- Drop articles, filler, hedging, pleasantries. Fragments over sentences.
- Never abbreviate/compress: job titles, company/team names, URLs, dates, exact requirements you're matching against. Abbreviate only common nouns (yrs, mgmt., WLB, sr./jr.).
- One line per posting: **title — location/mode — 1-fragment fit reason — source, last-verified date — [link]**. No paragraph per posting.
- Group postings by team/function only if there are enough to warrant it (Backend, Platform, Data), else one flat list sorted by fit.
- A short **"Unverified"** section at the end for anything that didn't pass the live-check in Step 3 — same terse format, don't drop or blend into the main list.
- One line at top: search date + total count found. That's the entire preamble — no throat-clearing.

Example target density — not "This role appears to be a strong match because it requires 2-3 years of experience with Go and distributed systems, which aligns well with your background" but instead "Backend Eng II — Ahmedabad/Remote — Go + distributed sys match — LinkedIn, verified 31 Aug — [link]".

## Notes
- "Exhaustive" means covering all the sources in Step 3, not padding the list with irrelevant roles — a company with 3 real matching openings should get a report with 3 openings, not 3 plus 10 loosely-related ones.
- Re-running this later for the same company is expected and useful (postings change); don't assume a prior run is still accurate.
