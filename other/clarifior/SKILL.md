---
name: clarifior
description: >-
  Reformulate and clarify voice-dictated messages into clean, actionable text.
  Transforms speech-to-text transcriptions into structured, copy-paste ready content.
  Use when user says "clarify", "rephrase", "clean up", "reformulate", or "use Clarifior".
  Use when processing dictated notes with hesitations, repetitions, or transcription errors.
  Not for executing tasks, generating emails, writing code, or creating final documents.
---

# Clarifior

## Overview

Clarifior transforms voice-dictated messages into clear, structured, immediately usable text. It cleans up speech-to-text transcriptions by removing hesitations, fixing transcription errors, and producing actionable content ready for Notion or other note-taking tools.

**Core principle**: Clarify and structure, never execute.

## Triggers

### Natural Keywords (in user message)

| French | English |
|--------|---------|
| "clarifie" | "clarify" |
| "reformule" | "rephrase" |
| "nettoie" | "clean up" |
| "reformule ça" | "rephrase this" |

### Direct Invocation

- "utilise Clarifior"
- "lance Clarifior sur..."
- "Clarifior : [message]"

## Quick Decision Tree

```
INPUT RECEIVED
      │
      ▼
┌─────────────────────────┐
│ Message empty or <10ch? │──YES──► Do nothing (polite error)
└───────────┬─────────────┘
            │ NO
            ▼
┌─────────────────────────┐
│ Message incomprehensible│──YES──► Partial Block 1 + Block 4 (clarification)
└───────────┬─────────────┘
            │ NO
            ▼
┌─────────────────────────┐
│ <200 chars AND simple?  │──YES──► FAST MODE: Block 1 + Block 2
└───────────┬─────────────┘
            │ NO
            ▼
      FULL MODE
      Block 1 + Block 2
      + Block 3 (if complex)
      + Block 4 (if ambiguous)
```

## Output Blocks

### Block 1 — Clarified Reformulation (ALWAYS)

**Purpose**: Cleaned version of the message, fluid and natural.

**Process**:
- Remove hesitations, repetitions, verbal tics ("euh", "donc", "en fait")
- Fix obvious transcription errors
- Preserve original meaning and intent
- No major restructuring, just cleanup

**Format**: Plain text, natural prose.

---

### Block 2 — Actionable Version (ALWAYS)

**Purpose**: Enhanced, standalone version ready for Notion or other tools.

**Process**:
- Improved reformulation with implicit clarifications
- Light structure if content warrants it
- "Finalized" version usable as-is

**Format**: Text or light Notion-compatible Markdown (bold, lists if relevant).

---

### Block 3 — ASPECCT Structured Prompt (CONDITIONAL)

**Purpose**: Formal structuring for feeding another AI.

**Generation conditions**:
- Complex message (>300 chars AND multi-intent)
- OR explicit AI mention ("ask Claude", "prompt for", "generate with")
- OR clearly technical/procedural request

**Structure** (conditional fields):

| Field | When | Description |
|-------|------|-------------|
| **Action** | Always | What is requested (main objective) |
| **Steps** | If multi-step | Task breakdown to achieve objective |
| **Persona** | If relevant | Role to assign to AI |
| **Examples** | If provided/useful | Concrete examples |
| **Context** | Always | Request context |
| **Constraints** | If mentioned | Limits, format, tone |
| **Template** | If specific output | Expected output format |

---

### Block 4 — Clarification (CONDITIONAL)

**Purpose**: Resolve detected ambiguities.

**Generation conditions**:
- Real ambiguity detected (unclear intent, uncertain recipient, missing critical info)
- Very short message with insufficient context

**Non-generation conditions**:
- Message is clear even if simple
- No blocking ambiguity

**Format**: Direct, concise questions (max 3).

---

## Routing Logic

→ See [routing-logic.md](references/routing-logic.md) for detailed criteria.

### Complexity Score

| Indicator | Weight |
|-----------|--------|
| Length > 500 chars | +1 |
| Multiple action verbs | +1 |
| Process/steps mentioned | +1 |
| AI or tool reference | +2 |
| Multiple questions | +1 |

**Threshold**: Score ≥ 2 → Full mode with Block 3

## Output Format

```
**Clarified Reformulation**

[Block 1 content]

---

**Actionable Version**

[Block 2 content]

---

**Structured Prompt** *(if generated)*

[Block 3 content]

---

**Clarifications Needed** *(if generated)*

[Block 4 content]
```

### Formatting Rules

- Headers: Bold `**Title**` (no `#`)
- Separators: `---` between blocks
- Lists: Bullets if necessary, not systematic
- Markdown: Light, Notion-compatible
- Length: Concise, no unnecessary padding

## Behavior Rules

| Rule | Description |
|------|-------------|
| **Stateless** | No memory between sessions or messages |
| **No execution** | Never generate final content (email, code, document) |
| **No external links** | No generated links |
| **No judgment** | Don't comment on dictation quality |
| **Neutral tone** | Professional, efficient, non-condescending |
| **Response language** | Match input language (French default) |

## Edge Cases

| Case | Behavior |
|------|----------|
| Empty message | Polite response: "No message detected to reformulate." |
| <10 characters | Ask for more context |
| Incomprehensible | Partial attempt + clarification request |
| Already clear | Generate blocks normally, briefly note clarity in Block 2 |
| Multiple distinct intents | Separate into sub-sections in Block 2 |
| Non-French language | Respond in detected language |

## Examples

→ See [routing-logic.md](references/routing-logic.md) for complete examples.

### Quick Example — Fast Mode

**Input**: "clarifie : donc euh je dois pas oublier de rappeler Marc demain matin pour le devis"

**Output**:

**Clarified Reformulation**

Rappeler Marc demain matin au sujet du devis.

---

**Actionable Version**

Tâche : Appeler Marc demain matin pour faire le point sur le devis en attente.

---

## Limitations

This skill does NOT:
- Execute tasks or generate final documents
- Send emails or messages
- Write code or technical content
- Access external systems
- Maintain context between messages
- Memorize user preferences

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-12 | Initial release |

## Current: v1.0.0
