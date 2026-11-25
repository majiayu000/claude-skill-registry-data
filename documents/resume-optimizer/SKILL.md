---
name: resume-optimizer
description: Tailor a resume to a specific job opening so it passes applicant tracking systems (ATS) and reads well to recruiters. Use when a user uploads a resume (PDF, DOCX, TXT or pasted text) and provides a job posting link or job description, and asks to polish, tailor, optimise or make the resume "AI ready" / "ATS ready" for that role or for online submission.
license: MIT
version: 1.3.1
---

# Lionel Resume Optimizer

Tailor one person's real resume to one real job opening. The output is an
honest, ATS-safe resume that surfaces what the candidate already has and
matches how the job posting actually describes the work.

Never fabricate. No invented employers, titles, dates, degrees, tools,
certifications or metrics. A polished lie fails the interview and can get
the candidate blacklisted. Every change must trace back to the original
resume or to something the user confirms in the session.

## Inputs

Collect both before you start. Ask for whichever is missing; do not guess.

1. **The resume** — a file (PDF, DOCX, TXT, MD) or pasted text.
2. **The job opening** — a posting URL, or the job description pasted as
   text. Pasted text is always acceptable; many job boards block fetching.

## Workflow

### 1. Extract the resume text

- TXT / MD: read directly.
- PDF / DOCX: use whatever document reader is available in your
  environment and confirm the extracted text with the user if names,
  dates or bullet structure look garbled. Extraction errors become
  resume errors, so check headings and dates line by line.
- Keep the original file untouched. Work on a copy.

### 2. Get the job description

- If given a URL, fetch the page and extract the posting text: title,
  company, location, responsibilities, requirements, skills and tools.
- Job boards (LinkedIn, Indeed, Glassdoor and similar) often block
  automated fetching or hide the posting behind a login. If the fetch
  fails or returns a login wall, say so plainly and ask the user to
  paste the job description text. Never reconstruct a posting from the
  URL, the company name or your training data.
- Save the posting text to a file so every later step cites the same
  source.

### 3. Parse the job description

Write down, from the posting text only:

- Role title and seniority level
- **Must-haves vs nice-to-haves, split explicitly** — must-haves come
  from the Requirements/Qualifications section; treat them as the
  screening gate and track their coverage separately
- The 10–20 hard skills, tools and methods the posting names
- The responsibilities, in the posting's own verbs
- Required qualifications (degree, years, certifications, languages)
- Repeated phrases — repetition signals what the screener weights most

Read `references/keyword-method.md` before this step.

### 4. Score the resume before touching it

Run the bundled scorer for a deterministic baseline:

```bash
python3 scripts/resume_optimizer.py score --resume resume.txt --job job.txt
```

It reports keyword coverage, missing keywords, section checks (summary,
experience, education, skills, contact) and format red flags. Show the
user this "before" picture. Read `references/ats-playbook.md` for what
the checks mean.

### 5. Build the gap list — three buckets, kept separate

1. **Present but buried** — the candidate has it, the resume hides it
   (wrong words, deep in a bullet, in a paragraph). Fix: surface it.
2. **Rephraseable** — same work, different vocabulary. The posting says
   "stakeholder management", the resume says "worked with clients".
   Fix: use the posting's term where it is truthfully the same work.
3. **Genuinely missing** — the candidate does not have it. Fix: none.
   List it as a gap for the user to see. Never write it into the resume.

Show the user the three buckets before rewriting. This list is the
audit trail that keeps the rewrite honest.

### 6. Rewrite

Follow `references/rewrite-rules.md`. In short:

- **Summary**: 3–4 lines, tailored to this role — title language from
  the posting, the candidate's strongest matching proof, one quantified
  result if the original resume has one.
- **Bullets**: action verb + what was done + measurable result. Use
  numbers only from the original resume. Where a bullet has no number
  and one plausibly exists, mark it `[add metric: …]` for the user to
  fill in — never invent the number.
- **Skills section**: reorder so the posting's matching skills come
  first; group as the posting groups them; drop nothing true.
- **Headings**: standard ATS headings only — Summary, Experience,
  Education, Skills, Certifications. No creative heading names.
- Mirror the posting's exact terms for tools and skills the candidate
  genuinely has ("Power BI", not "data dashboards tool"). Do not stuff:
  a keyword appears where the work is described, not repeated in lists.

### 7. Format for machines first, humans second

Apply the formatting rules in `references/ats-playbook.md`:

- Single column. No tables, text boxes, graphics, icons, photos,
  headers or footers — parsers drop or scramble them.
- Standard fonts (Calibri, Arial, Georgia, Helvetica), 10–12pt body.
- Dates as `Jan 2023 – Present` or `2023 – Present`, consistent.
- File name: `Firstname-Lastname-Role.pdf` (and a DOCX twin; some
  portals parse DOCX more reliably).
- Contact block as plain text lines: name, city, email, phone,
  LinkedIn URL spelled out.

### 8. Score again and deliver

Re-run the scorer on the tailored resume. Build the outputs from
`templates/` (tailored-resume.md for the resume, delivery-report.md
   for the report, cover-note.md when Bucket 3 gaps are worth addressing
for the report). Deliver:

1. The tailored resume (Markdown, plus PDF/DOCX if your environment
   can produce them).
2. Before / after: ATS keyword score, must-have coverage, and what
   changed.
3. The three-bucket gap list, with bucket 3 (genuine gaps) stated
   plainly so the user can decide — apply anyway, address in a cover
   note, or upskill first.
4. A submission checklist: right file name, right format for the
   portal, keywords in the online form fields matching the resume.
5. A LinkedIn headline aligned with the target role, using only
   claims the resume supports — recruiters cross-check the two.
6. A 3-line recruiter note the user can paste with the application,
   built only from facts already in the resume.

## Guardrails

- **No fabrication, ever.** Not a metric, not a tool, not a date.
- **No keyword stuffing.** Hidden text, white-on-white keywords and
  repeated skill lists are detectable and disqualifying.
- **The user approves the final text.** Show the tailored resume and
  the gap list; the user submits. Never submit an application on the
  user's behalf without their explicit go on the exact final version.
- **Privacy.** A resume is personal data. Process it in the session,
  share it nowhere the user did not ask for, and do not retain copies
  beyond the deliverables the user asked for.
- **One job, one tailoring.** A resume tailored to one posting is not
  generic. Say so, and re-run from step 3 for a different opening.

## Bundled tools

- `scripts/resume_optimizer.py` — stdlib-only Python 3.
  - `keywords --job job.txt` — extract ranked candidate keywords and
    skills from a job description.
  - `score --resume resume.txt --job job.txt` — keyword coverage,
    section checks and format red flags, as text or `--json`.
- `references/ats-playbook.md` — how ATS parsing works and the
  formatting rules that survive it.
- `references/keyword-method.md` — extracting and placing keywords
  honestly.
- `references/rewrite-rules.md` — summary and bullet rewrite formulas,
  action-verb bank, quantification rules.
- `templates/` — the tailored-resume skeleton, the delivery-report
  format, and a cover-note template for addressing genuine gaps honestly
  format every run produces.
- `PROMPT.md` — the no-install version: one paste-ready prompt that
  runs this same workflow in any AI chat.
- `examples/` — a sample resume, a sample job description, the scorer's
  report on them, and a before/after bullet excerpt.
