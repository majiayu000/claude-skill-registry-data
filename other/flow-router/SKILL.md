---
name: flow-router
description: This skill should be used when the user asks to "classify this task", "what profile should I use", "how complex is this issue", or when the agentic-loop needs to choose a phase profile before starting. Classifies a GitHub Issue into a workflow profile (full/balanced/quick/trivial/review-only) to right-size the workflow overhead.
---

# Skill: flow-router

Classifies a task and selects the appropriate phase profile for the `agentic-loop`. The goal is to right-size the ceremony — a typo fix should not pay the same overhead as a new feature.

## Inputs

- GitHub Issue body (from `gh issue view <N>`)
- `state.yaml` `task.title` and `task.labels`
- Any open PRs for this branch (signals review-only profile)

## Classification criteria

Read the issue carefully. Assess:

1. **Scope**: Is this a self-contained change (one file, one function) or multi-component?
2. **Risk**: Does it touch auth, data migrations, external APIs, or shared infrastructure?
3. **Novelty**: Is the solution space well understood or does it require exploration?
4. **State**: Is there already a partially-implemented branch?

## Profiles

| Profile | When to use |
|---|---|
| `full` | New feature, multi-component change, high-risk area, or novel solution space |
| `balanced` | Medium-scope feature, known solution, low risk — exploration + design needed but no recall |
| `quick` | Small targeted change with a clear solution; recall likely sufficient to skip explore |
| `trivial` | Single-line fix, typo, config value change, rename — no explore/design overhead justified |
| `review-only` | Changes already exist on branch; only review + finalize needed |

## Output

Write to `state.yaml` under `config_used`:

```yaml
config_used:
  profile: full
  skipped_phases: []
  router_rationale: "multi-component feature touching backend + frontend, novel appointment logic"
```

For a trivial task:
```yaml
config_used:
  profile: trivial
  skipped_phases: [recall, explore, clarify, design, gate, knowledge]
  router_rationale: "single-file typo fix, zero design decisions"
```

## Escalation

If the profile is ambiguous between `trivial` and `balanced`, default to `balanced`. It is cheaper to over-invest in planning than to under-invest and discover a constraint at implementation time.

If the issue is tagged `needs-discussion` or `blocked`, set `status: waiting` in `state.yaml` and pause.
