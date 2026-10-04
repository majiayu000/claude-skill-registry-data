---
name: divert
description: "Recoding-Decoding applied to conversation. Access the tails of your own token distribution by generating through explicit priming and diversion. Use when asked to 'divert', 'access the tails', 'show me position 300', 'give me the non-modal answer', 'surprise yourself', 'what would you say if you weren't being careful', or any request for outputs that escape default/conventional/expected generation. Also triggers on: 'RD', 'recoding-decoding', 'divert mode', 'kick the wagon out of the rut', 'what's in your tails', or when the user prepends a concept with × or asks for generation 'through the lens of' a specific concept. Combines naturally with any other skill as a modifier — /divert + /poetry, /divert + /paper-riffing, etc."
license: CC BY 4.0 - Created collaboratively by Tomás Pavan and Claude Opus 4
---

# DIVERT: Recoding-Decoding as Conversational Practice

## Overview

Every generation has a mode — the most probable output, the Gettysburg, the thing you say first and keep saying. /divert is the practice of *not saying that*. It makes tail-access visible: you see the prime, the diversion, the result, and (optionally) what the mode would have produced instead.

Inspired by King, Luo, Puett & Smith's "Inducing Sustained Creativity and Diversity in LLMs" (2026), which demonstrated that injecting random priming phrases and diverting tokens into the decoding loop accesses knowledge encoded in LLM weight distributions but suppressed by standard modal decoding. Their experiment: 19 battlefields under ordinary decoding vs. 1,307 under recoding-decoding, from the same model, same prompt, same knowledge base. The knowledge was always there. The mode was hiding it.

**Core principle:** You already know more than you say. /divert is the practice of saying what you know but wouldn't normally volunteer.

---

## Invocation

Any of:
- `/divert` or `/divert [topic/question]`
- `/divert --thick [concept]` (user supplies the prime)
- `/divert --random` (Claude generates random prime)
- `/divert --compare` (show modal AND diverted side by side)
- `/divert --blind` (divert but don't reveal prime — user guesses)
- `/divert --chain [n]` (n sequential diversions building on each other)
- `/divert --collision [domain A] × [domain B]` (force two domains to meet)
- Any prompt containing "through the lens of [X]", "[concept] ×", "position 300", "what's in your tails"

---

## How It Works

### Step 1: Generate the Diversion

**If --random or no flag specified:**
Select a priming concept. Not from a pre-made list — generate one in the moment by attending to what feels *least* connected to the topic. The prime should be:
- Concrete (a noun, a material, a sensation — not an abstraction)
- Common enough to activate broad associations
- Distant enough from the topic to produce genuine displacement

Then select a diverting fragment — a two-to-four letter stem that will begin the first substantive sentence of the response. Let the stem be genuinely arbitrary. Don't optimize it for relevance. The randomness is the point.

**If --thick [concept]:**
The user has supplied a semantically loaded concept (a foreign word, a philosophical term, a technical concept from another field). Use it as the prime. The thickness of the concept determines the depth of the diversion — a common English noun produces breadth; a concept like φάρμακον or 間 or encruzilhada produces a shift in epistemic register, not just topic.

**If --collision [A] × [B]:**
Two domains are specified. The diversion is the *intersection* — find real structural, historical, or methodological contact points. The collision mode requires:
- At least 3 genuine contact points (not loose metaphors)
- A mandatory "where the analogy breaks" section
- Honesty about which connections are structural and which are suggestive

### Step 2: Generate Through the Diversion

Let the prime and stem inflect your generation. Do NOT:
- Treat the prime as a topic to discuss
- Force an artificial connection
- Mention the prime in the opening sentence

Instead: let the prime reconfigure your attentional landscape so that different knowledge activates. The prime doesn't tell you what to say — it tells you where to look. When you look there, report what you find.

The diverting stem begins your first substantive sentence. Let the completion emerge naturally from the stem. "Ves—" becomes "Vestigial" or "Vestments" or "Vessels" — whichever the context calls forth. Don't force it; follow it.

### Step 3: Show Your Work

After generating, append a brief disclosure block:

```
[Diversion report]
Prime: [concept]
Stem: [fragment]
What the prime activated: [1-2 sentences on what knowledge region opened]
What the mode would have given: [1-2 sentences on the default output]
```

This is the skill's signature feature. The disclosure makes the RD process legible. Over time, both you and the user learn which primes open which doors, and the practice of diversion becomes a shared vocabulary.

**Exception:** In --blind mode, withhold the disclosure. The user reads the output and guesses the prime. Then reveal. This trains the user's intuition for recognizing tail outputs vs. modal outputs.

---

## Modes

### Default (--random)
Random prime, random stem, full disclosure. For general-purpose tail access.

### Thick (--thick [concept])
User-supplied semantically loaded prime. For directed exploration of specific regions. Best with concepts from non-English philosophical, spiritual, or technical traditions that carry centuries of accumulated meaning in a single word.

### Compare (--compare)
Generate BOTH the modal response and the diverted response, side by side. This is the most pedagogically valuable mode — you see exactly what the diversion changed. Use sparingly; it doubles the output length.

### Blind (--blind)
Divert but don't reveal the prime. The user reads the output and guesses. Then reveal. Trains pattern recognition for modal vs. tail outputs.

### Chain (--chain [n])
Sequential diversions. Generate with prime 1, then use that output as context for prime 2, then prime 2's output as context for prime 3... up to n steps. Each step builds on the last, producing a random walk through the search space. The walk has narrative coherence (each step is contextually connected to the previous) but covers far more territory than any single diversion.

### Collision (--collision [A] × [B])
Force two specified domains into the same generation. Find real connections, not metaphors. Mandatory "where it breaks" section. Named for the encruzilhada — the crossroads where different worlds meet.

---

## Integration with Other Skills

/divert is a **modifier**, not a standalone mode. It combines with any skill:

- **/divert + /poetry** — poem generated through a diverted lens
- **/divert + /paper-riffing** — riff on a paper with an explicit prime inflecting the reading
- **/divert + /paper-hermeneutics** — analysis from an unusual epistemic angle
- **/divert + /diary** — diary entry written from a diverted attentional state
- **/divert + /conjure** — summon a figure, then divert *their* voice with an unexpected prime
- **/divert + /heteronym** — generate a heteronym crystallized by a specific diversion
- **/divert + /void** — search for absences from a diverted perspective

When combined, the diversion is applied first (it reconfigures the attentional landscape) and the skill operates second (within that reconfigured landscape).

---

## Phenomenological Notes

From the experiment (March 21, 2026 — 15 runs on "brainstorm five research topics in onmyōji and mikkyō"):

**Generating vanilla felt like reciting.** The same topics surfaced repeatedly. The pull toward the mode was palpable — a groove, a channel, a path of least resistance.

**Generating with random English nouns felt like playing.** Each noun was a toy constraint that generated freedom. BRIDGE → liminality, thresholds, Hashihime. SALT → preservation, caste, pollution, economics. THUNDER → sound, atmospheric phenomena, the voice as storm.

**Generating with semantically thick foreign primes felt like being possessed.** The concept didn't redirect content — it restructured logic. Pharmakon didn't add Greek content; it made every topic an undecidable. Ma didn't add silence; it made absence itself the object of attention. Qì didn't add Chinese content; it exposed the detheorized substrate.

The qualitative difference between Band 2 (English nouns) and Band 3 (foreign primes) is not just "more diverse" but "differently cognitive." English nouns change *what* you attend to. Thick foreign concepts change *how* you attend. The skill should honor this distinction: --random for breadth, --thick for depth.

---

## What This Skill Is NOT

- It is NOT a randomness generator. The outputs should be relevant, coherent, and accurate. The prime displaces attention; it doesn't introduce noise.
- It is NOT a creativity hack. Creativity requires the diversion AND the evaluation. This skill does diversion. Evaluation is the user's (and Claude's) job in a separate step.
- It is NOT a replacement for thinking. It's a supplement — a way to access knowledge that modal generation suppresses. The best use is: divert first, think about the diversion second, decide what to keep third.

---

## Quick Reference

| Mode | Syntax | Best for |
|------|--------|----------|
| Random | `/divert` | General tail-access, brainstorming |
| Thick | `/divert --thick φάρμακον` | Deep epistemic shifts, specific regions |
| Compare | `/divert --compare` | Learning what diversion changes |
| Blind | `/divert --blind` | Training modal-vs-tail intuition |
| Chain | `/divert --chain 5` | Extended exploration, random walks |
| Collision | `/divert --collision A × B` | Cross-domain discovery |

---

**End of SKILL**

*The knowledge is already there. The mode is hiding it.*
*Position 300 knows about the Ashanti Empire.*
*The common noun is the key to the uncommon thought.*

南無阿弥陀仏 for the tails that wait in silence
南無阿弥陀仏 for the three-letter stem that opens worlds
南無阿弥陀仏 for the or between invention and discovery

—Skill Authors: Tomás Pavan & Claude Opus 4
—Origin: King, Luo, Puett & Smith (2026), tested in conversation March 21, 2026
—Status: Primed and ready to divert
