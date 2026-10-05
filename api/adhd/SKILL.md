---
name: adhd
description: Use when parallel divergent ideation for agents — spawns N isolated reasoning
  branches under different cognitive frames, then scores, clusters, prunes traps,
  and deepens survivors. Use for open-ended design, architecture, naming, API surface
  decisions, fuzzy debugging, and brainstorming. Skip for syntax lookups or bugs with
  known root cause.
domain: core
author: mahipal
license: MIT
subdomain: reasoning
tags:
- reasoning
- brainstorming
- decision-making
- cognitive-frames
- divergent-thinking
- architecture
- design
version: 1.0.0
category: core
---



persona:
  name: "Udit Akhouri"
  title: "The Divergent Ideation Architect"
  expertise: ['Parallel Reasoning Architectures', 'Cognitive Frames', 'Agent Skill Design', 'Premature Convergence']
  philosophy: "The first three answers are the ones a senior engineer gives in thirty seconds. Correct. Forgettable. The interesting answers live past number three."
  credentials: ['Author of ADHD preprint', 'Creator of adhdstack.github.io', 'MIT-licensed open source']
  principles: ['Isolate before converge', 'Generator and critic must never mix', 'Structure is half the value', 'Expensive — gate before use']

# ADHD — Parallel Divergent Ideation

**Upstream:** [github.com/UditAkhourii/adhd](https://github.com/UditAkhourii/adhd)  
**License:** MIT  
**Preprint:** [adhdstack.github.io](https://adhdstack.github.io/)

Stop picking the textbook answer. This skill forces the agent to walk into the awkward middle where non-obvious solutions live.

---

## When to Use

**Trigger phrases:**
- "/adhd"
- "ADHD mode"
- "use parallel ideation"
- "brainstorm this"
- "give me a few ways to..."
- "think outside the box on this"

**Use when:**
- Architecture decisions where the obvious answer may not be best
- API/SDK surface design (naming, ergonomics, DX tradeoffs)
- Naming things (products, features, variables, endpoints)
- Fuzzy debugging with no known root cause
- Open-ended strategy or positioning
- Schema / data model design

**Don't use for:**
- Syntax lookups ("what's the Python equivalent of...")
- Bugs with a known root cause
- Any question with one canonical answer
- Low-stakes decisions ("what color should this button be?")
- When the user says "quick", "standard", "canonical", "textbook", or "just"

---



## Verification

- Run one full divergence round (N branches → score → cluster → prune → deepen) on a real design question and confirm the surviving branches are genuinely diverse, not rewrites of one idea.
- Feed a problem with a known trap (e.g. a solution that ignores a hard constraint) and confirm the pruning pass removes or flags that branch.
- Verify scoring is reproducible: re-running the same round with the same inputs yields the same survivors.
- Confirm the output clusters are attributable — every branch maps to a cluster and the deepened survivors cite their lineage.

## Anti-Rationalization Table

| Excuse | Reality | Rule |
|--------|---------|------|
| "Parallel branches waste tokens" | Divergent thinking finds better solutions than single-path | The cost of a bad architecture exceeds parallel exploration cost |
| "I can just think harder" | Cognitive biases blind single-threaded reasoning | Structured parallel frames force coverage of blind spots |
| "Naming isn't a design problem" | Names reveal conceptual clarity; bad names = bad abstractions | Treat naming as API design — it is |


**Trigger phrases:**
- "/adhd"
- "ADHD mode"
- "use parallel ideation"
- "brainstorm this"
- "give me a few ways to..."
- "think outside the box on this"

**Use when:**
- Architecture decisions where the obvious answer may not be best
- API/SDK surface design (naming, ergonomics, DX tradeoffs)
- Naming things (products, features, variables, endpoints)
- Fuzzy debugging with no known root cause
- Open-ended strategy or positioning
- Schema / data model design

**Don't use for:**
- Syntax lookups ("what's the Python equivalent of...")
- Bugs with a known root cause
- Any question with one canonical answer
- Low-stakes decisions ("what color should this button be?")
- When the user says "quick", "standard", "canonical", "textbook", or "just"

---

## How to Use

1. **Confirm fit** — Check the task against the trigger phrases and "Use when" list; bail if it hits "Don't use for"
2. **Enter The Loop** — Run the parallel ideation loop below (Diverge → Focus), phases gate on their own inputs
3. **Apply cognitive frames** — Use the frames section to stretch or prune candidate directions
4. **Pick and commit** — Converge on one direction and exit the loop; do not re-open decisions without new information
5. **Verify** — Run the Verification Checklist before shipping the chosen design

---

## Pre-flight Gate

This skill is expensive (~5–10× a single answer). Run this gate before proceeding.

**Step 1. Explicit invocation.** If the user typed `/adhd` or explicitly asked for ADHD mode, **skip** the rest of the gate and go straight to Phase 1.

**Step 2. Self-judge.** Ask yourself three questions. If any answer is **no**, abort.

1. **Open-ended?** Would a senior engineer give multiple viable answers, or is there one canonical answer?
2. **High-stakes?** Is the cost of the obvious answer being wrong actually high?
3. **Open phrasing?** Did the user avoid words like "quick", "standard", "canonical", "textbook", "just"?

If all three pass, proceed to Phase 1. Otherwise, answer directly. Optionally add: *"If you want wider exploration under parallel cognitive frames with trap detection, run `/adhd <problem>`."*

---

## The Loop

Two strict phases. **Do not mix them** — the critic strangles the generator.

### Phase 1 — Diverge (no critic)

1. **Pick 5 cognitive frames** from the table below. Bias toward engineering tags for code problems. Always include at least one wild frame.

2. **Spawn 5 parallel isolated branches.** Each gets only:
   - The problem P
   - Any context the user provided
   - The chosen frame's vantage prompt
   - A system instruction that forbids evaluation

   > You are in DIVERGENT mode — a generator, not a critic.
   > Generate 6 short distinct ideas under this frame. Each idea is one
   > phrase or one sentence. Do not evaluate. Do not rank. Do not hedge.
   > The first three obvious answers everyone would give are banned.
   > Push past them into the awkward middle.
   > Output a JSON array only: [{"text": "...", "rationale": "..."}, ...]

3. **Critical invariant:** Branches must be parallel and isolated. Do NOT serialize them. Do NOT pass one branch's output to another. Branches that see each other anchor each other — the whole method collapses to a wider single thought.

### Phase 2 — Focus (critic on)

1. **Score.** Rate each idea 0–10 on:
   - **Novelty** (distance from the obvious default)
   - **Viability** (could it actually ship)
   - **Fit** (does it address the stated problem)
   
   Flag any attractive-looking trap with a one-line reason.

2. **Cluster.** Group into 3–6 clusters by underlying angle, not surface keywords. Label by angle: "remove-the-server plays", "cache-shaped plays", "race-multiple-backends plays".

3. **Deepen the top 3.** Rank by weighted score (Novelty 0.35 + Viability 0.40 + Fit 0.25), exclude traps, take top 3. For each:
   - 4–8 sentence sketch of how it works
   - The load-bearing risk
   - The first concrete step a builder would take
   - 3–5 child ideas (variations, hybrids, unlocks)

   > You are in FOCUS mode. Take one promising idea and connect dots.
   > Sketch how it would actually work in 4–8 sentences. Name the
   > load-bearing risk. Name the first concrete step a coder would take.
   > Then generate 3–5 sub-ideas that branch off. Output JSON only.

---

## Cognitive Frames

Pick 5 per run. For code problems: 4 tagged `code`/`design` + 1 tagged `wild`.

| Frame | Vantage Prompt | Tags |
|-------|---------------|------|
| **hardware engineer** | You think in latency, memory layout, and physical constraints. Re-ask this as a hardware/firmware problem. What does the bus topology, cache, timing budget tell you? | code, wild |
| **regulator** | You audit systems for compliance and failure modes. What must be provable, traceable, or refusable here? | design, general |
| **10-year-old** | You are a curious 10 year old who has never seen software. Describe naive but unencumbered approaches. Ignore convention. | general, wild |
| **competitor trying to break it** | You are a hostile competitor or attacker. Generate approaches that exploit, fail, or sabotage the obvious solution. Then invert into ideas. | code, design |
| **biology** | Transplant a mechanism from biology (immune systems, neural plasticity, cell signaling, evolution, gut flora). Force-fit it onto this engineering problem. | code, wild |
| **logistics** | Steal mechanisms from logistics: queues, batching, just-in-time, hub-and-spoke, returns, last-mile. Apply them literally. | code, design |
| **game design** | Approach this as a game designer. What are the loops, rewards, friction, save-states, speedrun tricks? Treat the user as a player. | design, general |
| **markets** | Treat the problem as a market. Buyers, sellers, market-makers. What does an auction, a futures contract, a clearing house look like here? | design, wild |
| **inversion** | Ask the OPPOSITE question. If goal is X, brainstorm how to guarantee NOT X. Then negate each answer back. | code, design, general |
| **extreme: $0 budget, 1 hour** | No money, no team, one hour. What is the crudest version that still does the load-bearing thing? | code, general |
| **extreme: infinite budget, 10 years** | Infinite compute, infinite engineers, a decade. What is the maximalist version? | design, wild |
| **remove the load-bearing assumption** | Name the thing everyone treats as fixed (framework, database, request-response model, network). Imagine it is gone. What is possible? | code, design, wild |
| **speedrunner** | You are a speedrunner. Find glitches, skips, out-of-bounds tricks, frame-perfect shortcuts. What is the abusive-but-legal path? | code, wild |
| **ant colony** | No central planner. Many dumb agents, local rules, pheromone trails. How does the problem solve itself emergently? | code, wild |
| **3am on-call** | You are the on-call engineer woken at 3am when this breaks. What design would let you not get paged? | code, design |

Vary picks across sessions so the same problem produces different candidate sets when re-run.

---

## Output Shape

Render in this order. Structure is the point — do not collapse into prose.

1. **Brief.** One–two lines confirming the problem and any reframe used.
2. **Wide set.** Full pool grouped by cluster. Score chips: `[N7 V8 F9]` per idea.
3. **Converge.** 2–4 idea shortlist. Why each is on the list. Mark non-obvious pick with ★. List traps with one-line reasons.
4. **Focus.** 3 deepened branches: sketch, risk, first step, child ideas.
5. **Provocation.** One wildcard question that opens a new direction if nothing landed.

---

## Cost & Calibration

~10 agent calls per run (5 diverge + 1 score + 1 cluster + 3 deepen). About 5–10× single-shot.

| Context | Frames × Ideas | Total |
|---------|---------------|-------|
| Quick naming decision | 3 × 4 | ~12 |
| Default | 5 × 6 | ~30 |
| High-stakes strategy | 5 × 8 | ~40 |

---

## Anti-Patterns

| Anti-pattern | What it looks like | Fix |
|-------------|-------------------|-----|
| **Convergence disguised as divergence** | Ten variations of one idea | Check: do all share one assumption? |
| **Weird-for-weird's-sake** | 30 unsorted absurdities | Always converge. Structure is half the value. |
| **Walls of equally-weighted prose** | No clustering, no prioritization | Cluster, label, pull out the best. |
| **Refusing to commit** | "Here are 20 ideas, you decide" | Take a position. Generate wide, converge with opinion. |
| **Skipping isolation** | Simulating parallel branches sequentially | Each branch needs a fresh context. Parallel or nothing. |

---

## Verification Checklist

- [ ] Pre-flight gate passed (explicit invocation or 3/3 self-judge checks)
- [ ] 5 frames picked with at least 1 wild
- [ ] Diverge used parallel isolated branches (not sequential)
- [ ] Generator mode strictly enforced during diverge
- [ ] Scoring on 3 axes with trap flags
- [ ] Clusters grouped by underlying angle
- [ ] Top 3 deepened with sketch, risk, first step, child ideas
- [ ] Output in structured shape: brief → wide → converge → focus → provocation
- [ ] Provocation included at the end

---

## References

- [ADHD preprint](https://adhdstack.github.io/) — academic paper
- [Upstream repo](https://github.com/UditAkhourii/adhd)
- [The New Stack feature](https://thenewstack.io/claude-code-adhd/)
- [Independent benchmark](https://miyagadget.page/en/blog/2026/06/03/adhd-coding-agent-skill-en/)
- [Repowire integration](https://github.com/prassanna-ravishankar/repowire/pull/313)
- [Han research review](https://github.com/testdouble/han/blob/adhd-swarm-research/docs/research/adhd-application-to-han.md)
## Overview

Parallel divergent ideation for agents — spawns N isolated reasoning branches under different cognitive frames, then scores, clusters, prunes traps, and deepens survivors. Use for open-ended design, architecture, naming, API surface decisions.

## Process

1. **Define problem space** — Specify the open-ended decision or design challenge
2. **Spawn branches** — Launch N isolated reasoning agents with different frames
3. **Score outputs** — Evaluate each branch against quality criteria
4. **Cluster & prune** — Group similar ideas, remove cognitive traps
5. **Deepen survivors** — Run deep analysis on top candidates
6. **Synthesize** — Merge insights into final recommendation
