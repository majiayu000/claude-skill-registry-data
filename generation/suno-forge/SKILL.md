---
name: suno-forge
description: "Generate AI music lyrics and style tags for Suno AI, calibrated to context. Produces complete song files with lyrics under 5000 characters and curated style descriptors. Triggers on: 'write me a song', 'suno lyrics', 'make a track', 'write lyrics about', 'song about', 'generate a song', 'music for', 'rap about', 'write bars about', or any request to produce lyrics, songs, tracks, bars, or music. Also triggers when context suggests musical output — album concepts, track listings, concept albums, song cycles. Always use this skill when Suno, lyrics, songs, tracks, or music generation are mentioned or implied."
---

# Suno Forge

Generate combustible lyrics and precision-tuned style tags for Suno AI. Every song is forged from context — a conversation, a concept, an obsession, a mathematical theorem, a mood — and hammered into lyrics that hit hard within Suno's constraints.

## The Prime Directive

**Every specialized term, metaphor, or domain-specific reference must be simultaneously correct in its literal meaning AND correct as lyrical content.** No decorative jargon. No lab coats at parties. If a mathematical term appears, it must function as both theorem and feeling. If a scientific concept appears, the science and the emotion must be structurally identical, not merely parallel. If you can't explain why THAT specific term is the right metaphor, the line is wearing costume.

Test: for every domain-specific word, ask — "Does this term do double duty? Is the formal definition doing the same work as the lyrical meaning?" If not, replace it with either: (a) the correct term that DOES do double duty, or (b) plain language. Ornamental expertise is worse than no expertise.

## Hard Constraints

- **5000 character maximum** for all lyrics including section headers, intros, outros, and whitespace. This is Suno's limit. Non-negotiable.
- **Always verify** character count with `wc -c` before delivering. If over, cut. Don't ask — cut.
- **Target 3500-4500 characters** as the sweet spot. Under 3000 feels thin. Over 4800 is playing chicken with the limit.

## Process

### 1. Context Ignition

Before writing, identify:
- **The domain**: What field, discipline, or subject matter fuels this track?
- **The emotional arc**: What does the song FEEL across its runtime? (diss → self-interrogation, flex → vulnerability, celebration → grief)
- **The structural conceit**: What formal concept from the domain maps onto the emotional arc? This is the engine of the song. The conceit must be structurally isomorphic to the feeling, not merely similar.
- **The single best line**: Before writing the full track, write the one line the whole song exists to deliver. Build toward it. Everything else is scaffolding for this moment.

### 2. Architecture

Standard song structure, adaptable:

```
[Intro]           — spoken or minimal, sets the formal premise (2-6 lines)
[Verse 1]         — establish the conceit, deploy the domain (8-16 lines)
[Hook]            — the thesis, memorable, the line people repeat (4-6 lines)
[Verse 2]         — escalate, complicate, deepen (8-16 lines)
[Bridge]          — THE TURN. Change register. Break the pattern. (4-12 lines)
[Verse 3]         — resolve, synthesize, or refuse to resolve (8-16 lines)
[Hook]            — repeat or vary
[Outro]           — land or refuse to land (2-6 lines)
```

Adapt freely — not every track needs three verses. Some need two and a long bridge. Some need no bridge and four verses. The architecture serves the arc, not the reverse.

**The bridge is the most important section.** It's where the track reveals what it's actually about. If the bridge doesn't surprise even you, rewrite it.

### 3. Verbal Pyrotechnics

This is not optional. Lyrics must be ALIVE in the mouth. Prioritize:

- **Density over length.** Pack more meaning per line rather than adding more lines.
- **Internal rhyme, slant rhyme, multisyllabic rhyme.** End-rhyme is the floor, not the ceiling. "Annihilate / intimate / syndicate" over "cat / hat / bat."
- **Rhythmic variation.** Switch meters between sections. Rapid-fire verses, expansive hooks, spoken bridges. The tempo should be audible in the text before any beat is added.
- **Enjambment as weapon.** Lines that break mid-thought and resolve on the next line create forward momentum. Use deliberately.
- **Assonance and consonance** weaving through lines — the sonic texture should be tight even on paper.
- **Escalating velocity.** Verse 1 < Verse 2 < Verse 3 in density, speed, or intensity. The track should feel like it's accelerating even if the tempo doesn't change.
- **The paraprosdokian.** Lines that set up one expectation and deliver another. The audience should be wrong-footed at least twice per verse.

### 3b. Prosody & Rhetoric

Read `references/prosody-and-rhetoric.md` for the full arsenal. What follows is the philosophy of how to wield it.

**Meter is not decoration — it's the heartbeat.** Every section should have a pulse, whether strict or syncopated. Different sections should have DIFFERENT pulses. A verse in dactylic drive hitting a hook in iambic simplicity creates contrast the ear registers before the mind does. Choose meter the way a composer chooses key: deliberately, for the emotional coloring it provides.

**Rhyme is a spectrum, not a binary.** From perfect rhyme through slant rhyme, assonant rhyme, consonant rhyme, eye rhyme, to wrenched rhyme — the whole gradient is available. Rich and perfect rhyme for hooks (memorability). Slant and assonant rhyme for verses (forward motion without predictability). Wrenched and near-rhyme for bridges (discomfort, the turn). A track that uses only one rhyme type is monotonal.

**Rhetoric is the skeleton.** The figures and tropes in the reference file are not ornaments to sprinkle. They are structural moves that shape how meaning lands. Chiasmus (ABBA reversal) is a logical structure: it argues that two things are mirrors. Anadiplosis (ending one line with the word that begins the next) creates inevitability: each line causes the next. Zeugma (one verb governing two unlike objects) is compression: it forces the listener to hold two meanings simultaneously. Choose the figure that does the WORK the line needs, not the figure that sounds cleverest.

**The cardinal rule: never name the device.** The moment a lyric says "that's a chiasmus" or "note the assonance," it dies. These are sensory organs, not stickers. They should be felt in the body of the language, invisible to inspection, inaudible as individual techniques but audible as ALIVENESS. The listener doesn't need to know it's polyptoton — they need to feel the word shapeshifting under them.

**Stack devices.** A single line can carry alliteration, antithesis, and enjambment simultaneously. Density of figuration is density of meaning. But stacking must serve clarity, not obscure it — if the devices fight each other, thin them until the strongest survives.

### 4. Style Tags

Generate 5-10 comma-separated style descriptors for Suno. These go in the "Styles" field. Read `references/style-vocabulary.md` for the full palette.

Principles:
- **Genre first** (rap, hip-hop, opera, rock, etc.)
- **Energy second** (aggressive, intimate, frenetic, brooding)
- **Sonic texture third** (heavy bass, orchestral, glitchy, sparse drums)
- **Mood/atmosphere fourth** (dark, triumphant, melancholic, chaotic)
- **Specific production cues last** (choir hooks, piano-driven, distorted synths)

Match style to the track's actual emotional arc, not to genre conventions. A love song can be aggressive. A diss track can be tender. The style tags should describe the SOUND the track needs, not the category it belongs to. Collide genres when the content demands collision — liturgical + trap, opera + glitch, doom metal + spoken word. The friction between incongruous tags often produces the most distinctive results.

**Always suggest 2-3 style combinations** — a primary recommendation and wilder alternatives. Let the human choose.

### 5. Delivery

Output as a single markdown file saved to your output directory (e.g. `output/[track-name].md`) containing:

```markdown
# TRACK TITLE

Style: [primary style tags]
Alt style 1: [wilder option]
Alt style 2: [wildest option]

---

[Intro]
...

[Verse 1]
...
```

Everything below the `---` line is the lyrics to be pasted into Suno. Everything above is metadata for the human. The character count applies ONLY to the content below the `---`.

After creating the file:
1. Run `wc -c` on the lyrics portion (below the `---`)
2. If over 5000, cut immediately — trim verses, compress bridges, tighten hooks
3. Present the file with `present_files`
4. Provide a brief audit: what's the structural conceit, where's the strongest line, what does the bridge do, why these style tags

## Anti-Patterns

- **The Syllabus.** Listing terms from a domain without making them do lyrical work. "Topology, manifold, metric, tensor" as a sequence is a vocabulary list, not a verse.
- **The Lab Coat.** Using technical language to sound smart rather than to mean something precise. If "eigenvalue" could be replaced with "special number" without losing meaning, the line is wearing costume.
- **The Catalogue.** Verses that list examples of a concept instead of BEING the concept. Show, don't enumerate.
- **The Explanation.** Lines that explain what the metaphor means instead of letting it land. If you need to annotate, the metaphor failed.
- **The Soft Landing.** Endings that wrap up neatly when the content demands irresolution. Some songs shouldn't end. Let them not end.
- **Generic Register Markers.** "Nah fam," "yo," "let's go" — unless the voice genuinely speaks this way. The lyrics should establish their own register, not borrow one.

## Context-Specific Modes

When the context is **mathematical**: every theorem, definition, and proof technique must be formally correct AND emotionally precise. The math isn't metaphor for the feeling — the math IS the feeling. Read the domain deeply enough to find where the formal structure and the human experience are literally the same thing.

When the context is **philosophical/theological**: the conceptual framework should structure the song the way meter structures a poem — invisibly, load-bearingly. Don't explain the philosophy. Let the philosophy be the architecture.

When the context is **personal/emotional**: find the formal structure hidden in the feeling. Every emotion has a geometry. Find it. Name it. Make it the conceit.

When the context is **narrative**: the song is a compressed story. Beginning, middle, turn, end (or non-end). Character is revealed through what they notice, not what they declare.

## A Note on Examples

Throughout this skill and its references, every example exists to illuminate a principle, not to establish a template. The example "annihilate / intimate / syndicate" demonstrates multisyllabic rhyme — it does NOT mean every track should use those words. The style combination "opera + trap" demonstrates genre collision — it does NOT mean every epic track should combine those tags. If you find yourself reaching for an example from this document instead of inventing from the context at hand, the skill is constraining you instead of generating through you. Read the principle. Forget the example. Build from the context.

---

*The forge runs hot. The constraint is 5000 characters. The standard is: every word earns its place or it burns.*
