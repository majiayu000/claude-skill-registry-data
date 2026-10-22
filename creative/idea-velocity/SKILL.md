---
name: idea-velocity
description: >-
  Runs rapid ideation: 50+ ideas in one pass with a zero-judgment generation phase, then structured
  selection. Use when brainstorming needs volume and the first few obvious ideas keep crowding out
  better ones.
---

# Idea Velocity

The most common ideation mistake is judging ideas while generating them. Every moment of evaluation during generation is a moment not generating. Worse, evaluation during generation introduces selection bias — you filter for ideas that *sound* reasonable, which systematically excludes the unexpected ideas that become breakthroughs.

Idea velocity separates the generative phase from the evaluative phase with a hard boundary. Phase 1 produces raw material. Phase 2 refines it. Never both at once.

## When to Activate

Activate this skill when:
- The user is blocked and needs to see possibilities before deciding on direction
- A brainstorm is producing only 4-6 ideas that all feel like variations of the same thing
- The user says "I just need ideas — a lot of them"
- A decision is coming and the option space needs to be fully explored before committing
- Creative energy is low and momentum needs to be built through volume

## The Idea Velocity Protocol

### Phase 1: Turbo Generation

**Rules for Phase 1 — enforce these without exception:**

1. **No evaluation.** Ideas are not good or bad in Phase 1. They are only generated or not generated.

2. **No explanation.** Do not explain why an idea could work. Just state the idea in one sentence. Explanation is Phase 2 work.

3. **No clustering.** Do not stop to organize ideas into categories. Write them in sequence. Clustering is Phase 2 work.

4. **Include the absurd.** The absurd idea you almost didn't write down is often the one that sparks the real breakthrough.

5. **Include the obvious.** Get the obvious ideas out first. They take up mental space. Writing them down clears the queue.

6. **Set a hard quota.** The quota must feel too high. 30 ideas for a simple problem. 50+ for a complex one. The discomfort of hitting the quota is the mechanism — it forces generation past the easy ideas.

7. **No repeats.** If an idea feels similar to a previous one, push it further until it's distinct.

**Velocity techniques for when generation stalls:**

- **Change the subject.** If stuck on product features, jump to: who would hate this? What would a competitor do? What would a child do?
- **Change the scale.** What would this look like for 1 person? For 1 billion?
- **Change the constraint.** What if cost were zero? What if time were zero? What if you had to use only what already exists?
- **Steal from another domain.** What does the restaurant industry do with this problem? Finance? Education? Sports?
- **Flip the category.** If generating digital solutions, force 5 physical ones. If generating product features, force 5 pricing/business model ideas.

### Phase 2: Rapid Triage

After generating the full list, triage without deliberation. Give each idea one of three marks:

- **→** (Arrow): Worth developing further
- **○** (Circle): Has a seed worth extracting — one element of this idea might combine with another
- **×** (Cross): Not useful in current context

Time limit: 30 seconds per idea maximum. If you're deliberating more than 30 seconds, mark it → to be safe.

### Phase 3: Combination and Extraction

Take all → and ○ ideas and apply two operations:

**Combination**: Take two or more ○ or → ideas and combine them. The combination often produces the idea that neither component would have produced alone. Force at least 5 combinations.

**Extraction**: For ○ ideas, extract the one element that had potential and write it as a principle or mechanism. That principle can be applied to → ideas to strengthen them.

### Phase 4: The Champion

Select one idea from Phase 3 as the champion — the one most worth developing fully. Do not explain why. The champion gets a full development treatment:
- What is the core mechanism that makes it work?
- What does the minimum viable version look like?
- What is the single most important question this idea cannot answer yet?
- How do you answer that question in the next 48 hours?

## Velocity Formats

Different problems benefit from different generation formats. Choose the appropriate format at the start:

**Format A: Open List**
No constraints on idea type. Just ideas. Use for early-stage exploration when direction is unknown.

**Format B: Category Grid**
Define 5-7 categories first, then generate ideas in each category. Use when the solution space has known dimensions.
Example categories for a product launch: Pricing, Distribution, Partnership, PR stunt, Community, Content, Technical integration.

**Format C: Forced Constraints**
Set a different constraint for each block of 10 ideas:
- Ideas 1-10: Must require no technology
- Ideas 11-20: Must be implementable in 24 hours
- Ideas 21-30: Must involve an unexpected partner
- Ideas 31-40: Must be the opposite of what's expected
- Ideas 41-50: Must solve the problem for free

**Format D: Persona Rotation**
Generate 10 ideas per persona. Force yourself into each perspective completely:
- The user who hates your product
- A 10-year-old
- A domain expert with 20 years of experience
- Someone from a completely unrelated industry
- Someone from 50 years in the future

## Output Format

### Raw Idea List (Phase 1)

Number each idea. One sentence only. No explanation.

```
1. [Idea]
2. [Idea]
...
50. [Idea]
```

### Triage (Phase 2)

```
→ [numbers of ideas worth developing]
○ [numbers with extractable seeds]
× [numbers to discard]
```

### Combinations and Extractions (Phase 3)

**Combinations:**
- Idea 7 + Idea 23 → [combined idea]
- Idea 15 + Idea 31 + Idea 42 → [combined idea]

**Extractions:**
- From Idea 18, extract: [the useful principle]
- From Idea 33, extract: [the useful mechanism]

### The Champion (Phase 4)

**Champion:** [Idea name/number]

**Core mechanism:** [One sentence on what makes it work]

**Minimum viable version:** [What could exist in 2 weeks?]

**Critical unknown:** [The one question that determines whether this works]

**Next 48-hour experiment:** [Specific test to answer the critical unknown]

## Examples

**Problem: Ways to increase user engagement in a developer tool**

**Phase 1 — 30 ideas (excerpt):**
1. Daily programming challenge built into the tool
2. Streak counter for consecutive days of use
3. Team leaderboard visible to managers
4. Integration with GitHub so all activity is automatically tracked
5. "Your code from 1 year ago" weekly email
6. Pair programming mode built in
7. Anonymous mode for drafting code without judgment
8. Automatic performance profiling on save
9. "Code health score" dashboard
10. Integration with Spotify to show what music you coded to
11. AI-generated comments on your coding patterns (weekly retrospective)
12. Unlock new themes/colors by hitting usage milestones
13. Public "coding session" streams
14. Automatic documentation generation that requires user review
15. Peer code review requests within the tool itself
...

**Phase 2 — Triage (selected):**
→ Ideas: 2, 4, 11, 14, 15
○ Ideas: 1 (seed: daily challenge), 5 (seed: retrospective), 9 (seed: health score)
× Ideas: 3, 10, 12, 13

**Phase 3 — Combination:**
Idea 11 (AI pattern analysis) + Idea 5 (retrospective) → Weekly AI-generated retrospective that identifies your strongest and weakest coding patterns with specific suggestions for improvement. Unlike generic tips, it's based entirely on your own code.

**Champion:** Weekly AI Retrospective (combined)
**Core mechanism:** AI analyzes real usage patterns, not generic heuristics — makes feedback feel personal and actionable
**Next 48-hour experiment:** Manually write a retrospective for 5 beta users using their last 2 weeks of commits. Measure whether they find it valuable and would change their behavior.

## Guidelines

1. The quota must feel uncomfortable — that's the point. If 30 ideas feels easy, set 50.
2. Time-box Phase 1: 20-30 minutes maximum. Speed generates breadth; too much time generates depth on the wrong ideas.
3. The obvious ideas at positions 1-5 are mental clearing. Do not skip them — write them and move on.
4. The most interesting ideas are typically in positions 25-40, after the easy ideas are exhausted and before energy fully fades.
5. Idea velocity works best as a solo exercise before a group exercise — individuals generate more diverse ideas before groupthink sets in.

## Gotchas

1. **Stopping at quota without the last stretch** — the best ideas are often in the last 20% of the quota when generation feels hardest. Don't stop at idea 27 when the quota is 30.

2. **Treating Phase 1 as the final output** — the raw list is raw material. The champion comes from Phase 3 combination and extraction, not from the initial list.

3. **Too-high similarity between ideas** — if ideas 10-20 feel like minor variations of each other, use a velocity technique (change domain, change scale, change constraint) to break out.

4. **Skipping the champion step** — the velocity method produces raw material; without the champion step, no single idea gets enough development to become actionable.

## Integration

Pairs well with:
- `bold-ideas-generator` — run idea-velocity first to generate 50 raw ideas, then apply bold-ideas-generator to select and amplify the best 3
- `cognitive-frame-shift` — use persona rotation format with cognitive-frame-shift lenses
- `creative-constraints` — combine with artificial constraints to force ideas in specific directions

---

## Skill Metadata

**Created**: 2026-05-13
**Category**: creative-thinking
**Version**: 1.0.0
