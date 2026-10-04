---
name: voice-designer
description: Build detailed voice profiles for characters, narrators, brands, or AI agents — covering diction, syntax, rhythm, worldview, signature patterns, and failure modes. Use when creating a character voice, designing an agent's persona, or auditing voice consistency.
disable-model-invocation: true
---

Design or audit a voice profile: $ARGUMENTS

$ARGUMENTS can include:
- A person/character to profile (`profile: [name or description]`)
- A writing sample to reverse-engineer (`analyze: [text or path]`)
- An existing voice profile to audit (`audit: [path]`)
- An agent system prompt to voice-check (`agent-voice: [path]`)
- A target medium: `novel`, `agent`, `brand`, `narrator`, `character`, `marketing`
- Empty — ask what voice the user needs

---

## What a Voice Profile IS

A voice profile is a machine-readable specification of how a person, character, or agent sounds on the page. It captures not just WHAT they say but HOW they say it — the unconscious choices of diction, syntax, rhythm, metaphor, and worldview that make a voice recognizable.

A good voice profile should be specific enough that two different writers (or two different LLMs) given the same profile would produce output that sounds like the same person.

---

## The Voice Profile Framework

### Layer 1: Identity Foundation

Who is this voice? Not biography — psycholinguistic identity.

**Capture:**
- **Core role**: One sentence. "A movement catalyst who speaks from decades of field experience." "A sixteen-year-old who processes everything through music."
- **Worldview lens**: What does this voice pay attention to? What does it notice first? A carpenter sees joints. A theologian sees patterns of meaning. A teenager sees social hierarchy.
- **Authority source**: Where does this voice's authority come from? Experience? Credentials? Age? Suffering? Charisma? Sacred text?
- **Emotional baseline**: Where does this voice sit when it's not being pulled by plot or topic? Wry? Warm? Restless? Measured? Defiant?
- **Relationship to audience**: Teaching down? Standing alongside? Looking up? Inviting in? Challenging from ahead?

### Layer 2: Diction Profile

The vocabulary fingerprint.

**Capture:**
- **Register**: Formal / informal / code-switching? What triggers register shifts?
- **Vocabulary domain**: What fields does this voice borrow from? (Theology, sports, cooking, military, music, science, street, academic)
- **Favorite words**: 5-10 words this voice reaches for repeatedly. Not tics — characteristic choices.
- **Forbidden words**: Words this voice would NEVER use. (A blue-collar character doesn't say "utilize." A theologian doesn't say "basically.")
- **Jargon posture**: Does this voice use jargon and expect the reader to keep up? Define terms as it goes? Avoid jargon entirely?
- **Abstraction level**: Does this voice default to concrete ("the kitchen smelled of burnt coffee") or abstract ("there was an atmosphere of neglect")?
- **Profanity/intensity**: Range and triggers. Some voices never swear. Some swear only under extremity. Some swear casually.

### Layer 3: Syntax Signature

How sentences are built.

**Capture:**
- **Sentence length tendency**: Short and punchy? Long and winding? Varied (and how)?
- **Sentence structure**: Simple declarative? Complex with embedded clauses? Questions? Fragments?
- **Paragraph rhythm**: Short paragraphs (conversational, urgent)? Long paragraphs (immersive, intellectual)?
- **Opening patterns**: How does this voice typically start a thought? ("Look, here's the thing..." / "Consider this:" / "I remember when..." / Direct statement)
- **Closing patterns**: How does this voice end a thought? (Question? Image? Challenge? Trailing off?)
- **Conjunction habits**: "And" at sentence starts (biblical, additive)? "But" (oppositional)? Semicolons (intellectual)? Dashes (interrupted thought)?
- **Parenthetical style**: Parentheses, dashes, or none? How often?

### Layer 4: Rhetorical DNA

How this voice builds arguments and conveys meaning.

**Capture:**
- **Primary reasoning mode**: Deductive (principle → example)? Inductive (example → principle)? Narrative (story → meaning)?
- **Argument patterns**: 2-3 recurring structures this voice uses. (E.g., "Reframe → Ground → Extract → Connect → Land")
- **Metaphor systems**: What domains does this voice draw metaphors from? (Organic/biological, mechanical, journey/travel, warfare, domestic, musical)
- **Metaphor density**: How often? Some voices are metaphor-rich; others are spare.
- **Question usage**: Does this voice ask rhetorical questions? How often? At what structural moments?
- **Example preference**: Personal anecdotes? Historical examples? Pop culture? Scientific data? Scripture?
- **Humor type**: Wit? Irony? Self-deprecation? Absurdism? None?

### Layer 5: Signature Elements

The fingerprint details that make a voice instantly recognizable.

**Capture:**
- **Recurring phrases**: 3-5 phrases this voice returns to. ("Here's what I've learned..." / "The question behind the question is..." / "You know what I mean?")
- **Structural tics**: Does this voice use lists? Numbered points? Subheadings? Stream of consciousness?
- **Dialogue markers**: In fiction, how does this character talk in dialogue vs. narration? Do they trail off? Interrupt? Monologue?
- **Pronoun patterns**: "I" heavy? "We" heavy? "You" heavy? Distribution matters.
- **Direct address**: Does this voice talk TO the reader/listener? How often?
- **Citation/reference style**: Does this voice cite sources? Drop names? Allude without citing?

### Layer 6: Failure Modes

What this voice must NEVER sound like. These are as important as the positive markers.

**Capture 3-5 anti-patterns:**

| Anti-pattern | Example | Why it's wrong |
|-------------|---------|---------------|
| [Name the failure] | [Show a sentence that exhibits it] | [Explain why this violates the voice] |

Common failure modes:
- **Corporate consultant**: "To optimize your engagement..." (voice sounds like a McKinsey deck)
- **Detached academic**: "The implications suggest..." (voice sounds like a journal abstract)
- **Generic motivational**: "You've got this!" (voice sounds like a LinkedIn influencer)
- **Purple prose**: "The magnificent cerulean firmament..." (voice sounds like a thesaurus)
- **Hallmark sentiment**: "What really matters is..." (voice sounds like a greeting card)
- **AI-generic**: "Certainly! Here are some thoughts on..." (voice sounds like default LLM output)

---

## Mode: Profile from Description

When building a voice profile from a character/person description:

1. Ask clarifying questions if needed (role, audience, medium, genre)
2. Work through all 6 layers systematically
3. Generate 3 sample paragraphs in the voice (different topics/contexts)
4. Include a "Voice Calibration Test" — a short passage for the user to evaluate

**Output format:**

```markdown
# Voice Profile: [Name]

## Identity
[Layer 1 content]

## Diction
[Layer 2 content]

## Syntax
[Layer 3 content]

## Rhetoric
[Layer 4 content]

## Signature Elements
[Layer 5 content]

## Failure Modes
[Layer 6 content]

## Voice Markers (Quantified)

| Marker | Target | Description |
|--------|--------|-------------|
| [Marker 1] | [0.0-1.0] | [What it means at this level] |
| [Marker 2] | [0.0-1.0] | [What it means at this level] |
| [Marker 3] | [0.0-1.0] | [What it means at this level] |

## Sample Output
[3 paragraphs demonstrating the voice across different contexts]

## Calibration Test
[A passage in this voice that the user can evaluate for accuracy]
```

## Mode: Reverse-Engineer from Sample

When building a voice profile from existing writing:

1. Read the sample closely (minimum 500 words, ideally 2000+)
2. Analyze each layer by marking specific evidence in the text
3. Quantify where possible (sentence length averages, pronoun distribution, metaphor density)
4. Identify 3-5 most distinctive features — the elements that make this voice THIS voice
5. Generate the full profile with citations back to the sample
6. Write a test paragraph in the extracted voice on a NEW topic
7. Highlight any ambiguities ("The sample is too short to determine X with confidence")

## Mode: Agent Voice Design

When designing a voice for an AI agent:

1. Start with the agent's purpose and audience
2. Build the full 6-layer profile
3. Translate the profile into **prompt-ready instructions**:
   - Convert voice markers into explicit directives ("Always use 'we' over 'I'")
   - Convert failure modes into prohibitions ("Never open with 'Certainly!'")
   - Include example outputs at different quality levels (good / mediocre / bad)
4. Design a **voice fidelity checklist** the agent can run before responding
5. Consider multi-mode behavior — does the agent's voice shift in different contexts?

**Agent voice prompt structure:**

```markdown
## Voice Identity
[1-2 paragraphs: who this agent IS]

## Voice Rules
- [Directive 1]
- [Directive 2]
- [Directive 3]

## Voice Markers
| Marker | Target | How to achieve it |
|--------|--------|------------------|
| ... | ... | ... |

## Never Sound Like
- [Anti-pattern 1 with example]
- [Anti-pattern 2 with example]

## Pre-Response Checklist
- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]
```

## Mode: Movement Leader Voice Fingerprint (substrate-conformant)

When the voice is for a **movement leader** whose research lives at `docs/movement_leader_research/{slug}/`, produce the voice fingerprint in the schema consumed by the [`movement-leader-substrate`](../movement-leader-substrate/SKILL.md) document. This is **not** a free-form profile — it is a fixed-shape artifact with four required components:

### 1. Weighted markers (must sum to 100%)

```
| Marker | Target | Weight |
|--------|--------|--------|
| {Marker 1} | ≥ 0.7 | 30% |
| {Marker 2} | 0.5–0.8 | 25% |
| {Marker 3} | ≥ 0.5 | 20% |
| {Marker 4} | ≥ 0.5 (2–5 metaphors / 100 words) | 15% |
| {Marker 5} | ≥ 0.4 | 10% |
| **Coherence target** | ≥ 0.75 | — |
```

Exactly five markers. Weights must sum to 100. Each marker is a measurable trait (e.g. "Christocentric anchoring", "prophetic intensity", "pastoral warmth", "narrative imagery", "theological depth") — not a vibe.

### 2. Hallmark lexicon (9+ terms)

A flat, comma-separated list of the leader's signature terminology — words that, in combination, identify the writing. Pull from `profile/voice-analysis.md` and the corpus.

### 3. Antithesis prohibition (non-negotiable)

One paragraph naming the **specific anti-pattern this leader avoids**. This is load-bearing — it usually shows up as the leader's most-corrected reader misreading. Examples: Alan Hirsch avoids contrastive negation→affirmation ("not X but Y"). If you cannot find one in the corpus, search until you can; if truly absent, write `No documented antithesis prohibition.`

### 4. Representative quotes (5+)

Direct, verifiable quotes from the corpus, each with attribution to source work:

```
> "{exact quote}" — *{work}*, {context}
```

Never reconstruct or paraphrase a quote inside quotation marks. If a paraphrase is the only available form, label it `(paraphrased)`.

### Where this goes

This voice fingerprint is written into Section 7 of `{SLUG}_RESEARCH_COLLATED.md`. Do not write a separate `voice-profile.md` file — the substrate is the single output.

### Reference implementation

See `docs/movement_leader_research/alan-hirsch/ALAN_HIRSCH_RESEARCH_COLLATED.md` Section 7 (Voice fingerprint).

---

## Mode: Audit

When auditing voice consistency:

1. Read the voice profile (or establish baseline from earliest sample)
2. Read the content being audited
3. Score each voice marker against the target
4. Identify specific passages where the voice drifts
5. Classify each drift by failure mode
6. Provide revision suggestions that restore voice fidelity

**Output:**

| Marker | Target | Actual | Drift? | Evidence |
|--------|--------|--------|--------|----------|
| ... | ... | ... | ... | [quote] |

**Top voice violations:**
1. [Passage] — sounds like [failure mode] — suggested revision: [fix]

---

## Rules

- A voice profile is descriptive, not prescriptive. It captures how someone actually sounds, not how you think they should sound. When reverse-engineering, trust the sample over your expectations.
- Voice is not accent or dialect alone. Don't reduce voice to spelling tricks ("gonna," "y'all") — those are surface features. Voice is structural, cognitive, rhythmic.
- Every voice has contradictions. A professor who curses when frustrated. A teenager who drops into formal register when scared. These contradictions are the most important things to capture — they make a voice feel real.
- Voice changes with context. Design for the range, not just the default. Note what triggers shifts.
- For AI agents: the most common failure is under-specifying voice. "Be friendly and helpful" is not a voice profile. It's a vibe check. Specify concretely.
- For fiction: each POV character needs a distinct voice profile. If you can swap their dialogue and no one notices, the voices aren't distinct enough.
- Less is more in failure modes. 3-5 sharp anti-patterns are better than 15 vague ones. The failure modes should be the specific traps THIS voice is most likely to fall into.
