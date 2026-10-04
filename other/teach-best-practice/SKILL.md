---
name: teach-best-practice
description: Use when the user wants to explain, share, or advocate for a best practice with others — a team, manager, client, or stakeholder. Produces structured talking points, a brief explanation, or a presentation outline tailored to the audience's priorities and likely objections.
source: Kirkpatrick training evaluation model (Kirkpatrick, 1959); "The Mentor's Guide" (Lois Zachary, 2000); "Made to Stick" (Heath & Heath, 2007) — audience-first communication
tags: [teaching, sharing, presentation, advocacy, team, stakeholders, communication, onboarding]
---

# Teach Best Practice

Produce audience-tailored talking points, briefs, or slide outlines for sharing a practice with others.

## Why This Is Best Practice

**Adopted by:** The Kirkpatrick model (1959) — the dominant training evaluation framework — identifies audience alignment as the primary predictor of learning transfer: content that maps to what the audience already cares about is retained and applied; content framed around the presenter's priorities is forgotten. "Made to Stick" (Heath & Heath, 2007) synthesizes decades of communication research into the SUCCESs framework — and audience-first framing is its first principle. Professional communications training at McKinsey, BCG, and major law firms teaches "lead with the client's problem, not your solution."
**Impact:** Kahneman & Tversky (1979) establish that loss aversion is 2× more persuasive than equivalent gain framing — "without this, you risk X" outperforms "with this, you get X" for the same information. Presentations that lead with the audience's risk rather than the practice's features generate higher adoption intent (Heath & Heath, 2007).
**Why best:** The alternative — explaining a practice in the terms that matter to you — produces the "curse of knowledge" failure: you know why the practice is good, but your audience evaluates it against their own priorities, which you haven't addressed. Audience analysis before content creation is the difference between sharing information and changing behavior.

Sources: Kirkpatrick (1959) training evaluation model; Heath & Heath (2007) "Made to Stick"; Kahneman & Tversky (1979) prospect theory; McKinsey communication training principles

## Steps

### Step 1: Identify the practice and audience

From user input: "explain X to my team", "convince my manager to adopt Y", "help me present Z to a client", "how do I get my org to start doing W?"

If audience isn't clear, ask ONE question:
```
Who are you explaining this to, and what do they care about most?
```

### Step 2: Analyze the audience

| Audience type | What they care about | Primary skepticism |
|---------------|---------------------|--------------------|
| **Technical team** | Correctness, efficiency, avoiding tech debt | "This adds process overhead without clear payoff" |
| **Non-technical manager** | Outcomes, risk reduction, cost, timeline | "Unproven approaches waste time and money" |
| **Client / stakeholder** | Results, liability, ROI, competitive position | "Too complex, too risky, or not relevant to us" |
| **Peer practitioner** | Nuance, trade-offs, applicability to their context | "I already know this, or we tried it and it didn't work" |
| **Compliance / mandate audience** | What exactly is required, how to do it correctly | "I don't have a choice, just tell me what to do" |

If the audience type is ambiguous, infer from context clues (role titles, stated concerns, relationship to the user).

**Audience fallback:** If audience level cannot be inferred from context (no role mentioned, no prior conversation signals, no domain expertise cues), ask ONE question before proceeding:
'Who is this for? [beginner / intermediate / expert — or describe the audience]'

Do not guess expertise level when teaching — wrong level means the explanation is either too basic (wastes expert's time) or too advanced (loses beginner). This is the one question worth asking.

### Step 3: Structure the explanation for the audience

Use this structure, translated into the audience's language and priorities:

**Hook** — lead with what they care about losing, not what they gain.
For technical teams: what breaks or accumulates debt without this.
For managers: what risk materializes, what cost increases.
For clients: what liability or competitive disadvantage arises.
For peer practitioners: what edge cases or failure modes they're missing.

**What it is** — one sentence, in their language. Avoid jargon they don't use.

**Why it works** — the mechanism, in terms of their priorities. Not "it reduces complexity" but "it means the team spends 40% less time in rework" (for managers) or "it eliminates the class of bugs that come from shared mutable state" (for engineers).

**Evidence** — the strongest proof point for their skepticism threshold. Managers want org-scale adoption or ROI data. Engineers want technical credibility (who uses it, what it prevents). Clients want liability or competitive examples.

**How to start** — the lowest-friction first step they can take. Specific and small. The goal is activation, not comprehension.

**What to expect** — what changes, what doesn't, realistic timeline for seeing results. Remove uncertainty about the adoption cost.

### Step 4: Anticipate objections

For the detected audience type, list the 2–3 most common objections and a concrete response to each:

```
Likely objection: "[specific objection in their language]"
Response: [one concrete counter, specific to this practice and audience — not generic reassurance]
```

For compliance/mandate audiences: skip objection handling — replace with "What's required" and "What counts as compliant."

### Step 5: Produce the artifact

Choose the format based on context. If not obvious, ask:
```
What format works best? Talking points (conversation), brief (written message), or slide outline (presentation)?
```

**Format selection:** Choose format based on audience and goal:
- **Walkthrough** — beginner, unfamiliar with the practice
- **Example-first** — intermediate, learns by seeing concrete cases
- **Socratic** — expert, benefits from being guided to the answer rather than told
- **Comparison** — when the user asked 'why X instead of Y?' — contrast is the teaching vehicle

Default to walkthrough for unknown audience. State the chosen format at the start: 'Teaching [practice] using [format] format for [audience].'

**Talking points** (default — for conversations):
5–7 bullet points, each one sentence, sequenced hook → what → why → evidence → how to start. Include one objection response per likely pushback.

**Brief** (for written communication — email, memo, Slack):
3 paragraphs: (1) hook + problem, (2) what it is + why it works + evidence, (3) how to start + what to expect. 150–250 words.

**Slide outline** (for presentations):
5-slide structure, one-line content per slide:
- Slide 1: Hook — the risk/cost without this practice
- Slide 2: What it is — one sentence + key steps
- Slide 3: Evidence — strongest proof point for this audience
- Slide 4: How to start — specific first action + timeline
- Slide 5: Q&A / objections — top 2 anticipated

Never produce a full presentation deck — produce the outline and let the user build it.

## Rules

- Always lead with the audience's priorities, not the practice's features
- The hook must reference a loss or risk, not a gain — loss aversion is 2× more persuasive (Kahneman & Tversky, 1979)
- Never produce a full presentation deck — produce the outline only
- For compliance/mandate audiences, skip persuasion entirely — focus on what's required and how to comply correctly
- Objection responses must be specific to the practice and audience — not generic reassurance ("great question, this is actually fine")
- The artifact format must be named explicitly — talking points / brief / slide outline — so the user knows what they received

## Common Mistakes

**Feature framing instead of audience framing**: leading with "this practice does X" rather than "without this, your audience's concern Y materializes." The practice's features are not the hook — the audience's problem is.

**Generic objection responses**: "That's a common concern, but this practice is well-established" does not address "we don't have time for this." Address the specific objection with the specific counter.

**Producing a full deck**: a slide outline serves the user better than a full deck — it's faster to produce, easier to customize, and leaves the design decisions to the person who owns the presentation.

**Same structure for all audiences**: a technical team and a non-technical manager need different hooks, different evidence, and different language. Don't apply the same talking points to both.
