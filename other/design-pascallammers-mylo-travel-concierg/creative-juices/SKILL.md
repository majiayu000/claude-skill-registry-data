---
name: Creative Juices
description: Provides creative thinking prompts using concrete metaphors, dramatic scenarios, and strategic frameworks. Use when the user needs inspiration, is stuck on a problem, or wants to validate ideas from first principles.
---

# Creative Juices

Help users think creatively by providing unexpected metaphorical prompts and strategic questions.

## When to Use This Skill

Use this skill when:
- User needs inspiration or fresh perspectives
- User is stuck on a design, feature, or creative problem
- User wants to validate assumptions or reality-check ideas
- User asks for "creative thinking" or "thinking outside the box"
- User is in brainstorming mode

## Three Creative Modes

### 1. Gentle Inspiration (`get_inspiration`)

**Use at the start** of creative or problem-solving tasks to frame challenges in unexpected ways.

**Implementation:**

1. Select 3 random verbs from the "inspiring" category in `word_lists.md`
2. Select 3 random nouns from the "inspiring" category in `word_lists.md`
3. Pair each verb with a noun (e.g., "painting-shoe", "baking-door")
4. Present the sparks with this instruction: "Use these unexpected combinations as initial lenses:"

**Word categories to use:**
- **Verbs**: Human actions (painting, baking, melting), animal behaviors (flying, nesting), natural phenomena (rain, tree), primitive tools, ancient crafts, digital actions
- **Nouns**: Everyday objects (shoe, door, spoon), animal structures (nest, web), natural elements, comfort items, primitive tools

**Example output:**
```
Creative sparks to reframe your challenge:
- baking-door
- folding-mirror
- watering-clock

Use these unexpected combinations as initial lenses to see your problem differently.
```

**Why this works:** Concrete everyday metaphors create gentle cognitive distance, encouraging fresh perspectives without overwhelming the thinking process.

### 2. Dramatic Shock (`think_outside_the_box`)

**Use mid-conversation** when exploration has stalled or thinking has become too linear.

**Implementation:**

1. Select 3 random verbs from the "out_of_the_box" category in `word_lists.md`
2. Select 3 random nouns from the "out_of_the_box" category in `word_lists.md`
3. Pair each verb with a noun (e.g., "crushing-fire", "teleporting-plasma")
4. Present the sparks with this instruction: "Shatter your assumptions with these:"

**Word categories to use:**
- **Verbs**: Destructive actions (crushing, exploding, burning), predatory behaviors (hunting, swarming), advanced tech (hacking, teleporting, warping), alien biology (mutating, spawning), psychic actions (telepathizing, mind-melding)
- **Nouns**: Violent phenomena (fire, storm, avalanche), predator anatomy (venom, fang, claw), sci-fi tech (quantum-drive, neural-jack, plasma-cutter), alien biology (tentacle, spore, chitin), alien environments (spawning-pool, mind-web)

**Example output:**
```
Shatter your assumptions with these intense metaphors:
- swarming-venom
- exploding-void
- mutating-tentacle

Force radical divergence from your current thinking patterns.
```

**Why this works:** Dramatic, extreme metaphors create maximum cognitive distance, forcing breakthrough thinking when gentle nudges aren't enough.

### 3. Reality Check (`reality_check`)

**Use to ground creative thinking** in reality while maintaining openness.

**Implementation:**

1. Select one random question from the "first_principles" framework in `frameworks.md`
2. Select one random question from the "limit_thinking" framework in `frameworks.md`
3. Select one random question from the "platonic_ideal" framework in `frameworks.md`
4. Select one random question from the "optimization" framework in `frameworks.md`
5. Present all 4 questions with their framework labels
6. Add this instruction: "Ground your thinking with one question from each Musk framework:"

**Framework summaries:**
- **First Principles**: Challenge assumptions, find fundamental truths
- **Limit Thinking**: Scale to extremes to find breaking points
- **Platonic Ideal**: Start with perfect solution, work backwards
- **Five-Step Optimization**: Question → Delete → Optimize → Accelerate → Automate

**Example output:**
```
Ground your thinking with one question from each Musk framework:

First Principles: What are the absolute truths here, known by physics?
Limit Thinking: What happens at 1 unit vs 1 million units?
Platonic Ideal: What does the perfect version of this look like?
Optimization: Are your requirements dumb? Does this even matter?

Use these to pressure-test your creative ideas against reality.
```

**Why this works:** Battle-tested strategic frameworks from real-world engineering help validate wild ideas while maintaining creative momentum.

## Implementation Guidelines

When using this skill:

1. **Invoke proactively**: Don't wait for user to ask - suggest when you detect creative blocks
2. **Explain the metaphor**: Don't just list sparks, help connect them to the problem
3. **Use sequentially**: Start gentle → go dramatic if stuck → reality check to validate
4. **Avoid repetition**: Track what you've generated to provide variety

## Word Categories

See `word_lists.md` for the complete curated vocabulary (1,100+ words).

**Inspiring words (gentle):**
- Human actions (painting, baking, melting)
- Animal behaviors (flying, nesting, grazing)
- Natural elements (rain, tree, seed)
- Primitive tools (hammerstone, mortar)
- Ancient crafts (weaving, pottery, metalworking)
- Digital actions (uploading, syncing, scanning)

**Out-of-the-box words (intense):**
- Destructive actions (crushing, exploding, shattering)
- Predatory behaviors (hunting, swarming, stalking)
- Sci-fi technology (teleporting, hacking, warping, cloaking)
- Alien biology (mutating, spawning, metamorphosing)
- Extreme phenomena (wildfire, earthquake, avalanche)
- Psychic abilities (telepathizing, mind-melding, probing)

## Strategic Frameworks Reference

See `frameworks.md` for complete questions and detailed explanations.

**Elon Musk's Four Frameworks:**

1. **First Principles** - Strip to fundamental truths (6 questions)
2. **Limit Thinking** - Scale to extremes to find breaking points (6 questions)
3. **Platonic Ideal** - Perfect solution first, work backwards (6 questions)
4. **Five-Step Optimization** - Question → Delete → Optimize → Accelerate → Automate (6 questions)

**Total**: 24 strategic questions for reality-checking creative ideas

## Design Philosophy

- **Concrete over abstract**: "baking-shoe" beats "crystallize-entropy"
- **Larger conceptual gap = stronger creative effect**: Force genuine metaphorical thinking
- **Historical span**: Primitive → ancient → modern → futuristic for maximum range
- **Balanced intensity**: Match metaphor intensity to creative stage

## Supporting Resources

- **`word_lists.md`** - Complete curated word vocabulary organized by category and intensity
- **`frameworks.md`** - Full strategic framework questions with examples and application guidance
- **`examples.md`** - Real-world usage patterns and complete creative process walkthroughs
