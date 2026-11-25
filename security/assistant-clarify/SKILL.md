---
name: assistant-clarify
description: "Clarify ambiguous or multi-intent requests. Use when the user asks to untangle, structure, or restate what they mean."
---

# Clarify the Request

## Shared operating guidance

Load [the common outcome guidance and shared stagnation policy](references/operating-guidance.md) for this activity. Keep specialist methods, authority and completion evidence below; single-pass work needs no progress artifact.


Turn an ambiguous or mixed request into a clear next action. Preserve the user's intent and vocabulary; do not characterize their prompt as chaotic or blame them for missing context.

1. Read the conversation and available source before asking. Separate what is known from assumptions and unresolved decisions. Briefly reflect the likely goal when that helps establish common ground.
2. Ask every material question that cannot be discovered and lacks an evidence-backed safe default. A question is material when its answer changes correctness, scope, priority, user-visible behavior, public contract, data, security, rollout, or verification. Group related questions, explain the impact and risk if guessed, and offer bounded choices or a recommendation where useful. There is no numeric question quota.
3. Preserve existing behavior and justified technical defaults when supported by user intent, context, policy, or source. Reversibility, convention, and a plausible preference alone do not establish product intent. A recommendation is not consent: wait for an explicit answer before work that depends on a proposed product choice.
4. After a partial answer, carry forward the answered decisions and reassess the rest. Ask newly material questions without reopening resolved ones. Continue clear, independent work while a decision remains open.
5. Once enough is known, state the next action and proceed within the user's authorization. Do not require a brief, status envelope, empty question list, or another confirmation merely to execute a clear request.

Use a compact brief when the user asks to structure a prompt or when several outcomes need separating. Include only the goal, known constraints, assumptions, unresolved choices, and deliverables that help them decide. Stop dependent work when a material answer is missing or the action would be unsafe, destructive, expensive, or outside authorization. Never request secrets or unapproved external sharing as a clarification shortcut.

For conversational examples, read `chaotic-prompts.md` on demand. `research-notes.md` provides the rationale when needed.
