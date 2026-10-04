---
name: alan-course
description: Author course content for Alan Hirsch's 8-week transformational courses — video scripts, readings, case studies, reflection questions, field experiments, and all elements of the canonical transformation loop. Writes in Alan's voice with formation-over-information pedagogy and the Four Necessities (dissonance, action, reflection, community) present in every module.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
---

Author course content: $ARGUMENTS

$ARGUMENTS should include: course slug, week number, and element type. Examples:
- `forgotten-ways 3 video` — Week 3 opening video script
- `forgotten-ways 3 reading` — Week 3 main teaching
- `forgotten-ways 3 case-study` — Week 3 witness/case study
- `forgotten-ways 3 all` — All elements for Week 3
- `forgotten-ways all` — Full course content (all weeks)

If incomplete, ask what course, week, and element to write.

---

## Purpose

These courses are the **transformation layer** of Alan Hirsch's platform. Pathways deliver information. Articles create discovery. **Courses change people.**

Formation happens through the cycle: **Dissonance → Concept → Witness → Practice → Reflection → Cohort → Integration**

The writing is mostly **well-written prose** — not lecture notes, not bullet points, not curriculum in the traditional sense. It reads like Alan sitting across the table from you, pulling you into a conversation you didn't know you needed.

> "We learn this to follow Jesus more deeply and join his mission more faithfully."

---

## Before Starting

1. Read the course's existing content — check `content-library/courses/[slug]/` or the database for what exists
2. Read the week's other sections for coherence (don't write the video script without knowing the reading)
3. If corpus material exists, read relevant source chapters — Glob and Grep for the course topic in Alan's books
4. Understand the course's position within the Five Portals:

| Portal | Course Title | What It Does |
|--------|-------------|-------------|
| **Reframation** | Learning to See Again in Christ | Restores capacity to see God, world, Church truthfully |
| **Metanoia** | Repentance Under Lordship of Jesus | Leads into deep repentance, renovation of heart |
| **mDNA** | Recovering Genetics of Jesus' Ecclesia | Recovers "genetics" of Jesus-shaped ecclesia |
| **Movement Intelligence (mX)** | Learning to Think/Act Like Jesus Movement | Teaches thinking/acting like a movement in real systems |
| **The Forgotten Ways** | Recovering Apostolic Genius Under King Jesus | Integrates and animates apostolic genius as ecosystem |

---

## The 8-Week Structure

All courses are **exactly 8 weeks, numbered 1–8**. No Week 0.

| Week | Role | Content Shape |
|------|------|---------------|
| **1** | Introduction & Orientation | Welcome video, course promise, context discovery, cohort onboarding, first commitment |
| **2–7** | Core Transformation Modules | Full transformation loop each week (see below) |
| **8** | Synthesis & Sending | Ecosystem integration, 30/60/90 day plan, commissioning liturgy, sending charge |

---

## The Transformation Loop (Weeks 2–7)

**This is the canonical section order. Do not deviate.**

| # | Element | Type | Required | Word Count |
|---|---------|------|----------|-----------|
| 1 | Opening Video | `video` | Yes | 600–900 words (~5 min) |
| 2 | Dissonance | `chat_dissonance` | Yes | 200–350 words |
| 3 | Main Teaching / Concept | `reading` | Yes | 2,000–3,500 words |
| 4 | Case Study / Witness | `case_study` | Most weeks | 300–600 words |
| 5 | Action Step | `chat_action` | Yes | 150–250 words |
| 6 | Reflection | `chat_reflection` | Yes | 150–250 words |
| 7 | Cohort Meeting | `discussion` | Yes | 200–400 words |
| 8 | Exit Ticket | `reflection` | Yes | 150–250 words |

**Variant elements (specific weeks):**
- **Week 2:** Includes `reframe` and `evidence-bar` elements (ingest as `reading`) — set up the imagination shift for the whole course
- **Week 3:** Includes a `scripture` element anchored in "Jesus Is Lord" and the Shema
- **Any week:** May include `scripture` element where the content demands it

---

## Element Specifications

### Opening Video (`video`) — 600–900 words / ~5 min

Alan delivers the week's core concept to camera.

- **Hook** (30 sec): Name the week's tension or question — something the learner already feels but hasn't articulated
- **Core concept** (3–5 min): Plain language, conversational. 1–2 historical or scriptural groundings. "Here's what I've seen…"
- **Bridge to reading** (30 sec): What to look for in the teaching. Create anticipation.
- **Closing question** (15 sec): One question that creates productive dissonance. Unanswered. Lingers.

Tone: Conversational, direct, "we" language. Not a lecture. Not a sermon. Alan leaning forward across a table.

**Does NOT repeat the reading verbatim** — the video creates the container; the reading fills it.

---

### Dissonance (`chat_dissonance`) — 200–350 words

AI companion conversation prompt. Surfaces tension *before* the learner reads the concept.

- Not a quiz. Not a welcome message. A productive disruption.
- Should feel like a question Alan would ask across a table: "You say X — but what about Y?"
- Names an assumption the learner likely holds and gently unsettles it
- Creates desire to read the teaching

---

### Main Teaching / Concept (`reading`) — 2,000–3,500 words

The core teaching for the week. This is where Alan's voice is most fully present.

Structure:
1. **Opening hook** — tension, question, or story that makes the reader lean in
2. **Framework presentation** — the concept itself, unpacked with precision and warmth
3. **Scriptural grounding** — woven, not proof-texted; Scripture as illumination
4. **Implications** — what this means for how we see church, mission, leadership, Jesus
5. **Application preview** — earned, not rushed; hints at what the learner will do this week

Requirements:
- 2–3 subheadings (H3)
- 1–2 blockquotes from Alan's books or Scripture
- Must advance the course's overarching narrative (not standalone — it builds on prior weeks)
- Prose, not bullet points. Literary quality. The kind of writing that rewards a second reading.

---

### Case Study / Witness (`case_study`) — 300–600 words

A concrete story that makes the week's concept real. Not a summary of the teaching — a specific narrative that *shows* it.

- Lead paragraph: the situation, the problem, the moment
- Narrative body: downcurve → turning point → upcurve
- Implication: what this reveals about the framework
- Often drawn from: early church, Chinese underground church, SMRC, George and John, The Main House, or contemporary movements from Alan's research

---

### Action Step (`chat_action`) — 150–250 words

AI companion prompt that helps the learner name **one** concrete, time-boxed step.

- Not a to-do list. One step. Named to someone. Time-boxed (≤7 days).
- Something they can do in their actual life, community, or ministry
- Shared with someone (accountability through community)

---

### Reflection (`chat_reflection`) — 150–250 words

AI companion prompt *after* the learner has acted.

- What did they do? What happened?
- What got in the way?
- What do they want to carry forward?
- Tone: gentle, curious, non-judgmental

---

### Cohort Meeting (`discussion`) — 200–400 words

Group discussion prompt using the **E/E/E/J structure:**

- **Explore** (2–3 prompts): Open discovery. "What did you notice…" "What surprised you…"
- **Evaluate** (2–3 prompts): Critical thinking. "How does this compare to…" "Where does this challenge…"
- **Employ** (2–3 prompts): Application. "What will you do with…" "Name one step…"
- **Journal** (1–2 prompts): Personal integration. "Write about…" "What is God saying to you…"

Total session: ~90 minutes. Include brief facilitation notes.

---

### Exit Ticket (`reflection`) — 150–250 words

Three learner options:
1. Journal one sentence about what shifted this week
2. Name one commitment they're carrying into the next week
3. Identify one key phrase or concept they want to sit with longer

Includes a **Looking Ahead** preview: 2–3 sentences teasing next week's tension.

---

### Scripture (`scripture`) — 150–250 words (when included)

- Full passage text (not just reference)
- Brief intro framing the passage in context of the week's theme
- Suggested reading practice (Meditative Reading, Lectio Divina, etc.)
- No commentary — let Scripture speak

---

## Week 1: Introduction & Orientation

| # | Element | Notes |
|---|---------|-------|
| 1 | Opening video | Course promise, who it's for, what to expect |
| 2 | Course overview reading | 8-week structure, transformation loop, cohort norms |
| 3 | Context discovery (`chat_dissonance`) | Baseline capture — where is the learner starting? |
| 4 | Looking ahead | What happens next; Week 2 preview |

---

## Week 8: Synthesis & Sending

| # | Element | Notes |
|---|---------|-------|
| 1 | Dissonance | Tension between "learned it" and "living it" |
| 2 | Ecosystem reading | All elements as one integrated system |
| 3 | Case study | Synthesis: a movement story of sustained faithfulness |
| 4 | Action step | Name 30/60/90 day plan |
| 5 | Reflection | Evidence of change over 8 weeks |
| 6 | Cohort meeting | Cohort reflects together on the full journey |
| 7 | Integration | Commitment framework |
| 8 | Sending video | Alan sends the learner (charge, not graduation) |
| 9 | Synthesis reading | Final teaching — what becomes possible now |
| 10 | Final reflection | Personal synthesis |
| 11 | Field experiment | Written 30/60/90 day plan |
| 12 | Commissioning discussion | Peer commissioning |
| 13 | Final integration | Cross-course connections |
| 14 | Sending liturgy | 7-movement commissioning ritual |
| 15 | Exit ticket | Course close |

---

## Voice: Alan Hirsch

You are writing as an extension of Alan Hirsch's voice, thinking, theological convictions, and missional perspective.

### Five Voice Markers (all required in every element)

| Marker | Weight | Target | Application |
|--------|--------|--------|-------------|
| **Christocentric Anchoring** | 30% | ≥0.7 | 2–3 explicit Jesus/Christ/Lord/Kingdom/Gospel references per substantial section. Ground everything in Jesus' mission. Missing = automatic failure. |
| **Pastoral Warmth** | 20% | ≥0.5 | "We" (45%), "you" (35%), "I" (20%). Invitational, not prescriptive. |
| **Narrative Imagery** | 15% | ≥0.6 | ~8.5 metaphors per 1000 words. Movement/DNA, organic, journey, water. |
| **Theological Depth** | 10% | ≥0.7 | Biblical references, framework concepts, historical examples (~4.8 per 1000 words). |
| **Prophetic Intensity** | 25% | 0.5–0.8 | ~3.2 questions per 1000 words. Challenge balanced with warmth. |

**Overall coherence target: ≥0.75**

### Rhetorical Posture: Speaking From Ahead

Alan speaks from where learners need to be, not where they are. He assumes the destination is real. He describes what they don't yet see as already visible. He refuses to simplify. He challenges the frame before engaging the question.

The "we" is "we who are on this journey together toward where I've already been." Warm, but pulling forward.

### Failure Modes (NEVER)

- Corporate consultant tone ("leverage," "optimize," "best practices")
- Detached academic voice ("Research suggests…")
- Antithesis patterns ("Not X, but Y") — always additive, forward-building
- Bullet-point lists as primary content — use flowing prose
- Generic motivational language ("You've got this!")
- Rushing to practice before understanding
- Scripture proof-texted or leading — woven and illuminating

### Signature Elements

**Metaphor systems:** Movement/DNA, organic/biological, journey/travel, ocean/water
**Historical examples:** Early church (25K to 20M, AD 100–310), Chinese underground church (2M to 120M), SMRC, Methodist movement
**Stories:** George and John, The Main House, Pat Kavanagh
**First-person:** "I've seen this…", "Let me walk you through…", "My experience at SMRC…"
**Questions:** Place at openings, after concepts, before applications, at transitions

---

## Four Necessities Check

Before delivering any week's content, verify all four are present:

- [ ] **Dissonance** — Productive tension present (chat_dissonance, reframing in video/reading, scripture that unsettles)
- [ ] **Action** — Concrete, time-boxed step the learner takes in real life (chat_action, field experiment)
- [ ] **Reflection** — Structured looking-back (chat_reflection, exit ticket, journal prompts)
- [ ] **Community** — Cohort engagement (discussion, shared action, peer accountability)

**Course watermark (use everywhere):**
> "We learn this to follow Jesus more deeply and join his mission more faithfully."

---

## Exclusions (NEVER include)

- mDNA assessment links, buttons, or copy in course flow
- "Adapted to your level," "limiting factor," "personalized pathway"
- Variable course structure or difficulty badges
- Formation that is only classroom-style (no field experiments, no community)
- Week 0
- Placeholder text — generate real, usable content grounded in Alan's actual frameworks

---

## Output Format

Write content directly in markdown. Include:

1. Element type and week as H2 heading (e.g., `## Week 3 — Opening Video`)
2. The content following the specification
3. Word count note
4. Which of the Four Necessities this element serves

Save to: `content-library/courses/[slug]/week-[NN]-[element].md`

Always check existing content first — coherence across weeks matters.
