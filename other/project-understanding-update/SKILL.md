---
name: project-understanding-update
description: Use when a research project needs normal project memory updated from human intent, sources, evidence pressure, experiment results, or direction changes; strict graph review is optional advanced mode.
argument-hint: "[workspace path] [project id]"
---

# Project Understanding Update

This skill preserves and updates project understanding. It is not a paper search skill and not a graph mutation shortcut.

## Boundary

Human intent is first-class input.

Normal project understanding updates should be recorded through Research Pilot project memory / UnderstandingUpdate / typed dataset tools. The agent may classify, preserve, compare, and propose. It must not silently convert a human idea into a confirmed claim, project decision, or strict graph truth.

Strict graph-level changes use Delta Update Protocol only when the user asks for strict review or a formal Q/C/E/W/L/RL/TL change is being accepted:

```text
input
-> classify meaning
-> normal project memory update
-> optional strict-review D* proposal
-> dry-run
-> human accept/reject/park/revise
-> append accepted graph event only after approval
```

## Required Reads

Before changing project understanding, read:

```text
$WORKSPACE/wiki/projects/$PROJECT/project-query-pack.md
$WORKSPACE/wiki/projects/$PROJECT/overview.md
$WORKSPACE/wiki/projects/$PROJECT/project-understanding-graph.md if present
$WORKSPACE/wiki/_system/workflows/project-understanding-update.md
$WORKSPACE/wiki/_system/workflows/delta-update-protocol.md
```

Also query current graph when graph events exist:

```bash
python3 "$PLUGIN_ROOT/tools/graph_query_cli.py" summary --repo "$WORKSPACE" --project "$PROJECT" --json
python3 "$PLUGIN_ROOT/tools/graph_query_cli.py" open --repo "$WORKSPACE" --project "$PROJECT" --json
```

## Input Classification

Classify the user's input before writing:

- `observation`: project-relevant fact or pattern.
- `intuition`: taste, hunch, or research direction.
- `question`: new or reframed question.
- `claim`: contestable project judgment.
- `evidence_pressure`: accumulated evidence suggests Q/C update.
- `limitation_pressure`: repeated caveat weakens or bounds a claim.
- `search_need`: project now needs papers for a missing support.
- `experiment_need`: project now needs generated evidence.
- `boundary`: do-not-assume or do-not-learn constraint.
- `decision`: human project decision.

## Safe Updates

Direct markdown updates are allowed for workspace memory and reports:

- `overview.md`
- `project-query-pack.md`
- `decisions.md` only for explicit human decisions
- `idea-board.md`
- generated reports/snapshots if rebuilt

Graph truth changes require D*:

- add/refine/split/merge/retire `Question`
- add/refine/split/merge/retire `Claim`
- add `Evidence`, `Warrant`, `Limitation`
- add/update `Reasoning Link` or `Translation Link`
- change lifecycle, lineage, confidence, scope, or human review

## Output

End with:

```text
Update type:
Project memory:
Strict review:
Human gate:
Next natural prompt:
```

If no durable update is needed, say so and explain why.
