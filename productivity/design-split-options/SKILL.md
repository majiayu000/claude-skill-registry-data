---
name: design-split-options
description: Compare 2-3 materially different initiative decompositions in `SPLIT_OPTIONS.md` when task boundaries or sequencing are still ambiguous before authoring `TASK_GRAPH.md`.
---

# design-split-options

Use only when jumping straight to `split-initiative` would lock in a weak task graph.

## Read first
- `../references/initiative-packet-contract.md`
- `../references/initiative-workflow-contract.md`
- `../references/final-state-authoring-policy.md`
- initiative `BRIEF.md`, `UBIQUITOUS_LANGUAGE.md`, `DECISIONS.md`, `INVARIANTS.md`, `REPO_MAP.md`, `CONTRACTS.md`, `OPEN_QUESTIONS.md`
- `../../references/communication-mode.md`

## Workflow
1. Enter initiative `Status: split_drafting` if split drafting has not already started.
2. Produce 2-3 materially different decomposition options.
3. Compare options on:
   - ownership clarity
   - coupling
   - validation fit
   - sequencing / uncertainty reduction
   - risk of hidden shared context
   - ease of handing each child to a fresh agent
4. Recommend one direction explicitly.
5. Write `SPLIT_OPTIONS.md`.

## Writing rule
Write compared options as candidate final task graphs, not as changelog commentary about prior split attempts.

## Do not
- produce cosmetic variants of the same split
- defer the recommendation when the evidence already favors one option
- reference outside Atelier skill files for option-design heuristics

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
