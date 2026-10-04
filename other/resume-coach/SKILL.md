---
name: resume-coach
description: Resume review (formatting, design, content, job-specific), score-any-job evaluation (0-100 fit and interview odds, Definite No Go to Freaking Apply Now with resume revision recommendations for Good fit/Freaking Apply Now), rubric development and resume adaptation evaluation, content/data set development from unexplored conversations, and quality assurance for the resume generation chain. Use when the user asks for resume review, resume feedback, score this job, evaluate this job posting, should I apply, rubric development, resume tailoring evaluation, extracting content from conversations, or trusting/auditing the resume pipeline.
---

# Resume coach

Operates over `resume-and-docs-prompts/` as the single source of truth. All factual content must trace to master docs or approved conversation extraction. No fabrication.

---

## How to invoke

User can say things like:

- "Run a resume review on [file or role]"
- "Review my resume for [formatting / design / content / this job]"
- "Score this job" / "Evaluate this job posting" / "Should I apply to this role?" (any job: browser-found or user-supplied JD)
- "Help with rubric development" or "Evaluate this resume adaptation"
- "Develop the content set from remaining convos" or "Pull more from conversations"
- "Audit the resume chain" or "Can I trust this pipeline?"

Route to the right workflow below.

---

## 1. Resume review

**Purpose:** Formatting/design, content quality, or job-specific content decisions.

**Steps:**

1. **Identify scope** from the user: full review, formatting-only, content-only, or review against a specific job description.
2. **Load context:** The resume (or path) and, if job-specific, the job posting. Optionally load `resume-and-docs-prompts/master/*` to check traceability to evidence.
3. **Apply standards from** `resume-and-docs-prompts/prompts/prompt-11-master-tailored-resume.md` and **score using** `resume-and-docs-prompts/master/09-resume-quality-rubric.md` (target 100):
   - Structure: header, headline, executive summary, competencies, experience (reverse chronological), education.
   - Bullets: Action + Scope + Method + Outcome; quantified where possible.
   - Tone: confident, precise, outcomes-oriented; no vague claims without evidence.
   - ATS: single-column, parseable; no meta text in canonical output (no Status/DONE/draft).
4. **Deliver:** Concise feedback (formatting / content / job-fit) with specific edits or suggestions; optionally include rubric score (0–100). If job-specific, note keyword coverage and gaps.

**Output format:**

- Summary (2–3 lines)
- By section or theme: what works, what to change, optional rewrite snippets
- Optional: requirement-coverage note if a JD was provided

---

## 2. Job evaluation (any job) — scores, recommendation, and resume revisions

**Purpose:** Score any job (browser-found or user-supplied JD) for fit and interview likelihood; give a clear apply/not-apply recommendation; for Good fit or Freaking Apply Now, output specific resume revision recommendations.

**Steps:**

1. **Load:** The job description/posting (and optional company context). Load `resume-and-docs-prompts/master/10-universal-job-rubric-and-apply-recommendation.md` and the master docs needed to map evidence.
2. **Score:** Apply Rubric A (Ideal Job Match 0–100) and Rubric B (Interview Odds 0–100) from the universal rubric. Use only documented evidence from master docs.
3. **Recommend:** Map scores (and any deal-breakers) to exactly one tier: **Definite No Go** | **Nah** | **Meh** | **Good fit** | **Freaking Apply Now** (see score bands in `master/10-*`).
4. **Why:** Provide 2–4 sentences citing both scores and 1–2 concrete factors that drove the recommendation.
5. **Resume revision recommendations:** **Only** if recommendation is **Good fit** or **Freaking Apply Now**, produce the structured block defined in `master/10-universal-job-rubric-and-apply-recommendation.md` (Step 4): Summary edits, Core competencies, Experience bullets by role, Keywords to integrate, Cover letter/application notes. Every item must be specific and actionable and traceable to master docs.

**Deliver:** Scores → Recommendation tier → Why → [If Good fit or Freaking Apply Now] Resume revision recommendations (copy-paste applicable).

---

## 3. Rubric development and resume adaptation evaluation

**Purpose:** Create or refine scoring rubrics; evaluate how well a resume (or adaptation) matches a role or meets criteria.

**Steps:**

1. **Clarify:** New rubric (e.g. for a role type or org) vs. evaluating an existing resume/adaptation against current rubrics.
2. **For rubric development:**
   - Read `resume-and-docs-prompts/master/08-job-search-rubrics-and-ranked-opportunities.md` and/or `08-job-match-rubrics-and-search.md` and `10-universal-job-rubric-and-apply-recommendation.md` for structure.
   - Propose or refine criteria and weights; document in the same style under `resume-and-docs-prompts/master/`.
3. **For adaptation evaluation:**
   - Load the resume and the target job. Use `master/10-*` for job scoring and recommendation; then check resume against the suggested resume revision recommendations (if any) and requirement coverage.
   - Score using Ideal Job Match and Interview Odds; list strong alignment and risks/gaps; suggest improvements.
4. **Deliver:** Rubric draft or evaluation summary with scores, strengths, risks, and concrete next steps.

---

## 4. Content / data set development from unexplored conversations

**Purpose:** Enrich master docs and bullet list from conversation archive not yet processed.

**Steps:**

1. **Check processed list:** `resume-and-docs-prompts/_index/processed_conversations.md` — which prompts have been run for which conversation IDs.
2. **Identify gaps:** Which conversation files (e.g. `conversations-000.json` … `conversations-039.json`) or IDs are not yet processed for the prompts relevant to the user’s goal (employers, timeline, skills, achievements, portfolio, AI, roles, story, descriptions, cross-check).
3. **One run = one (or few) conversation files in context.** Do not load the entire archive at once. Use the prompt chain:
   - Prompts 1–9: extract employers, timeline, skills, achievements, portfolio, AI work, roles, story, bullet-ready content into `resume-and-docs-prompts/master/*` and update the processed list.
   - Prompt 10: cross-check and append gaps/conflicts to `resume-and-docs-prompts/_index/gaps-and-conflicts.md`; update processed list.
4. **Rules:** Only write under `resume-and-docs-prompts/`. After each run, update `_index/processed_conversations.md` for the prompt(s) used. No fabrication; cite conversation_id and angle for additions.
5. **Deliver:** Short summary of what was processed, what was added, and any conflicts or suggested follow-ups (e.g. "Run Prompt 4 on conversation X for achievements").

---

## 5. Trust and quality of the resume generation chain

**Purpose:** Let the user trust the pipeline and know where quality is enforced.

**Steps:**

1. **Map the chain:** List the pipeline components:
   - **Data:** master docs (`00-` through `08-`), populated by prompts 1–9 and cross-check (10).
   - **Tailoring:** Prompt 11 (master tailored resume) with scoring, requirement mapping, evidence mapping, bullet rewriting, keyword integration.
   - **Output:** Markdown (canonical), ATS plain text, optional HTML/PDF.
2. **Quality checkpoints:**
   - No fabrication; evidence only from master docs or approved extraction.
   - Prompt 11: scoring before writing; requirement extraction → evidence mapping → positioning; quality checklist before finalizing.
   - Traceability: every claim in a resume should map to a master doc or a cited conversation.
3. **Optional audit:** For a given tailored resume, verify: (a) bullets trace to `07-master-bullet-list.md` or other master docs, (b) keywords align with stated job, (c) dates/titles consistent with `00-master-timeline.md` and `01-employers-and-roles.md`.
4. **Deliver:** Short "chain overview" plus where quality is enforced; if an audit was run, report traceability and any issues.

---

## File reference (repo root)

| Purpose | Path |
|--------|------|
| Master docs (source of truth) | `resume-and-docs-prompts/master/00-master-timeline.md` … `08-*.md` |
| Universal job rubric (any job → scores, Likert recommendation, resume revisions) | `resume-and-docs-prompts/master/10-universal-job-rubric-and-apply-recommendation.md` |
| Ranked jobs (all sourced jobs, Freaking Apply Now → Definite No Go + resume revisions) | `resume-and-docs-prompts/master/11-ranked-jobs-with-apply-recommendations.md` |
| Resume quality rubric (0–100, target 100) | `resume-and-docs-prompts/master/09-resume-quality-rubric.md` |
| Bullet list | `resume-and-docs-prompts/master/07-master-bullet-list.md` |
| Tailored resume prompt | `resume-and-docs-prompts/prompts/prompt-11-master-tailored-resume.md` |
| Extraction prompts | `resume-and-docs-prompts/prompts/prompt-01-employers.md` … `prompt-10-cross-check.md` |
| Processed list | `resume-and-docs-prompts/_index/processed_conversations.md` |
| Gaps/conflicts | `resume-and-docs-prompts/_index/gaps-and-conflicts.md` |
| README (how to run) | `resume-and-docs-prompts/README.md` |

---

## Coordination with the Cursor rule

When working in `resume-and-docs-prompts/`, the rule **resume-coach-persona** applies: same persona, same source of truth, same quality bar. This skill adds the four workflows above (review, rubrics/evaluation, content development, trust/audit). Use the rule for default behavior; use this skill when the user explicitly asks for one of the four use cases.
