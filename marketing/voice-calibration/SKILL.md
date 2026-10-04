---
name: voice-calibration
description: Interactive voice profiling — asks writing prompts in terminal, collects live responses, and distills a reusable voice profile for content generation. Use when calibrating tone for social posts, newsletters, or any written output.
user-invocable: true
argument-hint: "[--domain topic] to focus prompts on a specific subject area"
metadata:
  version: "1.0.0"
---

# Voice Calibration

Build a voice profile from live writing samples typed in the terminal. The profile captures sentence rhythm, rhetorical habits, vocabulary tendencies, and tonal signatures — then saves it as a reusable reference for future content generation.

## Why Live Samples

AI-assisted writing blends the author's voice with the model's defaults. To capture authentic voice, every sample must be typed fresh by the user in the terminal with no AI drafting or editing. Quantity matters less than authenticity — 6-8 raw responses are enough.

## Workflow

```
Round 1 (General)     → 4 prompts — capture base voice
Round 2 (Domain)      → 4 prompts — capture subject-matter tone
Analysis              → extract patterns
Voice profile         → save to file
```

---

## Round 1: General Voice (4 prompts)

Ask these one at a time using AskUserQuestion. Wait for each response before asking the next. Do NOT paraphrase or suggest answers.

### Prompt 1 — Opinion

> You have 3-4 sentences. What's something most people in your field get wrong?

### Prompt 2 — Explanation

> Explain something you understand deeply to someone who knows nothing about it. 3-5 sentences.

### Prompt 3 — Reaction

> Think of something you read recently that made you stop and think. What was it, and what was your reaction? Write it as if you're telling a friend.

### Prompt 4 — Contrast

> Describe two things that most people think are similar but you think are fundamentally different. 2-4 sentences.

---

## Round 2: Domain Voice (4 prompts)

If `--domain` was passed, use that topic. Otherwise ask:

> What domain will this voice profile be used for? (e.g., I-Ching commentary, product marketing, technical writing)

Then ask these one at a time, tailored to the stated domain:

### Prompt 5 — Hook

> Write the opening 2-3 sentences of a post about [domain topic]. Assume the reader doesn't care yet — make them care.

### Prompt 6 — Corrective

> What's a common misconception in [domain]? Correct it in 3-4 sentences the way you'd actually say it.

### Prompt 7 — Compression

> Take something complex in [domain] and compress it to 1-2 sentences. Make it land.

### Prompt 8 — Closing

> Write the last 2-3 sentences of a post. Leave the reader with something that stays.

---

## Analysis

After collecting all 8 samples, analyze them silently. Do NOT show intermediate analysis to the user. Extract:

### Sentence Mechanics
- Average sentence length (words)
- Sentence length variance (does the writer alternate short/long or stay uniform?)
- Punctuation habits (em dashes, semicolons, colons, ellipses, periods-as-fragments)
- Paragraph rhythm (single punchy lines vs. flowing multi-sentence blocks)

### Rhetorical Patterns
- Opening moves (declarative? interrogative? scene-setting? provocative claim?)
- Closing moves (callback? reframe? open question? decisive statement?)
- Use of contrast / juxtaposition
- Use of lists or parallel structure
- Use of direct address ("you")
- Use of imperatives
- Second-person vs. third-person vs. impersonal framing

### Vocabulary & Register
- Latinate vs. Anglo-Saxon word preference
- Technical jargon frequency (high/low, when deployed)
- Concrete vs. abstract imagery
- Metaphor density (heavy/light/none)
- Register (formal, conversational, elevated-casual, academic)

### Tonal Signature
- Confidence level (assertive, hedged, qualified)
- Humor presence and type (dry, none, self-deprecating, ironic)
- Emotional distance (intimate, arm's-length, detached)
- Attitude toward the reader (peer, teacher, co-conspirator, narrator)

---

## Voice Profile Output

Generate a voice profile document with this structure:

```markdown
# Voice Profile: [User Name or Handle]

Generated: [date]
Domain: [domain]
Samples: [count]

## Summary

[2-3 sentence distillation of the voice — what makes it recognizable]

## Sentence Rhythm

[Findings from sentence mechanics — concrete observations with examples from samples]

## Rhetorical Habits

[Patterns with direct quotes from samples as evidence]

## Vocabulary & Register

[Word-level observations]

## Tonal Signature

[The overall feel — how this writer comes across]

## Rules for Matching This Voice

1. [Concrete, actionable rule]
2. [Concrete, actionable rule]
3. [Concrete, actionable rule]
4. [Concrete, actionable rule]
5. [Concrete, actionable rule]
6. [Concrete, actionable rule]

## Anti-Patterns (Do NOT)

1. [Thing to avoid that would break the voice]
2. [Thing to avoid that would break the voice]
3. [Thing to avoid that would break the voice]

## Sample Sentences in This Voice

[3 original sentences written BY THE MODEL that demonstrate the captured voice — the user should read these and confirm they sound right]
```

---

## Saving the Profile

1. Show the voice profile to the user
2. Ask: "Do these sample sentences sound like you? Anything to adjust?"
3. Incorporate feedback if given
4. Save the final profile to `{skill-base-dir}/profiles/[handle-or-name].md`
5. Also offer to save a copy to the user's project (e.g., `docs/voice-profile.md`)

---

## Using the Profile Later

Other skills and prompts can reference the saved profile. When generating content in the user's voice:

1. Read the voice profile
2. Apply the "Rules for Matching This Voice" as hard constraints
3. Check output against "Anti-Patterns" before delivering
4. If in doubt, re-read the user's original samples for calibration

The profile is a living document — the user can re-run this skill anytime to update it with fresh samples.
