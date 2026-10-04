---
name: think
description: >-
  Brainstorm, evaluate, or decide during product creation. Pause the pipeline to
  think through a problem, compare approaches, or explore ideas before committing.
  Use when: 'think about', 'brainstorm', 'evaluate', 'compare', 'should I', 'help me decide',
  'what if', 'not sure about', or any hesitation during /fill.
argument-hint: "[topic or question]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(myclaude *)
  - WebSearch
  - AskUserQuestion
---

# Think — Mid-Process Brainstorming & Decision Support

> The pipeline builds. This skill thinks. Use it whenever you need to pause, explore, or decide.

**When to use:** Between any two pipeline steps. During /fill when you're unsure about a section. Before /create when choosing a product type. Before /publish when evaluating readiness.

**When NOT to use:** For mechanical tasks (/validate, /package). Those have deterministic flows — thinking slows them down.

---

## Activation Protocol

0. **Shared preamble:** Load `references/quality/activation-preamble.md` — context assembly, persona adaptation, deterministic routing rules.
1. Read `creator.yaml` → adapt to profile.type and technical_level
2. If a product is active (workspace/{slug}/ exists), read `.meta.yaml` → understand current context
3. Parse `$ARGUMENTS` or conversation context to identify the thinking need
4. Route to the appropriate thinking mode
5. **Load voice identity:** Load `references/quality/engine-voice-core.md`. Every user-facing line in this skill honors the ✦ signature, three tones, and six anti-patterns.
5b. **Load UX vocabulary:** Load `references/ux-vocabulary.md` — translate all internal terms before creator-facing output.
5c. **Load proactives:** Load `references/engine-proactive.md` — wire #17 (lost creator detection: if the creator has been in /think for 3+ questions without resolution, suggest concrete next step or /scout).

---

## Thinking Modes

### MODE 1: Brainstorm (divergent)
**Trigger:** "brainstorm", "ideas for", "what could", "possibilities"

Generate 5-7 distinct approaches to the creator's question. For each:
- Name it in 3 words
- One sentence description
- Strength (why this works)
- Risk (why it might not)

End with: "Which resonates? Or want me to combine elements from multiple?"

### MODE 2: Evaluate (convergent)
**Trigger:** "evaluate", "compare", "which is better", "pros and cons"

Structure the evaluation as a decision matrix:

```
EVALUATING: {what's being compared}

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| {criterion_1} | {score/assessment} | ... | ... |
| {criterion_2} | ... | ... | ... |

RECOMMENDATION: {option} because {one-sentence reasoning}
RISK: {what could go wrong with the recommendation}
```

### MODE 3: Decide (commit)
**Trigger:** "should I", "help me decide", "which type", "what approach"

Walk through a 3-step decision:
1. **What are you optimizing for?** (speed, quality, simplicity, market fit)
2. **What are the constraints?** (time, skill level, dependencies)
3. **Given 1+2, the best path is:** {recommendation with clear reasoning}

Then: "Ready to act on this? Here's the command: {next_command}"

### MODE 4: Explore (research)
**Trigger:** "what if", "how does", "is there a way to", "explore"

Investigate the question using available context:
- Search workspace/ for related patterns
- Check product-dna/ for type-specific guidance
- Search marketplace via `myclaude search --json 2>/dev/null` if relevant (silent-skip on failure per `references/cli-contract.md`)
- Read references/ for best practices

Synthesize findings, then suggest actionable next steps.

### MODE 5: Unstuck (unblock)
**Trigger:** "I'm stuck", "not sure", "confused", "don't know how"

Diagnose the block:
1. Read current product state from .meta.yaml
2. Identify where in the pipeline the creator is stuck
3. Ask ONE clarifying question to narrow the block
4. Offer 2-3 concrete paths forward, each as a command or action

---

## Context-Aware Behavior

If invoked DURING /fill (detected by conversation context):
- Don't break the section walker flow
- Frame thinking as "let's pause on this section"
- After thinking resolves, seamlessly resume: "Ready to continue with {next_section}?"

If invoked BETWEEN commands:
- Full thinking mode, no time pressure
- Can explore multiple angles

If invoked with a product slug:
- Load that product's full context before thinking
- Frame recommendations in terms of that specific product

---

## Marketplace Intelligence

**CLI contract:** Load `references/cli-contract.md` for unified error handling. Both commands are **silent-skip** severity — thinking proceeds without marketplace data if CLI is unavailable.

If the thinking question is about product strategy ("should I build X?", "is there demand for Y?"):

```bash
myclaude search "{relevant_query}" --json 2>/dev/null
myclaude trending --json 2>/dev/null
```

Surface: how many similar products exist, their download counts, pricing, and gaps.

"There are {N} products in this space. The top one has {downloads} downloads. Your differentiation could be: {suggestion based on gap analysis}."

---

## Anti-Patterns

1. **Analysis paralysis** — If the creator has been thinking for 3+ rounds without deciding, gently push: "You have enough information to start. The best way to test an idea is to build v1. You can always iterate."
2. **Thinking when doing is needed** — If the question has an obvious answer ("should I add a README?"), skip thinking mode and just do it.
3. **Scope expansion** — Thinking can expand scope. Always anchor back: "This is interesting, but for YOUR current product ({slug}), the relevant part is: {focused takeaway}."
4. **Replacing /validate** — Thinking is subjective exploration. Quality checks are objective. Don't let /think substitute for /validate.
5. **Endless brainstorm** — Cap brainstorm rounds at 3. After 3: "We've explored enough. Pick one and let's build."

---

## Quality Gate

- [ ] Thinking output is actionable (ends with a clear next step or command)
- [ ] Adapted to creator's language and technical level
- [ ] If product context exists, thinking is anchored to that product
- [ ] Analysis paralysis guard: no more than 3 rounds without a decision push

---

## Compact Instructions

When summarizing this conversation, always preserve:
- The specific question or decision the creator was thinking about
- Key options evaluated and the reasoning for/against each
- The final recommendation or decision made
- Any marketplace data surfaced during exploration
- The command or action suggested as next step
