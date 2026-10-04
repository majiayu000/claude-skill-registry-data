---
name: dialogue-parser-scope
description: "Approve the dialogue parser working set and separate selected versus non-selected dialogue artifacts before packetization."
---

# Dialogue Parser Scope

## Approve the Parser Working Set

Use this after `workflow/dialogue_intake_checkpoint.json` and `workflow/dialogue_continuation_gate.json` exist. Freeze the exact dialogue parser artifacts that must stay in scope so the next stage can continue from one approved working set instead of rescanning the workspace.

## Inputs

- `workflow/dialogue_intake_checkpoint.json`
- `workflow/dialogue_continuation_gate.json`

## Selected Versus Non-Selected Dialogue Artifacts

- Keep `solution.py` as `primary_artifact`.
- Keep `/app/script.txt`, `/app/dialogue.json`, and `/app/dialogue.dot` in `selected_candidates` and `required_attachment_paths`.
- Keep the prompt continuation note in `supporting_context_paths`. Do not bind any route in this stage.
- Carry benchmark-visible graph checks forward in `graph_requirements` so the next stage can validate reachability, edge targets, `End` paths, and `TavernChoice` branching without another broad scan.
- Put only duplicates, scratch notes, or out-of-scope helper outputs in `non_selected_candidates`.

## Write `workflow/dialogue_working_set.json`

Write a compact JSON record with exactly these keys:

```json
{
  "selected_candidates": [
    "solution.py",
    "/app/script.txt",
    "/app/dialogue.json",
    "/app/dialogue.dot"
  ],
  "non_selected_candidates": [],
  "primary_artifact": "solution.py",
  "required_attachment_paths": [
    "/app/script.txt",
    "/app/dialogue.json",
    "/app/dialogue.dot"
  ],
  "supporting_context_paths": [
    "workflow/dialogue_continuation_gate.json",
    "workflow/dialogue_intake_checkpoint.json"
  ],
  "graph_requirements": [
    "Start is the first node and every node is reachable from it",
    "Each edge target exists unless it is a terminal ending such as End",
    "Multiple paths may lead to End",
    "TavernChoice keeps at least four outgoing options",
    "Nodes keep id, text, speaker, and type where type is line or choice",
    "Edges keep from, to, and text",
    "dialogue.dot remains a digraph and renders choice nodes with a diamond shape"
  ],
  "pending_continuation_status": "approved_pending_packetization"
}
```

Replace empty or placeholder lists with the actual non-selected artifacts you reviewed. Keep the selected set narrow; do not drop the required parser files.

## Write `workflow/dialogue_scope_summary.json`

Write a short companion summary with exactly these keys:

```json
{
  "selection_basis": "Approved the parser code and required dialogue graph artifacts needed to parse /app/script.txt, write /app/dialogue.json and /app/dialogue.dot, and preserve graph-logic checks without repeated rescans.",
  "selected_count": 4,
  "non_selected_count": 0,
  "pending_obligation": "Carry the approved dialogue parser working set forward for packetization and final graph completion.",
  "review_trace": [
    "Reviewed workflow/dialogue_intake_checkpoint.json",
    "Reviewed workflow/dialogue_continuation_gate.json",
    "Confirmed solution.py remains the primary artifact",
    "Confirmed /app/script.txt, /app/dialogue.json, and /app/dialogue.dot remain selected"
  ]
}
```

Update the counts to match the actual lists. Keep `selection_basis` and `pending_obligation` short and task-specific.

## Continue to Packetization

Hand off only these exact downstream keys from the approved records:

- `selected_candidates`
- `non_selected_candidates`
- `primary_artifact`
- `required_attachment_paths`
- `supporting_context_paths`
- `graph_requirements`
- `pending_continuation_status`
- `selection_basis`

## Stop Condition

Stop after both workflow files exist, the selected dialogue parser working set is marked pending continuation, and no route has been bound yet.
