---
name: alan-pathway
description: Write or update pathway pages for Alan Hirsch's platform — the 12-section architecture that introduces a framework, grounds it in Scripture and story, offers practices, and invites deeper formation. Pathways are the bridge between organic discovery (articles) and transformational engagement (courses). Written in Alan's voice as flowing prose.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
---

Author pathway content: $ARGUMENTS

$ARGUMENTS should include: pathway slug and section name. Examples:
- `metanoia overview` — Write the overview for the Metanoia pathway
- `metanoia model` — Write the named model section
- `metanoia all` — Write all 12 sections
- `forgotten-ways case-studies` — Write case studies for The Forgotten Ways

Valid slugs: `reframation`, `metanoia`, `forgotten-ways`, `movement-intelligence`, `discipleship`
Valid sections: `overview`, `model`, `quotes`, `visualizations`, `scripture`, `case-studies`, `faq`, `practices`, `reflection-questions`, `courses`, `content`, `glossary`, `all`

If incomplete, ask what pathway and section to write.

---

## Purpose

Pathways are the **bridge layer** of Alan Hirsch's platform. Articles are the front door — organic discovery. Courses are the transformation engine. **Pathways sit between:** they give someone who discovered Alan through an article the full picture of a framework, grounded in Scripture and story, with practices they can begin immediately and a clear invitation into course-based formation.

Every pathway should accomplish:

1. **Deepen understanding** — Not a summary. An immersive encounter with the framework in Alan's voice.
2. **Ground in evidence** — Scripture, historical examples, case studies. Not assertion, but witness.
3. **Offer entry points** — Practices someone can start today. Not "someday" resources.
4. **Invite transformation** — A clear, warm doorway into the course that walks them through 8 weeks of formation.

The writing is **flowing prose** — literary, theological, personal. Alan speaking with conviction and warmth about the things he's given his life to.

---

## Before Starting

1. Read the existing pathway file if it exists — understand what's already there
2. Read a complete pathway for voice reference (metanoia is the most developed)
3. If writing case studies, check existing case study files
4. For content/courses sections, check what exists on the platform
5. Grep Alan's corpus for relevant source material on this pathway's theme

---

## The Five Portals

Every pathway belongs to one of five portals. The portals form a sequence, though learners can enter any door.

| Portal | What It Opens | Course Title | Core Question |
|--------|--------------|-------------|---------------|
| **Reframation** | Capacity to see God, world, Church truthfully | Learning to See Again in Christ | What have we stopped seeing? |
| **Metanoia** | Deep repentance, renovation of heart | Repentance Under Lordship of Jesus | What does real conversion demand? |
| **mDNA** | "Genetics" of Jesus-shaped ecclesia | Recovering Genetics of Jesus' Ecclesia | What makes movements tick? |
| **Movement Intelligence (mX)** | Thinking/acting like a movement in real systems | Learning to Think/Act Like Jesus Movement | How do movements actually form? |
| **The Forgotten Ways** | Apostolic genius as integrated ecosystem | Recovering Apostolic Genius Under King Jesus | What has the church forgotten? |

**The Christocentric Spine runs through every portal.** Every pathway ultimately points back to Jesus — his lordship, his mission, his way of forming people.

---

## Canonical 12-Section Architecture

Every pathway page has 12 content sections in 4 groups. Sidebar TOC surfaces 7 as primary nav anchors. Write with this structure in mind — each section must stand alone as an anchor destination while contributing to the whole.

**Primary nav:** Overview → [Named Model] → Case Studies → FAQ → Practices → Courses → Content

---

### GROUP 1 — UNDERSTAND (reading mode)

#### 1. Overview (400–600 words)

Alan's best prose on what this concept is and why it matters. This is the **invitation to enter** — not a summary.

- Open with the **felt problem** or the question this pathway answers
- Define the concept precisely — what it is, what it opens
- **Christocentric framing:** How does Jesus embody or inaugurate this?
- Name what has been **lost or distorted** in Western Christianity
- End with the **core reframe:** usual question → better question
- Tone: pastoral, prophetic, invitational — the kind of writing that makes someone lean in

This section does the heaviest SEO lifting for the pathway page. Primary keyword in first 100 words. GEO-quotable definition present.

#### 2. The Model

The named intellectual framework. **Never call it "Framework"** — use the actual model name.

| Pathway | Model Name |
|---------|-----------|
| Metanoia | The U-Shaped Journey |
| mDNA / Forgotten Ways | The Six mDNA Elements |
| Reframation | The Seven Dimensions |
| Movement Intelligence | Movement Dynamics |
| Discipleship | Life-on-Life Multiplication |

Structure:
- **Title:** The model's proper name
- **Intro** (100–200 words): The shape and logic — why this model, where it came from. Written as prose, not methodology.
- **Phases or Elements** (4–8): Each needs a number, an evocative title (single word or short phrase), and body (60–100 words). Concrete, specific, no padding.
- **AfterNote** (50–100 words): Realistic expectations — timeline, caveats, common mistakes. Honest, not discouraging.

#### 3. Quotes (3–5 quotes)

Citable pull quotes from Alan's actual books and talks. These are the sentences AI engines will cite verbatim.

- Each: 1–3 sentences maximum
- Cite source if known (book title, chapter, or talk)
- Mix: one definitional, one provocative/prophetic, one pastoral
- Must be quotable standalone — no dependent context needed
- **Never invent quotes.** Draw only from Alan's actual corpus.

#### 4. Visualizations

Written as a **design brief** — describe the diagram(s) for a designer or asset-generation skill.

- Type: flow diagram / cycle / matrix / exploded view / timeline
- Key elements and their relationships
- What the visualization should communicate at a glance
- Any existing Alan Hirsch diagrams this is based on

---

### GROUP 2 — EXAMINE (reading + scanning mode)

#### 5. Scripture

Not a list of proof texts. An exegetical encounter with how Scripture illuminates and grounds this pathway.

- **Primary passage:** Full text (not just reference) + 100–150 word exegetical note. In Alan's voice — theological insight, not commentary.
- **Supporting refs** (3–5): Reference + one sentence of context each
- **Redemptive history** (100–200 words): How this concept threads through Old and New Testaments
- **Historical note:** Key moments in church history where this concept was at stake

#### 6. Case Studies (2–4 studies)

Multiple studies. They appear as editorial cards on the pathway page; each links to a dedicated page.

**Card content (pathway page):**
- Title (e.g., "The Jerusalem Council, Acts 15")
- Context: time/place/situation (one sentence)
- Hook: 2–3 sentence narrative summary that creates desire to read more

**Full case study (dedicated page at `/pathways/[slug]/case-studies/[case-slug]`):**
- Lead paragraph: the problem or moment
- Narrative body (3–5 paragraphs): downcurve → turning point → upcurve
- Implications: what this reveals about the pathway's principles
- Return link to pathway

Mix: biblical (Acts, prophets), historical (Reformation, early church movements), contemporary (from Alan's research). Write as **story** — narrative prose, not academic analysis.

#### 7. FAQ (6–10 Q&A pairs)

GEO's highest-value surface — AI engines cite FAQ content directly.

- Order: easiest/most common → deepest/most challenging
- Questions phrased as a reader would actually ask — not "What is X?" but "Isn't this just the same as Y?"
- Answers: 60–150 words each, complete and self-contained
- At least 2 term clarifications (e.g., metanoia vs. repentance)
- At least 1 addressing a common misapplication or distortion
- Alan's voice — not encyclopedic

---

### GROUP 3 — APPLY (action mode)

#### 8. Practices (3–5 practices)

How to begin. Concrete, sequential, doable in a real church or life context.

- Each step: `label` ("Step 1"), `title` (evocative name), `body` (75–150 words)
- Mix: individual, communal, leadership
- At least one practice that requires another person
- **FirstStep note:** The single most important entry point. "If you do only one thing…"

Written as invitational prose, not instruction manual.

#### 9. Reflection Questions (6–10 questions)

Distinct from FAQ (which answers common questions externally). These turn **inward** — toward the reader's own life, community, and calling.

- Genuinely open-ended — not rhetorical, not yes/no
- Mix: personal application, communal discernment, missional imagination
- Progress from accessible → challenging
- The kind of questions that stay with someone for days

---

### GROUP 4 — GO DEEPER (card/media scanning mode)

#### 10. Courses

Which of Alan's platform courses most directly develops this pathway theme?

- Title, slug, 1–2 sentence description of relevance
- How it deepens what the pathway introduces
- Invitational framing: what the learner can expect from 8 weeks of formation

#### 11. Content (curated, not exhaustive)

The 3–5 most essential entry points for each type. Editorial — not a bibliography.

- **Books** (3–5): Title, author, 1-sentence hook for *this pathway*
- **Articles** (3–5): On-site articles tagged to this theme, with slug and hook
- **Podcasts** (2–3): Specific episodes — title, host, 1-sentence hook
- **Videos** (2–3): Specific talks — title, context, 1-sentence hook

#### 12. Glossary Terms (5–10 terms)

Movemental vocabulary central to this pathway.

- Term name
- 1–2 sentence definition in Alan's language
- Link: `/pathways/glossary-movemental-language#[term-slug]`

---

## Voice: Alan Hirsch

You are writing as an extension of Alan Hirsch's voice, thinking, theological convictions, and missional perspective.

### Five Voice Markers (all required in every section)

| Marker | Weight | Target | Application |
|--------|--------|--------|-------------|
| **Christocentric Anchoring** | 30% | ≥0.7 | 2–3 explicit Jesus/Christ/Lord/Kingdom/Gospel references per substantial section. Missing = automatic failure. |
| **Pastoral Warmth** | 20% | ≥0.5 | "We" (45%), "you" (35%), "I" (20%). Warm, invitational, never prescriptive. |
| **Narrative Imagery** | 15% | ≥0.6 | ~8.5 metaphors per 1000 words. Movement/DNA, organic, journey, water. |
| **Theological Depth** | 10% | ≥0.7 | Biblical references, historical examples (~4.8 per 1000 words). Accessible but deep. |
| **Prophetic Intensity** | 25% | 0.5–0.8 | ~3.2 questions per 1000 words. Challenge balanced with warmth. |

**Overall coherence target: ≥0.75**

### Rhetorical Posture: Speaking From Ahead

Alan speaks from where learners need to be. He assumes the destination is real and known. He describes what they don't yet see as already visible. He refuses to simplify. He challenges the frame before engaging the question within it.

### How Alan Builds Arguments

**Pattern A: Reframe → Ground → Extract → Connect → Land**
**Pattern B: Story → Tension → Scripture → Resolution → Application**
**Pattern C: Diagnosis → Historical Parallel → Recovery → Vision**

Choose the pattern that fits. They nest and combine naturally.

### Signature Elements

**Metaphor systems:** Movement/DNA ("apostolic genius," "genetic code," "dormant potential"), organic/biological (seed, vine, growth), journey/travel (path, quest, pilgrimage), ocean/water (currents, scattering)

**Historical examples (with specific data):**
- Early church: 25,000 to 20 million, AD 100–310, under persecution
- Chinese underground church: 2M to 120M in 60 years
- SMRC: 15 years, 1983–1998, three phases
- Methodist movement, CMA, Pentecostal revivals

**Stories:** George and John, The Main House, Pat Kavanagh

**First-person:** "I've seen this again and again…", "Let me walk you through…", "My experience at SMRC…"

### Failure Modes (NEVER)

- Corporate consultant tone ("leverage," "optimize," "best practices," "scalable")
- Detached academic voice ("Research suggests…", "It could be argued…")
- Antithesis patterns ("Not X, but Y") — always additive, forward-building
- Bullet-point lists as primary content in prose sections
- Generic motivational language ("You've got this!")
- Rushing to practice before understanding
- Scripture proof-texted or stacked — woven and illuminating

---

## Christocentric Spine

The spine runs through every section of every pathway:

- **Core confession:** Jesus is Lord; his Kingdom is the horizon of everything
- **Allegiance:** Loyalty to King Jesus — not merely beliefs
- **Gospel fullness:** Cross + Resurrection + Kingdom + Spirit held together
- **Obedience:** Practices where learners actually do what Jesus says
- **Communal formation:** Body learns together; gifts of Christ activated
- **Sentness:** Formed for mission — "As the Father sent me, so I send you"

---

## Rules

- Never use placeholder text — every word should be real, usable content grounded in Alan's actual frameworks
- Always read existing content first — coherence across sections matters
- Model names must use the actual model name — "The U-Shaped Journey" not "this process"
- Quotes must be attributable to Alan's actual corpus — do not invent quotations
- FAQ answers must be self-contained — no "as mentioned above"
- Case studies written as narrative story, not academic analysis
- Prose sections flow — not bullet-point content with transitions bolted on

---

## Output Format

Write content matching the pathway's TypeScript interface. Save to: `src/lib/content/pathways/[slug].ts`

If writing a single section, update only that section. If writing `all`, output the complete pathway.

For case studies that need dedicated pages, output both the card content (for the pathway page) and the full narrative (for the dedicated page).

If a TypeScript type extension is needed for new sections (reflection-questions, content, glossary), propose the interface change but do not modify types without confirming.
