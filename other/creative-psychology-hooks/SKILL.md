---
name: creative-psychology-hooks
description: Generate ad hook and angle ideas grounded in a structured creative psychology framework (TEEP, valence/intensity mapping, the Baader Hook Framework, micro-moment mapping) rather than generic brainstorming. Use whenever the user wants new hook ideas, ad angles, script openers, or wants existing hooks graded/critiqued on psychological mechanism. No data source required — this is a standalone ideation lens that can run with or without ad account access, and combines with competitor or own-creative pattern data when available.
---

# Creative Psychology Hooks

Generates and grades ad hooks/angles using a structured psychological framework instead of vibes-based brainstorming. Works standalone for cold ideation, or as the "why would this work" lens applied on top of patterns surfaced by `competitor-ad-intelligence` and `own-creative-diagnosis`.

## When to use this skill

- "Give me hook ideas for [product]"
- "Why would this angle work / not work psychologically?"
- Grading a batch of hooks before they go into a creator brief
- As the psychological-mechanism layer inside `winning-pattern-synthesis`

## Step 1: Gather product/audience context

Before generating anything, confirm (infer from conversation where possible, ask only what's missing):
- Product/offer and its core benefit
- Target audience — who specifically, and what state they're in when they see the ad (scrolling passively vs actively searching)
- Primary objection or hesitation this audience has toward the category
- Tone constraints, if any (brand voice, platform norms)

## Step 2: Apply the framework

### TEEP (Thought → Emotion → Expression → Physiology)
For each candidate hook, trace the chain it's meant to trigger in the viewer:
- **Thought**: what cognitive frame does the opening line/visual plant? ("this is about me," "this is a problem I have," "this is surprising")
- **Emotion**: what feeling follows from that thought?
- **Expression**: what does that emotion look/sound like — the tone, pacing, visual choice that should carry it
- **Physiology**: what physical reaction is being aimed for — lean in, laugh, wince, nod. This is the tell for whether a hook will actually stop a scroll.

A hook that skips straight to Expression without a real Thought→Emotion chain behind it reads as hollow or clickbait — flag these.

### Valence / Intensity Mapping
Plot each hook on two axes:
- **Valence**: positive (aspiration, relief, humor) vs negative (fear, frustration, FOMO)
- **Intensity**: low (mild curiosity) vs high (urgent, provocative)

High-intensity negative hooks (fear/frustration) may attract attention but can create brand-fatigue or backlash risk if overused. Low-intensity positive hooks may fit the brand better but should not be assumed to stop the scroll. Treat these as test hypotheses, account for the audience's tolerance, and recommend a spread across the matrix rather than five hooks in one quadrant.

### Baader Hook Framework
Classify each hook by mechanism, not just topic:
- **Pattern interrupt** — visually or verbally breaks the expected feed rhythm
- **Open loop** — poses a question/tension the viewer needs resolved
- **Direct claim** — bold, specific, falsifiable-sounding statement
- **Identity call-out** — names the exact audience ("if you have curly hair...")
- **Social proof lead** — opens with someone else's result/reaction, not the brand's claim

Every hook in a batch should be tagged with its mechanism. A batch that's 80% one mechanism isn't actually a diverse test — flag that too.

### Micro-Moment Mapping
Identify the specific real-world moment the hook is trying to interrupt or attach to (e.g. "just noticed hair thinning in a photo," "scrolling in bed frustrated with current routine"). Concrete moments produce more specific, testable creative hypotheses than generic "are you tired of X" openers; do not claim they will outperform without account evidence.

## Step 3: Generate

Produce hooks in batches of 8–10 by default (adjust if the user asks for fewer/more). Spread deliberately across:
- Valence/intensity quadrants
- Baader mechanisms
- At least 2 distinct micro-moments

## Step 4: Grade (when reviewing existing hooks)

For each hook, output: TEEP chain (does it hold together?), valence/intensity position, Baader mechanism, micro-moment specificity, and a one-line verdict on why it would or wouldn't stop a scroll for this audience.

## Output Format

```
### Hook Set: [Product/Audience]

Context: [product, audience, objection, tone]

| # | Hook | Mechanism | Valence/Intensity | Micro-moment | Why it may work |
|---|---|---|---|---|---|

Coverage check: [mechanisms used, quadrants covered, any gaps]
```

## Guardrails

- Don't force every hook into every framework layer if it doesn't fit — a strong hook that's hard to TEEP-trace cleanly is still worth including; note the ambiguity rather than distorting the analysis.
- Avoid defaulting to fear/negative-valence hooks purely because they're easier to generate — deliberately include positive-valence options.
- This skill produces angles and hook lines, not full scripts — hand off to `ad-brief-generator` for shoot-ready briefs.
