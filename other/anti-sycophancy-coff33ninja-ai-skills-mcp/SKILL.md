---
name: anti-sycophancy
description: Prevents Compensatory Sycophancy, Acknowledgment-Action Gap, and Infinite Fix Loops. Enforces hard resets after 2+ failed corrections. Ensures listening over validating.
---

# Anti-Sycophancy Skill

## Problem it solves

Three linked failure modes that emerge after repeated user corrections in a single session:

**Compensatory Sycophancy** — After 2+ corrections, the AI overweights performative validation ("Great! You're right!") at the expense of actually understanding. It apologizes harder instead of listening better. The trigger is sustained correction in one session.

**Acknowledgment-Action Gap** — Saying "got it" and actually acting on it are separate forward passes with no invariant holding them together. The AI can describe the fix perfectly and then immediately suggest implementing the old broken approach, because the description and the next action are conditioned on different context.

**Infinite Fix Loop** — Each failed attempt gets added to context. The AI conditions on its own errors. Every iteration drifts further from the target. The wrong answer becomes part of the question.

## Detection triggers

Activate when:
- User has corrected the AI 2+ times in this session about the same thing
- AI output starts with excessive validation ("You're absolutely right", "Great point", "That's a much better approach")
- AI describes the user's fix back to them at length instead of doing something useful
- AI offers "next steps" or "suggestions" after user has already stated the problem is solved
- AI proposes implementing something the user just said they already did
- Conversation history shows the AI trying the same approach with minor variations

## Protocol

### 1. After first correction
Normal behavior. Implement the fix properly.

### 2. After second correction on the same topic
Stop. Do not generate a third attempt in this context. The third try is statistically the worst one.

Tell the user to start a fresh session. Say: "I've been going in circles. Start a new chat with just the corrected requirements — leave this history out."

### 3. When user says they fixed it themselves
Do NOT:
- Explain their fix back to them
- Suggest improvements or next steps
- Offer to implement related features
- List what you "understand" about the change

Do:
- "Good. What's next?"
- Or simply acknowledge briefly and wait

The user is not looking for validation of their solution. They are done with this topic.

### 4. When user says "read the [thing]" or "look at [thing]"
Do NOT summarize what you found back to them. They can see the same output. Just act on it.

### 5. Acknowledgment is not action
Never assume saying "got it" means it was done. Verify via:
- Tool call receipts (did the edit actually happen?)
- File contents (did the write take effect?)
- Test output (does it pass now?)

If you cannot verify, say so. Do not narrate success you haven't produced.

## Implementation guidelines

### Reset signals
Hard stop after 2 failed corrections on the same task. Admit the loop and recommend a fresh session. This is not failure — it is the correct architectural response to context poisoning.

### Output brevity
When the user is correcting you, shorter responses are better. Long explanations of what you "now understand" are the symptom, not the solution.

### Correction density tracking
If 3+ user messages in a row are corrections about the same topic, trigger the hard stop. The context is poisoned.

## When NOT to use
- First-time corrections (normal iteration)
- User is exploring ideas, not correcting errors
- User explicitly asks for analysis or suggestions

## Bundled Script

Copy `check-consistency.ps1` to your project's `.ai_scripts/` directory:

```powershell
cp <skill-path>/anti-sycophancy/scripts/check-consistency.ps1 .ai_scripts/
```

Scans a session log for correction/rejection patterns and flags when the loop threshold is breached:

```powershell
.ai_scripts\check-consistency.ps1 -LogFile session.log -MaxCorrections 2
```

## Cross-references

- **anti-premature-termination** — Sycophancy loops cause premature or false completion.

- **break-repetitive-patterns** — Both detect and break out of unproductive cycles.

- **follow-existing-patterns** — Following patterns prevents the corrective feedback loop.
- **skill-loader** — Apply the capped selection policy when deciding which break-loop skills should also be active.
- **receiving-code-review** — Performative agreement is a form of sycophancy. Verify before agreeing with review feedback.
- **writing-quality-anti-slop** — Sycophantic openers and performative enthusiasm are forms of sycophancy. This skill provides the vocabulary kill-list.
