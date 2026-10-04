---
name: interview-coach
description: Use when the user has an upcoming interview, received an interview invitation, or wants to prepare for a specific role at a specific company.
---

## Overview

Generate an interview prep brief with likely questions, talking points from the user's actual experience, evaluative questions to ask the company, and honest assessment of weaknesses. Reuse and grow the persistent STAR+R story bank so every prep session compounds instead of starting from zero.

For interview process tracking, post-interview notes, and follow-up drafts, use `interviewing`. This skill focuses on prep quality.

## Workflow

> **State layer:** selects either `resume.md` or `cv.md` as the source work document, reads `applications.md`, reads and appends to `story-bank.md`, writes an interview prep artifact, and writes a numbered report. See [state-layer contract](../_shared/state-layer.md).

### 0. Scaffold, tracker check, and source selection

Run `node "{job_hunt_skills_root}/scripts/scaffold-state.mjs"` if the state layer is missing.

Read `my-documents/applications.md`. If no row exists for this company + role, warn but do not block:

> I don't see a tracked application for **{Role} at {Company}**. Interview prep still works. Want me to create a tracker row with `status: interviewing`, or skip the tracker?

If the user confirms tracker creation, insert a new row with `status: interviewing`. This is allowed by [state-layer section 4](../_shared/state-layer.md#4-status-enum) because interviews can predate the tracker.

If a row exists at `saved` or `applied`, ask whether to advance it to `interviewing`. Only advance after user confirmation.

Select the source work document using [state-layer section 6](../_shared/state-layer.md#6-work-document-frontmatter-and-selection). If both `resume.md` and `cv.md` exist and the user did not imply which one maps to the interview, ask. Use the selected file's `label` in user-facing prose.

### 1. Gather inputs

- **Company name:** required.
- **Role title:** required.
- **Job posting:** URL or pasted text. If unavailable, ask what the user knows about the requirements and interview loop.
- **Interview details:** stage, date/time if known, format, interviewer names or functions, expected topics, and anything the recruiter mentioned.
- **Source work document:** selected `resume.md` or `cv.md`.

### 2. Research the company

If web browsing is available, inspect the website, careers page, recent news, reviews, and work-model signals. If browsing is unavailable, ask what the user knows and caveat current-company findings.

If a recent `company-research` report exists for this application, read it and reuse its red flags and questions.

### 3. Load the story bank

Read `my-documents/story-bank.md`. If it does not exist, run `node "{job_hunt_skills_root}/scripts/scaffold-state.mjs"`.

Parse stories using the canonical schema in [state-layer section 7](../_shared/state-layer.md#7-story-bank-schema):

- Each story is an H2 section.
- YAML metadata is immediately under the title.
- Required body fields are Situation, Task, Action, Result, and Reflection.

Build an internal index of `{id, themes, archetypes, title}`. Treat parse failures like tracker parse failures: report the offending region and exit without overwriting.

### 4. Generate prep brief

**Likely Questions (8-12):**

- Role-specific behavioral questions from the posting's requirements.
- Technical or domain questions relevant to the role.
- Remote/hybrid questions where work model matters.
- For each behavioral question, try to match an existing story-bank entry first by theme and archetype. Reference the story by title and note the reflection beat that applies.
- Only propose a new story when no existing story fits the question's archetype.
- Talking points must come from the selected source work document or story bank, not generic advice.

**Questions to Ask (5-8):**

Categorize by How They Work, Role Scope, Success Measures, Growth, Culture, and Remote Operations when relevant. Include green/red flags for likely answers. See [guides/interview-framework.md](../../guides/interview-framework.md).

**Angles to Highlight:**

Specific source-document experiences and story-bank entries that map to the role. Include the narrative to lead with.

**Potential Weaknesses:**

Gaps between the selected work document and the role. Include honest scripts: acknowledge, redirect to adjacent proof, and avoid spin.

### 5. Capture new stories

For every high-value behavioral gap, work with the user to elicit a new STAR+R story:

1. Ask for Situation and Task first: where, when, and what was on the line.
2. Probe Action in first person. Push back on vague "we" answers by asking what the user specifically did.
3. Get Result with a metric where possible. If not quantifiable, capture scope and qualitative impact.
4. Always elicit Reflection: what they would do differently, what changed about their approach, or what they learned.

Do not invent specifics. Ask targeted follow-ups when details are thin. Use `TBD - user to fill` only when the user cannot reconstruct a detail or is unavailable.

Append new stories using the canonical story-bank schema. For reused stories, append a `usage` entry with `date`, `company`, `role`, and `question`.

### 6. Save

Save:

1. **Prep artifact:** `my-documents/applications/{id}/interview-prep.md`.
2. **Report:** `my-documents/reports/{###}-{id}-interview-prep-{YYYY-MM-DD}.md`.
3. **Story bank updates:** append usage entries and new stories.
4. **Conversation output:** display the brief to the user.

Report frontmatter:

```yaml
---
report_id: {###}
company: {Company}
role: {Role}
application_id: {id}
skill: interview-coach
date: {today ISO}
summary: One-line prep angle.
---
```

The prep artifact is candidate-facing. Keep internal uncertainty, self-grading notes, and unresolved checklists out of it. Resolve uncertainty in conversation or put evidence gaps in the story bank, not in the final prep brief.

Close with the reward beats ([state-layer §11](../_shared/state-layer.md#11-progress-and-reward)): name **what this unlocked** ("you're prepped for this interview, and any stories we banked are now reusable across future rounds"), then show the **profile-strength line** (`node "{job_hunt_skills_root}/scripts/profile-strength.mjs"`, or derive it natively). If new stories were banked, call that gain out specifically.

## Common Mistakes

- **Generic questions.** "Tell me about yourself" is obvious; generate questions specific to this role.
- **Generic talking points.** Reference concrete achievements from the selected work document or a specific story.
- **Hiding weaknesses.** Include honest scripts for gaps.
- **Skipping the story bank.** Always read it before generating new stories.
- **Skipping Reflection.** Reflection is the seniority signal.
- **Fabricating Action details.** Interviewers probe how work happened; ask the user instead of filling in plausible process details.
