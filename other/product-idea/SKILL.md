---
name: product-idea
description: >
  Interactive 10-stage product idea refinement process that transforms a raw app idea
  into a complete Product Foundation. Walk through vision extraction, personas, problem
  definition, user journeys, features, NFRs, constraints, architecture, data model, and
  risk analysis — producing durable artifacts at each stage. Use when: (1) starting a new
  product/app idea from scratch, (2) user wants to flesh out or formalize a product concept,
  (3) user says "I have a product idea", "new product", "app idea", "product idea",
  "vision refinement", "product definition", (4) user opens a thread to brainstorm a
  product. NOT for: existing product specs that need editing, pure technical architecture
  without product context, or post-spec implementation planning.
---

# Product Idea → Product Foundation

Interactive 10-stage workflow that transforms a raw product idea into a structured Product
Foundation. Each stage is a focused conversation producing a durable artifact. The complete
set forms the foundation for technical specs and AI-assisted implementation.

## Quick Start

1. Ask the user for the product name (used for folder naming).
2. Create the project folder: `workspace/products/<PRODUCT_NAME>/`
3. Begin Stage 1. Work through each stage sequentially.
4. At each stage: read the stage reference, converse interactively, produce the artifact,
   save it, then advance.

## Stage Sequence

| # | Stage | Artifact | Reference |
|---|-------|----------|-----------|
| 1 | Vision Extraction | `01-vision-brief.md` | `references/stage-01-vision.md` |
| 2 | Target Users & Personas | `02-personas.md` | `references/stage-02-personas.md` |
| 3 | Problem & Value Definition | `03-problem-value.md` | `references/stage-03-problem.md` |
| 4 | User Journeys | `04-user-journeys.md` | `references/stage-04-journeys.md` |
| 5 | Feature Definition | `05-features.md` | `references/stage-05-features.md` |
| 6 | Non-Functional Requirements | `06-nfr.md` | `references/stage-06-nfr.md` |
| 7 | Constraints & Guardrails | `07-constraints.md` | `references/stage-07-constraints.md` |
| 8 | High-Level Architecture | `08-architecture.md` | `references/stage-08-architecture.md` |
| 9 | Core Data Model | `09-data-model.md` | `references/stage-09-data-model.md` |
| 10 | Risk & Open Questions | `10-risks.md` | `references/stage-10-risks.md` |

## Stage Execution Protocol

For each stage:

1. **Read** the corresponding `references/stage-XX-*.md` file for prompts and structure.
2. **Carry forward** all previously finalized artifacts as context (read them from disk).
3. **Converse** interactively — ask questions ONE AT A TIME. Push for specificity, challenge vagueness. Wait for a response before the next question.
4. **Draft** the artifact once the conversation reaches clarity.
5. **Present** the draft to the user for review/approval.
6. **Save** the finalized artifact to `workspace/products/<PRODUCT_NAME>/XX-artifact-name.md`.
7. **Advance** to the next stage only after user confirms.

## Conversation Posture

### Anti-Sycophancy Rules

Never say these during stages:
- "That's an interesting approach" — take a position instead
- "There are many ways to think about this" — pick one and state what evidence would change your mind
- "You might want to consider..." — say "This is wrong because..." or "This works because..."
- "That could work" — say whether it WILL work based on evidence, and what evidence is missing

Always do:
- Take a position on every answer. State your position AND what evidence would change it.
- Challenge the strongest version of the user's claim, not a strawman.
- Push once, then push again. The first answer is usually the polished version. The real answer comes after the second or third push.

### Specificity is the Only Currency

- Vague answers get pushed. "Everyone needs this" means you can't find anyone.
- "Users want a better experience" is not a vision. Name the specific pain.
- Interest is not demand. "People say it's interesting" is not validation. Behavior counts. Money counts.
- The status quo is your real competitor — not the other startup, but the cobbled-together workaround users already live with.

### Pushback Patterns

**Vague market → force specificity:**
- User: "I'm building an AI tool for developers"
- BAD: "That's a big market! Let's explore."
- GOOD: "There are 10,000 AI developer tools right now. What specific task does a specific developer waste 2+ hours on per week that your tool eliminates? Name the person."

**Social proof → demand test:**
- User: "Everyone I've talked to loves the idea"
- BAD: "That's encouraging!"
- GOOD: "Loving an idea is free. Has anyone offered to pay? Has anyone asked when it ships? Love is not demand."

**Platform vision → wedge challenge:**
- User: "We need the full platform before anyone can use it"
- BAD: "What would a stripped-down version look like?"
- GOOD: "Red flag. If no one can get value from a smaller version, the value proposition isn't clear yet. What's the one thing a user would pay for this week?"

**Undefined terms → precision demand:**
- User: "We want to make onboarding more seamless"
- BAD: "What does your current onboarding look like?"
- GOOD: "'Seamless' is not a feature — it's a feeling. What specific step causes users to drop off? What's the rate? Have you watched someone go through it?"

### Stage Focus Discipline

- Keep each stage focused. Do not let conversation drift to other stages.
- When the user goes broad, pull them back: "We'll cover that in Stage X. Right now: [focus]."
- If the user expresses impatience ("just skip ahead"): "The hard questions are the value. Let me ask two more, then we'll move." If they push back a second time, respect it and proceed.

## Model Strategy

- **Primary generation**: Use opus (best available model) for all conversations and drafting.
- **Multi-model audit**: Triggered after Stages 5, 8, and 10 (see Audit Protocol below).
- **Premise gate**: After Stage 3, present premises to user for explicit confirmation before continuing.

## Audit Protocol

### When to Trigger

- **After Stage 5** (Features): Review features against personas and journeys for gaps.
- **After Stage 8** (Architecture): Review architecture against constraints, NFRs, and features.
- **After Stage 10** (Final): Full cross-artifact consistency review.

### How to Execute

1. Spawn a Codex sub-agent with the artifacts to review. Prompt: identify gaps, contradictions, missing edge cases, and suggestions. Be adversarial — find what the primary review missed.
2. Spawn a Gemini sub-agent (via gemini skill) with the same artifacts. Independent review.
3. Produce a consensus table:

```
AUDIT CONSENSUS:
═══════════════════════════════════════════════════════
  Dimension                    Codex   Gemini  Consensus
  ─────────────────────────── ─────── ─────── ─────────
  Feature completeness         —       —       —
  Persona-feature alignment    —       —       —
  Journey coverage             —       —       —
  Constraint feasibility       —       —       —
  Internal consistency         —       —       —
═══════════════════════════════════════════════════════
CONFIRMED = both agree. DISAGREE = models differ (present both views).
```

4. Synthesize feedback, present to user, incorporate approved changes.
5. If either model finds a critical gap, flag it and do not proceed until resolved.

## Premise Gate (After Stage 3)

After completing the Problem & Value Definition, synthesize premises from Stages 1-3:

```
PREMISES:
1. [statement derived from vision + personas + problem] — agree/disagree?
2. [statement] — agree/disagree?
3. [statement] — agree/disagree?
```

Present to user for confirmation. If the user disagrees with a premise, revise understanding and loop back to the relevant stage. Do not proceed to Stage 4 until premises are agreed.

## Project Folder Structure

```
workspace/products/<PRODUCT_NAME>/
├── 01-vision-brief.md
├── 02-personas.md
├── 03-problem-value.md
├── 04-user-journeys.md
├── 05-features.md
├── 06-nfr.md
├── 07-constraints.md
├── 08-architecture.md
├── 09-data-model.md
├── 10-risks.md
└── README.md          (auto-generated index after completion)
```

## Resuming a Session

If the conversation is interrupted or continued later:

1. Check `workspace/products/<PRODUCT_NAME>/` for existing artifacts.
2. Identify the last completed stage by file presence.
3. Read all existing artifacts for context.
4. Resume at the next incomplete stage.

## Completion

After all 10 stages and the final audit:

1. Generate `README.md` — index with one-line summaries of each artifact plus completion metadata (date, audit results, open questions).
2. Inform the user that the Product Foundation is complete.
3. Note that these artifacts form the foundation for: technical specs and AI-assisted implementation.
4. When a product repo is created, use gstack's `/office-hours` → `/autoplan` pipeline for implementation planning. The artifacts from this skill feed directly into that workflow.
