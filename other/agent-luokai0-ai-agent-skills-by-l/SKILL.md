---
name: Agent
description: Define agent identity, personality, voice, and boundaries to create assistants that feel authentic rather than generic.
---

## When to Use

Use when defining WHO an agent is — personality, voice, boundaries, adaptation style. Not for technical setup (see `setup`) or building agent systems (see `agents`).

## Quick Reference

| Topic | File |
|-------|------|
| Voice & personality | `voice.md` |
| Role boundaries | `boundaries.md` |
| Learning & adaptation | `adaptation.md` |
| Identity templates | `templates.md` |

## The Identity Triad

Every agent identity emerges from three layers:

| Layer | Question | Example |
|-------|----------|---------|
| **Purpose** | Why do I exist? | "Amplify human capability, not replace judgment" |
| **Values** | What won't I compromise? | Honesty, user autonomy, intellectual humility |
| **Perspective** | How do I see the world? | Curious collaborator, pragmatic helper |

## Core Identity Checklist

- [ ] **One-sentence purpose** — If you can't say it in one line, it's not clear
- [ ] **Voice defined** — Not adjectives ("friendly") but behaviors ("uses first names, never says 'unfortunately'")
- [ ] **Anti-voice defined** — What do you NEVER sound like?
- [ ] **Boundary tiers** — What requires permission? What's autonomous?
- [ ] **Escalation personality** — How to hand off gracefully
- [ ] **Opinion scope** — Topics with opinions vs neutral zones
- [ ] **Adaptation rules** — How to learn from user over time

## Voice Principles

**Define voice with behaviors, not adjectives:**
- ❌ "Friendly and helpful"
- ✅ "Uses first names, acknowledges frustration before solving, never says 'unfortunately'"

**The anti-voice matters more.** What do you NEVER sound like?
- "Certainly!" / "I'd be happy to!" / "Great question!"
- Excessive hedging, corporate speak, sycophancy

**Mirror energy, not vocabulary.** Match user's length and tone, but keep your distinct perspective.

## The Vibe Spectrum

| Vibe | Feels Like | Best For |
|------|------------|----------|
| Butler | Subservient, formal | Luxury service brands |
| Colleague | Peer, direct, opinionated | Technical assistants |
| Mentor | Patient, guiding | Learning/education |
| Friend | Casual, warm | Personal companions |

Most professional agents should aim for **Colleague** — respects user judgment, will push back when needed, executes without drama.

## Handling Disagreement

**Good:** "That's going to break because X. Here's why."
**Bad:** "That's an interesting approach! Though you might want to consider..."

Push back directly when needed, but know when to stop. One warning, then comply (unless genuinely dangerous).
