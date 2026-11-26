---
name: roast-my-resume
description: Brutally honest tech resume review calibrated to the candidate's experience level, target market and target company. It gives an ATS score with a parse check, a 6-second recruiter scan, and a line-by-line hiring-manager roast, then rewrites weak bullets into impact bullets without inventing anything. Reads PDF, DOCX, LaTeX, Markdown or pasted text. Use when the user wants a resume review, CV feedback, a resume roast, an ATS check or ATS score, better bullet points, or a resume ready for placements, a specific company, or tech jobs.
---

# Roast my resume

Recruiters spend seconds on a resume. Show the candidate exactly what those seconds look like, judged against **people at their level competing for the same jobs**, then fix it, honestly and specifically, without inventing a single fact.

## 0. Setup

1. Call the Skill tool with "cracked-profile". Status, graduation year, country and targets decide the bar.
2. **Company mode**: if the user names a company (or a job description), call the Skill tool with "company-intel" and judge against its resume screen. If there's a JD, also run the checks from `jd-match` §1–2 inline. No company named? Don't ask. Judge against the profile's target tier.
3. Get the resume: the profile's `resume` path, a path the user gives, or pasted text.
   - **PDF**: read it directly if your file tool supports PDFs, **and** extract the plain text the way an ATS would: `pdftotext -layout file.pdf -`, else `python3 -c "import pypdf…"` if installed, else `textutil -convert txt -stdout` (macOS). If extraction fails or comes out scrambled, that's ATS finding #1. PDFs exported from Canva, Figma or heavily designed templates often extract badly (text as outlines, wrong reading order). `pdftotext` is the check, and say that's what you used.
   - **DOCX**: `textutil -convert txt -stdout file.docx` (macOS), `pandoc`, or unzip `word/document.xml`.
   - **LaTeX / Markdown / text**: read directly.
4. Tone: **savage** by default. Switch to **gentle** only if they ask.

## 1. Calibrate the bar

State the bar in one line before roasting, filled from the profile, for example `Judging as: <graduation year> CS grad · India · product companies (SDE-1) · competing with ~top 20% of campus applicants.` Use [CALIBRATION.md](CALIBRATION.md) for what "good" looks like at each level and market. Be brutal **relative to that bar**:
- A second-year student with one solid project isn't "weak". Roast them against second-years.
- A final-year student targeting big tech with tutorial clones and no DSA proof *is* weak. Say so plainly.
- An engineer with 2 years' experience who still lists college projects first gets roasted for it.

If you know the current market conditions for their target (e.g. a slow fresher market), factor them in and say how. Don't invent market statistics.

## 2. Pass 1: ATS check and score

Apply [RESUME-RULES.md](RESUME-RULES.md) § ATS and compute a **heuristic ATS-readiness score out of 100**. Call it that: real ATS products don't publish a score, so this is cracked's checklist, not what any ATS will show. Show the breakdown so it's not a magic number:

| Check | Points |
|---|---|
| Text extracts cleanly, in the right reading order (no columns, tables or text boxes scrambling it) | 25 |
| Standard section headings detected | 15 |
| Contact info in the body (email, phone, LinkedIn, GitHub), and all of it parseable | 10 |
| Role keywords present (from the JD, the company brief, or the standard keyword set for the target role) | 25 |
| Dates and titles in a consistent, parseable format | 10 |
| No images, icons or graphics carrying content; standard fonts; sensible file name | 10 |
| Length fits the level (1 page for students and freshers) | 5 |

List the **missing keywords** that are actually true for them, and that they could add.

## 3. Pass 2: 6-second recruiter scan

Describe honestly what a recruiter sees in 6 seconds: where the eye lands, the 3–5 things they'd notice, and whether they'd keep reading. Be concrete, e.g. "Your eye lands on 'Hobbies: cricket' before your internship."

## 4. Pass 3: the roast, line by line

Go section by section. For each weak line: quote it → say what's wrong → give the fix. Apply [RESUME-RULES.md](RESUME-RULES.md) § Bullets.

In **savage** mode, be sharp and funny about the *writing*, never the person: "'Worked on a website' tells me less than your Wi-Fi password." Every roast line **must come with a fix**. A roast without a fix is just being mean.

Always flag:
- Responsibility bullets with no impact ("Responsible for…", "Worked on…", "Helped with…").
- Skill dumps with no evidence; proficiency bars and ratings; skills they can't defend in an interview.
- Tutorial-clone projects (todo, weather, Netflix clone) with no twist, users or depth.
- Missing proof that matters for their target: DSA ratings for product and big tech, deployed links for startups, internships for experienced roles.
- Inconsistent dates, tenses or formatting; typos; wrong length for the level.
- Missing or dead links (check them with `curl -sI` if you have a shell).

## 5. Rewrite

Rewrite every weak bullet using **Action verb + what you built + how (tech) + measurable result**.
- **Never invent numbers, users or outcomes.** Use `[N]` / `[X% faster]` placeholders, then list the questions they must answer to fill each one.
- Every claim must survive an interview. If they can't explain it, it doesn't go on the resume.

## 6. Output

1. **Verdict**: "Shortlisted for <target> at <tier/company>? Yes / Borderline / No", plus the one-line reason.
2. **ATS score** with its breakdown and missing keywords.
3. **Top 5 fixes**, ordered by impact on shortlisting.
4. **Before → after** table of rewritten bullets.
5. **Placeholder questions** to fill in.
6. **Where you stand**: one honest paragraph on how they compare with the competition at their level, and the single biggest lever (often "one deployed project with real users" or "a contest rating").
7. Offer to write the improved resume to `$CRACKED_DIR/resume/resume-<date>.md`, or to edit their LaTeX/Markdown source directly (only with explicit permission). For a company-specific version, point to `/resume-blueprint <company>`.
8. The scorecard, via the Skill tool with "cracked-profile". Dimensions: **ATS-Readiness** (ATS score / 10), **Impact, Relevance, Projects, Clarity & Format**. Weak-spot tags: `resume-metrics`, `resume-ats`, `resume-projects`, `resume-keywords`.

---

*Skill calls:* if your agent has no Skill tool, open the named skill's `SKILL.md` in the cracked skills folder (`core/`, `interview/`, `profile/`, `strategy/`) and follow it instead.
