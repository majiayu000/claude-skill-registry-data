---
name: technical-decision-helper
description: Present 2-3 viable technical options with pros/cons, trade-off comparisons, and a recommendation with fallback, decomposing complex decisions into sub-problems first. Use when user says 'help me choose between these technologies', 'should I use X or Y', 'compare these architecture options', or 'build vs buy for this feature'.
argument-hint: Describe the technical problem or question, project context, constraints, and any relevant information about previously considered alternatives.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.1.0"
---

# Technical Decision Helper

Presents 2-3 viable options with pros/cons, trade-offs, and project fit, then recommends one with a fallback. Every question to the user goes through an interactive question tool — never plain text.

## Interaction rule

Always use the environment's interactive question tool (`vscode_askQuestions` in VS Code, or equivalent) for every clarification, option selection, or confirmation. If none available, fall back to labeled options (A/B/C…Z, Z always "Other — describe freely") — see `references/templates.md`. When any essential context is missing or ambiguous, stop and ask before analyzing; never assume.

## Workflow

| Phase              | Action                                                                                                                                                                           | Gate                                                                     |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| 1. Understand      | Gather decision, problem, constraints (perf/cost/time/compat), current stack, non-functional reqs. If complex → decompose into 2-3 sub-problems, solve independently, integrate. | All ambiguities resolved via interactive question tool before proceeding |
| 2. Search context  | Search official docs for named techs; comparisons if multiple options; community patterns if novel problem. Check real open-source usage, benchmarks, community experience.      | Enough evidence to write pros/cons per option                            |
| 3. Present options | One block per option: Description, Pros, Cons, Trade-offs, Project fit — see `references/templates.md`                                                                           | Min 2-3 viable options                                                   |
| 4. Compare         | Matrix across: complexity, learning curve, performance, maintainability, community/support, architecture fit, cost, technical risk                                               | Matrix covers every option                                               |
| 5. Recommend       | Recommended option + justification, implementation plan, success metrics, Plan B                                                                                                 | Output matches `references/templates.md` final structure                 |

## When to use

✅ Choosing between 2+ techs/architectures · build vs external lib · trade-off evaluation · migration/refactor planning · pattern selection for recurring problems

❌ Debugging specific code · tactical implementation · problems with an already-established project pattern

## Usage tips

Specific question + context = better analysis. Mention constraints (budget, deadline, team skill). Give examples from prior work. Complex ask → decompose. Treat the decision as an ongoing check, not one-shot.

## Reference files

- `references/templates.md` — question format, interactive-tool JSON example, option analysis block, final output structure, worked usage example
