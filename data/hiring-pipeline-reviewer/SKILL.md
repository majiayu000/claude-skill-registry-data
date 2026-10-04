---
name: hiring-pipeline-reviewer
description: "Generate a structured weekly status report for all candidates in your hiring pipeline from interview notes and evaluation sheets. Flags stuck candidates, summarizes scores, and recommends next steps. Use when reviewing hiring pipeline, preparing for recruiter sync, or deciding next steps on candidates. Triggers: 'review hiring pipeline', 'hiring pipeline status', 'статус по кандидатам', 'ревью пайплайна найма'."
version: 1.0.0
---

# Hiring Pipeline Reviewer

Generates a structured weekly status report for all candidates in a hiring pipeline from the hiring manager's interview notes and evaluation sheets. Flags stuck candidates, consolidates scores, recommends next steps, and optionally drafts a recruiter update.

**Input:**
- Interview notes and/or evaluation sheets (plain text, .md, or .txt; one block or multiple files)
- Optional: position title, hiring criteria, cutoff date for "stuck" flag (default: 5 days)

**Output:**
- Candidate status table with stage, last action, score, next step, and flags
- Flags section (stuck candidates, missing data)
- Recommendations section (advance / decline / decision needed)
- Optional recruiter update narrative (2–4 sentences)

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Collect Input

1. Check what the user already provided in their trigger message:
   - Interview notes or evaluation text included → extract it
   - Position title mentioned → extract it
   - Hiring criteria mentioned → extract them

2. If no notes or evaluation data were provided, ask the user to paste them. Do not proceed without input data.

3. Accept any of these input formats:
   - Plain text pasted directly in chat
   - Single block of notes covering multiple candidates
   - Separate text blocks per candidate (labeled or unlabeled)

### Step 2: Extract Candidate Records

1. Parse the input to identify individual candidates:
   - Look for names, initials, or role labels (e.g., "Candidate 1", "Alex M.", "Senior iOS Dev")
   - Use date markers, section separators, or explicit labels as candidate boundaries

2. For each identified candidate, extract:
   - **Name / identifier** (use provided name; if ambiguous, assign [Candidate A], [Candidate B])
   - **Stage** (e.g., Applied, Phone Screen, Interview 1, Interview 2, Offer, Declined)
   - **Last action date** (most recent note or evaluation date; mark as `—` if absent)
   - **Score or evaluation summary** (numeric if present; narrative summary if not)
   - **Key strengths** (up to 2 phrases)
   - **Key concerns** (up to 2 phrases)
   - **Stated next step** (if mentioned in notes; otherwise `—`)

3. Handle unsegmented input:
   - If notes are one continuous block with no clear candidate separation, attempt segmentation by names, interview dates, or role references
   - Mark any fragments that couldn't be attributed to a specific candidate as `[unresolved]` and list them after the table

**Edge Cases:**
- Two candidates share the same name or only initials are given → assign unique labels ([Candidate A], [Candidate B]); note ambiguity in a footnote
- A candidate has notes from multiple interviewers → merge into a single record; list unique concerns from each reviewer
- Notes mention a candidate by first name only and context is unclear → use provided name, mark as `[first name only]`

### Step 3: Detect Stuck Candidates

1. For each candidate, calculate days since last action:
   - If last action date is known: compare to today's date
   - Default "stuck" threshold: 5 days of inactivity without a defined next step
   - If user specified a different threshold in input: use that value

2. Flag candidate as `⚠ stuck` if:
   - Days since last action ≥ threshold AND
   - Next step field is empty (`—`) or undefined

3. Flag candidate as `❓ incomplete` if:
   - Stage is unknown, OR
   - No evaluation score or notes are available

### Step 4: Build Status Table

Compile a candidate status table with these columns:

| Candidate | Stage | Last Action | Score | Next Step | Flag |
|-----------|-------|-------------|-------|-----------|------|

- **Candidate**: name or assigned label
- **Stage**: current pipeline stage
- **Last Action**: date in YYYY-MM-DD format (or `—`)
- **Score**: numeric (e.g., 4/5) or qualitative (Strong / Adequate / Weak) or `—`
- **Next Step**: specific action (e.g., "Schedule interview 2", "Send offer", "Decline") or `—`
- **Flag**: `⚠ stuck`, `❓ incomplete`, or `—`

### Step 5: Generate Flags Section

List all flagged candidates with brief explanation:

- `⚠ [Name]` — stuck since [date], no next step defined
- `❓ [Name]` — missing evaluation data / stage unknown
- `[unresolved]` — notes fragment not matched to a candidate (if applicable)

If no flags, write: "No flags. All candidates have defined next steps."

### Step 6: Generate Recommendations

Provide a concrete recommendation for each candidate in one of three categories:

- **Advance**: candidate meets criteria, recommend moving to next stage
- **Decline**: candidate does not meet criteria, recommend rejection
- **Decision needed**: team is split, evaluation is incomplete, or additional information is required before a decision

Format:
```
- Advance: [Name] — [1-sentence reason]
- Decline: [Name] — [1-sentence reason]
- Decision needed: [Name] — [1-sentence reason or what's missing]
```

Do not generate generic recommendations ("consider"). Every recommendation must be actionable.

### Step 7: Draft Recruiter Update (Optional)

1. After presenting the main output, ask:
   > "Would you like a brief recruiter update (2–4 sentences summarizing pipeline status)?"

2. If yes: generate a concise narrative covering:
   - Total candidates in pipeline
   - How many are active vs. stuck
   - Immediate actions required (offers to extend, interviews to schedule)

---

## Negative Cases

- **No input data provided:** Stop. Return: "Paste your interview notes or evaluation sheets to generate the pipeline review."
- **Input looks like resumes instead of interview notes:** Warn: "This appears to be a resume or candidate profile, not interview notes. This skill works with hiring manager's notes and evaluation sheets. Do you want to continue with this data?"
- **Only candidate names provided, no notes or stages:** Generate table with names only; flag all as `❓ incomplete`; note that no evaluation data was provided.

---

## Output Format

```markdown
## Hiring Pipeline Status — [Position or "Hiring Pipeline"] — [Date]

### Candidate Table

| Candidate | Stage | Last Action | Score | Next Step | Flag |
|-----------|-------|-------------|-------|-----------|------|
| [Name] | Interview 2 | 2026-04-14 | 4/5 | Send offer | — |
| [Name] | Phone screen | 2026-04-10 | 3/5 | Schedule interview | ⚠ stuck |
| [Name] | Applied | — | — | Review application | ❓ incomplete |

### Flags
- ⚠ [Name] — stuck since [date], no next step defined
- ❓ [Name] — missing evaluation data

### Recommendations
- Advance: [Name] — strong match on all criteria
- Decline: [Name] — [specific misalignment]
- Decision needed: [Name] — team is split; recommend sync before proceeding

### Recruiter Update (optional)
[2–4 sentence summary of pipeline status for the recruiter]
```
