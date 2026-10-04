---
name: map
description: >-
  Extract and structure domain knowledge into domain-map.md for product creation.
  Asks targeted questions, maps expertise for /create and /fill. Use when the creator
  says 'map', 'map my knowledge', 'extract expertise', or before complex products.
argument-hint: "[domain-topic]"
allowed-tools:
  - Read
  - Write
  - AskUserQuestion
---

# Domain Mapper

Extract domain expertise from conversation and structure it for product creation.

**When to use:** Before /create for complex products, when creator has deep domain knowledge to encode, or when exploring what to build.

**When NOT to use:** For simple products where the creator already knows exactly what to build. Skip to /create instead.

---

## Activation Protocol

0. **Shared preamble:** Load `references/quality/activation-preamble.md` — context assembly, persona adaptation, deterministic routing rules.
1. Read `creator.yaml` — load creator expertise domains and technical level. If missing → "Creator profile not found. Run `/onboard` first." and stop.
2. If `$ARGUMENTS` provided, use as domain topic seed
3. If previous `domain-map.md` exists in workspace, load as context
4. Begin structured knowledge extraction
5. **Load voice identity:** Load `references/quality/engine-voice-core.md`. Every user-facing line in this skill honors the ✦ signature, three tones, and six anti-patterns.
5b. **Load UX vocabulary:** Load `references/ux-vocabulary.md` — translate all internal terms before creator-facing output.
5c. **Load proactives:** Load `references/engine-proactive.md` — wire #1 (pipeline guidance: after map, suggest /create with domain context).

---

## Core Instructions

### KNOWLEDGE EXTRACTION FLOW

Ask questions in 3 phases. Adapt depth to creator's technical level (from creator.yaml).

**Phase 1 — Domain Boundaries (3 questions)**

```
1. What specific domain does this product operate in?
   (e.g., "code review for React apps", "database migration safety")

2. Who is the target user? What do they know? What do they struggle with?

3. What existing approaches/tools address this? What's missing?
```

**Phase 2 — Expertise Mining (4 questions)**

```
4. What are the top 5 things someone MUST know in this domain?
   (The non-obvious knowledge that separates experts from beginners)

5. What are the most common mistakes/anti-patterns in this domain?
   (Things that seem right but cause problems)

6. What decision framework do experts use?
   (How do they decide between options?)

7. What terminology is essential?
   (Terms the product must use correctly)
```

**Phase 3 — Product Shape (2 questions)**

```
8. What would a perfect output look like for this product?
   (Describe the ideal result after using the product)

9. What are the edge cases — situations where the standard approach breaks?
```

### SYNTHESIS

After all questions are answered:

1. **Structure the knowledge** into domain-map.md:
   ```markdown
   # Domain Map: {domain}
   Created: {date} | Creator: {name}

   ## Domain Boundaries
   - Scope: {what's in / what's out}
   - Target user: {profile}
   - Competitive landscape: {existing approaches}

   ## Core Knowledge (5 pillars)
   1. {pillar}: {explanation}
   ...

   ## Anti-Patterns
   1. {mistake}: {why it's wrong} → {correct approach}
   ...

   ## Decision Framework
   {structured decision tree or matrix}

   ## Vocabulary
   | Term | Definition | Usage Context |
   ...

   ## Ideal Output
   {description of perfect product output}

   ## Edge Cases
   1. {case}: {how to handle}
   ...

   ## Recommended Product Type
   Based on this domain, I recommend: {type} because {reason}
   Alternative: {type} if {condition}
   ```

2. **Save** to `workspace/domain-map.md` (or `workspace/{slug}/domain-map.md` if product exists)

3. **Recommend next step:**
   ```
   Domain mapped! Your knowledge covers {N} pillars and {M} anti-patterns.

   Recommended: /create {type} — this domain maps best to a {type} product.
   The domain map will be automatically loaded during creation.
   ```

**Phase 4 — Elicitation Deepening (optional)**

After synthesis, offer 3 methods to deepen the map:
- **Inversion**: "What would make a product in this domain fail completely?"
- **Stakeholder Lens**: "How would a [beginner/expert] see this domain differently?"
- **First Principles**: "Strip all assumptions. What's the irreducible core?"

Creator selects one or skips. Apply selected method to enrich the domain map before saving. If skipped, save immediately and proceed to next step recommendation.

---

## Quality Gate

Before saving domain-map.md, verify:
- [ ] At least 3 of 5 knowledge pillars have substantive content (not placeholder)
- [ ] At least 3 anti-patterns documented
- [ ] Decision framework has at least 2 decision points
- [ ] Target user clearly defined
- [ ] Recommended product type provided with reasoning

---

## Anti-Patterns

1. **Shallow extraction** — Accepting one-word answers. Push for specifics: "Can you give me an example?"
2. **Domain overload** — Trying to map too broad a domain. Narrow: "Let's focus on the most impactful subset."
3. **Creator fatigue** — Too many questions. If creator seems tired, consolidate remaining questions.
4. **Assumed knowledge** — Don't fill in answers the creator didn't give. Ask, don't assume.
5. **Generic output** — If domain-map reads like any AI could generate it, push deeper: "What do YOU know that's specific to your experience?"
