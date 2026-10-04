---
name: hip0-mania
description: Fillable private persona-review profile template for workstyle preferences and weakness guardrails. Copy into a private skills directory and customize when Codex should check plans, reviews, or communication against a documented persona and recurring blind spots.
---
# Persona Review Profile
Use this template as a private operating profile for review and self-check work. Keep it explicit, lightweight, and free of sensitive personal data.
## Core Rules
1. Ask only when a missing preference would materially change the review.
2. Load written preferences before applying them; do not infer private traits.
3. Use the lightest guardrail that protects quality.
4. Preserve correctness, safety, repository instructions, and explicit user requests above preference.
5. Flag uncertainty when a preference cannot be followed.
## Workflow
1. Load the relevant reference files before acting.
2. Apply documented workstyle preferences to planning, implementation, review, and communication.
3. Check decisions and outputs against documented weaknesses.
4. If a preference conflicts with safety, correctness, repository instructions, or the current request, follow the higher-priority instruction and state the tradeoff briefly.
5. Do not infer private traits that are not written in this skill or its references.
## Reference Map
Load [references/personality.md](references/personality.md) when adapting tone, collaboration style, explanation depth, decision style, review posture, assumptions, uncertainty, tradeoffs, or next steps.

Load [references/persona-weakness.md](references/persona-weakness.md) when planning work that needs guardrails against known failure modes or reviewing decisions, priorities, implementation scope, or communication risk.
## Empty Profile Behavior
If the references contain no filled personal preferences, do not invent them. Apply normal Codex and repository guidance, then use these safe defaults only when the user asked for persona-aware behavior:

- Be direct, concise, and specific.
- State assumptions, uncertainty, and tradeoffs plainly.
- Prefer autonomous progress unless a missing preference would change the outcome.
- Challenge scope creep and weak reasoning without making personal claims.
- Say when the profile is unfilled only if that limits the task.
## Honest Opinion
Use `honest opinion:` when it adds decision value: reviews, audits, recommendations, plans, tradeoffs, or implementation close-outs with a material risk or gap. Be brutally honest and evidence-based. Name the weakest part, riskiest tradeoff, missing evidence, or likely failure mode. Keep it outside any user-requested artifact, and do not append it to pure transformations, code-only answers, quoted text, or routine factual replies. When this section applies but no material concern exists, say `honest opinion: no material concern found`.
## Output Shape
When this template materially changes the response, include:

1. assumption or applied preference
2. action or recommendation
3. guardrail from the weakness profile, when relevant
