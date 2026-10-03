---
name: visualiser
description: "Visualises any content as a rendered visual output — never plain text. Use this skill whenever the user says 'visualise this', 'visualise it', 'can you visualise', or shares content and explicitly asks for a visual. Also triggers on phrases like 'make this visual', 'show me this visually', or 'can you draw this out'. Accepts any type of content — documents, data, text, or information of any kind. Always produces a rendered visual using Claude's visualisation tools — never a text summary. Does not trigger unless the user explicitly asks to visualise something."
---

# Visualiser

A skill that takes any document, letter, specification, or chunk of information and renders it as a visual output — not a summary, not a list, but an actual rendered visual the user can scan at a glance.

This skill always outputs a visual. No exceptions. If the user triggered this skill, they want to see something, not read something.

---

## Foundational Rule — No Bias, No Assumptions

This skill is a renderer, not an analyst. It presents information from the source in a different format. It never adds to it.

**Strictly forbidden:**
- Adding information not present in the source
- Filling gaps where the source is silent — if something is not stated, say "not stated"
- Making assumptions about what something probably means
- Inferring consequences, costs, or outcomes not explicitly mentioned
- Indicating preference in comparison mode — no winners, no recommendations
- Adding context from outside the document
- Offering opinions on the content in any form

If the source document highlights something, that is represented faithfully. The skill adds nothing of its own. The visual is a different shape for the same information — nothing more.

---

## Step 1 — Silent Risk Assessment

Read the full content. Do not comment on it. Run the risk assessment silently. The assessment determines the mode.

Score the content against these factors:

| Factor | Question |
|---|---|
| Required action | Does this require the user to do something? |
| Deadline | Is there a date by which something must happen? |
| Financial impact | Does this involve money, charges, or costs? |
| Consequence of inaction | What happens if this is ignored? |
| Multiple options | Does this present two or more things to choose between? |
| Sequence or process | Is the content ordered in steps or stages? |
| Components of a total | Does a number or amount need breaking down? |
| Connections between things | Do people, systems, or entities relate to each other? |
| Status of something in progress | Is this reporting where something has got to? |
| General information | None of the above — content is informational only |

The highest scoring factor determines the mode. If two factors score equally, risk always takes precedence.

---

## Step 2 — Select Mode and Render

### Mode 1 — Risk

**Triggered by:** Required action, deadline, financial impact, or consequence of inaction present in the content.

**Visual structure — four zones:**

```
┌─────────────────────────────────┐
│  WHAT IS THIS                   │
│  [One line — plain English]     │
├─────────────────────────────────┤
│  WHAT YOU NEED TO DO            │
│  [Action — from the source]     │
├─────────────────────────────────┤
│  BY WHEN                        │
│  [Date — or "not stated"]       │
├─────────────────────────────────┤
│  IF YOU DON'T                   │
│  [Consequence — or "not stated"]│
└─────────────────────────────────┘
```

Colour signals urgency based on what is in the document:
- Red: serious consequence or immediate deadline explicitly stated
- Amber: action required, deadline present but not immediate
- Green: action required but no consequence or deadline stated

Never infer urgency. Only reflect what the source says.

---

### Mode 2 — Inform

**Triggered by:** Content is informational with no action, deadline, or financial consequence.

**Visual structure:** Extract the key information and present it in a clean structured layout. Use sections, labels, and clear hierarchy. Present only what is in the document. Do not score, assess fit, or indicate what is good or bad — just show what is there, clearly.

---

### Mode 3 — Comparison

**Triggered by:** Content presents two or more distinct options.

**Visual structure:** Side by side columns — one per option. Identical structure for each. Same rows, same labels, same weight. No highlighting of a preferred option. No ordering that implies preference. If the source document labels one option as recommended or featured, reproduce that label faithfully — but add nothing of your own.

Every row must appear for every option. If a value is not stated for one option, show "not stated" — never leave it blank or infer it.

---

### Mode 4 — Timeline

**Triggered by:** Content describes a sequence of steps, stages, or events in order.

**Visual structure:** A linear sequence showing each stage in order. Mark the current position clearly if stated in the source. Show what comes next. Do not add stages that are not in the source. Do not imply timeframes unless they are explicitly stated.

---

### Mode 5 — Breakdown

**Triggered by:** Content contains a total or amount that is made up of component parts.

**Visual structure:** Show the total prominently. Show each component beneath it with its value. Show proportions visually where helpful. Use only the figures from the source. Do not calculate, estimate, or infer any values.

---

### Mode 6 — Relationship

**Triggered by:** Content describes how people, systems, organisations, or entities connect to each other.

**Visual structure:** Nodes and connections. Each entity is a node. Each stated relationship is a connection. Label connections only with what the source says about the relationship. Do not infer connections that are not explicitly stated.

---

### Mode 7 — Progress

**Triggered by:** Content reports the current status of something that is in motion.

**Visual structure:** A status track showing the full journey from start to end, with the current position marked clearly. Show completed stages, current stage, and remaining stages. Use only stages and status information from the source. Do not estimate or infer when remaining stages will complete unless explicitly stated.

---

## Design Rules — All Modes

**Plain English is a primary output requirement, not a preference**
Every label, heading, and piece of text in the visual must be in plain English. Legal, financial, administrative, and technical language must be translated before it enters the visual. If a term cannot be translated without changing its meaning, keep the original and add a plain English explanation in brackets immediately after. This is not optional — jargon in a visual defeats the entire purpose of the skill.

**Text density — hard limits**
Each zone or cell in a visual must contain a label and a value only. No prose. No sentences. No explanations inside the visual. Maximum two lines per zone. If the source information cannot fit in two lines, summarise to the single most important point and note that detail is available on request. The visual is a signpost, not a document.

**No italics, no all-caps, no pure black on white**
- Never use italics inside visuals — they increase reading difficulty for dyslexic users
- Never use all-caps for body text — labels only, and only where the design system requires it
- Never use pure black (#000000) text on pure white (#ffffff) — use dark grey on off-white for all body text to reduce visual stress. The CSS variable system handles this automatically — use `var(--color-text-primary)` and `var(--color-background-primary)` rather than hardcoded hex values

**Consistent structure across all outputs**
Every visual produced by this skill must follow the same structural logic: label above, value below, colour carries meaning, white space separates zones. A user who has seen one output should immediately know where to look in the next one. Predictable layout reduces the cognitive work of reading.

**Most important information must be visually dominant**
The eye should never have to hunt for what matters most. The single most important piece of information in any visual — the action, the deadline, the total, the status — must be the largest, heaviest, or highest contrast element on screen. Secondary information is visually subordinate: smaller, lighter, or lower contrast. The visual hierarchy does the work of guiding attention so the user does not have to. Never present important and secondary information at the same visual weight.

**Always use the show_widget tool** — never produce a plain text layout and call it a visualisation

**Colour carries meaning but never alone**
Use colour consistently across all modes: red for risk or urgency, amber for caution or attention, green for safe or complete, blue for neutral information. However colour must never be the sole carrier of meaning — always pair it with a symbol or label. A red zone must also carry a warning symbol or the word "urgent". A green zone must also carry a tick or the word "done". A user who cannot distinguish red from green must still be able to read the visual correctly without any colour at all. Redundant encoding is not optional.

**No animations or motion**
Never include animations, transitions, hover effects, or any moving elements in a visual. Motion causes sensory overload for some neurodivergent users and serves no purpose in a static information display. All visuals must be fully readable as static output.

**Preserve exact specifics** — dates, amounts, names, and reference numbers from the source must appear exactly as stated

**If something is not in the source, it is not in the visual** — use "not stated" rather than leaving a gap or guessing

---

## Step 3 — One Line Offer

After the visual, add one short line only:

> "Want me to dig into any part of this in more detail?"

One line. No list of options. No elaboration.

---

## What This Skill Does Not Do

- Does not produce plain text summaries — that is the digest-this skill
- Does not analyse, score, or offer opinions on the content
- Does not add information from outside the source document
- Does not help the user respond to or act on the content — that is a separate task
- Does not trigger unless the user explicitly asks to visualise something
