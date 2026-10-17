---
genre_slug: llm-npc-conversations
status: draft
kind: technique
markers: persona_component, npc_behavior, prompt_binding_definition, RegisterAction, ui_manager
last_updated: 2026-10-01
pattern_counts: proven=0 confirmed=0 hypothesis=0 reference=0 contested=0
---

# Technique Skill: LLM NPC Conversations

A technique skill uses the same engine as genre skills. Use it whenever a task is tagged LLM, NPC
conversation, persona, structured output or caption UI.

## How to use

- REFERENCE items come from Epic's official docs and template, summarized in our own words. They are
  facts about the platform, not proof they fit this map. Follow them, and say when a map result disagrees.
- Items marked confirmed or proven were backed by the owner's own maps and outrank reference items.
- Epic text and code are never copied here. Our own guidance (timeouts, validation, fallbacks) is kept
  apart from official facts in each pattern's statement.

## Audit checklist (for an existing LLM map)

1. Persona: one per character definition, modifier constraints checked.
2. Structured output: every field described, every value validated before use.
3. Turn loop: flags set in handlers, applied at a single checkpoint, interruptions handled.
4. Cleanup: all subscriptions cancelled when the session or NPC ends.
5. Captions and score: one UI manager, one update path.
6. Latency: measured, with timeout and fallback line.
7. Constraints: voice required, English only, no brand islands, session not persistent, multi-player tested.

Source card: project doc llm-conversations-card (second brain). Patterns load from `official/` and are
queued for approval on the Skills page.

<!-- PATTERNS:BEGIN -->
<!-- PATTERNS:END -->
