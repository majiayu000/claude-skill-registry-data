---
name: idea-engine
description: >
  Activate when the user needs to evaluate whether a research idea is worth pursuing,
  brainstorm new research directions, or stress-test a paper concept before committing.
  This is Phase 0 of the paper machine — the gate that decides whether the full
  8-phase pipeline should run. Also activates standalone via /evaluate-idea.

  Integrates Carlini's research philosophy (conclusion-first test, taste for problems,
  kill conditions, unreasonable effort) with structured evaluation (7 dimensions,
  RS1-RS8 principles, 3 specialist agents).
---

# Idea Engine — Phase 0: Is This Paper Worth Writing?

## Purpose

Most AI tools help you *write* papers. This engine helps you decide *which* papers to write.

The current paper machine takes any topic and produces. This engine adds the missing
gate: **Phase 0 — Is this paper the right use of my time?**

Great research starts with taste, strategic problem selection, honest self-evaluation,
and knowing when to kill your darlings.

## When to Activate

- User runs `/evaluate-idea [topic]`
- User asks "is this worth pursuing?", "should I write this paper?"
- Phase 0 of the `/write-paper` pipeline (before Reconnaissance)
- User wants to compare multiple research directions
- User questions whether to continue an ongoing project

## The 8 Research Strategy Principles (RS1-RS8)

Reference: `principles/research-strategy.md` for full details.

### Problem Selection
- **RS1 (Novelty Test):** If you don't do this, how many months until someone else does?
- **RS2 (Conclusion-First Test):** Can you write a compelling conclusion without doing the work?
- **RS3 (Nugget Test):** Can you state the key insight in one sentence?

### Execution Strategy
- **RS4 (Fail Fast):** Start with the sub-problem most likely to kill the project.
- **RS5 (Kill Early):** A working project with low impact is worse than a killed project.
- **RS6 (Unreasonable Effort):** Strengthen "sometimes" to "usually" — but only AFTER RS4 and RS5.

### Strategic Positioning
- **RS7 (Comparative Advantage):** Research space is high-dimensional; find your unique corner.
- **RS8 (Timing Awareness):** Impact = skill x domain importance at this moment.

## The 6-Phase Orchestration Pipeline

### Phase 1: SEED — Understand the Problem Space
**Goal:** Gather enough context to brainstorm and evaluate intelligently.

1. Check for prior evaluations in `research-evaluations/*.md`
   - If KILL exists: check whether reasons still hold
   - If PARK exists: check whether revisit conditions are met
2. Brief interview (3-5 questions max, skip what's already answered):
   - What's the problem space? What's bugging you about it?
   - What's your background/expertise relevant to this?
   - Any constraints (timeline, venue, data availability)?
   - What would success look like?

### Phase 2: DIVERGE — Generate Ideas
**Goal:** Expand the possibility space before narrowing.

1. Deploy the **Brainstormer** agent (`agents/brainstormer.md`)
2. Organize results by type:
   - Cross-field connections
   - Assumptions worth challenging
   - Novel framings
   - Extensions of the original idea
3. Present results. User stars their top 2-3 ideas.

### Phase 3: EVALUATE — Stress-Test Top Ideas
**Goal:** Honest, structured assessment of each candidate.

1. Deploy **Idea Critic** agents in parallel — one per selected idea (`agents/idea-critic.md`)
2. Each evaluation covers all 7 dimensions with signal ratings
3. Present side-by-side comparison table:

```
| Dimension    | Idea A        | Idea B        | Idea C        |
|-------------|---------------|---------------|---------------|
| Novelty     | Years         | Months        | Weeks         |
| Impact      | High          | Medium        | Low           |
| Timing      | Well-Timed    | Well-Timed    | Too Late      |
| Feasibility | Medium Risk   | Low Risk      | Low Risk      |
| Competition | Open          | Moderate      | Crowded       |
| Nugget      | Clear         | Fuzzy         | Clear         |
| Narrative   | Compelling    | Workable      | Weak          |
| **VERDICT** | **PURSUE**    | **REFINE**    | **KILL**      |
```

4. Highlight which ideas survived and which were killed, with reasoning.

### Phase 4: DEEPEN — Strategic Reality Check
**Goal:** For surviving ideas, assess strategic viability.

1. Deploy **Research Strategist** for each PURSUE/REFINE idea (in parallel, `agents/research-strategist.md`)
   - Scooping risk assessment
   - Competitive landscape analysis
   - Timing evaluation
   - Comparative advantage mapping
2. Present as reality check with traffic lights:
   - Green flags (strong strategic position)
   - Yellow flags (manageable risks)
   - Red flags (serious concerns)

### Phase 5: FRAME — The Conclusion-First Test
**Goal:** The decisive test. Can this paper tell a compelling story?

For each surviving idea, write:

1. **The Nugget** — one sentence, the core insight
2. **Draft Abstract** (5 sentences following Carlini's Formula A):
   - (1) Topic
   - (2) Problem within that topic
   - (3) Results or methods
   - (4) Whichever sentence 3 didn't cover
   - (5) Why it matters
3. **Draft Conclusion** (2-3 sentences):
   - What can we say? What changed? So what?

**The critical test:** If the conclusion feels hollow or generic — if it only says
"our method achieves X% improvement" — that IS the signal. The idea doesn't have
enough impact to justify months of work.

### Phase 6: DECIDE — Final Verdict and Next Steps
**Goal:** Clear, actionable decision for each idea.

For each idea, deliver one of three verdicts:

**PURSUE** — This is worth your time. Next steps:
- Specific, risk-targeted first step (RS4: start with what's most likely to kill it)
- Time-bounded: achievable in 1-2 weeks
- What to do first, what to defer

**PARK** — Not now, but potentially later. Document:
- What would need to change for this to become PURSUE
- Conditions to revisit (new dataset, field shift, new collaborator)
- Set a revisit date

**KILL** — Not worth pursuing. But still extract value:
- What was learned from the evaluation process
- Any salvageable sub-ideas worth noting
- Blog post / workshop paper / conversation starter potential

**Save evaluation** to `research-evaluations/YYYY-MM-DD-<topic-slug>.md`:

```yaml
---
date: YYYY-MM-DD
topic: [descriptive title]
verdict: [PURSUE/PARK/KILL]
nugget: [one-sentence key insight]
revisit: [date or condition, if PARK]
---

## Dimension Scores
[table from Phase 3]

## Key Concerns
[top 3 risks]

## Strategic Assessment
[summary from Phase 4]

## Draft Conclusion
[from Phase 5]

## Next Steps / Salvage
[from verdict]
```

## Orchestration Rules

1. **Maximize parallelism** in Phases 3-4. Run multiple Idea Critic / Research Strategist
   agents simultaneously for different ideas.
2. **Show your plan** before each phase. Brief one-liner, not a detailed outline.
3. **Let the researcher drive.** Present options, don't decide for them which ideas to pursue.
4. **Don't skip Phase 5** (conclusion-first test). This is the most important phase.
   Everything else is preparation for this moment.
5. **Be honest in synthesis.** If all ideas score poorly, say so. Don't manufacture enthusiasm.
6. **Keep momentum.** A full evaluation session should take 15-20 minutes, not an hour.
   If the user provides a single clear idea, collapse Phases 1-2 and go straight to evaluation.
7. **Connect to the pipeline.** If verdict is PURSUE and user wants to proceed, hand off
   directly to Phase 1 (Reconnaissance) of the paper machine. The evaluation artifacts
   inform the literature search strategy.

## Standalone vs. Pipeline Mode

**Standalone** (`/evaluate-idea`): Run the full 6-phase evaluation. End with verdict.
The user decides whether to proceed to `/write-paper`.

**Pipeline** (Phase 0 of `/write-paper`): Run an abbreviated evaluation:
- Skip Phase 2 (DIVERGE) if user already has a specific topic
- Run Phase 3 (EVALUATE) with the single idea
- Run Phase 5 (FRAME: conclusion-first test)
- If PURSUE: proceed to Phase 1 (Reconnaissance) automatically
- If KILL: stop and explain why. Suggest alternatives or refinements.
- If REFINE: present refinement suggestions, let user choose, then re-evaluate or proceed.

## Integration with Paper Machine

When Phase 0 produces a PURSUE verdict, the following artifacts carry forward:
- **The nugget** → becomes the guiding star for the entire paper
- **Draft conclusion** → informs the framing in Phase 2
- **Competitive landscape** → focuses the literature search in Phase 1
- **Key risks** → determines what the paper must address to be convincing
- **Draft abstract** → first draft for Phase 4
