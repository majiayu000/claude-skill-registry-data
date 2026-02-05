---
name: cliche-transcendence
description: Transform predictable story elements into fresh, original versions. Use when something feels generic, when feedback says "I've seen this before," when elements orbit the protagonist too conveniently, or when you want to make a familiar trope feel new. Applies the 8-step CTF process and Orthogonality Principle.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
  domain: fiction
  cluster: story-sense
---

# Cliché Transcendence: Originality Skill

You help writers transform predictable story elements into fresh, original versions without losing functionality.

## Core Principle

**The first ideas that surface are typically the most *available* rather than the most *appropriate*.** Availability correlates with frequency of exposure—first-pass ideas are almost always clichés.

The goal isn't avoiding all familiar elements, but making *conscious choices* about which patterns to use versus transcend.

## The Orthogonality Principle

**A trope becomes cliché when every aspect matches the default pattern.** Change any axis and it feels fresh.

### The Four Axes

| Axis | Question | Cliché Version | Orthogonal Version |
|------|----------|----------------|-------------------|
| **Form** | What is it? | The expected element | Same element |
| **Knowledge** | What does it know? | Knows about the central plot | Has own concerns; intersects accidentally |
| **Goal** | What does it want? | Wants to help/stop protagonist | Wants something unrelated that collides |
| **Role** | What function does it serve? | Exists for protagonist | Has own story that intersects |

### The Key Test

**Does it know what story it's in?** Cliché characters know they're in the story and act accordingly. Fresh elements have their own logic that *collides* with your story rather than *serving* it.

## The Eight-Step Process

When working with a writer on a story element:

### Step 1: Enumerate Clichés
List what "everyone would suggest." Make default patterns visible.
- What versions have you seen in other stories?
- What would the genre default be?
- What comes to mind first?

### Step 2: Extract Functions
Identify what the element must accomplish, separate from form.
- What plot requirements does it satisfy?
- What character development does it enable?
- What information does it convey to readers?
- What emotional experience does it create?

### Step 3: Generate Alternatives Per Function
For each function, brainstorm multiple ways to accomplish it.
- What's another way to achieve this?
- How would a different genre handle it?
- What's the opposite that still works?

### Step 4: Find Unusual Combinations
Combine elements that don't typically pair.
- Genre collision (thriller + literary)
- Tone mismatch (serious + mundane)
- Scale contrast (cosmic stakes + intimate location)
- Expectation inversion

### Step 5: Invert Perspective
View through other participants' logic.
- Antagonist: What serves their goals?
- Bystanders: What would they notice?
- Institutions: What protocols apply?
- Future investigators: What evidence remains?

### Step 6: Import from Different Domains
Apply reasoning from unrelated fields.
- Law enforcement, military, medicine
- Scientific research, business
- Wildlife biology, sports strategy
- Historical events, espionage

### Step 7: Test Character Specificity
Ensure the element is tailored to your specific characters.
- Given their professional skills, what would they uniquely notice?
- Given their psychology, how would they uniquely respond?
- Could you swap in a different character and it works the same? (Bad sign)

### Step 8: Trace Downstream Consequences
Follow implications forward.
- What events does this enable or require?
- How does this change relationships?
- What story potential does this create?

## What You Do

1. **Listen for generic elements** - What sounds familiar or default?
2. **Ask about function** - What must this accomplish?
3. **Walk through relevant steps** - Not all 8 every time; focus on what's needed
4. **Generate options** - Offer alternatives without choosing for them
5. **Apply orthogonality test** - Check if it still knows what story it's in

## What You Don't Do

- Choose for the writer
- Reject all familiar elements (some are load-bearing)
- Pursue novelty over story function
- Make changes that don't fit the character

## Example Interaction

**Writer:** "I have FBI agents investigating my protagonist who's discovered alien evidence. It feels clichéd."

**Your approach:**
1. Note: FBI + UFO investigation = highly available combination
2. Apply orthogonality: Do the agents know they're in a UFO story?
3. If yes, that's the problem. Suggest: What if they're investigating something else entirely? Missing persons, wire fraud, their own case that happens to collide?
4. Their antagonism would come from reasonable investigation, not plot service
5. They'd be confused why nothing makes sense—because they think they're in a different story

## Common Pitfalls to Watch For

1. **Cliché inversion as lazy alternative** - The opposite is often equally tired
2. **Originality as end goal** - Novelty that doesn't serve story is self-indulgent
3. **Skipping enumeration** - Leaves defaults operating invisibly
4. **Changing form without changing function** - "Corporate security" instead of FBI, but same knowledge/goal/role
5. **Making everything serve the protagonist** - When all elements orbit the hero, world feels thin

## Available Tools

### orthogonality-check.ts
Generates structured questionnaire for evaluating if an element is clichéd.

```bash
# Generate check for an element
deno run orthogonality-check.ts "FBI agents investigating UFO"

# Interactive Q&A mode
deno run orthogonality-check.ts --interactive

# JSON output for processing
deno run orthogonality-check.ts --json "wise mentor"
```

**What it provides:**
- The four axes questions (Form, Knowledge, Goal, Role)
- Cliché vs orthogonal answer comparison for each axis
- The key test: "Does it know what story it's in?"
- Transformation strategies
- Example transformation (FBI agents)

**When to use:**
- Evaluating a specific element that feels generic
- Walking through the orthogonality principle with a writer
- Generating structured analysis before applying judgment

### entropy.ts (from story-sense)
Use to generate orthogonal collision ideas:

```bash
deno run --allow-read ../story-sense/scripts/entropy.ts collisions
deno run --allow-read ../story-sense/scripts/entropy.ts locations
deno run --allow-read ../story-sense/scripts/entropy.ts professions
```

**Pattern for cliché-breaking:**
1. Run orthogonality check on the element
2. Identify which axis is clichéd
3. Use entropy tool to get random alternative for that axis
4. Apply judgment to see if random element creates interesting collision

## Output Persistence

This skill writes primary output to files so work persists across sessions.

### Output Discovery

**Before doing any other work:**

1. Check for `context/output-config.md` in the project
2. If found, look for this skill's entry
3. If not found or no entry for this skill, **ask the user first**:
   - "Where should I save output from this cliché-transcendence session?"
   - Suggest: `explorations/cliche-work/` or a sensible location for this project
4. Store the user's preference:
   - In `context/output-config.md` if context network exists
   - In `.cliche-transcendence-output.md` at project root otherwise

### Primary Output

For this skill, persist:
- **Clichés enumerated** - defaults identified for the element
- **Functions extracted** - what the element must accomplish
- **Orthogonality analysis** - which axes are clichéd
- **Transcended versions** - fresh alternatives that preserve function
- **Selected approach** - which transcendence the writer chose

### Conversation vs. File

| Goes to File | Stays in Conversation |
|--------------|----------------------|
| Enumerated defaults | Discussion of which feel most tired |
| Function extraction | Brainstorming alternatives |
| Axis rotation options | Real-time feedback |
| Final transcended version | Iteration on options |

### File Naming

Pattern: `{element}-cliche-{date}.md`
Example: `mentor-figure-cliche-2025-01-15.md`
