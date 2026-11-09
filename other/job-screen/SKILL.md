---
name: job-screen
description: Sort the Job Hunt search results into apply / check / dismiss buckets and hide the unfit ones in the dashboard. Use when asked to screen, triage or clean up the Search tab, hide unsuitable vacancies, or build a shortlist before applying. Needs the dashboard running at http://localhost:4321.
---

# job-screen — triage the Search tab

Goal: every card on the Search tab is either worth applying to, or hidden with a
reason. The deterministic part is a script; the judgement part is you.

## 1. Run the rules

```
node scripts/funnel.mjs screen --json <scratchpad>/screen.json
```

Dry run. It prints five buckets, one line per job: `index source match/fit geo
age company — title [location] {salary} <reason> url`.

| Bucket | Meaning | What you do |
| --- | --- | --- |
| `apply` | geo confirmed (Indeed says remote, or Himalayas open to Poland) and nothing in the title disqualifies it | hand to `job-apply` |
| `check` | LinkedIn rows: location unknown or "onsite/hybrid" — LinkedIn omits `is_remote`, so this is unverified, not a rejection | open the posting, decide (step 3) |
| `needs-you` | marketplaces that need an account (lemon.io, Jobgether, GitStart, Proxify, Alignerr…) — accounts are never created by the skill | list for the user |
| `dismiss` | rule hit: junior/mid, management, wrong stack, backend-only, another language, onsite per Indeed, same role already applied to on another board, same role hidden before (by the user — rule-written hides do not count), company hidden for 2+ different roles by hand or marked "company not of interest", second posting of a role already in this search | review; nothing to write — the dashboard already leaves them out |
| `skip` | already in the funnel or already hidden | nothing |

`claude:skip/12` (or `apply/86`, `maybe/60`) is Claude's verdict, made by the
dashboard from the full posting text against `src/verdict-criteria.md`
(src/verdict.ts). A `skip` is already out of the stacks ("Skipped by Claude"); do
not hide it on top — a hide is permanent, and a criteria change may bring the
card back. `maybe` is a card for the user to check, never a hide.

`!…` after a line is a flag, not a verdict: an earlier application at the same
company, or a role that looks like one already applied to. Same-role
applications are flagged rather than dismissed because different levels at one
company (EPAM Lead vs Senior) were applied to on purpose — decide per row.

The rule lists are `SCREEN_TITLE_RULES`, `SCREEN_FRONTEND`, `SCREEN_BACKEND_ONLY`
and `SCREEN_MARKETPLACES` in [src/profile.ts](../../../src/profile.ts); the
mechanics are `decide()` in [src/screening.ts](../../../src/screening.ts). The
dashboard runs the same rules on every search and keeps their hits behind the
"Hidden by rules" toggle, so the Search tab already shows roughly the `apply`
bucket. Edit the rules there, not in prose.

## 2. Review the dismiss bucket

Skim the `dismiss` lines for a reason that is wrong for this title (the rules
are whole-word regexes on the title; a title like "Full Stack Engineer
(Node.js, Preact)" has been mis-filed before). Fix the rule in profile.ts and
re-run. Nothing needs committing: the dashboard and `find_jobs` apply the rules
on every read, and the hits sit under "Hidden by rules" with their reason.
`--commit` would make today's hits permanent hides — don't.

## 3. Decide the `check` bucket — without a browser

```
node scripts/jobs-fetch.mjs --screen <scratchpad>/screen.json --buckets apply,check --out <scratchpad>/fetched.json
node scripts/jobs-fetch.mjs --retry <scratchpad>/fetched.json      # LinkedIn answers 429 — re-fetch the errors
```

One line per posting, read from the board's own JSON (LinkedIn guest API,
Greenhouse, Lever, Ashby, SmartRecruiters, Recruitee, Himalayas search API)
or from the stripped HTML:

`idx | company — title | claude:apply/84 | !low-pay !applied-before | mode «context» | lock:US | senior/8y | +react,typescript | -angular×2 | lang:german | pay:… | apply:<vendor> form:3req "…"`

Decide from the line, in this order:

1. **claude** `skip` → leave it (it is in "Skipped by Claude"); `maybe`, `(old)` or
   `—` → needs-you list. Only `claude:apply` goes on.
2. **!low-pay** / **!applied-before** → needs-you list: the user's call.
3. **mode**, **lock**, **lang**, **-neg** that Claude did not mention → read the
   text of that one job and report what it says. The regexes misfire ("hybrid
   cloud", "remote or hybrid, your choice"); do not hide on them. A giant's
   office in Warsaw (Settings → "My terms") is fine.
4. `CLOSED` → hide: `posting closed`. `ERR` → `--retry`, then decide.
5. **apply:** `portal` (Workday, Cognizant, EPAM, Luxoft), `himalayas-account`,
   `indeed` → cannot be scripted (account) → needs-you list, not hidden.
6. Otherwise it is an `apply` row for `job-apply`.

When the line is ambiguous, print the text of that one job
(`python -c` over `fetched.json`, or `--text` for a single URL) — never the
whole set.

Hide with:

```
node scripts/funnel.mjs dismiss "<url>" --reason "<reason>" --title "<title>" --company "<company>"
```

Hidden means hidden from every future search and from `find_jobs`, and the
screening rules learn from it (same role, same company), so hide only what is
closed or what the user asked to hide.

## Don'ts

- Do not hide a job only because the company rejected a *different* role
  before. The same role already applied to on another board is hidden by the
  rules themselves.
- Do not hide `needs-you` rows — the user may want to apply by hand.
- Do not widen the search here (sources, hoursOld); that is profile.ts.
