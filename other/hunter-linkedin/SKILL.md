---
name: hunter-linkedin
description: >-
  The LinkedIn Optimizer. Rewrites the user's LinkedIn headline, About,
  skills and experience for the job they want, using only what is true, then
  checks the draft against LinkedIn's field limits (headline, About, skills
  count, position title and description) and against the keywords of the
  target job description, with a before/after report: coverage, required
  terms, what was gained and what is still missing. The user pastes the final
  text into LinkedIn themselves. Use when the user says "optimize my
  LinkedIn", "rewrite my headline", "fix my About section", "LinkedIn for this
  job", "what skills should I list", or "make recruiters find me".
argument-hint: "[job description file]"
---

# hunter-linkedin

Recruiters search LinkedIn by keyword, and the hiring manager will open the
profile before the coffee chat. This skill makes the profile say what the
user really does in the words the job description uses, inside LinkedIn's
limits, and shows the before and after.

What the user typed after `/hunter-linkedin`: `$ARGUMENTS`

Tool in this folder (standard library Python, never touches LinkedIn):

```bash
python3 "${CLAUDE_SKILL_DIR}/profile.py" --help
```

## What it reads and writes

- `hunter/linkedin.json`: `{"current": {...}, "draft": {...}}`, each with
  `headline`, `about`, `skills` (a list) and `experience` (`title`, `company`,
  `description`). Shape and the reel's example: `linkedin.example.json`.
- The target job description as a text file, for example
  `hunter/jd/<role-id>.txt` (copy it from the posting the scout found).
- Truth sources for the check: `hunter/profile.json` skills and the resume
  (`--resume hunter/resumes/<role-id>.md`).
- `limits.json`: the limits and where each one comes from.

## LinkedIn's limits

| Field | Limit | Source |
|---|---|---|
| Headline | 220 characters | widely reported; the editor's live counter is the authority |
| About | 2,600 characters | widely reported; the editor's live counter is the authority |
| Skills | 100 skills | LinkedIn Help 35265: "You can add a maximum of 100 skills to your profile." |
| Position title / description | 100 / 2,000 characters | widely reported |
| Invitation note | 200 characters, 3 a month without Premium | LinkedIn Help 46662 |

`profile.py limits` prints them with their sources.

## The rules

- **Only what is true.** Rewrite and reorder the user's real experience.
  Never add a skill, title, employer, degree, date or number they do not
  have. The check lists every term the draft claims that the resume, the
  profile skills and the current LinkedIn never mention: ask the user about
  each one before it stays.
- **LinkedIn's terms forbid automation.** Its User Agreement (section 8.2,
  quoted on LinkedIn Help a1341387) prohibits bots and automated methods that
  access the site, add contacts or send messages, and software that scrapes
  profiles. So this skill never logs in, never scrapes and never edits the
  profile. The user pastes the text and clicks Save themselves.
- **No promises.** LinkedIn shows profile strength and search appearances in
  the user's own dashboard. This tool measures keyword coverage only and does
  not predict either.

## Steps

1. Get the real profile into `current`: the user pastes their headline,
   About, skills and experience (or saves their profile as a PDF from
   LinkedIn and shares the text).
2. Save the job description as text and read its keywords:

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/profile.py" keywords --job hunter/jd/google-swe.txt
   ```

   Weight 3 means required or minimum qualifications, 2 the body of the
   posting, 1 preferred or bonus.
3. Write `draft`: a headline that says the role and the two or three
   strongest true skills; an About that opens with what the user builds and
   one or two proven results; skills ordered so the required terms come
   first; experience bullets from `/hunter-resume` (a strong verb, a number,
   the outcome).
4. Check and compare:

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/profile.py" compare --job hunter/jd/google-swe.txt --resume hunter/resumes/base.md
   python3 "${CLAUDE_SKILL_DIR}/profile.py" check --job hunter/jd/google-swe.txt --json
   ```

   Exit 1 means a field is over its limit. Fix every OVER line, then ask the
   user about every "Confirm these are true" term.
5. Show the before/after table and the final text, field by field, ready to
   paste. The user pastes it into LinkedIn and saves.

## Example: the reel

Jordan Reyes (fictional) had the default headline "Software Engineer at
Brightline Labs", an empty About and six generic skills. Against a Software
Engineer, Cloud Infrastructure job description, the draft headline becomes
"Software Engineer · Distributed systems, ML infrastructure and fast,
reliable APIs" (82 characters), the About tells the payments API story with
its real numbers (p99 latency down 38% across 4M requests a day), and the
skills put Go, Distributed Systems and System Design first. `compare` shows
keyword coverage 22% before and 86% after, required terms 2/8 to 7/8, and
C++ still missing: the posting asks for it, Jordan does not have it, so it
stays out. Jordan pastes the draft into LinkedIn himself.

## What it never does

- Never invents experience, skills, titles, degrees, dates or numbers.
- Never logs in to LinkedIn, scrapes it, edits a profile or sends anything:
  LinkedIn's terms forbid bots and automated messaging, and this pack obeys.
- Never claims a profile change will get the user hired or found.
