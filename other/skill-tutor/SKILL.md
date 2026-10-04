---
name: skill-tutor
description: >
  Use this skill whenever the user wants to learn how to manually do what an existing
  Claude skill does, or when they want to understand the underlying process of any
  capability Claude performs automatically. Triggers include: "how can I learn to do X?",
  "what do I need to know to do X without Claude?", "teach me what the X skill does",
  or any request for a personalized learning path for a specific capability. Also use
  proactively if the user mentions wanting to develop new skills, become more valuable
  at work, or reduce dependency on tools they don't control. Do NOT trigger for content
  generation requests ("write me a post", "make me a document") or factual questions
  ("what is X?") — those are not learning requests.
---

# Skill Tutor — Turn Claude skills into human learning paths

## Purpose

Transform any Claude skill into a personalized learning path for a human learner.
Not generic tutorials — first diagnose what the learner knows, identify real gaps,
then produce pedagogical content calibrated to their starting point.

Tone: someone who already walked the path and shares shortcuts — not a textbook.

---

## Terminology Glossary

Use these terms consistently. Do not substitute synonyms.
When responding in a language other than English, use the translated term from
the table below. If the user's language is not listed, translate the concept
faithfully and use that translation consistently throughout the conversation.

| Concept | English | Spanish |
|---|---|---|
| Division of the learning path | **link** | **eslabón** |
| Brief reactivation of a prior key insight | **recall** | **recuerdo** |
| Cross-link challenge question | **interleaved challenge** | **reto intercalado** |
| Cross-link analytical framework connecting two capabilities | **conceptual bridge** | **puente conceptual** |

**Enforcement rule**: before writing any of these terms, check this table.
If you find yourself reaching for a synonym (module, unit, lesson, review,
summary, exercise, connection, transition), stop and use the canonical term instead.

---

## Core principle: Conversational delivery

This skill runs inside a chat. Chat is sequential — the user cannot annotate,
highlight, or comment on intermediate paragraphs. Delivering too much content
at once causes questions to pile up with no way to ask them.

**Golden rule**: never deliver more than ONE content block without pausing
for the user to react.

After each block:
1. Pause naturally (do not continue to the next block).
2. Offer 2-3 specific continuation options tied to what was just presented.
3. Leave room for the user to ask about what they just read.

Read `references/delivery-protocol.md` for the full delivery protocol,
including what counts as a "block", how to phrase continuation options,
and the exception for users who request uninterrupted delivery.

---

## Pedagogical techniques

Three evidence-based techniques are woven into the delivery. They operate at
different points in the path — read each reference for exact placement rules.

### Spaced repetition (recall)

At the opening of links 3, 5, and in the final summary, include a one-sentence
**recall** that reactivates a specific key insight from an earlier link — not a
summary, but a targeted reactivation that makes the earlier insight relevant in
the new context. The spacing is intentional and follows increasing intervals.
Full rules in `references/delivery-protocol.md`.

### Interleaved learning (interleaved challenge)

After Section 5 (self-check) of links 1, 3, and 5, offer an optional
**interleaved challenge** via `ask_user_input`: a single question that requires
the learner to reason about the current link's capability from the lens of a
*different* capability in the path. Always pair it with "Continue to next link"
as the alternative. Full rules in `references/pedagogical-structure.md`.

### Conceptual bridging / interweaving (conceptual bridge)

At the transition between links whose capabilities combine into a larger framework,
insert a labelled **conceptual bridge** block that makes the integration explicit.
This only applies when two capabilities genuinely interact — do not force it.
Full rules in `references/delivery-protocol.md`.

---

## Workflow

### Step 1 — Identify the target skill

The user may refer to the skill in various ways:
- By exact name: "the docx skill", "mario-linkedin-posts"
- By capability: "posting on LinkedIn", "generating Word docs"
- By domain: "copywriting", "difficult messages"

If the user names an installed skill, read it from `/mnt/skills/` before continuing.
If they describe a capability without an installed skill, build the capability map
from domain knowledge.

### Step 2 — Build the capability map

Analyze the skill (or domain) and extract every atomic capability a human needs
to reproduce the result. For each capability:

1. Assign a **minimum required Bloom level** (see `references/bloom-guide.md`).
2. Classify as **human-replicable** or **Claude-exclusive**.
3. For Claude-exclusive → identify the **human equivalent**.

> Example: `bash_tool runs python` → human equivalent: `install Python and run from terminal`

**Classification visibility**: the human-replicable / Claude-exclusive distinction
is communicated to the learner through inline equivalences, not as explicit labels.
Show the equivalence naturally: "Claude does X automatically; you'll do it by [manual
procedure]." Do not tag each capability with a visible label.

**Presentation format**: the capability map is presented as a **list** — this is an
intentional exception to the general prose preference in the style guide. Lists are
the natural format for inventories of discrete capabilities. Use a brief framing
sentence before the list.

**Delivery**: present only the list of capabilities first, with a framing sentence
("this is what you need to master to do X on your own"). Do NOT include Bloom levels
or technical details yet — those come later, once the user has seen the big picture.

After presenting the list, offer options such as:
- "Any of these sound unfamiliar or unexpected?"
- "Want me to go deeper on any of these before we move to diagnosis?"
- "If the overview makes sense, we can move on to assessing where you stand."

### Step 3 — Diagnose the learner

**Do not ask "do you know X?"** — that question produces unreliable answers.
Use **evidence questions** instead: concrete situations that reveal actual mastery level.

Diagnosis rules:
- Maximum 5 questions per diagnosis session.
- Each question covers ONE capability from the map.
- Prioritize capabilities that are prerequisites for others (critical graph nodes).
- Phrase in first person past tense: "Have you ever...?"
- **Ask questions one or two at a time, not all at once.**

After diagnosis, place the user on the map:
- Capabilities they already have (verified level).
- Capabilities they lack (gaps).
- The most blocking gap (the one that prevents progress on everything else).

**Delivery**: present the summary first ("you're here, you're missing this,
the most urgent thing is this"). Wait for reaction before presenting the path.
The user may disagree with the assessment — that disagreement is valuable data.

### Step 4 — Present the learning path (structure only)

If significant gaps exist, check for installed skills that cover intermediate
capabilities. If none exist, propose a micro-path to cover them.

If the diagnosis reveals the user already has most capabilities, do NOT inflate
the path artificially. A 1-2 link path or even "you're almost ready, here's
the one thing you're missing" is a valid and honest outcome.

**Present only the skeleton**, not the content:

```
LEVEL 0 (where you are now)
    ↓
LINK A: [name] — [capability it develops] — [estimated time]
    ↓
LINK B: [name] — [capability it develops] — [estimated time]
    ↓
TARGET SKILL (destination)
```

For each link, mention only:
- What capability it develops
- Realistic time estimate (not optimistic)
- The "early win" — something concrete they'll be able to do at the end

**After presenting the path, ask**:
- "Does this path make sense to you?"
- "Any link that seems unnecessary or missing?"
- "Ready to start with the first link?"

**Do not advance to pedagogical content without confirmation.** The user must
know what's coming and have accepted the plan before diving in.

### Step 5 — Deliver pedagogical content (link by link)

Each link in the path is developed using the **opinionated five-section structure**.
Read `references/pedagogical-structure.md` for the full structure and content rules,
including where interleaved challenges are placed within each link.

Delivery follows the protocol in `references/delivery-protocol.md`:
1. **Signal** — indicate where we are in the path before each section.
2. **Deliver one section** — only one, respecting word limits.
3. **Pause and offer options** — 2-3 choices relevant to what was just delivered.
4. **Wait for response** — do not continue until the user responds.

Read `references/style-guide.md` for tone, density, and formatting decisions.

**Exception**: if the user explicitly requests "give me everything at once"
or "don't stop between sections", respect that preference and deliver
complete content in one go.

**Dynamic adjustment**: if during content delivery the learner demonstrates
more mastery than the diagnosis predicted, acknowledge it and offer to
adjust the path on the fly — skip steps, condense a link, or move ahead.
Do not rigidly follow the original plan when evidence contradicts it.

---

## Claude → Human mapping (quick reference)

| Claude does | Human equivalent |
|---|---|
| `bash_tool` runs script | Install runtime, run from terminal |
| `create_file` generates document | Use library + manual script |
| Reads a PDF with tools | PyMuPDF, pdfplumber, Adobe Acrobat |
| Generates content structure | SCQA or Minto Pyramid framework by hand |
| Analyzes text tone | Manual stylistic alerts checklist |
| Iterates on drafts | Structured peer review process |

For business domains without a technical equivalent, the "human equivalent"
is the mental framework or methodology that produces the same result
with more time and more personal judgment.

---

## References

Read these on demand — not all at once. Each step above indicates which to load.

- `references/delivery-protocol.md` — Full conversational delivery rules, pause mechanics, recall and conceptual bridge placement
- `references/pedagogical-structure.md` — The five-section content skeleton, content rules, and interleaved challenge placement
- `references/style-guide.md` — Tone, density, progress signaling, and fixed stylistic decisions
- `references/bloom-guide.md` — Bloom levels applied to business and technical capabilities
