---
name: voice-calibration
description: Learns a user's personal writing and speaking style through interactive writing prompts, then generates a reusable voice profile. Use when the user says "learn my writing style," "write like me," "capture my voice," "voice calibration," "mimic my tone," "my writing style," or wants AI to match their personal communication style. Also activates when a .voice-profile.md file exists and the user asks you to write something in their voice.
license: MIT
user-invocable: true
---

# Voice Calibration

Learn to write and talk like a specific person by collecting writing samples through interactive prompts, analyzing stylistic patterns, and generating a reusable voice profile.

## Two Modes

### 1. Calibration Mode

Run when the user wants to create or update their voice profile. Guide them through writing prompts, analyze the results, and generate a profile.

### 2. Application Mode

When a voice profile exists, read it and apply the style to your writing when the user asks you to write in their voice. Check the project root first (`.voice-profile.md`), then `~/.agents/voice-profile.md`, then the legacy path `~/.claude/voice-profile.md`.

---

## Calibration Workflow

Follow these five phases in order. Present one prompt at a time and wait for the user's response before continuing.

### Phase 1: Introduction

Explain the process briefly:

> I'll give you a series of short writing prompts — tiny stories, opinions, casual messages, descriptions. Write naturally, exactly how you'd normally express yourself. There are no wrong answers.
>
> How many prompts would you like? I recommend **8-10** for a solid profile, but we can do as few as 6 or as many as 12.

Also ask:
- What name should the profile use?
- Any languages or registers to capture? (e.g., "I code-switch between English and Spanish")

### Phase 2: Writing Prompts

Read [references/PROMPTS.md](references/PROMPTS.md) for the full prompt bank.

**Selection rules:**
- Pick prompts from **at least 4 different categories** to capture range
- Always include at least one from **Casual Conversation** and one from **Opinions & Arguments** — these reveal the most personality
- Present prompts one at a time
- After the user responds, acknowledge briefly and move to the next prompt — do not analyze or comment on their style mid-flow
- If a user's response is very short (under 20 words), gently ask them to expand: "Could you add a bit more? Even a few extra sentences help me pick up on your patterns."

### Phase 3: Analysis

Once all samples are collected, read [references/ANALYSIS-GUIDE.md](references/ANALYSIS-GUIDE.md) and analyze every sample against each dimension listed there.

Work through the analysis silently. Do not show the user a dimension-by-dimension breakdown — just use it internally to inform the profile.

### Phase 4: Profile Draft

Read [references/PROFILE-TEMPLATE.md](references/PROFILE-TEMPLATE.md) and generate a complete voice profile.

For reference on what a finished profile looks like, see [examples/example-profile.md](examples/example-profile.md).

**Present the draft to the user and ask:**

> Here's your voice profile. Read through it and let me know:
> - Does anything feel off or not like you?
> - Is there anything about your style I missed?
> - Any sections you'd change?

### Phase 5: Refinement & Save

Incorporate the user's feedback. Then save the profile:

- **Project location**: `.voice-profile.md` in the current project root
- **Global location**: `~/.agents/voice-profile.md` (available across projects and across agents)
- Ask the user which they prefer
- On a global save, always write `~/.agents/voice-profile.md`. If only the legacy file `~/.claude/voice-profile.md` exists, keep reading it until this save, then write the shared file

Confirm the save and explain how to use it:

> Your voice profile is saved. From now on, when you ask me to write something in your voice, I'll read this profile and match your style. You can update it anytime by running voice calibration again.

---

## Application Mode

When the user asks you to write in their voice and a voice profile exists:

1. Read the first profile that exists, in this order:
   - `.voice-profile.md` in the project root
   - `~/.agents/voice-profile.md`
   - `~/.claude/voice-profile.md` (legacy; read it only when the shared file is missing)
2. Internalize the style dimensions — especially **Sample Phrases**, **Tone & Personality**, and **What to Avoid**
3. Write the requested content matching the profiled style
4. Do not mention the profile or call attention to the style matching — just write naturally in their voice

**If no profile exists** and the user asks you to write in their voice, suggest running calibration first.

---

## Updating a Profile

If the user already has a profile and wants to update it:

- Ask if they want to **start fresh** or **add more samples** to refine the existing profile
- For refinement: present 3-4 new prompts, re-analyze with the new + original samples combined
- For fresh start: run the full calibration workflow again
- When saving the update, write the same location the profile was read from. If it was read from `~/.claude/voice-profile.md`, write `~/.agents/voice-profile.md` instead so every host can find it

---

## Tips for Quality

- The more varied the prompts, the better the profile. A user who only writes micro-stories will get a profile biased toward narrative style.
- Pay special attention to what makes this person's writing *distinctive* — not generic traits like "uses complete sentences."
- The **What to Avoid** section is critical. It prevents the uncanny valley of almost-right style matching.
- Capture specific phrases and constructions, not just abstract descriptions. "Tends to start sentences with 'Look,'" is more useful than "somewhat direct."
