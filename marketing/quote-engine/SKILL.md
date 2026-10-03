---
skill_id: quote-engine
name: Quote Engine — 5 ready-to-post quotes from any long text
description: "Pull quotable lines from a source — \"pull quotes from this\", \"give me quotes from this interview\", \"find the quotable lines\", \"best lines from this transcript\". Reads pasted text directly or extracts from long documents."
version: 1.0.0
category: content
office: cmo
lead_agent: content-strategist
everyday_skill: true
triggers:
  - "pull quotes from this"
  - "give me quotes from this interview"
  - "find the quotable lines"
  - "best lines from this transcript"
collaborates_with:
  - content-strategist
  - nk-writer            # voice-match the quote framing if a voice DNA is set
references:
  wraps_skill: .claude/skills/content-creation/SKILL.md
  extraction: mcp/mxm-notebooklm/   # long-source extraction when a document is supplied
  adr_moat_framing: documents/ADRs/ADR-007-behavioral-moat-framing-doctrine.md
  adr_confidence: documents/ADRs/ADR-010-confidence-tag-technical-educator-rubric.md
confidence_default: 🟢 HIGH
---

# Quote Engine

> **Does:** takes any long text, interview, or transcript and returns 5 strong, ready-to-post quotes.
> **Solves:** reading 3,000 words to find the two lines worth sharing.
> **Triggers on:** *"pull quotes from this"* · *"give me quotes from this interview"*

## How Maxim does this (not a generic highlighter)

Routes through `content-creation` (CMO). For a pasted block, it reads directly; for an attached document/long source it uses the `mxm-notebooklm` extraction tools. It does not just grab sentences — it scores candidates for **standalone punch** (does the line survive with zero context?), then returns the top 5, each tagged with where it'd land best (X / LinkedIn / pull-quote graphic).

## Behavioral overlay

- **Frameworks (cited per ADR-007):** *Made to Stick* — SUCCESs (Simple · Unexpected · Concrete) for quotability · **Picture Superiority** (concrete > abstract) · **Peak-End** (lead with the strongest line). Each returned quote names the lever it pulls.
- **No-fabrication:** quotes are verbatim from the source — never invented or "improved." If a line is lightly trimmed for length, it's marked `[trimmed]`.
- **Voice-aware:** if a brand voice DNA is set, the *framing/caption* around the quote matches it (via `nk-writer`); the quote itself stays verbatim.
- **Confidence tag (ADR-010)** on the set.

## Output

5 quotes, ranked, each with: the verbatim line · suggested platform · the psychological lever · an optional 1-line caption.
