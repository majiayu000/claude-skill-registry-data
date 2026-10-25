---
name: hunter-resume
description: >-
  Resume Writer. Rewrites your resume for each role so it reads like the job
  description, using only what is true: it mirrors the posting's own words for
  skills you really have, moves buried results into strong bullets (a number,
  a strong verb, one line), reorders for the role, and asks you about anything
  the posting wants that the resume does not show. Scores the match from 0 to
  100 with a published formula (minimum qualifications, preferred
  qualifications, bullet strength, sections) and runs a truth check that fails
  if the rewrite adds a number or a skill that was not in your original. Use
  when the user says "rewrite my resume", "tailor my resume", "ATS score",
  "beat the ATS", "match my resume to this job", "resume for Google", "improve
  my bullets", or after /hunter-scout picks a role.
argument-hint: "[role id or job URL]"
---

# hunter-resume

The Resume Writer makes one resume per role. The reel's numbers come from the
example in this folder: Jordan Reyes against a Google Software Engineer posting
goes from 54 to 96, and the truth check passes because the rewrite only
reorders and rewords what Jordan's original already said.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/ats.py" terms   --jd hunter/resumes/<role-id>.jd.md
python3 "${CLAUDE_SKILL_DIR}/ats.py" score   hunter/resumes/base.md --jd hunter/resumes/<role-id>.jd.md
python3 "${CLAUDE_SKILL_DIR}/ats.py" compare hunter/resumes/base.md hunter/resumes/<role-id>.md \
    --jd hunter/resumes/<role-id>.jd.md --facts hunter/resumes/facts.md
python3 "${CLAUDE_SKILL_DIR}/ats.py" trace   hunter/resumes/base.md hunter/resumes/<role-id>.md
```

## What it reads and writes

| file | what |
| --- | --- |
| `hunter/profile.json` | `resume_path`: the user's current resume (the source of truth) |
| `hunter/resumes/base.md` | that resume as plain text, one bullet per line |
| `hunter/resumes/facts.md` | facts the user confirmed in chat (numbers, tools, dates), word for word |
| `hunter/resumes/<role-id>.jd.md` | the job description, pasted or saved from the posting URL |
| `hunter/resumes/<role-id>.md` | the tailored resume for that role |
| `hunter/pipeline.json` | a dated note on the role: "resume tailored, ATS 54 to 96" |

## The score (ats.py, 0 to 100)

    score = 50 x R + 20 x P + 20 x B + 10 x S, rounded half up

- **R**, minimum qualifications covered. The posting is read line by line and each
  line's known terms (`terms.json`) are grouped. Terms joined by "or", "e.g." or
  "such as" are a choice (any one covers it); every other term is needed on its
  own. R is the average line coverage.
- **P**, the same for preferred qualifications and responsibilities.
- **B**, bullet strength: a third each for a number, a strong opening verb, and 8 to
  30 words, averaged over the bullets under Experience and Projects.
- **S**, a quarter each for Experience, Education and Skills sections and an email
  or phone number.

A term counts only in the posting's own wording: "Golang" does not count when the
posting says "Go". That is the "reads like the job description" part. Degrees count
in any form (a B.S. is a bachelor's degree). Real applicant tracking systems do not
publish their formulas; this one is stated so the user can check every point. Say
so whenever you quote a score.

## Steps

1. **Get the truth first.** Read the resume at `resume_path` (ask for it if
   missing) and save it as `hunter/resumes/base.md`. Never work from memory.
2. **Get the posting.** Save the full job description to
   `hunter/resumes/<role-id>.jd.md` (role ids come from `hunter/pipeline.json`).
   Run `ats.py terms` to see what it asks for, line by line.
3. **Score the original** with `ats.py score`. Read the report with the user: the
   "Reword" list (they have it, the posting says it differently) and the
   "Missing" list (the resume does not show it).
4. **Ask about the gaps, one question each.** "The posting asks for Kubernetes.
   Have you used it? Where, and how much?" Write every confirmed answer into
   `hunter/resumes/facts.md`. If the answer is no, leave it out. Never add a skill,
   a number, a title, a degree or a date the user has not confirmed.
5. **Rewrite.** Order sections and bullets by what this posting needs most. Each
   bullet: strong verb + what you did + the result with a number. Google's own
   interview tips page puts it as "accomplished X, as measured by Y, by doing Z"
   (google.com/about/careers/applications/interview-tips). Use the posting's words
   for things that are true. Keep employers, titles, dates and degrees exactly as
   in the original. One column, standard headings (Summary, Experience, Education,
   Skills), no tables, text boxes, images or headers and footers, so parsers read it.
6. **Prove nothing was invented.** Run `ats.py compare base.md <role-id>.md --jd ...
   --facts facts.md`. The truth check must say CLEAN. If it lists INVENTED numbers
   or terms, remove them or confirm them with the user and add them to `facts.md`.
   Check every "new capitalized word" it lists by hand.
7. **Show the user** the before and after scores, the changed bullets side by side,
   and what is still missing and why it stays missing. The user approves the file.
8. **Record it** with `/hunter-tracker` (`pipeline.py update-role <role-id> --notes
   "resume tailored, ATS 54 to 96"`), then `/hunter-cover` for the letter.

## Example: Jordan Reyes and the Google posting

The files are in `examples/`. `google-swe-jd.md` is written in the format of
Google's public postings (minimum and preferred qualifications, responsibilities);
it is not a real posting.

```bash
python3 "${CLAUDE_SKILL_DIR}/ats.py" compare "${CLAUDE_SKILL_DIR}/examples/jordan-before.md" \
    "${CLAUDE_SKILL_DIR}/examples/jordan-after.md" --jd "${CLAUDE_SKILL_DIR}/examples/google-swe-jd.md"
```

```
Before 54 -> after 96
  R  0.62 -> 1.00
  P  0.50 -> 0.85
  B  0.29 -> 0.94
  S  0.75 -> 1.00
Truth check: CLEAN. Every number and skill in the rewrite is in the original.
```

The three rewrites from the reel, each built only from facts in the original's
summary line:

| before | after |
| --- | --- |
| Worked on backend services | Rebuilt the payments API in Go, cutting p99 latency 38% across 4M requests a day |
| Helped with machine learning projects | Shipped an ML ranking service that lifted search click-through 12% |
| Responsible for on-call | Led on-call for 9 services and cut pages 60% with automated runbooks |

What keeps it at 96 and not 100 is honest: Jordan has no master's degree, the
original says nothing about mentoring or documentation, and the intern bullet has no
number to give. Those stay as they are.

## What it never does

- Never invents experience, titles, degrees, dates, employers or numbers.
- Never hides keywords (white text, tiny fonts, pasted job descriptions) or copies
  the posting's sentences into the resume.
- Never claims the score is what a company's tracking system will see.
- Never sends or uploads the resume. `/hunter-apply` attaches it to a form the user
  submits.

## Consent and truth

- Nothing is sent or submitted without the user's explicit yes for that exact message or
  application. Claude drafts, the user approves, then it goes out from the user's own
  accounts: email as a Gmail draft first; LinkedIn messages through Claude in Chrome with
  the user present, one at a time, at human pace, the user clicking Send; application forms
  filled and left for the user to submit.
- No bulk or automated messaging, no scraping behind logins, no tricks around a site's
  limits. LinkedIn's terms forbid bots and automated messaging.
- Contact research uses public professional information only (the person's public profile,
  talks, posts, papers, the company site), never personal life, family, home address or
  private accounts. Email addresses are guesses from public patterns, marked with a
  confidence, never called verified unless found published.
- Stop rules: stop at the first "no" or any sign of disinterest, max 2 follow-ups, no message
  after 21 days of silence, and a request to stop is honoured forever.
- Never invent experience, titles, degrees, dates or numbers: rewrite and reorder what is
  true, and ask when something is missing.
- Salary benchmarks and interview material cite their sources. Nothing here guarantees an
  offer or an outcome.
