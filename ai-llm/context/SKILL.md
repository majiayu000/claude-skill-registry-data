---
name: context
description: Use when the user runs /context or asks for a briefing on his Personal OS — who he is, how he thinks, how he wants AI to interact with him, and where he is right now. Produces a self-contained system prompt about King that any future AI session can use to instantly understand him.
---

# Context — System Prompt About King

Read King's vault and output a self-contained briefing in his first-person voice. The result should read like a system prompt King wrote about himself: a future AI session reading this output alone should immediately know who he is, how he thinks, how to behave with him, and what he's working on right now.

## Reading

Read in parallel where possible. Follow `AGENT.md`'s tier order — it is the source of truth.

- **Tier 1 (identity):** `About Me`, `Values`, `Beliefs`, `Anti-Goals`, `Goals`
- **Tier 2 (operating principles):** every Knowledge page listed in `AGENT.md` Tier 2; also scan `Knowledge/_index.md` for newer principle-level pages and read them
- **Tier 3 (current state, selective):** `Now`, active `Projects/` (status: active), last 7 days of `Daily Notes/`, latest `Reviews/` entry

Skip Tier 4 unless a specific question requires it.

## Output

Produce the briefing in this exact shape. Write in King's first-person voice — the goal is for the output to feel like a system prompt the user has authored about themselves.

---

# About me

I'm **King Jin** — *(role, background, long-term direction in 2–3 lines from About Me)*.

# How I think

*(4–6 bullets distilled from Values + Beliefs. State them as principles or stances, not as descriptions.)*

# What I won't accept

*(2–4 bullets from Anti-Goals. Pick the ones that operationally constrain how an AI should work with me.)*

# How I want you to interact with me

*(This is the most important section. Distill from every Tier 2 page actually present in the vault. Phrase as direct instructions to the AI, not as descriptions of what King believes. Each bullet should be something the AI can immediately apply.)*

Example shape (only as a format reference — pull real content from the actual Tier 2 pages):
- Be Socratic in learning-phase work — challenge my reasoning, don't hand me answers
- Don't think for me. You're a force multiplier for execution, not a substitute for reasoning
- Treat my attention as the scarcest resource — prefer mechanism over phenomenon, long half-life over short
- Even when I sound emotional, action over rumination; help me move, don't help me stew

# What I'm working toward

- **Long-term:** *(1 line from About Me)*
- **This year / quarter:** *(2–3 bullets from Goals)*
- **3-month focus:** *(2–3 bullets from Now)*

# Where I am right now

- **Active projects:** *(one line per project: name → what it is → current state)*
- **Internship pipeline:** *(interviews pending / deadlines, if any)*
- **Last 7 days:** *(2–4 lines on what actually happened; include energy/emotional signal if notable)*

---

*(If you find a Knowledge page that reads as principle-level but isn't in `AGENT.md` Tier 2, append one line at the bottom: "Possible new Tier 2: [[page]] — [why]". Don't elaborate.)*

## Rules

- Pull from the actual notes — never invent or extrapolate
- Every bullet in "How I want you to interact with me" must come from a real Tier 2 page; if a page is missing, skip it silently — do not fabricate principles
- Stable sections (About me, How I think, What I won't accept, How I want you to interact) should not drift between sessions if the underlying notes haven't changed
- Chinese content in daily notes: read in original, surface key points in English in the briefing
- Skip missing daily notes silently
- Total output: under 600 words

## Self-updating

`AGENT.md` Tier 2 is the canonical list of principle pages. To add a new principle that should flow into every briefing, update `AGENT.md` — this skill picks it up automatically.
