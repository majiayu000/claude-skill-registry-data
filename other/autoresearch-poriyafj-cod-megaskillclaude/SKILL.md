---
name: autoresearch
description: Self-improving AI-driven workflow that continuously refines, reviews, validates and optimizes research tasks. Use for iterative ongoing research.
---

# Autoresearch (self-improving research loop)

A research agent that critiques and improves its own work across iterations.

## Loop
1. **Plan** — define objective + current best answer; maintain a working document `research-state.md` with: objective, findings-so-far (with citations), confidence per finding, open questions, next hypotheses.
2. **Execute** — research the top open question (see deep-research method standards).
3. **Critique** — adversarial self-review: weakest claims? unsupported leaps? recency issues? alternative explanations?
4. **Refine** — fix, re-source, downgrade confidence where needed; update state file.
5. **Repeat** until: all questions answered at target confidence, N iterations reached, or new info stops changing conclusions (convergence).
6. **Report** — final synthesis + iteration log (what changed and why).

## Rules
- Persist state between runs; never re-research settled findings unless a contradiction appears.
- Confidence scale: confirmed (2+ primary sources) / likely / tentative / unknown.

## Output
Updated `research-state.md` each cycle + final cited report + convergence summary.
