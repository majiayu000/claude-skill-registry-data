---
name: seekter-init
description: Set up Seekter for a new candidate. Interviews the user one question at a time and writes profile/profile.md, profile/search.json and profile/documents/. Use when the user runs /seekter-init, says "set up seekter", or when profile/profile.md is missing.
---

# /seekter-init — build the candidate profile

The goal is a complete `profile/profile.md` (from `templates/profile.md`) and `profile/search.json` (from `templates/search.example.json`). Every other Seekter skill reads only these files, so nothing may be guessed here: a value the user didn't give stays `ASK`.

## Rules for the interview

- **One question per message.** Short, plain, in the user's language. Offer choices with the question tool when the answer is one of a few options; free text otherwise.
- **Draft, then confirm.** If a CV (or a LinkedIn profile saved as PDF) is available, read it first and turn questions into confirmations ("Your CV says 8 years in this field. Correct?"). Never write a value from the CV without the user confirming it.
- **Skippable.** "Skip" or "later" writes `ASK` and moves on. Sensitive items (birth date, ethnicity, disability, gender, salary history) default to "prefer not to say" unless the user volunteers a value.
- **Resumable.** After each answered section, save progress to `profile/.init-state.json` (`{"done": ["identity", ...], "answers": {...}}`) and write what's known into `profile/profile.md`. On restart, read the state file, say where you're resuming, and continue.
- **Explain once why** at the start, right after the disclaimer: "I'll ask about 40 short questions in 9 groups. Everything stays in `profile/`, which git ignores."
- Don't ask what you can derive: timezone from city, ASCII fallback from name, E.164 phone from local number + country.

## Order

**Before anything else: the disclaimer.** Show this, as one message, before creating a folder or reading a file:

> Before we start: Seekter sends applications in your name and you are responsible for what they say, the terms of the job sites you use are yours to follow, and it runs on your own paid Claude plan with no guarantee of results. Details are in [DISCLAIMER.md](DISCLAIMER.md). Shall we continue? (yes / no)

- **No**, or anything that is not a yes: stop. Create nothing, write nothing, and say they can run `/seekter-init` again whenever they want.
- **Yes**: keep the date in `profile/.init-state.json` and write it to the profile's `Disclaimer accepted:` line when the profile is first written. Then continue.
- Don't paraphrase it into something softer or longer, and don't ask it again on a resumed run that already has the date.

0. **Setup check.** Create `profile/`, `profile/documents/`, `applications/`, `runs/` if missing. If `profile/profile.md` already exists, ask: update section by section, or start over (keep a copy as `profile/profile.backup-<date>.md`).
1. **Documents first** (they make the rest faster). Ask for the CV file path(s). Copy them into `profile/documents/` keeping the file name. Ask which is the default and whether another CV is for a different role type. Optional: portfolio PDF.
   Read the CV and pre-fill a draft of §1, §3 (employer, years, education), §8 (work history, facts, stack, certifications).
2. **Identity and contact (§1).** Name as written on the CV, first/last split, **the one email to use in every form**, phone, city + country + postcode, nationality, languages with levels, portfolio / LinkedIn / GitHub / other links, case-study URLs.
3. **Targets (§5).** Titles to apply for (suggest from CV), titles and seniority to exclude, management vs individual contributor, a one-paragraph recruiter statement (draft it, let them edit).
4. **Location and work model (§6).** Work authorization (where they may legally work today). For the home country: on-site / hybrid / remote allowed, and city exceptions. Relocation: yes/no, which countries in priority order, conditions (only with sponsorship?), regions never to relocate to.
5. **Money (§4).** Bands by employer region (monthly or annual, gross or net, currency). Minimum acceptable. Freelance rate if relevant. Salary history answer (a number or "prefer not to say").
6. **Standard answers (§3).** Notice period, contract types (employee / contractor / EOR), VAT or company registration, sponsorship need for remote vs relocation, non-compete, background questions, references, education search terms, AI-usage level, consents. Demographics last, with "prefer not to say" as the first option.
7. **Boundaries (§7).** Sectors never to apply to (offer: gambling/betting, adult, weapons/defense, tobacco, crypto, fast fashion, none). Companies to never apply to. Sectors to ask about first.
8. **Fact bank and stories (§8).** Walk through each job on the CV and ask for **2–3 concrete facts** each (a number, a product, a decision, a tool combination). Then ask for 3 short stories for behavioural questions: a time they were wrong, a conflict, a failure, a system they built outside work. Only facts and stories captured here may appear in applications.
9. **Voice (§9).** Show two short sample answers in different registers and ask which sounds like them. Ask for phrases they hate. Ask about punctuation habits (em dashes, exclamation marks) and US vs UK English.
10. **Search config.** Build `profile/search.json` from the template. **Every search value is theirs; the template ships the keys empty on purpose, so fill them from this candidate's field and geography rather than from an example.**
    - freehire `queries` (their target titles, lowercase) and `categories`: don't guess the taxonomy — run `curl -sS -A seekter "https://freehire.me/api/v1/jobs/facets?q=<their main title>"` and pick the categories that actually carry their field, then show them the counts.
    - `regions` and `home_country` from §6; `languages` from §1.
    - `title_keep`: the title families worth opening. `title_drop`: wrong seniority **plus the other industries that share their job title** — ask them which ones ("who else calls themselves this?"), because they know their field's collisions and you don't. The template's `_title_filters` comment holds a worked example from another discipline; use its shape, not its words.
    - LinkedIn `searches`: one row per title family × geography (`keywords`, `location` for the alert, `geo_id` from the table in `reference/sources/linkedin.md`, `remote` per §6), plus a second row without the remote flag for any geography where they can work on-site. Each row is a job alert **they** create on LinkedIn, delivered by **Email**, and in `read` mode also a search Seekter runs. Apply the alert-quality rules from the same file while building the rows (no quotes, one row per title variant, EEA leaves out the UK and Switzerland, narrow beats broad because a digest mail shows only about six postings).
    - LinkedIn `mode`: ask, and say this first, in plain words: "Seekter never fills Easy Apply and never takes an action on LinkedIn. By default it doesn't open LinkedIn at all: it reads your job-alert emails and any links you give it. It can also read LinkedIn searches and job details itself, with a daily limit and pauses, and it turns that off at the first warning. That is still against LinkedIn's terms, and LinkedIn can restrict accounts that do it. The risk is to your account. Do you want it on?" `email` unless they say yes; on a yes, write `read` and quote their answer in the profile's §10.
    - `boards`: ask which boards they already read. A niche board for their own discipline beats every generic remote board (`reference/sources/_core.md`, the report card). Every board they name needs a file in `reference/sources/`; a board with no file has never been measured.
    Show the finished list and let them trim it.
11. **Tracker import (optional).** Ask whether they already track applications somewhere. Notion or any spreadsheet → export as CSV → `python3 scripts/import_csv.py <file>.csv --dry-run`, show the counts, then run it for real. This is what makes dedup work from day one.
12. **Finish.** Write the final `profile/profile.md` (fill §10–§12, set "Last updated"), delete `profile/.init-state.json`, run `python3 scripts/seekter.py index`, then print:
    - which fields are still `ASK` (each one line),
    - the browser prerequisite (Claude in Chrome extension, with their webmail logged in in the same Chrome),
    - the LinkedIn alerts to create by hand, one line each from `linkedin.searches`, delivered by Email,
    - that they can drop links they find into `profile/links.txt` (or paste them in chat) and those are filled first,
    - the next command: `/seekter-run`.

## Writing the files

- `profile/profile.md`: copy `templates/profile.md`, replace every `{{…}}`. Remove table rows that don't apply rather than leaving placeholders. Leave no `{{` in the finished file (check with grep).
- `profile/search.json`: valid JSON (check with `python3 -m json.tool`).
- Keep the user's exact words for rules they state; quote them in the profile, as they're the ground truth later.
