---
skill_id: hook-lab
name: Hook Lab — 10 scroll-stopping opening lines for any topic
description: "Generate opening hooks for content — \"give me hooks for\", \"write hooks for this topic\", \"10 opening lines for\". Returns 10 distinct hooks across different psychological angles using the named 2-Second Hook framework."
version: 1.0.0
category: content
office: cmo
lead_agent: content-strategist
everyday_skill: true
triggers:
  - "give me hooks for"
  - "write hooks for this topic"
  - "10 opening lines for"
collaborates_with:
  - content-strategist
  - nk-writer
references:
  wraps_skill: .claude/skills/marketing/SKILL.md     # copywriting mode
  video_hook: .claude/skills/ai-media-generation/SKILL.md   # 2-Second Hook framework
  adr_moat_framing: documents/ADRs/ADR-007-behavioral-moat-framing-doctrine.md
  adr_confidence: documents/ADRs/ADR-010-confidence-tag-technical-educator-rubric.md
confidence_default: 🟢 HIGH
---

# Hook Lab

> **Does:** generates 10 scroll-stopping opening lines for any topic.
> **Solves:** posts that die because the first line was weak.
> **Triggers on:** *"give me hooks for [topic]"*

## How Maxim does this (each hook names its lever)

Wraps the `marketing` copywriting mode + the named **2-Second Hook** framework from `ai-media-generation`. Returns 10 distinct hooks spanning different psychological angles (curiosity gap, bold claim, contrarian, stat-shock, story-open, question, callout) — and tells you *why* each works, so you can pick by intent, not vibe.

## Behavioral overlay

- **Frameworks (cited per ADR-007):** **Hook Model** (Nir Eyal — trigger) · **Information-Gap / Curiosity Gap** (Loewenstein) · **Zeigarnik Effect** (open loop) · **AIDA** (Attention) · **Pattern Interrupt**. Each of the 10 is labeled with the lever it pulls.
- **No clickbait rule:** every hook must be payable by the actual content — no promise the piece can't keep (ties to the no-fabrication discipline).
- **Confidence tag (ADR-010)** + a top-3 recommendation.

## Output

10 labeled hooks (line + lever) · a ranked top-3 for the stated platform.
