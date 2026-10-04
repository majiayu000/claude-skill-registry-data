---
name: research-plan-workshop
version: 1.0.1
description: Use when starting a new research project or when the research question is still unsettled, to draft a one-page research plan (question, audience/venue, definition of done) through interactive dialogue with the user
---

# Research Plan Workshop Skill

## Purpose
As Phase 0 of paper writing, lock the research question, target audience/venue, and definition of done to a single page through dialogue with the user. The agent elicits the user's decisions rather than inventing a plan, and stops oversized scope on the spot.

## Trigger Conditions
- When starting a new paper or research project
- When the research question is not yet a single sentence
- When `docs/design/research-plan.md` is missing or outdated
- When Phase 0 of [`paper-writing-onboarding`](../paper-writing-onboarding/SKILL.md) begins

## Dialogue Rules (Required)

1. **Do not write first**: Do not create or overwrite `docs/design/research-plan.md` until the user approves the draft.
2. **One topic per turn**: Ask about one theme at a time. Do not dump a list of ten questions.
3. **Do not decide**: The agent must not finalize the research question, venue, or deadline. Candidates are allowed; the user chooses.
4. **Do not invent facts**: Do not present nonexistent conference names, deadlines, or length rules as confirmed. Mark unknowns as tentative.
5. **If the user says "you decide"**: Still offer 2–3 candidates and ask them to pick.
6. **Prefer existing files**: If `docs/design/research-plan.md` exists, read it first and ask only what to revise.

If the host has a structured-question UI, still keep the one-theme-per-turn constraint. Do not depend on a specific tool.

## Pre-Checks

At the start of the dialogue, check the following (read if present; do not create if absent):

- `docs/design/research-plan.md` (existing plan)
- `docs/design/domain-concepts.md` (early concept notes)
- `docs/literature/literature-matrix.md` (existing literature grasp)
- [`config/user_preferences.json`](../../../config/user_preferences.json) (writing language)

Create `docs/design/` if missing. Write the plan file only after approval.

## Dialogue Protocol

At the end of each turn, restate what was locked in that turn and confirm before moving on.

### Turn 1: Motive and Puzzle
Ask only what is needed:

- What is bothering them (a phenomenon, contradiction, or practical problem)
- What they already know / do not know
- What this paper should not try to do (out-of-scope candidates)

Paraphrase the user's words and correct any mismatch. Do not finalize the research-question sentence in this turn.

**Task Initiation Support (S1 Principle)**: If the user falls silent or appears confused, offer 2–3 **priming questions** to lower the initiation barrier:
- "Is there a paper or article you read recently that stuck with you?"
- "Have you noticed any contradiction or puzzle in your work or daily life?"
- "Is there a topic you've been curious about but haven't had time to explore?"

### Turn 2: One-Sentence Research Question
From Turn 1, offer **2–3 one-sentence research-question candidates**. Each candidate must:

- Be one sentence (do not join two independent claims with "and")
- Be investigable or arguable (not just a topic label)
- Make clear what will be established

Ask the user to choose or edit. Send it back if any of the following hold:

- The sentence contains two or more claims
- It only says "this paper examines X" without a question
- The scope belongs to a dissertation, not one paper

Adopt only the locked one-sentence question.

### Turn 3: Audience and Venue
Ask:

- Whom they need to convince (field, role, imagined reviewers)
- Preferred venue type (conference / journal / preprint server)
- Writing language

When offering candidates:

- Show a small set that matches field custom
- Label specific names as "to confirm" or "tentative"
- Leave final venue selection to [`submission-venue-advisor`](../submission-venue-advisor/SKILL.md); lock audience and venue *type* here

### Turn 4: Definition of Done
Ask:

- Chapter structure (do not impose a field template; if unset, offer IMRaD vs. chaptered monograph)
- Target length in words or characters (mark "tentative" if the venue rule is unknown)
- Deadline (distinguish submission date from draft deadline)

If length is unset, offer these as tentative ranges and let the user pick:

- Conference paper: 4,000–8,000 words
- Journal article: 6,000–10,000 words
- Preprint / working paper: user decides

### Turn 5: Approve and Write
Show a one-page draft in chat. Write the file only after the user approves. If it exceeds one page, cut and reshow (about 400 words of body).

Write `docs/design/research-plan.md` (one page maximum):
- The research question in a single sentence
- Target audience and venue (conference, journal, preprint server)
- Definition of done (chapter outline, target length, deadline)

## Output Template

```markdown
# Research Plan

## Research Question
[one sentence]

## Audience and Venue
- Readers:
- Venue (conference / journal / preprint server):
- Status: confirmed | tentative

## Definition of Done
- Chapter structure:
- Target length:
- Deadline:

## Scope
- In scope:
- Out of scope:

## Open Items
- [ ]

## Next Phase
→ scholarly-concept-modeling
```

Keep optional sections (scope, open items) to short bullets. The one-page limit outranks extra sections.

## After Completion
Propose [`scholarly-concept-modeling`](../scholarly-concept-modeling/SKILL.md) as the next move (do not force it). If the method is diachronic (conceptual history, genealogy, institutional history), propose [`diachronic-claim-typing`](../diachronic-claim-typing/SKILL.md) before literature search. If the venue is still tentative, note in the plan that [`submission-venue-advisor`](../submission-venue-advisor/SKILL.md) will reselect it after manuscript verification.

## Outputs
- `docs/design/research-plan.md` (Research plan: question, target venue, definition of done)
