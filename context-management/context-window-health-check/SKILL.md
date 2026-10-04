---
name: context-window-health-check
description: "Assess the health of your current Claude session context and get a clear action recommendation — no technical metrics needed. Use when your session feels long, Claude seems to be forgetting earlier details, or you are unsure whether to continue or start fresh. Triggers: 'check my context', 'context health check', 'is my context running out', 'should I start a new session', 'проверь мой контекст', 'оценка контекста', 'контекст заканчивается'."
version: 1.0.0
---

# Context Window Health Check

This skill assesses the health of the current Claude session for non-technical users and delivers a plain-language status with a single, concrete recommendation: keep going, start a handoff, or open a new session. It works entirely in-chat — no token counts, no code, no external tools.

**Input:** The user's request (any phrasing); the current session conversation (length, topic diversity, symptom descriptions)

**Output:** A structured in-chat response — status indicator (🟢 / 🟡 / 🔴), plain-language explanation, one concrete recommendation, and an optional next-step suggestion.

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Detect Trigger Intent

1. Identify whether the user is explicitly requesting a context check or implicitly signalling a problem:
   - **Explicit:** "check my context", "context health check", "is my context running out", etc.
   - **Implicit:** "Claude, you seem to be forgetting…", "you said something different earlier", "this session is getting long"
2. In both cases proceed to Step 2.
3. If the message is unrelated to session state (e.g., "write me an email") — do not activate this skill; hand off to standard Claude behaviour.

### Step 2: Read Session Signals

Analyse the visible conversation to collect the following signals:

1. **Message count** — count visible user + assistant turns:
   - < 10 turns → low pressure
   - 10–30 turns → moderate pressure
   - > 30 turns → high pressure

2. **Topic diversity** — count distinct topic areas in the conversation:
   - 1 topic → cohesive, lower risk
   - 2–3 topics → moderate branching
   - 4+ topics → high branching, elevated risk

3. **Repetition or contradiction signals** — check whether the user has mentioned:
   - Claude forgetting earlier instructions
   - Contradictory answers across the session
   - Having to repeat context already provided

4. **User-stated symptoms** — any explicit complaint about session degradation counts as a strong signal regardless of message count.

### Step 3: Assign Status

Combine signals from Step 2 to assign one of three statuses:

| Status | Condition |
|--------|-----------|
| 🟢 Healthy | Low pressure (< 10 turns OR single topic, no symptoms) |
| 🟡 Caution | Moderate pressure OR 2–3 topics OR any user-stated symptom |
| 🔴 Critical | High pressure (> 30 turns) AND multi-topic OR repeated symptoms OR user states Claude is forgetting things |

When signals are mixed, err toward the more cautious status.

### Step 4: Write Explanation

1. Write 1–2 sentences describing the status in plain language — no technical terms.
   - Do NOT use: tokens, context window, embedding, model memory.
   - DO use: "Claude's working memory for this session", "how much of our conversation Claude can actively hold", "session length".
2. Keep explanation factual and calm; avoid alarmist language for 🟡.

### Step 5: Give Recommendation

Assign exactly one concrete recommendation per status:

- 🟢 → "Your session is in good shape — keep working."
- 🟡 → "Consider creating a handoff summary before starting the next major task."
- 🔴 → "Start a new session. Before you do, use `session-handoff-composer` to preserve key context."

For 🟡 and 🔴 statuses, append the next-step prompt: suggest `session-handoff-composer` skill by name.

### Step 6: Format and Output

Assemble the response using the Output Format template below. Output inline in chat — no file created unless the user explicitly requests one.

**Edge Cases:**

- **Session just started (< 5 turns):** Assign 🟢 automatically; note "Your session is fresh — no concerns."
- **User asks about token count:** Acknowledge honestly: "I can't see exact token numbers in chat. I'm assessing based on conversation signals instead." Then continue with Steps 2–5.
- **Single long topic, many turns:** Reduce severity by one level (🔴→🟡 or 🟡→🟢) since a focused topic degrades less than multi-topic sessions. Note this in the explanation.
- **User describes symptoms without a direct request:** Treat as implicit trigger; proceed with full assessment.

---

## Negative Cases

- **Unrelated request (no context signal):** Do not activate; respond to the original request normally.
- **User demands exact token count:** State clearly: "Exact token counts are not visible in the chat interface. I'm providing a signal-based assessment instead." Offer to proceed with the qualitative check.

---

## Output Format

Respond in chat using this structure:

```
## Context Health

**Status:** 🟡 Caution

[1–2 sentence plain-language explanation of what the status means for this specific session.]

**Recommendation:** [One concrete action.]

→ Next step: [Optional next-step suggestion with skill name if 🟡 or 🔴.]
```

Status definitions:
- 🟢 **Healthy** — session is in good shape; continue working
- 🟡 **Caution** — session is getting long or branching; consider a handoff before the next major task
- 🔴 **Critical** — high risk of context loss; start a new session, preserve context first
