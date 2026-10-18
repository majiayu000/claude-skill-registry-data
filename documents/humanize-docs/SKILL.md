---
name: humanize-docs
version: 1.0.0
description: |
  Transform AI-generated documentation into human-readable prose with personality.
  USE WHEN: Converting rigid AI docs (checklist spam, CAPS LOCK emphasis, perfect symmetric
  structures, template dumps) into flowing, conversational writing that feels colleague-authored.
  Different from /humanizer — that skill detects AI writing patterns (Wikipedia taxonomy).
  This skill does aggressive deformalization of document structure and flow.
  PRIMARY TRIGGERS: "humanize this doc", "make this readable", "remove AI patterns from doc",
  "add human touch to this"
  See also: humanizer skill for text-level AI pattern removal.
license: MIT
compatibility: claude-code opencode
source: https://github.com/skillkit-marketplace/skills/tree/main/skills/humanize-docs
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
---

# Humanize Docs

Transforms robotic AI-generated documentation into prose that sounds like an actual human wrote it. The approach is **aggressive deformalization** — not just tweaking tone, but restructuring how information flows to break AI's predictable patterns.

This is a different tool than the humanizer skill. Humanizer removes AI writing tells at the sentence/phrase level (em-dashes, rule-of-three, vague attributions, sycophantic openers). Humanize-docs attacks structural AI-ness: checkbox spam, template overload, perfect symmetry, emotional flatness across an entire document.

## When to use this

Clear signals you're dealing with AI-generated docs:
- Checkbox overload: `- [x] Task 1: Do the thing (AC: #1)`
- CAPS LOCK for CRITICAL IMPORTANT NOTES
- 8+ code templates embedded in one document
- Every section has exactly 3 perfectly balanced paragraphs
- Headers like "LLM Developer Guardrails"
- Phrases: "Certainly, here is...", "It's important to note that...", "Furthermore..."

## Transformation workflow

### Step 1: Detect

Quick test — does the doc have 5+ of these?
- Perfect structural symmetry (every section same length)
- Zero sentence length variation (all 15-20 words)
- Checkbox addiction
- Template embedding mania
- Emotional flatness (no "wait, why?" or "honestly...")

If yes, proceed. If no, it might already be human-written — don't over-transform.

### Step 2: Apply the five core transformations

Execute in order. Don't apply all of them everywhere — humans are inconsistent. Some sections stay formal, others get playful. That asymmetry is the point.

**1. Burstiness injection**
Mix 5-word punches with 30-word reflections. AI writes at one rhythm. Humans don't.

Before:
> The system processes requests through a standardized pipeline that validates inputs and returns structured responses to the calling service.

After:
> It's a pipeline. Request comes in, gets validated, structured response goes back out. Nothing exotic — but the validation step is where things quietly break.

**2. Structure dismantling**
Break perfect 3-paragraph blocks. Add digressions. Not every section needs the same shape.

**3. Checkbox annihilation**
Convert checklists to flowing prose with "anyway, you'll need..." or "first thing is..."

Before:
> - [x] Install package A (required for Task 3)
> - [x] Verify installation with command X
> - [x] Proceed to next task only after confirmation

After:
> Install package A first — Task 3 depends on it. Run command X to verify it worked. Once you get confirmation, move on. If it errors out, the next step breaks, so don't skip this.

**4. Template contextualization**
Replace code dumps with "here's what worked for me..." framing. Give the template a reason to exist before showing it.

**5. Vocabulary swap**
Kill: utilize, leverage, facilitate, ensure, enable, enhance, robust, seamless
Use: use, use, help, make sure, let, improve, solid, smooth

### Step 3: Quality check

Read the output aloud. Does it sound like you'd actually say this to someone?

Red flags the transformation failed:
- Still too even (every paragraph same vibe)
- No variation in sentence rhythm
- Feels like a "professional robot" instead of a person
- You removed personality instead of adding it

Good signals:
- Some sentences feel almost too casual (then you toned it back)
- It reads faster than before
- You can hear a specific person's voice

### Step 4: Domain calibration

Intensity varies by doc type:

| Doc type | Intensity |
|---|---|
| READMEs, internal team docs, onboarding guides, tutorials | High |
| API docs, help docs, technical specs | Moderate |
| Legal, compliance, medical, financial | Gentle only |

## Quick mode (30 seconds)

Just need to make something readable without full transformation:

1. Kill the checkboxes — flowing list with "you'll need: X, Y, and Z"
2. Replace one CAPS LOCK section with italics + context
3. Add one burstiness break — a 5-word sentence after a long paragraph
4. Swap 3-5 AI vocabulary words (utilize→use, leverage→use, facilitate→help)

Not perfect, but 70% better readability.

## Common mistakes

Don't:
- Remove ALL structure (humans still use headers)
- Make everything casual (inconsistency is human)
- Add emojis
- Force humor
- Ignore domain context

Do:
- Vary transformation intensity across sections
- Keep some sections more formal for contrast
- Read aloud to check naturalness
- Preserve technical accuracy above all

## Philosophy

AI writes like it's afraid to break rules. Humans write like they're explaining something to a friend while occasionally remembering they should sound professional. Capture that tension.

## Related skills

- humanizer — sentence/phrase level AI pattern removal (Wikipedia taxonomy, 29 rules)
