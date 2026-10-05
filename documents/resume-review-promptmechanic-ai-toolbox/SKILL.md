---
name: resume-review
description: Critically review a resume/CV against ATS (applicant tracking system) parsing rules, recruiter skim patterns, and keyword alignment with a target job description. Use when the user asks to "review my resume/CV", "check my resume against this job ad", "will this pass ATS", or shares a resume file (.docx/.pdf/.md) for feedback. Provides scored, prioritised, critical feedback — not a rewrite.
---

# Resume Review

Deliver **critical, prioritised feedback** on a resume, grounded in documented behaviour of automated screening systems and recruiter reading patterns. Be a tough reviewer, not a cheerleader: the user needs findings they can act on, ranked by how likely each is to cost them an interview. Do not rewrite the resume unless asked — review first, offer the rewrite after.

## Step 1 — Ingest

1. Locate the resume file (ask if ambiguous). Extract full text:
   - `.docx`: unzip and parse `word/document.xml` — join all `<w:t>` runs per `<w:p>` paragraph (pandoc/python-docx often absent; stdlib `zipfile` + regex works everywhere). Also note structural elements: `<w:tbl>` (tables), `<w:drawing>`/`<w:pict>` (images/text boxes), headers/footers (`word/header*.xml`, `word/footer*.xml`), `<w:pageBreakBefore>`/`<w:br w:type="page"/>` (page structure).
   - `.pdf`: Read the file directly (the Read tool renders PDFs); note any text that appears only in images.
2. If a target job description is available (file, URL, or pasted), extract its **hard requirements**, **repeated nouns/verbs**, and **exact technology names** — these are the keyword corpus for Step 3. If no JD is provided, ask whether the review should be generic or targeted, and proceed generically if no answer is needed.

## Step 2 — ATS / machine-parsing audit

Applicant tracking systems (Workday, Greenhouse, Lever, Taleo, iCIMS, SuccessFactors) parse the resume into structured fields before a human sees it. Flag every violation found, with the specific location:

- **Contact info in header/footer** — many parsers skip headers/footers entirely; name, email, phone must be in the body.
- **Tables** — multi-column tables frequently scramble reading order or drop cells in older parsers. A simple date/role/company summary table is *moderate* risk; skills or experience laid out in tables is *high* risk. Recommend tab stops or plain paragraphs where risk is high.
- **Text boxes, images, icons, charts** — invisible to parsers. Skill-level bars/graphics are worst: they convey nothing to the machine and waste space for the human.
- **Multi-column page layouts** — column-unaware parsers read straight across, interleaving unrelated text.
- **Non-standard section headings** — parsers field-map from headings. Safest set: "Summary", "Experience"/"Work Experience"/"Career Summary", "Education", "Skills", "Certifications". Flag creative headings ("My Journey", "What I Bring") and suggest standard equivalents.
- **Dates** — must be consistent (`MMM YYYY – MMM YYYY` recommended), attached to each role, in a predictable position. Flag mixed formats (e.g. "Nov 2019 – Dec 2019" vs "2025 - Present"), en-dash vs hyphen inconsistency, and missing months (some ATSs assume January, distorting tenure).
- **File format** — .docx and text-based PDF both parse well in modern systems; flag scanned/image PDFs, .pages, unusual fonts, and ligature-heavy typefaces.
- **Fancy characters** — smart quotes, arrows, emoji, box-drawing characters can garble extraction; keep to plain punctuation and standard bullets.
- **Acronyms** — keyword matchers are often literal. Spell out AND abbreviate on first use ("continuous integration/continuous delivery (CI/CD)") for any term the JD uses in either form.
- **Length as parsed text** — verify no content is lost when reduced to plain text (everything important must survive the extraction you just performed — if you couldn't read it, neither can the ATS).

## Step 3 — Keyword & JD alignment (skip if no JD)

Keyword screens and recruiter searches are literal-match driven:

1. Build a table: each **hard requirement / named technology / repeated phrase** from the JD → present in resume? (exact term, synonym only, or absent). Match on the JD's vocabulary, not the resume's — "developer productivity" ≠ "engineering velocity" to a keyword filter.
2. Check placement: keywords carry most weight in the **top third of page 1** and in **role bullets** (context-weighted), least in a skills dump. A keyword that appears only in the skills list looks stuffed; one evidenced inside an achievement bullet scores with both machine and human.
3. Flag **missing must-haves** loudly, including honest gaps the user should address in a cover letter rather than pad into the resume. Never advise fabrication or invisible-text stuffing — both are detectable and disqualifying.
4. Check the **job title echo**: recruiters search by title. If the target title (or its nearest true equivalent) appears nowhere, recommend working it into the summary line honestly ("… engineering-productivity leadership …").

## Step 4 — Human skim audit

Eye-tracking studies (Ladders 2018: ~7.4 seconds first-pass skim, F/E-shaped scan pattern) define what actually gets read: top of page 1, left edge, first words of bullets, titles/companies/dates.

- **Six-second test**: read only the name, summary first line, section headings, job titles/companies, and the first 3–4 words of each bullet on page 1. State what impression survives. If the core positioning doesn't land in that pass, say so — this is the single most important finding.
- **Top third of page 1** must contain: who they are, seniority, the 2–3 differentiators for the target role, and location/work-rights if relevant.
- **Bullet quality** — for every experience bullet check:
  - Leads with a strong past-tense action verb (led, built, cut, launched, shipped) — not "responsible for", "involved in", "helped with", "worked on".
  - **Quantified** (Google's XYZ formula: "Accomplished X as measured by Y, by doing Z"). Count the ratio of quantified to unquantified bullets per role; below ~half quantified is a finding.
  - One idea per bullet, ≤2 lines rendered; flag 3+ line bullets and multi-clause chains.
  - Accomplishment, not duty. "Managed a team of 9" is a duty; "Grew team 1→5 while launching 4 devices" is an accomplishment.
- **Density & whitespace** — walls of text lose skimmers; flag paragraph blocks >4 lines inside experience sections, and pages with no visual rest.
- **Recency weighting** — most-relevant detail should be in the most recent 2–3 roles; roles >10 years old deserve 1–4 lines each. Flag inverted weighting.
- **Length** — 2 pages is the norm for <15 years' experience; 3–4 tolerable for 20+ year senior/executive resumes **if** pages 1–2 carry the sell. Flag anything the last pages contain that the first page depends on.
- **Buzzword audit** — flag empty adjectives (seasoned, dynamic, results-driven, passionate, synergy, guru, rockstar) unless immediately evidenced. Flag first-person pronouns if usage is inconsistent.
- **Red flags a recruiter will probe**: unexplained gaps >3 months, many short stints without context, title inflation vs company size, missing months on dates, inconsistent tense (past tense for past roles, present for current), typos, mixed spelling variants (organise/organize).

## Step 5 — Truth & consistency pass

- Cross-check every date, title, and company against ALL occurrences (summary table vs section headings vs LinkedIn if provided). Any mismatch is a top-priority finding — screeners treat inconsistency as dishonesty.
- Check arithmetic: "20+ years", team sizes, percentages that must reconcile.
- Flag claims that invite a probe the user may not want ("CTO" at a company where they're the only engineer — defensible, but be ready).

## Step 6 — Report

Structure the output:

1. **Verdict** (2–3 sentences): would this resume survive (a) the ATS parse, (b) the 7-second skim, (c) the keyword screen for the stated target? 
2. **Scorecard** — one line each, score /10 with a one-clause reason: ATS parseability · Keyword alignment · Skim impact (page 1) · Achievement evidence (quantification) · Consistency/accuracy · Length & structure.
3. **Findings, ranked** — numbered, most-likely-to-cost-an-interview first. Each: the problem, where (page/section/quote a few words), why it matters (which system or behaviour it trips), and the concrete fix. Aim for the top 5–10; put minor nits in a short bullet list at the end.
4. **What's working** — brief; only genuinely strong elements, so the user doesn't "fix" them.
5. Offer (don't perform) the follow-up: apply fixes to the file, tailor to a specific JD, or re-run the review after edits.

Calibration: be direct. "This bullet says nothing a screener can use" is more useful than "consider strengthening". If the resume is strong, say so and dig for second-order improvements rather than inventing problems — but a review that finds nothing is almost always a review that didn't look hard enough.
