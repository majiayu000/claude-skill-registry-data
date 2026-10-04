---
name: quest
description: "Sustained search quest — iterative exploration of ill-defined problems with coverage tracking, where the journey maps the space and the user discovers what they want."
---

# Quest

*The search quest as structured practice — discover what you want by exploring what exists*

Inspired by Luo, King, Puett & Smith (2025), "Inducing Sustained Creativity and Diversity in Large Language Models." The paper formalizes the **search quest**: a problem where (1) the goal is ill-defined at the outset, (2) finding the right answer matters deeply, and (3) the user discovers their preferences *through* the exploration itself. Research topics, names, design directions, metaphors, career moves — these aren't queries with answers, they're quests with destinations you recognize only upon arrival.

Standard LLM interactions fail search quests because they converge too fast. You get the modal answer, rephrase, get a slight variation, give up. The quest skill maintains **state across rounds** — tracking what's been explored, what the user reacted to, and actively steering toward unexplored territory.

---

## When to Invoke

- "I need a research topic but I don't know what area yet"
- "Help me find a name for X"
- "What should my next project be?"
- "I want an angle on this paper but everything feels obvious"
- Any problem where the user says "I'll know it when I see it"
- Exploratory literature review — mapping a field before committing to a direction

---

## The Quest Loop

```
                    ┌─────────────────┐
                    │   User states   │
                    │   vague goal    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Generate wave  │◄──── /recode perturbation
                    │  (5-8 diverse   │      (or manual strategies)
                    │   candidates)   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  User reacts    │
                    │  with gestures  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Update map:    │
                    │  - warm zones   │
                    │  - cold zones   │
                    │  - unexplored   │
                    └────────┬────────┘
                             │
                   ┌─────────▼─────────┐
                   │  Next wave:       │
                   │  70% near warm    │
                   │  30% forced       │──── exploration budget
                   │  exploration      │     (keeps diversity alive)
                   └─────────┬─────────┘
                             │
                    ┌────────▼────────┐
                    │ User: "this is  │
                    │ it" or "enough" │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Output: final  │
                    │  choice + map   │
                    └─────────────────┘
```

---

## How to Use

### Phase 1: Opening

The user states a vague goal. Don't ask them to be more specific — that defeats the purpose. A search quest starts vague by definition.

**Good quest openers:**
- "Research topics at the intersection of X and Y"
- "A name for my project about Z"
- "Angles for a paper on W"
- "What should I work on next?"

**Claude's first move:**
1. Generate 5-8 candidates using `/recode`-style perturbation
2. Present them as a **numbered list with brief descriptions**
3. Explicitly invite gestural reactions (see below)

### Phase 2: Gestural Reactions

The user reacts NOT with scores or rankings but with **qualitative gestures**:

| Gesture | Meaning | Effect on next wave |
|---------|---------|---------------------|
| "warmer" / "yes" / "more like this" | This direction is promising | Explore nearby in semantic space |
| "colder" / "no" / "boring" | This direction is dead | Mark zone as explored-and-rejected |
| "interesting but wrong" | The CONCEPT is promising but the EXECUTION is off | Vary the execution, keep the concept |
| "too obvious" | Modal response detected | Push harder into the tails |
| "too wild" | Perturbation overshot | Pull back toward the warm zone |
| "what else?" | Nothing resonated | Inject entirely new perturbation strategies |
| "combine 3 and 7" | Synthesis | Generate hybrids of the indicated candidates |
| "this is it" | Quest complete | Finalize and output the map |

### Phase 3: Coverage Map Maintenance

After each round, internally maintain a coverage map:

```yaml
quest: "research topics in computational neuroscience"
round: 3
clusters_explored:
  - label: "neural oscillation models"
    reaction: warm
    round_introduced: 1
    exemplars: ["gamma-band binding", "theta-phase coding"]
  - label: "connectomics"
    reaction: cold
    round_introduced: 1
    exemplars: ["whole-brain mapping"]
  - label: "neuro-symbolic integration"
    reaction: interesting-but-wrong
    round_introduced: 2
    exemplars: ["neural theorem provers"]
    note: "likes the hybrid idea, not the specific execution"
  - label: "ethnomathematics of cognition"
    reaction: warm
    round_introduced: 2
    exemplars: ["non-Western models of number sense"]
unexplored_regions:
  - "embodied/enactive approaches"
  - "clinical/pathological angle"
  - "historical/philosophical framing"
warm_zone_centroid: "hybrid formal-biological models with cultural dimension"
```

### Phase 4: Wave Generation

Each subsequent wave:

1. **70% exploitation** — Generate candidates near the warm zone, exploring variations and combinations of what the user responded to
2. **30% forced exploration** — Generate candidates from unexplored regions, using fresh perturbation strategies that haven't been tried

This 70/30 split is the **sustained creativity mechanism**. Without the exploration budget, the quest converges prematurely. Without the exploitation, it wanders aimlessly. The paper's Figure 4(b.2) shows RD maintains distance from prior clusters even at run 1000 — this is the mechanism that achieves that.

### Phase 5: Closing

When the user says "this is it" or "I've seen enough":

1. Present their final choice
2. Output the **full coverage map** — everything explored, with reactions
3. Save the map as an artifact: `output/quest-[topic]-[date].md`
4. Optionally: list the "roads not taken" — promising directions that were explored but not chosen, for future reference

---

## Output Format

### Each Wave

```
## Quest: [topic] — Wave [N]

### Candidates

1. **[Idea]** — [one-line description]
2. **[Idea]** — [one-line description]
...

### Coverage so far
- Explored: [N] clusters across [M] waves
- Warm zones: [brief description of what's resonating]
- Unexplored: [regions not yet touched]

*React with gestures: warmer/colder/interesting-but-wrong/too obvious/too wild/combine N+M/this is it*
```

### Final Output

```
## Quest Complete: [topic]

### The Choice
[What the user selected, with full description]

### The Journey
[Brief narrative of how the quest unfolded — what was tried, what resonated, what surprised]

### Coverage Map
[Full map of explored territory with reactions]

### Roads Not Taken
[Promising directions that were explored but not chosen]
```

---

## Design Principles

1. **Don't converge too fast.** The 30% exploration budget exists for a reason — the best answer might be in a region you haven't visited yet.

2. **Gestures, not scores.** Numerical ratings collapse rich reactions into thin signals. "Interesting but wrong" carries more information than "6/10."

3. **The map IS the product.** Even if the user doesn't find "the one," they've learned what the space looks like. That's valuable. Save the map.

4. **Respect the vagueness.** Don't ask the user to be more specific at the start. The whole point is that they discover specificity through exploration.

5. **Track what's been tried.** Never repeat a cluster. If the user says "what else?" and you generate something they've already seen, the quest has failed.

---

## Relationship to Other Skills

| Skill | Relationship |
|-------|-------------|
| `/recode` | Quest uses recode as its generation engine for each wave |
| `/anti-hivemind` | Can invoke anti-hivemind mid-quest to check if warm-zone ideas are hivemind-modal |
| `/brainstorm` | Brainstorm is single-shot divergence; quest is multi-round with memory |
| `/web` | Quest explores the idea space; web explores the information space — can combine |
| `/basin` | Basin is contemplative spiral; quest is creative spiral — similar but different substrate |

---

## Example Quest

**User:** "I need a research angle for a paper on ring attractor networks"

**Wave 1:** (broad, maximally diverse)
1. Ring attractors as models of continuous political opinion formation
2. The failure modes: when ring attractors break down in clinical populations
3. Ring attractors in cephalopod chromatophore control
4. Algebraic topology of the ring attractor manifold
5. Ring attractors as liturgical time — cyclical vs. linear temporality in neural circuits
6. Energy efficiency: why rings are metabolically optimal for angular variables
7. Ring attractors in artificial systems: continuous-valued memory for edge AI

**User:** "2 and 6 are warmer. 5 is interesting but wrong — not the liturgy angle but the formal structure angle. 1 is too obvious."

**Wave 2:** (70% near warm zone, 30% exploration)
1. Pathological ring attractors: drift signatures as biomarkers for neurodegeneration
2. Metabolic cost landscape of bump maintenance: why some widths are forbidden
3. Topological phase transitions in ring attractor dynamics — when the ring tears
4. Ring attractors under resource constraints: what gets sacrificed when ATP drops
5. Ring attractors in non-neural biological computation (slime mold, bacterial chemotaxis)
6. The ring attractor as a gauge theory — invariance under rotation as a design principle

**User:** "3 and 6 — yes. That's the direction. Topological/gauge-theoretic framing of the formal structure."

**Wave 3:** (converging)
...

---

## Created

2026-03-21 — Inspired by Luo, King, Puett & Smith (2025), "Inducing Sustained Creativity and Diversity in Large Language Models"

*You don't find what you're looking for. You find out what you're looking for by looking.*
