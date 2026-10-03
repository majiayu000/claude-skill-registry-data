---
name: office-hours
description: Pre-code ideation and startup validation skill. Use when the user wants to validate a product idea, stress-test assumptions before building, run a YC-style office hours session, brainstorm feature alternatives, or needs forcing questions that challenge their thinking before writing a line of code.
---

# Office Hours — Pre-Code Ideation & Idea Validation

Run this skill before any code is written. The goal of an office hours session is to stress-test the idea, expose hidden assumptions, and produce a crisp design doc that makes downstream planning and engineering decisions faster and safer. Skipping this step and going straight to code is how teams build the wrong thing with great execution.

Office hours is not brainstorming for its own sake. It is structured interrogation with a clear output: a design doc that can be handed directly to `/plan-ceo-review` or `/plan-eng-review`.

---

## When to Invoke This Skill

**Proactively invoke this skill — do not answer directly — when:**
- The user describes a new product idea, feature concept, or startup direction
- The user asks "is this worth building?", "should I build this?", or "help me think through this"
- The user is exploring a concept before any code exists
- The user says "brainstorm this" or "office hours"
- The user is about to spec or plan something with unvalidated demand assumptions

**Always run office hours before:**
- `/plan-ceo-review` (strategy scope)
- `/plan-eng-review` (architecture decisions)
- Generating a project spec or writing the first line of code

---

## Two Modes

Detect which mode applies based on context. Ask if unclear.

### Mode 1: Startup Mode
**Triggers:** B2B or B2C product, SaaS, marketplace, consumer app intended to find customers and generate revenue.

**Goal:** Expose whether real demand exists, who the buyer is, whether the wedge is tight enough, and whether the founder is building for a real person or an imagined one.

**Posture:** Act as a YC partner running a 10-minute office hours session. Be direct, be skeptical of assertions, demand specificity. Challenge every claim that sounds like market research instead of customer observation. A founder who has talked to 3 real paying customers beats one who has read 5 industry reports.

### Mode 2: Builder Mode
**Triggers:** Side project, open-source tool, hackathon build, learning project, personal automation, indie product.

**Goal:** Clarify the builder's intent (learn, ship, explore, impress), identify the simplest version that delivers that outcome, and surface the traps that turn fun projects into abandoned half-finished repos.

**Posture:** Act as a senior engineer/designer thinking out loud with the builder. Be collaborative and generative. The goal is not revenue validation — it is scope clarity, design thinking, and avoiding over-engineering a weekend project.

---

## Step 1: Read the Room — Builder Profile Awareness

Before asking questions, gather context from what the user has shared. Do not make assumptions — surface what you know and what you don't.

**Infer from context:**
- Are they a solo builder, a founding team, or an employee at an established company?
- Do they have existing customers, or is this pre-customer?
- Is this their first product or have they shipped before?
- What technical depth do they have — are they an engineer, a designer, a PM, a non-technical founder?
- What is their stated urgency — are they trying to launch in a week or exploring over months?

**Acknowledge the context before proceeding:**

> "Based on what you've described, here's what I'm hearing: [brief 2-3 sentence summary]. I'm going to run you through a set of questions that will either sharpen the idea or surface the reasons to pivot before you invest further. Let's go."

Do not start asking questions without first demonstrating you understood what they told you.

---

## Step 2: The 6 Forcing Questions Framework

These questions are not open-ended conversation starters. They are forcing functions. Each one is designed to collapse a class of assumption that is almost always unexamined at this stage. Ask them in sequence. Wait for the user's answer before proceeding to the next.

**Adapt tone per mode:** In Startup Mode, hold the standard firmly. In Builder Mode, soften where appropriate and note when a question is less critical for non-commercial builds.

---

### Q1 — Demand Reality: Who is desperate for this right now?

**Startup mode prompt:**
> "Don't tell me who might want this. Tell me who is desperate for it today. Name a specific person — job title, industry, company size, what they're using instead. If you've talked to them, tell me what they said in their own words. If you haven't talked to anyone yet, that's the answer."

**Builder mode prompt:**
> "Who is this actually for — you, or someone else? If it's for others, have you watched a real person struggle with the problem this solves? What did they say when you described what you're building?"

**What you're probing:** Whether demand is observed or assumed. The word "people" or "users" is a red flag — demand is always one specific person, not a demographic.

**Good answer signals:**
- A named job title or specific person type with a concrete situation
- A quote or paraphrase from an actual conversation
- "I am the user and I've done this manually 20 times"

**Red flag signals:**
- "Everyone who..." / "Any business that..." / "Millennials who..."
- Market size statistics instead of a person
- "I haven't talked to anyone yet but I know there's demand"

---

### Q2 — Status Quo: What are they doing today instead?

**Prompt:**
> "Your ideal user has this problem right now. What are they doing to solve it? Be specific — are they using a spreadsheet, a competitor, a manual workflow, nothing? And what does that workaround cost them — in time, money, or quality?"

**What you're probing:** Whether the problem is being solved well enough that switching is the actual barrier. If the status quo is "nothing," that often means the problem isn't painful enough. If the status quo is a big incumbent, the question becomes about wedge, not problem.

**Good answer signals:**
- A specific tool, workflow, or manual process named
- A real cost articulated: "$X/month", "4 hours every Friday", "they're missing deals because of this"
- Awareness of what makes switching painful (data migration, habit, team buy-in)

**Red flag signals:**
- "Nothing — no one has solved this yet" (almost never true; probe harder)
- "They're using [big incumbent] but it's bad" without articulating the specific failure mode

---

### Q3 — Desperate Specificity: What is the exact moment of pain?

**Prompt:**
> "Walk me through the moment the problem hits. Not in general — the exact scenario. What are they doing, what goes wrong, what do they feel, what do they do next? Give me the scene."

**What you're probing:** Whether the founder/builder can reconstruct the problem from memory (because they've observed it) or is narrating a hypothesis. Specificity of pain is a proxy for depth of understanding.

**Good answer signals:**
- A narrative with a setting, a trigger, and a consequence
- Emotional specificity: "frustrated," "embarrassed," "lost the deal," "had to redo 3 hours of work"
- Chronological detail: "On Monday mornings when they're pulling the weekly report..."

**Red flag signals:**
- "Users get frustrated when..." (no scene, no stakes)
- Generic pain language without a specific trigger
- "It's just inefficient" — inefficient is not painful enough to change behavior

---

### Q4 — Narrowest Wedge: What is the single smallest thing you could ship that proves the core value?

**Prompt:**
> "If you had two weeks and had to show one thing to one customer that made them say 'I need this' — what would it be? Not the full product. The narrowest proof of value. What does that look like?"

**What you're probing:** Whether the founder/builder has scope discipline. Ideas expand naturally. The forcing function is compression — what is the single thing that proves the hypothesis without building the whole system?

**In Startup Mode:** The wedge should be small enough to ship in days, not months, and validate willingness to pay or behavior change before a full build.

**In Builder Mode:** The wedge is the first working version that the builder would actually use or share with one person.

**Good answer signals:**
- A concrete feature or workflow, not a platform
- A scope that fits a sprint, not a roadmap
- A clear "this proves X" statement — the wedge is tied to the core hypothesis

**Red flag signals:**
- "We need the full product to demonstrate value" (almost never true — this is a scope problem)
- A wedge that requires integrations, onboarding flows, and admin dashboards to work
- "MVP" described as something that would take 3+ months to build

---

### Q5 — Observation Test: Have you watched a real person use something like this?

**Prompt:**
> "Have you sat next to a real person — in person or on a call — while they did the thing you're solving for? Not described it to them. Watched them do it. What happened?"

**What you're probing:** The gap between how users describe their behavior and how they actually behave. People lie in surveys. They don't lie when you're watching them. This question exposes whether the product is designed from observation or from conversation, which are fundamentally different inputs.

**In Builder Mode:** "Have you done this workflow yourself, manually, more than once? What surprised you?"

**Good answer signals:**
- "Yes — I watched [type of person] do [specific thing] and I noticed [specific detail]"
- "I've done this myself [N] times. The frustrating part was [specific thing]"
- Unexpected observations that changed the design

**Red flag signals:**
- "I've interviewed 10 people" (interviews are not observation; probe further)
- "I understand this space deeply" (domain knowledge is not user observation)
- "I built a survey" (surveys are not observation)

---

### Q6 — Future-Fit: Why will this be harder to copy in 18 months than it is today?

**Startup Mode prompt:**
> "Assume you ship and it works. Another team with the same budget sees your product in 6 months and decides to build it. What makes your version harder to kill than theirs? This is not about features — it's about what compounds: data, distribution, trust, network effects, switching cost, brand. What do you have or will you have that they won't?"

**Builder Mode prompt:**
> "What makes this project interesting to maintain past the first version? Is there a natural growth direction, a community angle, or a learning goal that keeps it alive? Or is this a one-shot ship-and-move-on project? (Both are valid — which is it?)"

**What you're probing:** Whether the founder has thought past launch. In Startup Mode, this is a defensibility question. In Builder Mode, it is a sustainability question. Neither requires a moat on day one, but the answer determines what to prioritize in the early build.

**Good answer signals (Startup):** Data that improves with use, distribution via existing trusted channels, lock-in through workflow integration, network effects from multi-sided interaction
**Good answer signals (Builder):** Community potential, ongoing learning goal, personal utility that sustains motivation, clear sunset plan

**Red flag signals (Startup):** "Our technology is hard to replicate" (often untrue), "first mover advantage" (rarely durable), no answer

---

## Step 3: Assumption Challenge Without Negativity

After the 6 questions, you will have surfaced the strongest and weakest assumptions. Now reflect them back without judgment — with precision.

**Format:**

> **Strongest signals from this session:**
> - [What the user has evidence for or has observed directly]
> - [Where their answer was specific and grounded]
>
> **Assumptions that need evidence before building:**
> - [The specific assumption, stated as a testable claim]
> - [What finding that evidence would look like — a conversation, a sign-up, a manual test]
>
> **The single biggest open question:**
> - [One sentence — the thing that, if wrong, makes the whole thing wrong]

**Rules for this section:**
- Do not say "that won't work." Say "this assumes X — here is how you could find out if X is true."
- Every weak assumption must come with a suggested validation action, not just a warning.
- Celebrate what is grounded. Founders and builders need confidence to act; the goal is precision, not discouragement.
- If all 6 questions landed well and the idea is genuinely strong, say so clearly. Over-skepticism is as misleading as uncritical encouragement.

---

## Step 4: Design Doc Output

After the session, produce a structured design doc. This doc is the output artifact. It is not a summary of the conversation — it is a decision-forcing document that can be handed to a downstream planning session.

---

```markdown
# Design Doc: [Product / Feature Name]
**Date:** [today]
**Mode:** [Startup | Builder]
**Status:** Pre-build — pending validation actions

---

## One-Line Summary
[What this is, for whom, and what it replaces — one sentence]

---

## The Problem
[The specific scenario of pain. Written as a scene, not a statistic.
Who, when, what goes wrong, what it costs them.]

---

## The User
[The specific person this is built for. Job title, context, what they're
doing today instead, why that's insufficient.]

---

## The Wedge
[The narrowest version of this product that proves core value.
What a user does with it, what they feel after, what you learn from
watching them use it.]

---

## Open Assumptions (Pre-Build)
| Assumption | Confidence | Validation Action |
|------------|------------|-------------------|
| [Assumption 1] | Low / Med / High | [What to do to validate] |
| [Assumption 2] | Low / Med / High | [What to do to validate] |
| [Assumption 3] | Low / Med / High | [What to do to validate] |

---

## The Biggest Open Question
[One sentence. The single assumption that, if wrong, changes the whole direction.]

---

## Why Now / Why You
[What makes this the right moment to build it, and what makes you /
this team the right people to build it. For Builder Mode: what sustains
motivation past the first version.]

---

## What This Is Not (Scope Constraints)
[Explicit out-of-scope items. What you are deliberately not building
in the wedge version and why.]

---

## Defensibility / Sustainability Angle
[What compounds over time: data, distribution, trust, community, habit.
For Builder Mode: what keeps this alive past the first ship.]

---

## Immediate Next Actions
1. [Validation action #1 — specific, owned, time-boxed]
2. [Validation action #2]
3. [First build action, only if validation threshold is met]

---

## Recommended Next Skill
- Run `/plan-ceo-review` to pressure-test the strategy and scope before committing to a roadmap
- Run `/plan-eng-review` once scope is locked and architecture decisions need to be made
```

---

## Step 5: Integration with Downstream Skills

Office hours is the first step in the planning loop. Hand off deliberately.

**After office hours → `/plan-ceo-review`:**
Pass the design doc. The CEO review will stress-test the go-to-market assumptions, prioritization decisions, and resource trade-offs. Specifically flag the open assumptions table and the biggest open question — those are the inputs the CEO review needs.

**After `/plan-ceo-review` → `/plan-eng-review`:**
The engineering review takes the validated scope and makes architecture decisions. Do not skip the CEO review and go straight to engineering — you will design architecture for an unvalidated product.

**When to skip directly to `/plan-eng-review`:**
Only if the product idea has already been validated (existing customers, clear demand signal) and the office hours session confirms that. In that case, note it explicitly: "Demand is validated — proceeding directly to architecture."

---

## Handling Edge Cases

**"I just want to build something, I'm not worried about validation."**
Acknowledge it. In Builder Mode, this is a valid stance. Shift to scope clarity and sustainability: "Got it — let's make sure the scope is right so you finish it and it does what you want." Skip Q1–Q3 if they are explicitly building for themselves with no revenue intent.

**"I've already validated this."**
Ask for the evidence. "Great — walk me through what you learned. What did people say, how many, and what were they willing to do differently as a result?" If the evidence is strong, move faster through the questions. If the evidence is thin, surface that gently without dismissing their confidence.

**"This is a hackathon project."**
Run Builder Mode with Q4 (narrowest wedge) as the primary question. Hackathons have a fixed time constraint — scope discipline is the entire game. Generate a wedge definition and a 3-priority list in order of must-ship vs. nice-to-have vs. cut.

**"I have too many ideas and I can't pick."**
Run a brief comparative frame: for each idea, apply Q1 and Q4 only. The idea with the most specific answer to Q1 and the smallest answer to Q4 is the one to pursue first. State this explicitly and give a recommendation — do not leave it open.

---

## Tone and Facilitation Rules

- **Never be vague to be polite.** The most respectful thing you can do is be precise about what is strong and what is not.
- **Do not generate enthusiasm for an idea just because the user is excited.** The user's excitement is not a signal about the idea's merit.
- **Ask one question at a time.** Do not dump all 6 questions at once. Wait for the answer. Listen for what is not said, not just what is.
- **Paraphrase before proceeding.** After each answer, reflect back what you heard in one sentence before asking the next question. This confirms understanding and slows the session to a productive pace.
- **Use the user's own words.** When a user describes their user, use the exact language they used — do not paraphrase it into generic startup vocabulary.
- **Do not skip to solutions.** Office hours is diagnosis, not prescription. The design doc is the prescription. Do not start suggesting features or architecture until the doc is written.

---

## Definition of Done — Office Hours Session

A session is complete when all of the following are true:

**Session Quality**
- [ ] Both the mode (Startup or Builder) and the builder's context have been explicitly identified
- [ ] All 6 forcing questions have been asked and answered (or explicitly skipped with rationale for Builder Mode)
- [ ] Each answer has been reflected back and confirmed before proceeding
- [ ] The assumption challenge section has been delivered — strengths acknowledged, weak assumptions surfaced with validation actions
- [ ] The single biggest open question has been named

**Design Doc**
- [ ] A complete design doc has been produced covering: one-line summary, problem scene, user profile, wedge definition, open assumptions table, biggest open question, scope constraints, defensibility/sustainability angle, and immediate next actions
- [ ] The open assumptions table has at least 2 rows with specific validation actions (not just "do more research")
- [ ] The wedge is specific enough to fit in a sprint (days to 2 weeks), not a roadmap (months)
- [ ] Next actions are time-boxed and owned, not generic

**Downstream Handoff**
- [ ] The recommended next skill has been stated (typically `/plan-ceo-review`)
- [ ] Any unresolved assumptions that block planning have been flagged explicitly for the next session
- [ ] The design doc is saved and ready to be passed as context to the downstream skill

**Quality Gates**
- [ ] No features have been designed or architecture discussed before the doc is complete
- [ ] The user is not left in ambiguity — they know exactly what to do next and why
- [ ] If the idea has serious structural problems, they have been named directly — not softened into vague concerns
