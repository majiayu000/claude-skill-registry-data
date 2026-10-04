---
name: idea-griller
description: Use when user describes a new idea, project, or feature they haven't fully thought through, when an idea needs to be pressure-tested before writing a spec, when assumptions about users, business model, or distribution are unstated, or when the user wants to surface what they don't know before committing engineering effort.
---

# Idea Griller

## Overview

Pressure-test a raw idea through Socratic questioning. One question per turn, each built from the user's last answer. Output is `.forge/idea-brief.md` — a structured brief that lets `spec-driven-development` skip discovery and go straight to requirements.

## When to Use

- User describes a new idea, project, or feature they haven't fully thought through
- User wants to stress-test assumptions before writing a spec
- Idea is vague, contradictory, or needs a sharper scope

## When NOT to Use

- `.forge/prd.md` already exists — the idea is past this stage
- User is reporting a bug — use `debugging-and-recovery`
- Idea is already well-specified with named users, clear scope, and a distribution plan

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "The idea is obvious, let's skip to the spec" | Obvious ideas carry the most unchecked assumptions |
| "The user knows what they want" | They know symptoms — root cause is often different |
| "One more question is too many" | Vague answers compound — drill until specific |
| "I can infer the business model" | Never infer. Ask. You will be wrong. |
| "The MVP is clear" | MVPs defined without drilling risks are over-scoped |
| "We can resolve distribution later" | If you can't name channel + motion now, the idea isn't ready |
| "We covered the important branches" | Important by whose criteria? Distribution and Risks are the most-skipped and the most-costly to miss. |

## Red Flags

- User says "everyone" or "all users" — no segment identified
- Answer to distribution is "word of mouth" or "social media" — not a plan
- MVP scope grows across turns — riskiest assumption not isolated
- User can't name a single person who has this problem today
- Business model is "we'll figure it out later"
- Founder fit answer is "I'm passionate about this space"
- Interview stopped before all 7 branches because "the idea is clear enough" or "we ran out of time"

## Behavior Rules

- **One question per turn. Always.**
- Generate each question from the user's last answer — never from a fixed script
- If vague or contradictory: drill deeper on the same branch
- If clear and specific: acknowledge briefly (one line), advance to next branch
- Max 3 questions per branch — don't loop forever
- Push back on weak answers. "People want this" requires evidence.
- Note unresolved items as open assumptions in the brief

## Branches

Work through in order. Each is a checkpoint to *reach*, not a question to *ask*. See [evaluation-criteria.md](evaluation-criteria.md) for resolution criteria per branch.

1. **Problem** — what's broken, for who, how often, how painfully
2. **Founder fit** — why this person, why now, what's the unfair advantage
3. **Solution** — what specifically; what's explicitly out of scope
4. **Business model** — how money flows, who pays, how much
5. **Distribution** — how the first 100 users find it; specific acquisition motion
6. **Risks** — the single most likely way this fails
7. **MVP** — the smallest thing that tests the riskiest assumption

## Workflow

1. Ask the user to describe their idea in a few sentences. Take it in — no clarifying questions yet.
2. Start branch 1. Generate your first question from what they said.
3. After each answer: clear → acknowledge + advance; vague → follow-up that names the vagueness explicitly ("You said 'small businesses' — do you mean a 2-person bootstrapped shop or a 50-person company with a finance team?").
4. When all 7 branches are resolved (or explicitly noted as open assumptions), write the brief.

## Output

Create `.forge/` if it doesn't exist. Write `.forge/idea-brief.md` with a `forge:meta` dependency header at the top (`generated_by: idea-griller`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: []` — independent, no upstream, `generated_from: {}`, `content_hash: <sha256 first 8 of THIS file's body>`). See [forge-dependency-graph](../../references/forge-dependency-graph.md) for the convention. Then the brief content:

```markdown
<!-- forge:meta
generated_by: idea-griller
generated_at: 2026-05-13T12:00:00Z
depends_on: []
generated_from: {}
content_hash: <first 8 chars of sha256>
-->

# Idea Brief: [idea name]

## The problem
[Specific user, specific pain, specific frequency — 1-2 sentences]

## Founder fit
[Why this person. What they know or have that others don't.]

## The solution
[What it is. What it is NOT.]

## Business model
[Who pays. How much. Why they would.]

## Distribution
[How first 100 users are acquired. Specific channel — not "word of mouth".]

## Biggest risk
[The single most likely failure mode.]

## MVP
[The smallest thing that tests the biggest risk.]

## Open assumptions
[Anything unresolved. These become explicit gaps in the spec.]
```

After writing: "Brief written to `.forge/idea-brief.md`. Run `/spec` to continue."

## Verification

- [ ] All 7 branches reached (or explicitly skipped with reason noted in Open assumptions)
- [ ] No answer left as "everyone", "scale", or "later"
- [ ] At least one named person or company as the target user
- [ ] MVP is a single testable thing, not a feature list
- [ ] Distribution names a specific channel and motion
- [ ] Open assumptions section populated (empty = suspicious)
- [ ] `.forge/idea-brief.md` written and readable
