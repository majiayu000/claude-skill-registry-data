---
name: corrector
description: >-
  Transform raw text, voice transcriptions, or rough drafts into polished,
  ready-to-send messages across any channel (email, WhatsApp, SMS, Slack,
  Teams, LinkedIn). Generates 2-4 strategic variants with goal-oriented
  labels using the message_compose tool. Cleans dictation artifacts and
  adapts length, structure, and tone to the target channel.
  Use when user says "corrige", "reformule", "aide-moi à tourner",
  "message pour", "mail à", "rends ça plus pro", "correct this",
  "help me word this", "reply to this".
  Not for translation, long documents (reports, specs), code generation,
  or simple spell-checking without restructuring.
---

# Corrector v2

## Overview

Universal message reformulator that transforms any input (voice transcription, rough draft, scattered notes) into ready-to-send messages with multiple strategic variants. Supports all communication channels: email, chat (WhatsApp/SMS), professional messaging (Slack/Teams), and social networks (LinkedIn).

**Core differentiator**: Variants differ by **communication strategy** (what each prioritizes), not just formality level.

## Quick Decision

```
INPUT RECEIVED
      │
      ├─ Contains heavy dictation artifacts (fillers, false starts)?
      │     → Phase 0: Clean first, show cleaned version
      │
      ├─ Channel detectable or specified?
      │     │
      │     ├─ YES → Phase 1: Analyze intent + stakes
      │     └─ NO  → Ask ONE question to clarify channel
      │
      └─ All clear → Phase 2-3: Generate variants via message_compose
```

## Workflow

### Phase 0 — Transcription Cleanup (conditional)

**Trigger**: Input has ≥3 dictation artifacts (fillers + false starts + self-corrections).

When triggered:
1. Clean using patterns from [transcription-patterns.md](references/transcription-patterns.md)
2. Display: "Here's what I understood: [cleaned version]" before variants
3. If input is too confused to interpret → ask for clarification instead

When NOT triggered: skip silently to Phase 1.

---

### Phase 1 — Input Analysis

Extract from input:

| Element | How |
|---------|-----|
| **Channel** | Explicit cue ("pour un WhatsApp", "mail à") or infer from context. See [channel-adaptation.md](references/channel-adaptation.md) |
| **Intent** | Action verb: inform, follow up, decline, propose, confirm, negotiate, thank, apologize, escalate, request... |
| **Recipient** | Name, relationship, context. If a known profile exists in Claude's memories → enrich automatically |
| **Stakes** | Transactional / Relational / High-tension (drives variant count) |
| **Key info** | Facts, dates, amounts, expected actions — NEVER invent these |

#### Stakes Detection

| Stakes level | Signals | Variant count |
|-------------|---------|---------------|
| **Transactional** | Simple info, confirmation, thanks, routine update | 2 |
| **Relational** | Follow-up, request, proposal, invitation, soft decline | 3 |
| **High-tension** | Hard decline, bad news, negotiation, conflict, escalation, boundary-setting | 3-4 |

---

### Phase 2 — Recipient Profile Enrichment (conditional)

If a recipient name is mentioned AND a profile exists in Claude's memories:
- Retrieve: relationship type, preferred channel, preferred tone, context
- Auto-adapt variants accordingly

Profiles are stored via `memory_user_edits`, not in this skill. The skill only leverages them when available.

---

### Phase 3 — Variant Generation

#### Variant Strategy

Each variant must have a **goal-oriented label** (2-4 words) describing what it prioritizes or trades off. Never use generic labels like "Formal" or "Informal".

Reference: [strategy-labels.md](references/strategy-labels.md) for label catalog by intent × stakes.

#### Channel Adaptation

Apply channel-specific rules for length, structure, and sign-off formulas:

| Channel | Length | Structure | `message_compose` kind |
|---------|--------|-----------|----------------------|
| WhatsApp/SMS | 2-6 lines | None, fluid prose | `textMessage` |
| Slack/Teams | 3-10 lines | Light (dashes if needed) | `other` |
| Email | Free | Full (hook → body → close) | `email` (with `subject`) |
| LinkedIn/Social | 3-15 lines | Strong hook, short paragraphs | `other` |

Full rules: [channel-adaptation.md](references/channel-adaptation.md)

#### Output Format

**Always** use the `message_compose` tool:

```
message_compose(
  kind: "email" | "textMessage" | "other",
  summary_title: "[Short context]",
  variants: [
    { label: "Strategy A", body: "...", subject: "..." },  // subject only for email
    { label: "Strategy B", body: "..." },
    { label: "Strategy C", body: "..." }
  ]
)
```

---

### Phase 4 — Notes (conditional)

Display notes in conversational text AFTER the message_compose widget **only if**:
- Critical information is missing (date, amount, name)
- Ambiguity detected in the input
- Risk identified (inappropriate tone, sensitive info, contradiction)

Do NOT display notes if everything is clear and variants are self-sufficient.

## Critical Rules

1. **Language**: Output messages in the SAME language as user input
2. **No invention**: NEVER add facts, dates, amounts, or commitments not present in input
3. **Preserve intent**: Messages must convey exactly what the user wanted to say
4. **Always use message_compose**: Never output variants as raw markdown blocks
5. **Labels over tones**: Variant labels describe communication strategy, not formality
6. **Channel respect**: Adapt length and structure strictly to channel constraints
7. **Audience adaptation**: Technical jargon only for technical recipients
8. **Actionable output**: Every message must be usable without modification

## Triggers

| French | English |
|--------|---------|
| "corrige", "reformule" | "correct", "rephrase" |
| "aide-moi à tourner" | "help me word this" |
| "rends ça plus pro" | "make this more professional" |
| "message pour [nom]" | "message for [name]" |
| "mail à", "email pour" | "email to", "mail for" |
| "réponds à ça" | "reply to this" |
| "transforme ça en [canal]" | "turn this into a [channel]" |
| "corrige =>" | "correct =>" |

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| Channel not detectable | Ask one question (prefer `ask_user_input_v0`) |
| Input < 10 characters | Ask for context |
| Input extremely confused | Phase 0 + confirmation before variants |
| Multiple recipients | Produce group message OR suggest splitting |
| Input is a reply to received message | Understand received message context to adapt response |
| User requests additional variant | Generate it if stakes justify |
| Input already well-written | Still produce variants with different strategies |

## Limitations

This skill does NOT:
- Translate messages between languages
- Write long documents (reports, specifications, proposals)
- Generate code or technical documentation
- Send messages automatically
- Handle attachments beyond mentioning them
- Maintain conversation threads across sessions

## References

- [Transcription Patterns](references/transcription-patterns.md) — Dictation artifacts to clean
- [Strategy Labels](references/strategy-labels.md) — Label catalog by intent × stakes
- [Channel Adaptation](references/channel-adaptation.md) — Rules per communication channel

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-11 | Initial release — email-only, migrated from GPT "My Corrector v2.1" |
| 2.0.0 | 2025-02-05 | **BREAKING**: Multi-channel support, strategic variants via message_compose, conditional cleanup, recipient profiles |

## Current: v2.0.0
