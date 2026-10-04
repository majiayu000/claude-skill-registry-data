---
name: explore-experience
description: Interview the user to surface experience that is real but undocumented, mapped against a specific role's requirements, then update the profile. Use when a fit assessment or an adversarial review flags a section as thin.
argument-hint: "<role folder path or gap keywords>"
license: MIT
---

# Explore Experience

Most gaps in a fit assessment are documentation gaps, not experience gaps. The user did the thing; it never made it into `profile.md`, usually because they did not think of it as the thing the posting is asking for.

This skill finds those, by interview, and writes them down.

**Announce at start:** "Exploring undocumented experience for $ROLE. Reading the profile and the role requirements now."

**Arguments:**
- `$1` — a role folder path (containing `role_analysis.md` and/or `job_description.md`), or keywords naming the gap areas to explore

**Examples:**
```
/slushpile:explore-experience applications/Acme/Engineering/Staff-SRE
/slushpile:explore-experience evaluation pipelines golden datasets
/slushpile:explore-experience incident command on-call escalation
```

## Prerequisites

- `profile.md` — the full background
- `stories.md` — so a story surfaced here gets written to the right file
- The role's `job_description.md` and `role_analysis.md`, if a role path was given

## Phase 1: Gap Identification

### 1a. Map requirements to profile

For each responsibility and qualification in the JD, check whether `profile.md` contains specific, detailed evidence. Classify each as:

| Status | Meaning |
|--------|---------|
| COVERED | Profile has specific, detailed evidence with metrics/examples |
| THIN | Profile mentions the area but lacks depth (e.g., one-line bullet for a complex program) |
| MISSING | Profile has no evidence for this requirement |
| ADJACENT | Profile has experience in a related domain that could transfer but isn't framed for this role |

**Focus on THIN and ADJACENT items.** These are the highest-value interview targets. The user likely has experience here that simply hasn't been documented.

MISSING items are also worth exploring, but set expectations: the user may genuinely not have this experience. Don't force a match.

### 1b. Prioritize by impact

Rank the gaps by how much surfacing new evidence would improve the fit assessment:
1. **Responsibilities gaps** — these are what the hiring manager will evaluate daily work against
2. **Min qual gaps** — these gate the application
3. **Preferred qual gaps** — these differentiate but don't gate

### 1c. Present the gap analysis

Show the user a table:

```
| Requirement | Status | Current Evidence | Question Priority |
|-------------|--------|-----------------|-------------------|
| ... | THIN | "one bullet about machine vision" | HIGH |
```

Then say: "I'm going to ask you about the HIGH priority gaps first. For each one, think about: what did you actually do, what was the scale, what were the results, and what was your specific role vs. the team's."

## Phase 2: Targeted Interview

### 2a. Interview structure

For each gap, ask **specific, probing questions** designed to surface transferable experience. Do NOT ask generic questions. Map the JD's language to concrete scenarios the user might recognize.

**Good questions** are specific and scenario-based. They describe a situation the user might recognize, in language from *their* world rather than the posting's:

- "The posting asks for 'evaluation pipelines with golden datasets.' Have you ever built a reference set you used to check whether a system was performing correctly? That could be manufacturing QA, a test suite, a data-validation step — any domain."
- "They want monitoring dashboards with accuracy and failure-rate KPIs. Have you built or run anything that tracks pass/fail or quality metrics continuously?"
- "The role involves defining system behavior with customers. In your client meetings, how much of that was you deciding what the thing should do, versus presenting a decision already made?"

**Bad questions** are generic or leading:

- "Do you have experience with golden datasets?" — a yes/no that surfaces no detail
- "Tell me about your evaluation experience." — too broad; the user cannot tell what is relevant
- "Would you say your quality management experience is similar to model evaluation?" — leading, and it puts the answer in their mouth

### 2b. Interview rules

1. **Ask 3-5 questions per gap, max.** Don't exhaust the user. If a gap isn't surfacing anything after 3 questions, note it as a genuine gap and move on.
2. **Ask one gap area at a time.** Don't mix topics. Finish exploring one area before moving to the next.
3. **Number your questions** so the user can reference them in answers.
4. **Listen for adjacent experience.** The user will describe something that maps to the requirement through a different lens without noticing. Manufacturing quality inspection maps to model evaluation pipelines. Government client delivery maps to enterprise customer engagement. Running an on-call rotation maps to incident command. The user usually cannot see these connections from inside their own domain, and surfacing them is the entire point of this skill.
5. **Follow up on thin answers.** If the user says "yeah, I did something like that," ask for specifics: scale, duration, team size, outcomes, what they personally owned vs. delegated.
6. **Don't argue with "no."** If the user says they don't have experience in an area, accept it. Note the genuine gap and move on.
7. **Point the user to their own codebase when relevant.** If they mention a project that might contain evidence, suggest looking at specific files or repos together. Example: "You mentioned a pipeline — where's the code? I can look at it and ask more specific questions."
8. **Batch related questions.** If multiple JD requirements map to the same potential experience area, ask about them together rather than making the user repeat context.

### 2c. Cross-reference during interview

As the user answers, actively cross-reference against:
- Other roles in the job tracker (new evidence may improve fit for multiple roles)
- Existing profile sections that might benefit from expansion
- Blog posts, repos, and projects the user has mentioned previously

If the user reveals experience that connects to another assessed role, note it: "This also strengthens your fit for [role X] — the [responsibility Y] maps directly."

## Phase 3: Profile Update

### 3a. Draft profile additions

After the interview, draft the new content for `profile.md`. For each piece of surfaced experience:

- Write it at the same level of detail as existing profile entries
- Include: what was done, scale/metrics, user's specific role, outcome
- Place it in the correct section of the profile (don't create new sections unless genuinely needed)
- If expanding an existing bullet, preserve the original content and add the new detail below it or inline

### 3b. Present additions for review

Show the user exactly what you plan to add, organized by profile section. Ask for corrections before writing.

Common issues to watch for:

- **Scale inflation.** Do not round up. "About 10,000 units" is written as "10,000 units", never "10,000+".
- **Role attribution.** Do not claim for the user what their team did. If they convened the working group and someone else built the model, write that. This is the error most likely to blow up in an interview.
- **Jargon mapping.** Use the user's own terminology from the interview, not the posting's. The profile is source of truth in the user's language; the resume does the mapping later. A profile written in a posting's vocabulary is a profile that only fits that one posting.
- **Missing baselines.** Every new number gets its before-state and an as-of date, and goes into the "Numbers You Can Defend" table.

### 3c. Write updates

Update `profile.md` with the approved additions. Use targeted edits, not a full rewrite.

If the interview surfaced something with a scene, stakes, and an arc, it is a story. Add it to `stories.md` as well, using that file's structure. Stories surfaced this way are usually better than the ones people volunteer at onboarding, because they came out while the user was thinking about something else.

### 3d. Update role analysis (if applicable)

If a role folder was provided, update the `role_analysis.md`:
- Revise responsibility mapping ratings (PARTIAL → STRONG, etc.)
- Update the fit assessment score if warranted
- Revise the narrative angle to incorporate new evidence
- Update the gaps section to reflect what's been closed

## Phase 4: Summary

### 4a. Present results

Show the user:
1. **Gaps closed**: Which requirements moved from THIN/MISSING/ADJACENT to COVERED
2. **Gaps remaining**: Which requirements are genuine gaps with no transferable experience
3. **Cross-role impact**: Which other assessed roles benefit from the newly surfaced experience
4. **Updated fit score**: If applicable

### 4b. Recommend next steps

Based on what was surfaced:
- "Your fit score for [role] moved from X% to Y%"
- "The new [experience] also strengthens [other role] — consider updating that analysis"
- "The remaining gaps in [area] are genuine — the resume/cover letter should acknowledge these through framing rather than trying to claim them"

## Anti-Patterns to Avoid

1. **Don't lead the witness.** Ask what they did, not "did you do X?" The goal is to surface real experience, not manufacture claims.
2. **Don't map everything to the JD in real-time.** Explore the experience first, then map it. If you start with "the JD says X, do you have X?" the user will either stretch to fit or dismiss relevant adjacent experience.
3. **Don't write profile entries in JD language.** The profile is the source of truth. Resume tailoring happens later. Profile entries should use the user's domain language.
4. **Don't skip the review step.** Always show the user what you're adding to the profile before writing it. They'll catch attribution errors and scale mistakes.
5. **Don't explore more than 5-6 gaps in one session.** The interview gets fatiguing. Prioritize the highest-impact gaps and save the rest for another session.
6. **Don't update the profile with speculation.** If the user says "I think we might have done something like that," that's not enough to write a profile entry. Ask follow-up questions to confirm, or note it as unconfirmed.
