---
name: discovery-brief
description: Run a structured discovery interview for a new client project and turn the answers into a completed brief plus a strategy starter document. Conversational, skips what is already known, and never fabricates unanswered questions. Use when the user says "run discovery", "brief for this client", "discovery questionnaire", or "help me figure out what this client needs".
---

# Discovery Brief

A project priced before discovery is a project scoped by hope. This skill runs the discovery conversation and turns the answers into two working documents: the brief (the project's source of truth) and a strategy starter (the first thinking pass).

This is the interview counterpart to a client-facing intake form: the `client-intake-builder` skill generates an HTML questionnaire the CLIENT fills in alone; this skill interviews YOU (or processes the client's answers) and writes the documents.

## Step 1: Read what already exists

Before asking anything, read whatever the user points at: an existing brief, intake form answers, emails, meeting notes, the client's website. Never ask a question the material already answers.

## Step 2: Interview across seven areas

Ask in small batches, not twenty questions at once. Skip known answers.

1. **Business**: what the client does, how they make money, what stage they are at (new, rebrand, growing).
2. **Audience**: who buys now, who they WANT to buy, price positioning (budget, mid, premium).
3. **Competitors**: two or three names, what the client envies or hates about each.
4. **Personality**: three to five adjectives the brand should own, two or three it must never be.
5. **Style direction**: references they love, styles or colours that are off-limits.
6. **Deliverables**: exactly what the project produces (logo, identity system, guidelines, packaging, website, motion, other).
7. **Timeline and budget**: deadline and budget range, mapped against the user's own tiers if a pricing config exists (see the `proposal-writer` skill).

## Step 3: Write the two documents

**The brief** (default `Brief.md` in the client's folder): status, started date, scope checklist, and every answer organized under the seven areas. Keep the client's own words where they are vivid; quote them. Unknowns stay visible as open items, never filled with guesses.

**The strategy starter** (default `Strategy/01_Strategy.md`):

```markdown
# <Client> Strategy Starter

## Positioning (draft)
One sentence: for WHOM, the brand is WHAT, unlike COMPETITOR because REASON.

## Audience snapshot
## Competitive picture
What competitors do visually or verbally, and where the gap is.

## Personality and tone
The adjectives, and what each means in practice.

## Direction hypotheses
Two or three distinct directions worth exploring, two lines each.

## Open questions
Everything discovery did not answer.
```

## Step 4: Report

Summarize the positioning sentence and the direction hypotheses in chat, with both file paths. Suggest the natural next step (a proposal, or moodboards).

## Rules

- Never fabricate answers. Unanswered questions go under Open questions.
- One project per run. Discovery does not batch.
- No em dashes in any output.

## Output

A completed brief and a strategy starter document, plus a chat summary of positioning and direction hypotheses.
