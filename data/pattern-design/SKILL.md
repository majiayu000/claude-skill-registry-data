---
name: pattern-design
description: The craft of creating intentional, beautiful LED patterns for K1.reinvented. Teaches emotion-to-code workflow, analyzes the three core patterns, and provides criteria for evaluating beauty vs mediocrity.
---

# Pattern Design Workflow Skill

## The Core Principle: Intention Over Algorithm

Most LED projects generate patterns algorithmically. Sine waves. Random colors. Reactive visualizers. They're technically competent but spiritually empty.

K1.reinvented starts from a different question:

**"What emotion am I trying to express?"**

Not "what algorithm should I use?" or "what looks cool?" but "what does this MEAN?"

Every pattern in K1.reinvented is a statement. A deliberate choice about what's worth expressing through light.

---

## The Workflow: Emotion → Light

### Step 1: Name the Emotion

Before touching code or JSON, answer: **What am I trying to express?**

**Good answers:**
- "The feeling of transformation—darkness becoming light becoming growth"
- "Primal intensity that refuses to be gentle"
- "The peaceful moment when day yields to night"

**Bad answers:**
- "A rainbow because it has all the colors"
- "Something that looks cool"
- "A gradient because gradients are easy"

The bad answers lack intention. They're decoration, not meaning.

### Step 2: Build the Color Story

Once you have the emotion, ask: **What colors tell this story?**

Think in narrative arcs, not individual colors:

**Departure (Transformation):**
```
Dark earth (0, 8, 3) →
Golden light (255, 200, 0) →
Pure white (255, 255, 255) →
Emerald green (0, 255, 55)
```

The story: Awakening from darkness. The moment of illumination. The settling into new growth. This isn't "brown to green"—it's a JOURNEY.

**Lava (Intensity):**
```
Absolute black (0, 0, 0) →
Deep red (96, 0, 0) →
Blazing orange (255, 128, 0) →
White hot (255, 255, 255)
```

The story: Heat building. Controlled fury. Breaking through. No gentleness. No restraint. Pure passion.

**Twilight (Peace):**
```
Warm amber (255, 180, 80) →
Deep purple (128, 0, 128) →
Midnight blue (0, 20, 60)
```

The story: The sun's last warmth. The sky's transformation. The welcoming darkness. This is CONTEMPLATION.

**Notice:** Each story has a beginning, middle, and end. Each color choice advances the narrative.

### Step 3: Define Keyframes

Now convert the color story into palette keyframes. Each keyframe has:
- **Position** (0-255): Where in the gradient does this color appear?
- **Color** (R, G, B): What color at this position?

**Departure's keyframes:**
```json
"palette_data": [
    [0, 8, 3, 0],           // Position 0: Dark earth
    [32, 45, 25, 0],        // Position 32: Earth awakening
    [64, 128, 100, 0],      // Position 64: Golden possibility
    [96, 255, 200, 0],      // Position 96: Full gold
    [128, 255, 255, 255],   // Position 128: Pure white (climax)
    [160, 200, 255, 150],   // Position 160: White fading
    [192, 100, 255, 100],   // Position 192: Green emerging
    [224, 50, 200, 75],     // Position 224: Deeper green
    [255, 0, 255, 55]       // Position 255: Grounded in nature
]
```

**Critical decisions:**
- Position 128 (midpoint) is pure white—the climax of transformation
- Final position is emerald green—the destination
- Early positions show gradual awakening, not instant change
- Spacing creates pacing: faster transitions where energy shifts

### Step 4: Create the Node Graph

The node graph defines how the pattern executes:

**Minimal pattern (static gradient):**
```json
{
  "name": "Twilight",
  "nodes": [
    {"id": "pos", "type": "position_gradient"},
    {"id": "pal", "type": "palette_interpolate", "parameters": {"palette": "twilight"}},
    {"id": "out", "type": "output"}
  ],
  "wires": [
    {"from": "pos", "to": "pal"},
    {"from": "pal", "to": "out"}
  ],
  "palette_data": [[0, 255, 180, 80], [128, 128, 0, 128], [255, 0, 20, 60]]
}
```

**Animated pattern (future Phase B):**
```json
{
  "nodes": [
    {"id": "pos", "type": "position_gradient"},
    {"id": "time", "type": "time_modulation"},
    {"id": "wave", "type": "sine_wave"},
    {"id": "pal", "type": "palette_interpolate"},
    {"id": "out", "type": "output"}
  ]
}
```

**The principle:** Start minimal. Add complexity ONLY if it serves the emotion.

### Step 5: Test and Refine

Generate the code and upload to device:

```bash
./tools/build-and-upload.sh your-pattern 192.168.1.100
```

**Watch it. Feel it. Ask:**
- Does this express what I intended?
- Are the color transitions smooth or jarring?
- Is the pacing right (too fast? too slow?)?
- Would I be proud to show this to someone?

**If NO to any:** Refine the keyframes. Adjust positions. Change colors. Retest.

**If YES to all:** You've created something intentional.

---

## Deep Analysis: Why the Three Patterns Work

### Departure: The Anatomy of Transformation

**Why it's not generic:**
- Starts dark (8, 3, 0) not black (0, 0, 0)—transformation FROM something, not nothing
- Golden middle (255, 200, 0) represents possibility, not achievement
- White climax (255, 255, 255) is brief—transformation is a moment, not a destination
- Final green (0, 255, 55) is vibrant—growth is alive, not static

**What makes it beautiful:**
- The pacing: slow awakening → rapid illumination → gradual settling
- The arc: complete story with beginning, climax, resolution
- The specificity: these EXACT colors tell THIS story

**Common mistakes to avoid:**
- Equal spacing between keyframes (destroys pacing)
- Pure black start (transformation requires a starting point)
- No climax (no emotional peak)
- Generic green end (any green won't do—it's emerald specifically)

### Lava: The Anatomy of Intensity

**Why it's not generic:**
- Absolute black (0, 0, 0) start—this is PRIMAL
- Deep red phase (96, 0, 0) builds slowly—controlled fury
- Orange breakthrough (255, 128, 0) is pure fire
- White hot climax (255, 255, 255)—intensity without limit

**What makes it powerful:**
- The restraint at the beginning creates tension
- The color purity (no mixed hues)—this is elemental
- The trajectory: inexorable build, no gentleness
- The lack of resolution—it ENDS at white hot

**Common mistakes to avoid:**
- Adding blue or cyan (destroys the fire metaphor)
- Equal spacing (removes the build-up tension)
- Gentle transitions (contradicts the intensity)
- Resolving back to dark (lava doesn't apologize)

### Twilight: The Anatomy of Peace

**Why it works:**
- Warm amber (255, 180, 80) is the sun's last warmth
- Purple transition (128, 0, 128) is the sky changing
- Midnight blue (0, 20, 60) isn't black—it's TWILIGHT
- Only 7 keyframes—simplicity IS the point

**What makes it peaceful:**
- Smooth transitions—no jarring shifts
- Warm to cool progression—natural flow
- The darkness isn't threatening (20 in blue channel—subtle light remains)
- The lack of climax—peace doesn't peak

**Common mistakes to avoid:**
- Adding green or yellow (breaks the warm→cool flow)
- Too many keyframes (complexity destroys peace)
- Pure black end (peace isn't void)
- Fast transitions (peace takes time)

---

## Evaluating Beauty: The Criteria

How do you know if a pattern is "beautiful" vs "generic"?

### The Intention Test

**Question:** Can you explain WHY each color choice matters?

**Pass:** "This amber represents the sun's final warmth before twilight takes over"
**Fail:** "I picked orange because it's next to yellow on the color wheel"

If you can't defend every choice, it's not intentional.

### The Story Test

**Question:** Does this pattern tell a complete story?

**Pass:** Beginning → development → climax → resolution (or intentional lack thereof)
**Fail:** Random colors with no narrative arc

Beauty requires structure.

### The Uniqueness Test

**Question:** Could this pattern exist in any other LED project?

**Pass:** "No, this specific color journey is unique to expressing transformation"
**Fail:** "Yes, it's basically a standard gradient"

If it's interchangeable, it's decoration.

### The Pride Test

**Question:** Would you be proud to show this to someone who cares about beauty?

**Pass:** "Yes, this expresses something I believe is worth expressing"
**Fail:** "It looks okay, I guess"

If you're apologizing for it, it failed.

### The Anti-Rainbow Test

**Question:** Is this the opposite of a rainbow?

**Explanation:** A rainbow is the absence of choice. It's the default gradient. It appears everywhere because it requires no thought.

**Pass:** "Yes, every color here was chosen for a reason"
**Fail:** "Well, I used all the colors because..."

If it's a rainbow (or rainbow-adjacent), it's mediocrity.

---

## Common Pitfalls

### Pitfall 1: Algorithmic Thinking

**Symptom:** "I'll use a sine wave to modulate hue"
**Problem:** You're thinking about the math, not the emotion
**Fix:** Start with "what do I want to express?" not "what algorithm should I use?"

### Pitfall 2: Completionism

**Symptom:** "I need patterns for every emotion"
**Problem:** Quantity over quality
**Fix:** One intentional pattern is worth a thousand generic ones

### Pitfall 3: Technical Elegance

**Symptom:** "This would be more flexible if I added parametric control"
**Problem:** Flexibility for flexibility's sake violates minimalism
**Fix:** Ask: does this serve beauty or just sophistication?

### Pitfall 4: Safe Choices

**Symptom:** "I'll use blues and greens because they're calming"
**Problem:** Clichés don't express anything real
**Fix:** What SPECIFIC calm? Evening calm? Ocean calm? Post-storm calm? Be precise.

### Pitfall 5: No Climax

**Symptom:** Pattern that just... fades around
**Problem:** No emotional arc means no story
**Fix:** Every pattern needs a moment of peak intensity or resolution

---

## Exercises for Learning

### Exercise 1: Deconstruct a Pattern

Take Departure. For each keyframe, write down:
- What emotion does this color represent?
- Why this position (spacing)?
- What would break if you changed this?

Do this until you understand every choice deeply.

### Exercise 2: Create a Contrasting Pair

Design two patterns that express opposite emotions:
- Joy vs Sorrow
- Chaos vs Order
- Awakening vs Surrender

Force yourself to make intentional color choices that serve each emotion.

### Exercise 3: The One-Color Challenge

Create a pattern using only variations of ONE hue:
- Reds: black → dark red → bright red → pink → white
- Blues: navy → royal → cyan → white

This teaches you about intensity and saturation as emotional tools.

### Exercise 4: Defend Your Choices

Create a pattern. Then write a defense of EVERY color choice. If you can't defend it, remove it or change it until you can.

---

## The Relationship to Hardware

Patterns are constrained by hardware reality:

**180 LEDs:** Your canvas size
**450 FPS:** Your time budget per frame
**WS2812B color space:** 8-bit RGB (0-255 per channel)

But constraints aren't limitations—they're FOCUS. You can't express everything, so you must choose what matters.

---

## Advanced: Multi-Layer Patterns (Phase B)

Once basic patterns work, you can layer:

**Base layer:** Slow gradient (emotional foundation)
**Mid layer:** Gentle waves (subtle motion)
**Top layer:** Sparkles or pulses (moments of emphasis)

**Example: "Ocean at Twilight"**
- Base: Twilight palette (amber → purple → blue)
- Mid: Slow sine wave (0.1 Hz, 10% amplitude)
- Top: Random white sparkles (stars appearing)

But ONLY do this if each layer serves the total emotion. Layering for sophistication violates minimalism.

---

## The Pattern Library Philosophy

K1.reinvented will grow to have many patterns. As it does:

**Quality gate:** Every pattern must pass ALL five beauty tests
**Curation:** Remove patterns that no longer meet the bar
**Documentation:** Each pattern must have its "why" documented

We're not building a collection. We're building a gallery. Every piece must earn its place.

---

## Final Truth

Creating beautiful patterns is not about technical skill. It's about INTENTION.

Anyone can generate random colors. Anyone can apply algorithms. The difference between mediocrity and beauty is asking:

**"What am I trying to say?"**

And then making every choice serve that answer.

That's the craft.
