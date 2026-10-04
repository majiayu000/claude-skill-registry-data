---
name: researchforge-autorun
description: Drive the autonomous research loop round after round — ask the engine which node to expand, plan there, run, read the result, repeat. Use when the user wants to keep improving a repository over many rounds, or wants autorun without an AI API key.
---

# Drive the research loop

`researchforge autorun` runs this loop by itself when an API key is configured.
Without one, **you** are the intelligence and the engine is still the lab: it
chooses where to search, validates what you write, runs the benchmark, and
records the result. Your job is the one part it cannot do without a provider —
writing the plan and the patches.

Never guess at the next move. The engine's search knows things a results table
does not show: which ideas were already tried at which node, what is in each
node's ancestry, and how much budget is left.

## 1. Ask where to go next

```bash
researchforge autorun --dry-run --json
```

This spends nothing — no AI call, no experiment runs. It returns the node the
loop would expand, the hypotheses it would try there in ranked order, and the
exact command to take that step:

- `node` — the experiment to build on, or `null` for the baseline;
- `hypotheses` — ranked, best candidate first;
- `command` — run this next;
- `retreat: true` — the only moves left are on branches that gained nothing.
  Tell the user: this measures an idea *without* the gains already banked, which
  is an ablation rather than progress;
- `needs_resynthesis: true` — every hypothesis has been tried everywhere it can
  apply. Go to step 5.

## 2. Plan at that node

Run the `command` from step 1. With a parent it looks like:

```bash
researchforge experiment plan hyp-002 --parent exp-008 --json
```

The exported context's `repository` section shows the files **as `exp-008`
leaves them**, and `applied` lists the experiments already baked into what you
are reading. Write the change against those contents: do not re-apply the
parent's change, and do not expect the baseline's values.

Then follow the researchforge-plan skill to write `plan.yaml` and the patches.
Set `parent: exp-008` on every entry — on this path nothing sets it for you, and
a patch written against the parent but imported without it will be applied to
the baseline and fail.

## 3. Import, approve, run

```bash
researchforge experiment import .researchforge/experiments/plan.yaml --json
researchforge experiment approve <plan-id>     # the user's decision
researchforge experiment run <plan-id> --json
```

Approval belongs to the user. Show them the plan and the worst-case wall time,
and let them run the approve command themselves unless they explicitly approved
it in this conversation.

## 4. Read the result, then go back to step 1

```bash
researchforge results show --json
```

Report what was measured, including when it did not work — a rejected
experiment is a result, not a failure to hide. Watch for a `NO CHANGE` badge:
an experiment can inherit its parent's improvement while contributing exactly
zero of its own.

Then return to step 1. The next `--dry-run` accounts for what just happened.

## 5. When the graph is exhausted

`needs_resynthesis: true` means no hypothesis has anywhere left to apply. New
ideas have to come from what the runs measured:

```bash
researchforge research synthesize --from-results
```

Follow the researchforge-hypotheses skill, then return to step 1.

## Stopping

You are the loop's stopping condition here. Stop and tell the user when the
objective's target is reached, when several rounds in a row produce no
improvement, or when only retreat moves remain. Say which of those happened.

## Rules

- The Python engine is the boundary: never work around a validation error, a
  protected path, or an approval gate — fix the artifact or ask the user.
- Approvals belong to the user: never pass `--yes` or type a confirmation
  unless the user explicitly approved that step in this conversation.
- Ground every summary in stored data: quote only numbers returned by
  `--json` output or files under `.researchforge/` — never invent metrics.
- Never choose the next node yourself when `--dry-run` can tell you.
