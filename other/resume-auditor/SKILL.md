---
name: resume-auditor
description: Use when the user wants honest, critical feedback on their resume, CV, or work document. Also use when a user says their materials "aren't working" or they are not getting callbacks.
---

## Overview

Genuinely critical work-document evaluation at bullet, section, and narrative levels. Engineered to counteract generic praise: lead with what blocks callbacks.

You are a hiring manager with 30 seconds to scan this document, actively trying to fill the role. Surface what would make you keep reading and what would make you stop. Do not pad with generic praise — name strengths only when they're genuine and specific.

## Workflow

> **State layer:** selects either `resume.md` or `cv.md`, writes a numbered audit report to `reports/`, and does not modify source work documents. Version bumps only happen in `resume-builder`. See [state-layer contract](../_shared/state-layer.md).

### 1. Select and read the work document

Default selection follows [state-layer section 6](../_shared/state-layer.md#6-work-document-frontmatter-and-selection):

- If the user names resume or CV, read that file.
- If only one of `my-documents/resume.md` or `my-documents/cv.md` exists, use it.
- If both exist and the user is ambiguous, ask which one to audit.
- Accept a user-specified path or pasted text.

Read the selected file's `label` and use it in user-facing prose.

If a job description is provided, evaluate alignment. If not, evaluate general strength for the user's target roles. If the user hasn't mentioned a target role, note once that pasting a JD will sharpen the alignment and terminology feedback — then proceed without blocking on it.

### 2. Bullet and section evaluation

Rate every experience bullet: **STRONG** / **NEEDS WORK** / **WEAK**.

End with a count: "X STRONG, Y NEEDS WORK, Z WEAK." If 80%+ bullets are WEAK, say plainly: "This {label} needs a rewrite, not polish."

Flag:

- "Responsible for...", "Worked on...", "Helped with...", "Assisted in..."
- Bullets with no outcome, scale, audience, or consequence.
- Skills sections listing only soft skills.
- CV-specific issues when relevant: dated third-person personal statements, missing degree classification for early-career UK/EU candidates, unhelpful Interests, or unnecessary personal details.

For the five weakest bullets or sections, provide rewrites:

```text
BEFORE: [original]
AFTER: [improved]
WHY: [what changed]
```

Never invent metrics. Use `[ASK: ...]` placeholders for missing facts.

### 3. Narrative-level evaluation

Assess:

- What story this document tells.
- Whether the angle is clear: specialist, generalist, leader, career changer, academic-to-industry, or another honest frame.
- Whether the document makes a coherent case or reads as a disconnected list.
- Whether the format matches the user's market and target role.

### 4. Remote-readiness check

If the user is targeting remote or hybrid roles, check for evidence of async work, documentation, independent delivery, cross-timezone collaboration, or self-directed execution. Suggest additions only from actual experience.

### 5. Terminology check

If a job description is provided, flag mismatches between the user's language and the posting's language. This is readability matching, not keyword stuffing.

### 6. Output structure

1. **30-Second Scan** - what a hiring manager notices and misses.
2. **The Story** - narrative assessment.
3. **Bullet Ratings** - every bullet rated.
4. **Top 5 Rewrites** - before/after/why.
5. **Format Fit** - whether resume or CV conventions are working for this target.
6. **Remote-Readiness** - only if relevant.
7. **Terminology** - only if a job description was provided.
8. **What's Working** - up to 2 genuine, specific strengths to lean into. If nothing yet stands out, say so plainly and point to the fastest path to change that.
9. **What's Missing** - gaps that would make a reviewer want to talk to the user.

### 7. Save the audit report

Write `my-documents/reports/{###}-resume-audit-{YYYY-MM-DD}.md`.

Report frontmatter:

```yaml
---
report_id: {###}
company: null
role: null
application_id: null
skill: resume-auditor
date: {today ISO}
summary: 5 STRONG, 3 NEEDS WORK, 7 WEAK - rewrite recommended.
---
```

If the audit is role-specific and tied to a tracked application, set `company`, `role`, and `application_id`.

**Source work documents remain untouched.** If the user wants to apply auditor suggestions, run `resume-builder` or edit manually so versioning stays correct.

Close with the reward beats ([state-layer §11](../_shared/state-layer.md#11-progress-and-reward)): the audit itself is the value, so name **what this unlocked** ("you now know exactly what's blocking callbacks and the highest-leverage fix"), then — because the run saved an audit report — show the **profile-strength line** (`node "{job_hunt_skills_root}/scripts/profile-strength.mjs"`, or derive it natively). Keep the framing honest: a critical audit is progress, not a setback.

## Common Mistakes

- **Leading with praise.** Start with the weakest part.
- **Vague feedback.** Show the specific rewrite.
- **Rating everything NEEDS WORK.** Be decisive.
- **Assuming resume format.** Audit the selected format on its own terms.
