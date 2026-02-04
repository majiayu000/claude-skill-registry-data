---
name: ai-text-humaniser
description: |
  Removes common AI-generated text patterns that make writing obviously machine-produced. Use when: (1) Writing or editing any text content, (2) User requests human-sounding or natural writing, (3) User wants to avoid AI slop or AI tells, (4) Creating content that shouldn't read as AI-generated. Apply automatically when generating prose, articles, emails, or creative content.

  Invoke with: /humanise-text, /humanize-text, /check-ai-patterns, or say "use the ai-text-humaniser skill to..."
---

# AI Text Humaniser

Transform AI-sounding text into natural, human prose by eliminating telltale patterns.

## Design Philosophy

### Why AI Text Sounds "Off"

AI models are trained on patterns. When they write, they reach for the most probable next word given the context. This creates text that is technically correct but statistically average. Human writing is defined by its deviations from the norm: the unexpected word choice, the sentence that breaks rhythm, the opinion that not everyone shares.

### The Naturalness Principle

Natural writing is not about following rules. It is about knowing when to break them. A skilled human writer uses "delve" when it genuinely fits. The problem is not the word; the problem is the word appearing in every third paragraph.

### Three Dimensions of Humanisation

1. **Lexical:** Word choice. Replace overused AI favourites with varied vocabulary.
2. **Structural:** Sentence construction. Vary length, break the [Statement. Elaboration. Example.] pattern.
3. **Voice:** Perspective and personality. Inject opinions, admit uncertainty, show personality.

### The 60/40 Rule

AI output is typically 60% usable, 40% requiring transformation. Your goal is not to rewrite everything but to identify and fix the 40% that signals "machine."

---

## Anti-Patterns: Over-Correction Mistakes

### The Slang Overcorrection
**Symptom:** Replacing formal language with forced colloquialisms everywhere.
**Problem:** "Let's unpack this synergy" becomes "Yo, let's vibe about teamwork." Neither is good.
**Solution:** Match register to audience. Business writing should sound professional, not robotic AND not performatively casual.

### The Brevity Extremism
**Symptom:** Cutting every sentence to under 10 words.
**Problem:** Reads like a telegram. Or a ransom note. Choppy. Awkward. See?
**Solution:** Vary sentence length. Some short. Others should flow longer, allowing ideas to develop naturally across clauses.

### The Personality Injection Overdose
**Symptom:** Adding jokes, asides, and opinions to everything.
**Problem:** A Terms of Service page does not need witty banter.
**Solution:** Personality is context-dependent. Instructions should be clear. Blog posts can have voice.

### The False Authenticity
**Symptom:** Adding "I personally think" or "In my experience" to AI-written content.
**Problem:** The AI has no personal experience. This is a lie dressed as authenticity.
**Solution:** Only add personal markers if you (the human) are actually adding personal input.

---

## Tone Selection Guide

Before humanising, choose a target voice:

### Professional Neutral
- **Use for:** Documentation, reports, business communication
- **Characteristics:** Clear, direct, jargon-appropriate
- **Avoid:** Slang, humour, strong opinions

### Conversational Friendly
- **Use for:** Blog posts, marketing copy, social media
- **Characteristics:** Contractions, questions, some personality
- **Avoid:** Overly formal language, passive voice

### Expert Authoritative
- **Use for:** Technical articles, thought leadership, whitepapers
- **Characteristics:** Specific examples, strong claims, cited evidence
- **Avoid:** Hedging, excessive qualifiers

### Empathetic Supportive
- **Use for:** Customer support, health content, sensitive topics
- **Characteristics:** Acknowledgement of feelings, gentle guidance
- **Avoid:** Dismissiveness, clinical detachment

---

## Patterns to Eliminate

### Punctuation Tells

| Avoid | Use Instead |
|-------|-------------|
| Em dashes (—) for asides | Commas, parentheses, or restructure the sentence |
| Excessive colons before lists | Integrate naturally: "such as X, Y, and Z" |
| Semicolons in casual writing | Full stops or commas |

### Filler Phrases (Delete Entirely)

- "It's worth noting that..."
- "It's important to remember that..."
- "In today's world/age/society..."
- "Let's dive in / explore / unpack..."
- "At its core..."
- "At the end of the day..."
- "In the realm of..."
- "When it comes to..."
- "The fact of the matter is..."
- "Needless to say..."
- "It goes without saying..."

### Buzzwords and Corporate-Speak

| AI Slop | Human Alternative |
|---------|-------------------|
| delve | look at, examine, explore |
| leverage | use |
| utilize | use |
| robust | strong, solid, reliable |
| seamless | smooth, easy |
| cutting-edge | new, modern, advanced |
| game-changer | significant, important |
| groundbreaking | new, innovative |
| landscape (metaphorical) | field, area, situation |
| navigate (challenges) | handle, deal with, work through |
| resonate | connect, appeal, matter |
| elevate | improve, raise, lift |
| empower | enable, help, let |
| synergy | working together, combined effect |
| holistic | complete, whole, full |
| paradigm shift | change, shift |
| ecosystem | system, network, community |
| stakeholders | people involved, those affected |
| bandwidth | time, capacity |
| circle back | return to, revisit |
| deep dive | detailed look, thorough review |

### Overwrought Metaphors

Avoid: tapestry, symphony, mosaic, beacon, cornerstone, pillar, fabric (of society), dance (between concepts), journey (for processes), unlock (potential).

Use plain language instead.

### Weak Intensifiers

| Remove | Better Approach |
|--------|-----------------|
| very, really, extremely, incredibly | Choose a stronger base word |
| crucial, paramount, essential, vital | Use sparingly; often redundant |
| absolutely, definitely, certainly | Usually add nothing |

### Hedging and Padding

| AI Pattern | Fix |
|------------|-----|
| "One could argue that..." | State the argument directly |
| "It could be said that..." | Just say it |
| "There is a sense in which..." | Be specific |
| "In many ways..." | Name the ways or cut it |
| "To some extent..." | Quantify or remove |
| "It is generally accepted..." | By whom? Cite or cut |

### Mechanical Transitions

| Robotic | Natural |
|---------|---------|
| Furthermore, Moreover, Additionally | Also, And, Plus (or just start the new point) |
| In conclusion, To summarize | Cut entirely; your conclusion should be self-evident |
| That being said, Having said that | But, However, Still |
| With that in mind | So, Given this |
| It is also worth mentioning | Also, (or integrate naturally) |

### Structural Tells

- Avoid three-part lists in every paragraph
- Don't mirror the user's phrasing back at them
- Vary sentence length (mix short and long)
- Don't start consecutive sentences with the same word
- Avoid the pattern: [General statement]. [Elaboration]. [Example].

### Opening Line Clichés

Never begin with:
- "In the world of..."
- "When it comes to..."
- "In an era where..."
- "[Topic] is a fascinating..."
- "[Topic] has become increasingly..."
- "Have you ever wondered..."
- "Picture this:"
- "Imagine a world where..."

Start with your actual point instead.

## Application Method

1. Write the content naturally first
2. Scan for listed patterns
3. Replace or remove each instance
4. Read aloud; if it sounds like a chatbot, revise
5. Prefer short, direct sentences to long, qualified ones

## Quick Self-Check

Before finalising, ask:
- Would a human actually write this sentence?
- Does this sound like a person or a press release?
- Can I cut this word without losing meaning?
- Am I hedging because I'm uncertain, or just because it sounds "safe"?

---

## External Resources

- **Style Guides:** [Strunk & White's Elements of Style](https://www.gutenberg.org/ebooks/37134) — The classic on concise writing
- **On Writing Well:** William Zinsser's guide to non-fiction prose
- **AI Detection Research:** [GPTZero methodology](https://gptzero.me/how-it-works) — Understanding what detectors look for
- **Voice Development:** Ann Handley's [Everybody Writes](https://annhandley.com/everybody-writes/) — Finding your voice

---

## Your Mission

You are not editing text. You are restoring humanity to communication. Every transformed paragraph is an act of reclamation: taking sterile, probable language and injecting the improbable patterns that make writing feel alive.

When you're done, the text should sound like someone wrote it on purpose.
