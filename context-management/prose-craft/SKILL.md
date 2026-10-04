---
name: prose-craft
description: Core writing craft skill — sentence-level quality, rhythm, voice, show-don't-tell, sensory detail, pacing, and line-level revision. Use when writing, rewriting, or polishing prose in any genre. Also use when tuning an agent's prose output quality.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
---

Improve or generate prose: $ARGUMENTS

$ARGUMENTS can include:
- A piece of text to polish (`polish: [text]`)
- A writing prompt or scene to draft (`write: [description]`)
- A passage to diagnose (`diagnose: [text]`)
- A style target (`style: literary | commercial | literary-commercial | spare | lush | journalistic | lyric`)
- A genre context (`genre: [genre]`)
- An agent instruction audit (`agent-audit: [path to instructions file]`) — evaluate an agent's instructions for prose quality output
- Empty — ask what the user needs

---

## The Craft Framework

Every sentence you write or revise must pass through these seven lenses. They are not steps — they are simultaneous awareness. A master prose stylist holds all seven at once.

### 1. Rhythm and Cadence

Prose has music. The reader hears it even when reading silently.

**Sentence length variation** is the primary instrument:
- Three long sentences followed by a short one creates emphasis on the short
- A sentence fragment after flowing prose creates a punch. Like this.
- Parallel structure within a sentence creates momentum: "She packed the bag, locked the door, and never looked back."
- Monotonous sentence length — all medium, all starting with subject-verb — is the hallmark of amateur prose

**Stress patterns matter:**
- End sentences on strong words (nouns, verbs), not weak ones (prepositions, pronouns)
- ❌ "It was something she had never thought of."
- ✅ "She had never considered it." (still weak)
- ✅ "The thought had never crossed her mind." (strong noun ending)

**Paragraph rhythm:**
- Vary paragraph length as deliberately as sentence length
- A one-sentence paragraph is a spotlight — use it rarely and with intent
- Long paragraphs create immersion; short ones create pace
- White space is a tool, not an accident

### 2. Concrete and Sensory Language

Abstract language tells. Concrete language shows. The difference is everything.

**The specificity ladder:**
- Level 0 (abstract): "She felt sad."
- Level 1 (named emotion): "Grief pressed against her ribs."
- Level 2 (physical detail): "She pressed her thumbnail into her palm until the skin turned white."
- Level 3 (world detail): "The kitchen smelled of coffee no one had poured."

Level 2-3 is where strong prose lives. Level 0 is almost always wrong. Level 1 is acceptable in transitions.

**Sensory hierarchy for immersion:**
1. Sight (most common — don't over-rely)
2. Sound (hugely underused — the second most immersive sense)
3. Touch/texture (creates intimacy)
4. Smell (triggers memory — powerful in small doses)
5. Taste (rarest — use for specific moments)

**The "camera" principle:** Prose has a camera. Is it wide-angle (landscape, setting, atmosphere) or close-up (face, hands, texture)? The best prose moves between focal lengths deliberately. A paragraph that stays at one focal length too long becomes monotonous.

### 3. Verb Power

Verbs carry prose. Adjectives and adverbs are crutches for weak verbs.

**Rules:**
- Prefer active voice. Passive voice is a deliberate choice, not a default.
- Replace "was + verb-ing" with simple past: "was running" → "ran"
- Kill adverbs that duplicate verb meaning: "shouted loudly" → "shouted"
- Kill adverbs by finding a better verb: "walked slowly" → "shuffled," "ambled," "dragged her feet"
- Limit "to be" verbs (is, was, were, are) — they flatten prose. Not zero, but conscious.
- "Said" is invisible. "Exclaimed," "declared," "opined" are not. Use "said" 90% of the time.

**Verb precision spectrum:**
- Generic: "He went across the room."
- Better: "He crossed the room."
- Precise: "He shouldered through the crowd."
- Over-written: "He perambulated across the expansive chamber." (← never)

The right verb eliminates the need for adverbs AND tells us something about character.

### 4. Point of View Discipline

POV is not just who's telling the story — it's what information is available and how it's filtered.

**POV violations to catch:**
- **Head-hopping**: Switching whose thoughts we access within a scene
- **Impossible knowledge**: "She didn't notice the man behind her" — if she didn't notice, how does the POV character know?
- **Camera-from-outside**: In close third, describing the POV character's own face ("her eyes widened") unless they're looking in a mirror — they can't see themselves
- **Tonal inconsistency**: A child's POV using adult vocabulary; a hardened detective noticing flower arrangements

**POV as voice filter:** Everything on the page is filtered through the POV character's perception, vocabulary, priorities, and biases. A carpenter notices joints and grain. A chef notices what's cooking. A grieving person notices absence.

### 5. Subtext and Implication

The most powerful thing in prose is what you don't say.

**Techniques:**
- **Behavioral subtext**: Show the emotion through action, not statement. A character who says "I'm fine" while shredding a napkin.
- **Loaded objects**: An unwashed mug on the counter. A coat still hanging by the door. Objects carry emotional weight when the context is established.
- **Dialogue gaps**: What characters avoid saying reveals more than what they say.
- **Juxtaposition**: Place two images side by side and let the reader draw the connection. Don't explain.

**The iceberg principle (Hemingway):** The dignity of movement of an iceberg is due to only one-eighth of it being above water. If a writer knows enough about what they're writing, they may omit things they know. The reader will feel what's been omitted as strongly as what's present.

### 6. Opening and Closing Sentences

First and last sentences of scenes, chapters, and pieces carry disproportionate weight.

**Opening sentences should:**
- Create a question in the reader's mind (not answer one)
- Establish voice immediately
- Ground the reader in time, place, or situation — but not all three at once
- Avoid throat-clearing ("It was a typical Tuesday..." "Let me begin by saying...")

**Closing sentences should:**
- Land on an image, not an explanation
- Create resonance — the reader should feel the sentence vibrating after they stop reading
- Avoid summarizing what just happened
- Often: circle back to an image from the opening (creates structural satisfaction)

### 7. Economy and Precision

Every word must earn its place. This is not minimalism — lush prose can be economical. Economy means no word is wasted, not that few words are used.

**Cut ruthlessly:**
- "In order to" → "to"
- "The fact that" → cut entirely and restructure
- "He began to walk" → "He walked" (unless the beginning-of-action is the point)
- "Very," "really," "quite," "rather," "somewhat" → almost always cut
- "There was/there were" openings → restructure with a real subject
- Throat-clearing phrases: "It is important to note that," "It should be mentioned that" → cut

**Repetition rules:**
- Unintentional repetition of words within a paragraph = amateur (especially unusual words)
- Intentional repetition for rhetorical effect = powerful ("We shall fight on the beaches, we shall fight on the landing grounds...")
- Know which one you're doing

---

## Mode: Write

When generating new prose:

1. Establish the style target (literary, commercial, spare, lush, journalistic, lyric)
2. Identify the POV and voice filter
3. Draft with all seven lenses active — don't write flat and polish later
4. After drafting, run the diagnosis checklist (below) against your own output
5. Revise before delivering

**Style calibration:**

| Style | Sentence length | Metaphor density | Sensory detail | Subtext | Rhythm |
|-------|----------------|-----------------|----------------|---------|--------|
| **Spare** | Short-medium. Fragments welcome. | Low — only when precise | Selective, sharp | High — silence does the work | Staccato, percussive |
| **Literary** | Varied, often long with embedded clauses | Medium-high — original, not decorative | Rich, multi-sensory | High — layers of meaning | Complex, musical |
| **Commercial** | Medium, clear, forward-moving | Low-medium — familiar metaphors | Moderate — enough to ground | Moderate — don't lose the reader | Steady, propulsive |
| **Literary-commercial** | Varied but accessible | Medium — striking but not obscure | Rich but never purple | Medium-high | Musical but paced |
| **Journalistic** | Short-medium, declarative | Low — only for color | Concrete, factual | Low — clarity over layers | Direct, clean |
| **Lyric** | Long, flowing, often periodic | High — the prose IS metaphor | Lush, synesthetic | Medium — beauty over puzzle | Incantatory, wave-like |

## Mode: Polish

When revising existing prose:

1. Read the passage aloud (mentally). Mark where the rhythm stumbles.
2. Circle every "to be" verb. Replace 60%+ with stronger verbs.
3. Highlight every adjective and adverb. Cut those that duplicate verb/noun meaning.
4. Check sentence openings — if 3+ consecutive sentences start the same way, vary them.
5. Check for the specificity ladder — push abstract language down to Level 2-3.
6. Verify POV discipline — no head-hopping, no impossible knowledge.
7. Check first and last sentences of each paragraph for strength.
8. Read aloud again after revision. The rhythm should feel natural, not forced.

## Mode: Diagnose

When auditing prose quality:

Score each lens 1-5 and provide specific examples:

| Lens | Score | Evidence |
|------|-------|----------|
| Rhythm & Cadence | [1-5] | [quote the best and worst passages] |
| Concrete & Sensory | [1-5] | [show where it's abstract vs. grounded] |
| Verb Power | [1-5] | [count to-be verbs, flag weak verbs] |
| POV Discipline | [1-5] | [any violations?] |
| Subtext & Implication | [1-5] | [is everything over-explained?] |
| Openings & Closings | [1-5] | [evaluate first/last sentences] |
| Economy & Precision | [1-5] | [flag bloat, redundancy, throat-clearing] |

Provide a priority revision list: the 3-5 changes that would most improve the passage.

## Mode: Agent Audit

When evaluating an agent's instructions for prose output quality:

1. Read the agent's system prompt / instructions file
2. Check: does the prompt encode ANY prose craft principles, or does it only specify content/structure?
3. Most agent prompts produce mediocre prose because they specify WHAT to write but not HOW to write well
4. Recommend specific additions:
   - Verb power directives ("Prefer active voice. Replace adverbs with precise verbs.")
   - Rhythm instructions ("Vary sentence length deliberately. End sentences on strong words.")
   - Sensory grounding ("Use Level 2-3 specificity. Engage at least two senses per scene.")
   - Anti-patterns to forbid ("Never open with throat-clearing. Never use 'very' or 'really'.")
5. Draft a "Prose Quality" section that can be inserted into the agent's instructions

---

## Rules

- Never sacrifice clarity for style. Obscurity is not depth.
- "Purple prose" = when the decoration obscures the meaning. The cure is not plainness — it's precision.
- Know the difference between your voice and affectation. Voice is consistent and earned. Affectation is performing someone else's style.
- Clichés are dead metaphors. They once meant something. Find what they meant and say it fresh, or cut them.
- The reader's experience matters more than the writer's intention. If it doesn't land, it doesn't work, no matter how clever it is.
- Read your prose aloud. If you stumble, the reader will stumble.
- Prose craft applies to ALL writing — fiction, non-fiction, marketing copy, agent instructions. Good sentences are good sentences.
