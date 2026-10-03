---
skill_id: repurpose-engine
name: Repurpose Engine — one piece → native X / LinkedIn / short-video
description: "Repurpose one piece of content across platforms — \"repurpose this for all platforms\", \"turn this into a thread and a LinkedIn post\", \"make platform versions of this\". Each output is written for its platform, not reformatted."
version: 1.0.0
category: content
office: cmo
lead_agent: content-strategist
everyday_skill: true
triggers:
  - "repurpose this for all platforms"
  - "turn this into a thread and a LinkedIn post"
  - "make platform versions of this"
collaborates_with:
  - content-strategist
  - nk-writer            # preserve the saved voice DNA across every variant
references:
  wraps_skill: .claude/skills/content-creation/SKILL.md
  channels: .claude/skills/marketing/SKILL.md
  voice: .claude/skills/voice-routing/SKILL.md
  adr_moat_framing: documents/ADRs/ADR-007-behavioral-moat-framing-doctrine.md
  adr_confidence: documents/ADRs/ADR-010-confidence-tag-technical-educator-rubric.md
confidence_default: 🟢 HIGH
---

# Repurpose Engine

> **Does:** takes one piece and outputs native versions for X, LinkedIn, and a short-video script.
> **Solves:** manually rewriting the same content three times for three platforms.
> **Triggers on:** *"repurpose this for all platforms"*

## How Maxim does this (native, not copy-paste)

Wraps `content-creation` + the `marketing` channel modes. Each output is **written for its platform**, not reformatted: X = punchy thread with a hook + line breaks; LinkedIn = narrative + insight + soft CTA; short-video = a spoken script with on-screen beats (hook → point → payoff). If a brand voice DNA is set, every variant stays in that voice via `voice-routing` — the differentiator no single-platform tool has.

## Behavioral overlay

- **Frameworks (cited per ADR-007):** **AIDA** (per-channel attention→action) · **Channel-native adaptation** (medium-specific norms) · **Dual Coding Theory** (the video script pairs words + visual beats) · **Diffusion of Innovations** (shareability cues).
- **Voice DNA preserved** across all three (vs. three generic rewrites).
- **Confidence tag (ADR-010)** per variant.

## Output

3 native assets: an X thread · a LinkedIn post · a short-video script (hook/point/payoff + on-screen beats). Optional: hashtags + best-time note.
