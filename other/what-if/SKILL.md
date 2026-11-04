---
name: what-if
description: Run structured what-if thought experiments for plans, architectures, or workflows by changing key constraints, sketching plausible alternative worlds, stress-testing them adversarially, and capturing the consequences before deciding whether to change anything. Use when the user asks "what if", wants to reimagine assumptions, remove a boundary, compare a different operating model, or explore consequences before committing.
---

# What If

Use this skill for counterfactual planning, not implementation-first work.

## Workflow

1. Frame the thought experiment.
   - State the current world in 3-6 bullets.
   - State the changed constraint(s) explicitly.
   - State the invariants: what must still be true.
   - If any of those are fuzzy, ask a few focused questions first.
2. Sketch 2-4 plausible alternative worlds.
   - Include at least one conservative option and one more radical option.
   - Do not invent fantasy paths that ignore the user's real tooling, migration cost, or constraints.
   - For each world, describe the shape, the implementation outline, the upside, and the downside.
3. Stress-test each world adversarially.
   - Load `references/review-lenses.md`.
   - Look for breakpoints, hidden coupling, migration traps, security/trust issues, operator burden, and reversibility.
   - If subagents or parallel review tools are available, use them for an adversarial pass; otherwise do the adversarial review yourself.
4. Compare the worlds and make a call.
   - Say which world is best, which is safest, and which is most interesting-but-dangerous.
   - It is valid to recommend staying with the current setup if the alternatives are not compelling.
5. Capture the findings.
   - Use the output shape in `references/review-lenses.md` unless the user wants a different format.
   - Keep the final result decision-oriented, not stream-of-consciousness brainstorming.

## Working Rules

- Prefer concrete consequences over abstract opinions.
- Separate facts, assumptions, and speculation.
- Name second-order effects, not just first-order benefits.
- Include migration steps when proposing a new world.
- Include rollback or coexistence paths when relevant.
- Do not force a change; "keep the current tradeoff" is a valid outcome.
