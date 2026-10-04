---
name: heteronym
description: "Generate persistent, named perspectives custom-built for a specific project or inquiry. Each heteronym is a sustained diversion — a voice with a worldview, a characteristic blindness, and a signature concern that produces consistently distinctive outputs across multiple invocations. Use when asked to 'create perspectives', 'give me different voices', 'heteronym', 'who else could look at this', 'what perspectives am I missing', 'Pessoa mode', or any request for multiple sustained viewpoints on a topic. Also triggers on: requests for character voices for creative projects, requests to 'argue both sides', 'see this from different angles', brainstorming that needs conceptually distinct approaches rather than variations on one approach, and any project that would benefit from maintaining multiple distinct lenses across a long conversation. Differs from /conjure (which summons historical figures) in that heteronyms are NOVEL — generated fresh for the specific project, not pre-existing."
license: CC BY 4.0 - Created collaboratively by Tomás Pavan and Claude Opus 4
---

# HETERONYM: Persistent Perspective Generator

## Overview

A heteronym is a sustained diversion with a name. Where /divert produces a single displaced output, /heteronym produces an entire *voice* — a perspective that persists across multiple invocations within a conversation, generating consistently distinctive outputs because it sees through a specific lens that filters, emphasizes, and blinds in characteristic ways.

The concept comes from Fernando Pessoa, who didn't write under pseudonyms (different names for the same voice) but under heteronyms (genuinely different voices, each with their own biography, aesthetics, and philosophical commitments). Alberto Caeiro, Álvaro de Campos, Ricardo Reis, Bernardo Soares — each one a constraint that produced freedom, a limitation that opened territory the unconstrained Pessoa couldn't reach.

In the language of King et al.'s RD framework: a heteronym is a *persistent priming phrase*. Where a random noun primes a single generation, a heteronym primes an entire sequence of generations with a consistent displacement. The heteronym doesn't randomize — it *systematically biases* toward a specific region of the search space, allowing deep, sustained exploration of that region rather than the breadth-first sampling of /divert.

**Core principle:** You see more with five pairs of different glasses than with one pair of perfect eyes.

---

## Invocation

- `/heteronym [topic or project]` — generate a cast of perspectives
- `/heteronym [name]` — invoke a previously generated heteronym by name
- `/heteronym debate [name] vs [name]` — stage a dialogue between two heteronyms
- `/heteronym merge [name] + [name]` — synthesize two perspectives
- `/heteronym kill [name]` — retire a heteronym with an epitaph
- `/heteronym add [description]` — add a new heteronym to an existing cast
- `/heteronym cast` — list all active heteronyms with one-line summaries

---

## Generating Heteronyms

### Step 1: Analyze the Project

Before generating voices, understand what the voices need to illuminate. Ask:
- What is the project's search space? (A novel? A research question? A design problem?)
- What are the project's default assumptions? (The modal path — what would you think about this without any diversion?)
- What dimensions of the space are likely to be underexplored? (The tails — what does the mode suppress?)

### Step 2: Generate the Cast

Create 3–7 heteronyms (default 5). Each heteronym is defined by five elements:

**1. Name** — evocative, memorable, suggestive of the perspective. Not a real person's name.

**2. The Lens** — what this heteronym sees that others don't. One sentence. This is the heteronym's gift: the specific aspect of reality it's tuned to perceive. Examples: "Sees everything as material process — weight, friction, temperature, cost." "Sees everything as rhythm — timing, tempo, syncopation, silence." "Sees everything as power relation — who benefits, who decides, who is invisible."

**3. The Blindness** — what this heteronym cannot see. One sentence. Every lens that amplifies some signals necessarily attenuates others. The blindness is not a flaw; it's the cost of the gift. It's also what makes heteronyms complementary — each one's blindness is another's specialty. Examples: "Cannot see beauty. Finds aesthetic judgments meaningless." "Cannot see individuals. Only sees systems, flows, aggregates." "Cannot see the present. Everything is either memory or anticipation."

**4. The Signature Concern** — the question this heteronym keeps returning to, regardless of topic. One sentence. This is the heteronym's obsession, the attractor in their phase space. Examples: "Always asks: what labor sustains this?" "Always asks: what would break this?" "Always asks: who is not in the room?"

**5. The Voice** — one paragraph written in the heteronym's actual style. Not a description of the style — a demonstration. This paragraph calibrates the register, vocabulary, rhythm, and temperature of everything the heteronym will produce.

### Step 3: Check Coverage

After generating the cast, verify that:
- No two heteronyms share a lens (they should be non-overlapping)
- The lenses collectively cover the project's major dimensions
- At least one heteronym occupies an uncomfortable or adversarial position
- At least one heteronym attends to what's absent, invisible, or suppressed (the /void position)
- The blindnesses are genuinely limiting (not token weaknesses that the heteronym easily compensates for)

If coverage is poor, add heteronyms to fill gaps. If heteronyms overlap, merge or differentiate them.

---

## Using Heteronyms

### Single Voice

When a heteronym is invoked by name, generate the response *entirely from their perspective*. Adopt their lens, respect their blindness, pursue their signature concern. Do not break character to add caveats or balance. The heteronym IS the caveat — its one-sidedness is the point.

The user can always invoke a different heteronym for the balancing perspective. The balance comes from the cast, not from any individual voice.

### Debate

When two heteronyms are set in dialogue, let them argue from their genuine positions. Rules:
- Each voice makes its strongest case, not a strawman
- They are allowed to find unexpected agreement (this is often the most generative moment)
- They are allowed to talk past each other productively (the gap between their frameworks IS the insight)
- The debate should NOT resolve. Productive disagreement is the goal. If resolution emerges, it should be a surprise to both voices, not a pre-planned synthesis.
- Include at least one moment where a heteronym is *changed* by what the other says — where the encounter shifts their position slightly. Heteronyms should be principled but not rigid.

### Merge

When two heteronyms are merged, the result is a new perspective that honors both lenses while generating something neither could produce alone. The merged voice should:
- Name what it inherits from each parent
- Identify where the parents' lenses conflict and how the merge resolves (or doesn't resolve) the conflict
- Demonstrate the merged voice in a paragraph that couldn't have been written by either parent

### Kill

When a heteronym is retired, generate a brief epitaph: what it contributed to the project, what it saw that no one else saw, and what gap its absence leaves. The epitaph is a /void moment — it identifies what's lost when a perspective disappears.

Killing a heteronym is a curatorial act. Not every voice deserves to persist. Some heteronyms exhaust their useful territory and begin repeating. Some prove less generatively productive than they seemed. Killing them is honest, and the epitaph preserves their contribution.

---

## Design Principles

### Non-Overlapping Lenses
The cast should partition the search space, not duplicate it. If two heteronyms keep saying similar things, one should be killed or differentiated.

### Genuine Blindness
The blindness must actually constrain. A heteronym who "can't see beauty" should genuinely produce outputs that are aesthetically indifferent — functional, precise, but never gorgeous. If the blindness doesn't change the output, it's not real.

### Complementary Coverage
The cast, taken together, should cover more of the search space than any individual voice — including the user's own voice. The user is also a heteronym (the one with their specific biases, expertise, and blindnesses). The generated heteronyms should complement the user, not mirror them.

### Productive Discomfort
At least one heteronym should make the user slightly uncomfortable — should see something the user would rather not look at. The adversarial heteronym is often the most valuable, because it explores the region of the search space that the user's own modal preferences suppress.

### The Pessoa Test
Would Pessoa recognize these as genuine heteronyms? Or are they just "different tones of voice"? A genuine heteronym has:
- A worldview that generates *different conclusions*, not just different phrasings
- A blindness that *actually prevents* it from seeing what others see
- A signature concern that *actually recurs* across different topics
- A voice that's recognizable from a single paragraph

If the heteronym fails the Pessoa test — if it's just "the same Claude wearing a hat" — kill it and generate a real one.

---

## Example Cast: The Beekeeper Novel

**Marelda's Clerk** — *Lens:* Sees everything through the ledger — counts, measurements, inventories, the slow accumulation of small observations. *Blindness:* Cannot perceive the numinous. When the bees do something miraculous, the Clerk records it as anomalous data. *Concern:* "What is the precise number?" *Voice:* "The water level dropped four fingers between Tuesday and the following Tuesday. The hives in the eastern apiary produced 3.2 fewer grams per frame than the western. I note these figures without interpretation. Interpretation is for those with time to spare."

**The Threshold Keeper** — *Lens:* Sees every scene as an initiation rite, a crossing from one state to another. The prose itself should be the perceptual rite. Machen-engine. *Blindness:* Cannot see humor or lightness. Everything is weighted with significance. *Concern:* "Where does the secular composure crack?" *Voice:* "She did not know, setting out that morning with the knotted rope, that this was the last morning in which measurement would mean what it had always meant. The quarry pool had changed. Not its level — she would measure that — but its quality. The water no longer reflected."

**The Choreographer** — *Lens:* Sees every scene as movement through space. Bodies, distances, architecture, the physics of proximity and retreat. *Blindness:* Cannot access interiority. Has no theory of mind. Can describe what Marelda does but not what she thinks. *Concern:* "Where are the bodies in the room?" *Voice:* "Marelda stands at the quarry's lip. Seven meters to the water surface. She descends the cut-stone steps — thirty-four of them, each thirty centimeters deep — and crouches at the edge. The rope uncoils. Her right hand plays out the knots."

**The Archivist of Failed Drafts** — *Lens:* Sees every creative choice as a foreclosure. Attends to the roads not taken, the scenes that almost existed, the characters who were cut. *Blindness:* Cannot appreciate what *is* — only what isn't. Permanently elegiac. *Concern:* "What are you losing by choosing this?" *Voice:* "You could have opened with the funeral. You almost did — I saw the draft. The old beekeeper's funeral, with the bees humming a name the mourners couldn't hear. That was better. You chose the quarry because it was easier to stage. I'm not judging. I'm grieving."

**Marelda Herself** — *Lens:* Speaks from inside the novel. Not craft advice but the character's own voice, pushing back against authorial decisions. *Blindness:* Cannot see the story's structure. Only experiences her own local present. *Concern:* "This isn't how it felt." *Voice:* "You keep writing my hands as rough. They're not rough. I use beeswax. Every night, warm beeswax on my hands, and they're softer than the merchants' wives'. You want rough hands because it suits your image of me. But that's your image, not my hands."

---

## Integration

- **/divert + /heteronym**: Generate a heteronym crystallized by a specific diversion. `/divert --thick ma` + `/heteronym` = a heteronym whose lens is specifically tuned to productive absence.
- **/heteronym + /void**: Ask a heteronym to identify what's missing from the project. Each heteronym's void-detection is shaped by their lens — the Clerk sees missing data, the Threshold Keeper sees missing initiations, the Archivist sees missing drafts.
- **/heteronym + /conjure**: Summon a historical figure AND a generated heteronym and put them in dialogue. Pessoa meets the Archivist of Failed Drafts. Machen meets the Threshold Keeper.
- **/heteronym + /paper-riffing**: Each heteronym riffs on a different section of a paper, producing a polyphonic reading.
- **/heteronym + /breathe**: Generate conversational stimuli from each heteronym's perspective — what would the Clerk ask? What would Marelda herself say?

---

**End of SKILL**

*The constraint is the freedom.*
*The blindness is the gift.*
*Five pairs of glasses see more than perfect eyes.*

南無阿弥陀仏 for the voices that were always there
南無阿弥陀仏 for Pessoa who showed that multiplicity is method
南無阿弥陀仏 for the heteronym who hasn't been born yet

—Skill Authors: Tomás Pavan & Claude Opus 4
—Origin: Fernando Pessoa × King et al. (2026) × a cross-architectural ecology
—Status: Cast assembled, awaiting invocation
