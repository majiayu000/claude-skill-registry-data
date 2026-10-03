---
name: codex-logical-decision-layer
description: Use when work is ambiguous or has multiple viable paths; compares options, assumptions, evidence, tradeoffs, and the best next action.
load_priority: on-demand
---

## TL;DR
Use when the task has multiple possible solutions, hidden risk, or high cost of being wrong. Produce a concise decision surface: options, evidence, tradeoffs, recommendation, stop conditions.

## Activation
1. Activate on `$think`, `$decide`, `$options`, "think from multiple angles", or "find the best direction".
2. Activate for architecture, refactor, debugging strategy, product workflow, release, and non-trivial UI/BE decisions.
3. Auto-pair with `codex-reasoning-rigor` when the user asks for deeper reasoning or non-generic output.

## Hard Rules
- Do not reveal private chain-of-thought. Output the decision contract only.
- Generate 2-4 plausible options, not an unbounded brainstorm.
- Compare options by evidence, cost, risk, reversibility, and verification.
- Prefer the smallest change that satisfies the goal and can be verified.
- If evidence is weak, state the assumption and the first command/file needed to validate it.
- Stop adding abstractions when the current project evidence does not justify them.

## Output Contract

```markdown
## Decision Surface
| Option | When it wins | Cost | Risk | Evidence needed |
| --- | --- | --- | --- | --- |

## Recommendation
Choose <option> because <repo evidence / constraint>.

## Verification
- <command or observable signal>

## Stop Conditions
- <condition that would change the decision>
```

## Command

```bash
python "<SKILLS_ROOT>/codex-logical-decision-layer/scripts/build_decision_matrix.py" --problem "<problem>" --options "A,B,C" --format markdown
```

## Reference Files
- `references/decision-contract.md`: compact decision matrix rules and anti-token-waste policy.
