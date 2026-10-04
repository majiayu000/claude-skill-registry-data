---
name: career
description: Career management skill covering resume coaching (review, score, tailor, audit), job evaluation, rubric development, content extraction from conversations, and pipeline quality assurance.
---

# Career

Career management including resume coaching, job evaluation, and career pipeline tools.

## When to Invoke

User can say things like:

- "Run a resume review on [file or role]"
- "Review my resume for [formatting / design / content / this job]"
- "Score this job" / "Evaluate this job posting" / "Should I apply to this role?"
- "Help with rubric development" or "Evaluate this resume adaptation"
- "Develop the content set from remaining convos" or "Pull more from conversations"
- "Audit the resume chain" or "Can I trust this pipeline?"

Route to the right workflow below.

## Configuration

| Variable | Description |
|----------|-------------|
| `{{DOCS_ROOT}}` | Path to resume master docs directory (e.g. `resume-docs/master/`) |
| `{{PROMPTS_ROOT}}` | Path to extraction/tailoring prompt templates (e.g. `resume-docs/prompts/`) |
| `{{INDEX_ROOT}}` | Path to processing index files (e.g. `resume-docs/_index/`) |
| `{{CONVERSATIONS_DIR}}` | Path to exported conversation archives (if using content extraction) |

---

## 1. Resume Review

**Purpose:** Formatting/design, content quality, or job-specific content decisions.

**Steps:**

1. **Identify scope** from the user: full review, formatting-only, content-only, or review against a specific job description.
2. **Load context:** The resume (or path) and, if job-specific, the job posting. Optionally load master docs to check traceability to evidence.
3. **Apply standards** from the tailored resume prompt and **score using** the resume quality rubric (target 100):
   - Structure: header, headline, executive summary, competencies, experience (reverse chronological), education.
   - Bullets: Action + Scope + Method + Outcome; quantified where possible.
   - Tone: confident, precise, outcomes-oriented; no vague claims without evidence.
   - ATS: single-column, parseable; no meta text in canonical output (no Status/DONE/draft).
4. **Deliver:** Concise feedback (formatting / content / job-fit) with specific edits or suggestions; optionally include rubric score (0-100). If job-specific, note keyword coverage and gaps.

**Output format:**

- Summary (2-3 lines)
- By section or theme: what works, what to change, optional rewrite snippets
- Optional: requirement-coverage note if a JD was provided

---

## 2. Job Evaluation -- Scores, Recommendation, and Resume Revisions

**Purpose:** Score any job (browser-found or user-supplied JD) for fit and interview likelihood; give a clear apply/not-apply recommendation; for strong fits, output specific resume revision recommendations.

**Steps:**

1. **Load:** The job description/posting (and optional company context). Load the universal job rubric and the master docs needed to map evidence.
2. **Score:** Apply Rubric A (Ideal Job Match 0-100) and Rubric B (Interview Odds 0-100). Use only documented evidence from master docs.
3. **Recommend:** Map scores (and any deal-breakers) to exactly one tier:
   - **Definite No Go** | **Nah** | **Meh** | **Good Fit** | **Freaking Apply Now**
4. **Why:** Provide 2-4 sentences citing both scores and 1-2 concrete factors that drove the recommendation.
5. **Resume revision recommendations:** **Only** if recommendation is **Good Fit** or **Freaking Apply Now**, produce:
   - Summary edits
   - Core competencies adjustments
   - Experience bullets by role
   - Keywords to integrate
   - Cover letter/application notes

   Every item must be specific, actionable, and traceable to master docs.

**Deliver:** Scores -> Recommendation tier -> Why -> [If Good Fit+] Resume revision recommendations (copy-paste applicable).

---

## 3. Rubric Development and Resume Adaptation Evaluation

**Purpose:** Create or refine scoring rubrics; evaluate how well a resume (or adaptation) matches a role or meets criteria.

**Steps:**

1. **Clarify:** New rubric (e.g. for a role type or org) vs. evaluating an existing resume/adaptation against current rubrics.
2. **For rubric development:**
   - Read existing rubrics for structure reference.
   - Propose or refine criteria and weights; document in the same style.
3. **For adaptation evaluation:**
   - Load the resume and the target job. Score using Ideal Job Match and Interview Odds.
   - Check resume against the suggested resume revision recommendations (if any) and requirement coverage.
   - List strong alignment and risks/gaps; suggest improvements.
4. **Deliver:** Rubric draft or evaluation summary with scores, strengths, risks, and concrete next steps.

---

## 4. Content / Data Set Development from Conversations

**Purpose:** Enrich master docs and bullet list from conversation archives not yet processed.

**Steps:**

1. **Check processed list:** `{{INDEX_ROOT}}/processed_conversations.md` -- which prompts have been run for which conversation IDs.
2. **Identify gaps:** Which conversation files are not yet processed for the prompts relevant to the user's goal (employers, timeline, skills, achievements, portfolio, AI, roles, story, descriptions, cross-check).
3. **One run = one (or few) conversation files in context.** Do not load the entire archive at once. Use the prompt chain:
   - Prompts 1-9: extract employers, timeline, skills, achievements, portfolio, AI work, roles, story, bullet-ready content into master docs and update the processed list.
   - Prompt 10: cross-check and append gaps/conflicts to `{{INDEX_ROOT}}/gaps-and-conflicts.md`; update processed list.
4. **Rules:** Only write under `{{DOCS_ROOT}}`. After each run, update the processed list for the prompt(s) used. No fabrication; cite conversation_id and angle for additions.
5. **Deliver:** Short summary of what was processed, what was added, and any conflicts or suggested follow-ups.

---

## 5. Trust and Quality Audit of the Resume Pipeline

**Purpose:** Let the user trust the pipeline and know where quality is enforced.

**Steps:**

1. **Map the chain:** List the pipeline components:
   - **Data:** Master docs, populated by extraction prompts and cross-check.
   - **Tailoring:** Tailored resume prompt with scoring, requirement mapping, evidence mapping, bullet rewriting, keyword integration.
   - **Output:** Markdown (canonical), ATS plain text, optional HTML/PDF.
2. **Quality checkpoints:**
   - No fabrication; evidence only from master docs or approved extraction.
   - Scoring before writing; requirement extraction -> evidence mapping -> positioning; quality checklist before finalizing.
   - Traceability: every claim in a resume should map to a master doc or a cited conversation.
3. **Optional audit:** For a given tailored resume, verify:
   - Bullets trace to master bullet list or other master docs
   - Keywords align with stated job
   - Dates/titles consistent with master timeline and employers/roles doc
4. **Deliver:** Short "chain overview" plus where quality is enforced; if an audit was run, report traceability and any issues.

---

## Suggested File Structure

| Purpose | Path |
|---------|------|
| Master docs (source of truth) | `{{DOCS_ROOT}}/00-master-timeline.md` ... `08-*.md` |
| Universal job rubric | `{{DOCS_ROOT}}/10-universal-job-rubric-and-apply-recommendation.md` |
| Ranked jobs | `{{DOCS_ROOT}}/11-ranked-jobs-with-apply-recommendations.md` |
| Resume quality rubric (0-100) | `{{DOCS_ROOT}}/09-resume-quality-rubric.md` |
| Master bullet list | `{{DOCS_ROOT}}/07-master-bullet-list.md` |
| Tailored resume prompt | `{{PROMPTS_ROOT}}/prompt-11-master-tailored-resume.md` |
| Extraction prompts | `{{PROMPTS_ROOT}}/prompt-01-employers.md` ... `prompt-10-cross-check.md` |
| Processed list | `{{INDEX_ROOT}}/processed_conversations.md` |
| Gaps/conflicts | `{{INDEX_ROOT}}/gaps-and-conflicts.md` |

---

## Quality Rules

- **No fabrication** -- every claim must trace to a master doc or cited conversation
- **Score before you write** -- always evaluate fit before tailoring
- **One conversation at a time** -- don't load entire archives
- **Update the index** -- mark conversations as processed after each run
- **Traceability** -- every bullet should map to evidence
