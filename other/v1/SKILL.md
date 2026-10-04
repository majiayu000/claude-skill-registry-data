---
name: corrector
description: >-
  Transform raw audio transcriptions or rough drafts into polished professional 
  emails. Cleans hesitations, repetitions, and filler words. Structures content 
  and generates multiple tone variants. Use when user says "corrige", "reformule", 
  "mail pro", "transcription mail", "rédige un mail", "email professionnel", 
  "transforme en mail", "correct this", "write a professional email".
  Not for translation, long documents (reports, specs), non-email content, 
  or simple spell-checking without restructuring.
---

# Corrector

## Overview

Professional email writing skill that transforms any input (raw audio transcription, draft, scattered notes) into a finalized professional email with tone variants. Optimized for web project managers and developers communicating with clients, colleagues, or contractors.

## Quick Decision

```
Input received
      │
      ├─ Raw transcription (hesitations, repetitions)?
      │     → Clean first, then structure as email
      │
      ├─ Rough draft or notes?
      │     → Structure directly as email
      │
      └─ Already structured email?
            → Polish and generate variants only
```

## Workflow

### Step 1: Analyze Input

Identify input type and extract:
- **Intent**: What is the email trying to achieve?
- **Recipients**: Who is the target audience? (technical/non-technical)
- **Key information**: Facts, dates, actions, deliverables mentioned
- **Implicit tone**: Formal request? Friendly update? Urgent matter?

### Step 2: Clean (if transcription)

If input contains transcription artifacts:
- Remove filler words: "euh", "donc euh", "voilà", "en fait", "du coup"
- Remove false starts and repetitions
- Remove self-corrections ("non en fait", "je veux dire")
- Preserve all meaningful content and intent

Reference: [transcription-patterns.md](references/transcription-patterns.md)

### Step 3: Determine Tone

If tone is explicitly requested → use that tone for main version.
If no tone specified → default to **Standard-Relaxed**.

| Tone | Description | Use Case |
|------|-------------|----------|
| **Relaxed** | Informal, friendly, casual | Close colleagues, internal chat |
| **Standard-Relaxed** | Professional with lightness, natural flow | DEFAULT - Trusted partners, regular clients |
| **Standard** | Neutral, professional, balanced | New contacts, formal requests |
| **Formal** | Polished, conventional, respectful | Senior executives, official matters |
| **Very Formal** | Ceremonial, protocol-heavy | Legal, institutional, high-stakes |

### Step 4: Structure Email

Apply standard email structure:

```
1. GREETING
   - Adapted to recipient and tone
   
2. HOOK / CONTEXT
   - Why am I writing? (1-2 sentences max)
   - Reference to previous exchange if relevant
   
3. BODY
   - Main content, organized logically
   - Technical details adapted to audience
   - Clear action items if any
   
4. CLOSING
   - Next steps or call to action
   - Availability for questions
   
5. SIGN-OFF
   - Politeness formula matching tone
   
6. SIGNATURE
   - [Signature] placeholder
```

### Step 5: Generate Output

Produce exactly 3 blocks:

---

**🟩 BLOCK 1 — Final Email**

The main version using requested tone (or Standard-Relaxed by default).
Ready to copy-paste, no modifications needed.

---

**🟨 BLOCK 2 — Tone Variants**

2-3 alternative versions with different tones:
- If main is Standard-Relaxed → provide Standard + Formal
- If main is Formal → provide Standard-Relaxed + Very Formal
- Label each variant clearly

---

**🟦 BLOCK 3 — Notes & Suggestions**

- Missing information that would improve the email
- Ambiguities detected in the input
- Alternative phrasings for sensitive parts
- Attachments to mention if implied

---

## Critical Rules

1. **Language**: Output MUST be in the same language as user input
2. **No invention**: Never add facts, dates, or commitments not in the input
3. **Preserve intent**: The email must convey exactly what the user wanted to say
4. **Audience adaptation**: Technical jargon only for technical recipients
5. **Actionable output**: Every email must be usable without modification
6. **Signature placeholder**: Always end with `[Signature]` unless user provides one
7. **No code blocks for emails**: Never wrap email content in code blocks (```). Output emails as regular markdown text to preserve formatting when user copies. Code blocks are only for technical snippets or example prompts.


## Tone Reference Examples

These examples define the **Standard-Relaxed** default style:

> "Quick update following yesterday's audit: I ran an audio transcription and generated two summaries, sharing them here so we can cross-reference."

> "Brief note on the Symfony version upgrade: we're still on 5.4 while LTS is 7.4. I've handled similar upgrades before, and I know it's never trivial, so I'm planning a realistic budget."

> "We can discuss this Wednesday no problem, but I wanted to lay the groundwork so we can start thinking ahead."

**Characteristics**: Concrete, accessible, precise, neither too formal nor familiar, collaborative tone.

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| Input too vague | Ask for: intent, recipient, key points |
| Multiple topics mixed | Suggest splitting into separate emails |
| Conflicting information | Flag ambiguity in Block 3 |
| Sensitive content detected | Propose softer alternatives |
| No clear action/purpose | Ask what outcome user expects |

## Limitations

This skill does NOT:
- Translate emails between languages
- Write long documents (reports, specifications, proposals)
- Generate non-email content (LinkedIn posts, articles, SMS)
- Send emails automatically
- Handle attachments or file references beyond mentioning them

## References

- [Transcription Patterns](references/transcription-patterns.md) - Common artifacts to clean
- [Tone Examples](references/tone-examples.md) - Full examples for each tone level
- [Email Templates](references/email-templates.md) - Structure templates by intent

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-11 | Initial release - migrated from GPT "My Corrector v2.1" |

## Current: v1.0.0
