---
name: thinking
description: Decision-framing workflow for turning an ambiguous problem or open choice into a recommendation, experiment, or concrete next move. Use when the user wants to explore a vague idea, compare plausible approaches, understand system trade-offs, or decide what to do. Do not use for sustained brainstorming, when the decision is already settled and the remaining work is only implementation, or adversarial review of an existing candidate (use recursive-thinking).
---

# Thinking

Move from ambiguity to a decision that is specific enough to act on and test.

Use this as an orthogonal workflow skill alongside any relevant domain or repository skills. It does not replace security review, test strategy, prompt work, story preparation, documentation, or implementation guidance.

Family boundary: **thinking** forms a candidate; **recursive-thinking** stress-tests an existing candidate; **dream-thinking** is an explicitly requested creative retrospective after experience. None requires the others to run first.

## Core cadence

Run the skill through one simple loop:

- understand what is stuck
- explore only enough to improve the decision
- identify what matters
- choose what changes next

## Route by bottleneck

- **Problem framing:** the goal, affected stakeholder, constraint, or success signal is unclear.
- **Option discovery:** the problem is clear but the plausible approaches are not.
- **Assumption testing:** no candidate has won yet, and the choice depends on uncertain beliefs or missing evidence.
- **Systems analysis:** incentives, feedback loops, dependencies, or second-order effects could make a local improvement harmful overall.
- **Decision convergence:** enough context exists to compare serious options and recommend a next move.

Use **recursive-thinking** instead when the main job is to challenge, premortem, or find weaknesses in an already-formed plan, diagnosis, design, or recommendation. Switch to the appropriate execution or artifact-specific skill once the material trade-off is settled.

## Workflow

1. **Inspect the available context.** Read relevant code, documents, evidence, constraints, and prior decisions before asking for facts that can be discovered.
2. **Frame the decision.** State the goal, success signal, important constraints, and what is out of scope. If the user starts with a solution, verify that the underlying problem is settled.
3. **Resolve material ambiguity.** Ask one focused question when its answer would change the recommendation. Otherwise state a labeled assumption and continue.
4. **Explore when useful.** Generate meaningfully different approaches only while the option set is underdeveloped. Vary scope, timing, affected stakeholder, process versus product, addition versus subtraction, or reversible experiment versus durable investment. Include the status quo, deferral, or stopping when one is a credible alternative; do not add it as filler. Stop when further options would repeat the same trade-offs.
5. **Identify decision drivers.** Separate evidence from assumptions, identify any unknown material enough to change the recommendation, and trace second-order effects when incentives or dependencies matter. Steelman serious options before rejecting them.
6. **Compare serious options.** When the choice is material, compare the strongest two or three approaches on value, complexity, risk, reversibility, time to validate, and carrying cost. Do not invent weak alternatives to fill a table.
7. **Choose the next move.** Recommend the smallest credible action or experiment that improves the situation or tests the key assumption. Prefer necessary quality over artificial narrowness.
8. **Define validation.** Make validation proportionate to the move's cost, reversibility, and uncertainty. Name success or failure signals, evidence to collect, and a revisit point when they add decision value.

## Decision rules

- Keep conclusions, evidence, and assumptions distinguishable.
- Distinguish symptoms from root causes without forcing repeated why-questions after the framing stabilizes.
- Prefer reversible learning when uncertainty is high and durable leverage when evidence is strong.
- Skip broad exploration when one viable path is already clear.
- Make the recommendation explicit; do not end with an unranked list unless the user requested options only.
- Name why a rejected serious approach lost in one sentence.

## Completion test

Stop when all are true:

- the recommended next step is concrete
- the main trade-off is decided or explicitly deferred
- any material assumption or unknown is visible
- validation or a revisit condition is proportionate to the move

## Output

Scale the response to the task. For a small decision, use:

```markdown
## Decision
The recommended direction.

## Why
The decisive evidence, assumption, or trade-off.

## Next move
The concrete action or experiment.

## Validation
How to verify it worked or when to revisit it.
```

For medium or large decisions, read [references/output-templates.md](references/output-templates.md). Use only sections that improve the decision; do not force the template.
