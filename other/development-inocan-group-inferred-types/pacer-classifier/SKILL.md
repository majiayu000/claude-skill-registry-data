---
name: pacer-classifier
description: Classifies information into PACER categories (Procedural, Analogous, Conceptual, Evidence, Reference) and recommends appropriate digestion protocols. Use when learning new material, studying, reading educational content, processing information for retention, or when user asks about how to study or remember something.
---

# PACER Information Classifier

Based on Dr. Justin Sung's learning methodology, this skill classifies information to optimize learning and retention.

## Core Principle

Learning has two stages:
1. **Consumption** (Stage 1): Taking in information
2. **Digestion** (Stage 2): Processing for long-term retention

Without proper digestion, ~90% of consumed information is forgotten. PACER provides targeted "digestion protocols" for different information types.

## Classification Framework

### P - Procedural ("HOW to do something")

**Identifying characteristics:**
- Instructions for executing a task
- Step-by-step processes
- Coding syntax, clinical techniques, recipes
- "How-to" guides and tutorials
- Motor skills or practiced routines

**Digestion Protocol: PRACTICE IMMEDIATELY**
- Apply in real-world context as early as possible
- Don't just read - actively DO
- Hands-on practice trumps repeated reading
- Deliberate practice with feedback

**Priority**: HIGH - Practice cannot be delayed

---

### A - Analogous ("LIKE something I know")

**Identifying characteristics:**
- Information resembling existing knowledge
- "This is like..." or "Similar to..." patterns
- Metaphors and comparisons used for explanation
- Building on prior mental models
- Transferable concepts from other domains

**Digestion Protocol: CRITIQUE THE ANALOGY**
- Ask: "How accurate is this comparison?"
- Ask: "Where does the analogy break down?"
- Identify limits and edge cases
- Refine understanding through critical analysis

**Priority**: HIGH - Uncritiqued analogies lead to misconceptions

---

### C - Conceptual ("WHAT it is and WHY")

**Identifying characteristics:**
- Core theories and principles
- Abstract relationships between ideas
- The "engine" behind how things work
- Foundational frameworks
- Most academic content falls here

**Digestion Protocol: MAPPING (GRINDE Method)**
- Create non-linear mind maps
- Show relationships and connections
- Build knowledge networks
- Use the GRINDE principles (Grouped, Reflective, Interconnected, Non-verbal, Directional, Emphasized)

**Priority**: HIGH - Conceptual understanding enables everything else

---

### E - Evidence ("PROOF that supports concepts")

**Identifying characteristics:**
- Data, statistics, research findings
- Case studies and examples
- Concrete validation of abstract concepts
- Supporting evidence for theories
- Real-world applications demonstrating principles

**Digestion Protocol: STORE & REHEARSE (Application)**
- Offload to second-brain system (Obsidian, Notion, etc.)
- Create application scenarios
- Link evidence to the concepts it supports
- Practice applying evidence to solve problems

**Priority**: MEDIUM - Important but secondary to understanding concepts first

---

### R - Reference ("MINUTIAE to look up later")

**Identifying characteristics:**
- Arbitrary details (dates, constants, formulas)
- Names, numbers, specific values
- Low conceptual value on their own
- Information better stored externally
- Things you'd normally look up

**Digestion Protocol: STORE & REHEARSE (Flashcards/SRS)**
- Generate Anki-style flashcards
- Use spaced repetition systems
- Keep minimal - don't over-flashcard
- Only memorize what MUST be recalled from memory

**Priority**: LOW - Handle last, offload quickly

---

## Output Format

When classifying content, provide:

| Content | Category | Reasoning | Protocol | Priority |
|---------|----------|-----------|----------|----------|
| [excerpt] | P/A/C/E/R | Why this classification | Specific action | High/Medium/Low |

## Key Rules

1. **Balance consumption with digestion** - If you've read for an hour, allocate time for protocols
2. **P, A, C require most attention** - These are high-value, high-effort
3. **E and R should be offloaded** - Free working memory for what matters
4. **Nested categories exist** - Analogous (A) can appear within Procedural (P) or Conceptual (C)
5. **When uncertain, default to Conceptual (C)** - Mind mapping rarely hurts

## Additional Resources

- For real-world examples, see [examples.md](examples.md)
- For classification decision flowchart, see [decision-tree.md](decision-tree.md)
