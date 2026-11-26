---
name: jd-match
description: Match a resume against a specific job description, giving a transparent match score, requirement-by-requirement evidence map, gaps sorted into "fix on resume" vs "learn in 7 days" vs "can't close quickly", tailored bullets (no fabrication), and a 7-day plan to close the gaps before applying or interviewing. Use when the user pastes a job description or JD link, asks "am I a fit for this role", wants to tailor their resume to a job, or prepare for a specific company's role.
---

# JD match

A job description is the exam paper, handed over in advance. This skill reads it properly, maps the candidate's real evidence against it, and turns the gaps into a plan.

## 0. Inputs

1. Call the Skill tool with "cracked-profile" (resume path, level).
2. Get the **job description**: pasted text, a file, or a URL (fetch it if you have a web tool; otherwise ask them to paste it).
3. Call the Skill tool with "company-intel" for the JD's company, unless it's unnamed or a staffing agency. Its process and DSA focus feed the "likely interview questions" and 7-day plan below.
4. Get the **resume** (same reading rules as the `roast-my-resume` skill: PDF/DOCX/LaTeX/MD/text). Also accept extra evidence the resume doesn't show ("I also know Docker from my internship"), and note that it isn't on the resume yet.

## 1. Decode the JD

Extract into a table:

| # | Requirement | Type | Weight |
|---|---|---|---|

- **Type**: `must` (stated as required, or repeated), `nice` (preferred/bonus), or `implicit` (not stated but obvious from the role, e.g. Git, DSA for SDE roles, SQL for backend).
- **Weight**: 3 for must, 2 for implicit, 1 for nice.
- Also pull out the **seniority signals** (years, "own", "lead"), **interview hints** (the stack implies likely questions), and **ATS keywords**, using the exact phrasing in the JD.

Note anything unusual: unrealistic requirements for the level, bond or service-agreement mentions, or a mismatch between title and responsibilities.

## 2. Evidence map

For each requirement, find the strongest evidence in the resume or extra evidence:

| Requirement | Evidence | Strength |
|---|---|---|
| REST APIs (Node.js) | "Built order APIs…" (Projects › ShopKart) | ✅ strong |
| Docker | mentioned verbally, not on resume | 🟡 hidden |
| Kubernetes | none | ❌ missing |

Strength: `strong` (demonstrated with context) = 1.0, `weak` (listed in skills only) = 0.5, `hidden` (true but not on the resume) = 0.5, `missing` = 0.

**Match score** = Σ(weight × strength) / Σ(weight), shown as a percentage *with the formula visible*, so the candidate can trust it. Then interpret it: ≥ 75% apply confidently · 55–75% apply after the fixes below · < 55% a stretch, so apply only if the "can't close" list is short.

## 3. Gap triage

Sort every non-strong item into exactly one bucket:

1. **Fix on resume (today)**: they have it but it's hidden or weak. Give the exact rewritten bullet or skills line. **Only use real experience.** Missing numbers become placeholders.
2. **Learn in 7 days**: closable fast enough to talk about credibly (a tool, a library, a concept). For each, name a concrete mini-project or exercise that produces *evidence*, not just "watch a tutorial".
3. **Can't close quickly**: years of experience, deep specialisations. Advise how to address it honestly if it comes up in the interview.

## 4. Output

1. Match score and interpretation.
2. Evidence map table.
3. Tailored resume edits (before → after), plus the ATS keywords to add, where true.
4. **7-day plan**: a day-by-day table mixing gap-closing work with role-specific interview prep. Example: day 3, "Dockerise your ShopKart backend and push the image; add one bullet." Day 6, "Run /mock-interview on graphs, which this team's domain implies."
5. **Likely interview questions** for this JD: 5 technical (from the stack, plus the company's most reported DSA topics) and 2 behavioral (from its values), each labelled with where it came from.
6. Save everything to `$CRACKED_DIR/jd/<company>-<role>.md` and mention the path.
7. Log a scorecard via the Skill tool with "cracked-profile", titled `<Role> @ <Company>`. Dimensions: **Must-haves, Implicit Skills, Nice-to-haves, Resume Alignment**. Overall = match score / 10.

## Rules

- No fabrication, ever. Recommending someone claim a skill they don't have gets them rejected in the interview, or fired later.
- Quote the JD's exact wording for keywords. ATS matching is often literal.

---

*Skill calls:* if your agent has no Skill tool, open the named skill's `SKILL.md` in the cracked skills folder (`core/`, `interview/`, `profile/`, `strategy/`) and follow it instead.
