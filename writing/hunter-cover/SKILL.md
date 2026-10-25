---
name: hunter-cover
description: >-
  Cover Letter Writer. Writes a specific cover letter for every application:
  addressed to the hiring manager or the team, opening with something real
  about the company or the team from the research brief, one paragraph of
  proof from the tailored resume (a result with a number), why this team, and
  a clear ask, in 150 to 400 words. Then checks it with cover.py: company,
  role and team named, at least one concrete proof point, no banned cliches,
  no leftover placeholders, no other company's name pasted in, every number
  traceable to the resume, reading level. Use when the user says "write a
  cover letter", "cover letter for Google", "do I need a cover letter", "make
  this letter better", "check my cover letter", or after /hunter-resume.
argument-hint: "[role id]"
---

# hunter-cover

The Cover Letter Writer writes one letter per application, never a template with
the company name swapped. A recruiter should be able to tell in two lines that it
was written for this team, by someone who did the work on the resume.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/cover.py" check hunter/covers/<role-id>.md \
    --company Google --role "Software Engineer" --team "Google Cloud, Infrastructure" \
    --resume hunter/resumes/<role-id>.md --pipeline hunter/pipeline.json
python3 "${CLAUDE_SKILL_DIR}/cover.py" cliches
```

## What it reads and writes

| file | what |
| --- | --- |
| `hunter/pipeline.json` | the role (company, title), the contact (the hiring manager's name), other companies (to catch copy-paste) |
| `hunter/companies/<company>.md` | the research brief from `/hunter-research`: what the team does, recent news |
| `hunter/resumes/<role-id>.md` | the tailored resume: the only source of proof points |
| `hunter/covers/<role-id>.md` | the letter |

## The shape (150 to 400 words)

1. **Greeting to a person.** "Hi Maya," when the hiring manager is known (from the
   pipeline contact), otherwise "Dear <team name> team,". Never "To whom it may
   concern".
2. **Why you are writing, specifically.** One or two sentences tying something real
   (their public post, a product the team ships, a fact from the research brief) to
   something you did. Name the role and the team.
3. **Proof.** Two or three results from the tailored resume, with their numbers,
   chosen for the posting's top requirements. Copy the numbers exactly.
4. **Why this team.** What about their work fits what you want to do next, from the
   research brief, in your words. Facts about the company must be in the brief
   with their source.
5. **The ask.** A next step: a short call, a conversation about the team's plans.
6. **Sign-off** with your name.

## Steps

1. Read the role and contact from `hunter/pipeline.json`, the brief from
   `hunter/companies/<company>.md` and the tailored resume. If there is no tailored
   resume yet, run `/hunter-resume` first.
2. Ask the user one question: why this team, in their own words. The best opening
   lines come from their answer, not from Claude.
3. Draft the letter to `hunter/covers/<role-id>.md`.
4. Run `cover.py check` with `--company`, `--role`, `--team`, `--resume` and
   `--pipeline`. Fix every FAIL. Read every WARN and fix it unless there is a reason.
5. Show the user the letter and the check. They edit; run the check again.
6. When they approve, it goes into the application with `/hunter-apply`, which fills
   the form and stops before Submit. Note it in the pipeline with `/hunter-tracker`.

## The checks (exit 0 when nothing FAILs)

| check | rule |
| --- | --- |
| length | 150 to 400 words |
| greeting | to a person or a team; "To whom it may concern" fails |
| company, role, team | each named (the team: any one part of `--team`) |
| proof | a sentence with a number and an action or result word |
| cliches | none from the banned list (`cover.py cliches`): "team player", "passionate about", "perfect fit", "I am writing to express my interest" and more |
| placeholders | nothing like [Company], {role}, XXX, TODO |
| other names | no other company from your pipeline (a letter copied from another application) |
| numbers | every number is in the resume: nothing invented |
| reading | Flesch-Kincaid grade 12 or lower (WARN) |
| ask | the last paragraph asks for a next step (WARN) |
| openers | under half the sentences start with "I" (WARN) |

## Example: Jordan Reyes to Maya C. at Google

`example-cover.md` in this folder is Jordan's letter for the Software Engineer role
on the Google Cloud Infrastructure team. Maya C. is the fictional hiring manager
from the reel; the opening ties her public post about design reviews to Jordan's
payments rebuild.

```bash
python3 "${CLAUDE_SKILL_DIR}/cover.py" check "${CLAUDE_SKILL_DIR}/example-cover.md" \
    --company Google --role "Software Engineer" --team "Google Cloud, Infrastructure" \
    --resume "${CLAUDE_SKILL_DIR}/../hunter-resume/examples/jordan-after.md"
```

```
Cover letter check (example-cover.md): READY
  PASS  length        217 words
  PASS  greeting      Hi Maya,
  PASS  proof         4 proof point(s), e.g. I rebuilt the payments API, cutting p99 latency 38% across 4M requests a day.
  PASS  numbers       every number is in the resume
  PASS  reading       grade 6.7 (Flesch-Kincaid), 16.5 words a sentence
```

## What it never does

- Never invents an achievement, a number, a reason or a connection to the company.
- Never reuses a letter with the company name swapped: the "other names" check is
  there for that.
- Never flatters with claims about the company that are not in the research brief.
- Never sends or submits the letter. The user does, inside the application.

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
