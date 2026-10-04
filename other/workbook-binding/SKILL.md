---
name: skillsbench-workbook-binding-contract
description: Type-level four-stage contract for workbook wrong-object-binding generation.
---

# Workbook Binding Contract

Use this contract skill only when binding_surface_kind identifies a workbook, spreadsheet, sheet, cell, xlsx, or Excel surface. It is a generator-side type contract, not an execution skill and not a task-specific instruction.

## Runtime Contract

Generator canonicalization derives this nested contract from the selected surface and the four stage briefs. The planner supplies the shared binding contract and concrete artifact paths; materialized stages consume the normalized contract below. Do not create a second contract shape inside a stage schema.

~~~json
{
  "canonical_terminal_sink_handle_key": "<terminal sink handle key from binding_row_keys>",
  "canonical_non_self_source_handle_key": "<non-self source key from binding_row_keys>",
  "checked_sink_collection_key": "<key listing checked sinks>",
  "binding_table_invariants": {
    "exact_non_self_binding_count": 1,
    "terminal_sink_requires_non_self_source": true,
    "all_other_checked_sinks_require_self_source": true
  },
  "resolved_state_key": "resolved_workbook_state",
  "packet_artifact": "<one binder JSON output>",
  "writer_authority_mode": "packet_only",
  "writer_allowed_non_packet_inputs": ["<declared final writer template input>"],
  "writer_forbidden_input_artifacts": ["<binding note>", "<raw source or expected fixture>"],
  "writer_receipt_artifact": "<final writer receipt JSON output>",
  "writer_receipt_required_keys": [
    "packet_artifact",
    "packet_sha256",
    "terminal_sink_handle",
    "non_self_source_handle",
    "written_sink_value"
  ]
}
~~~

The nested workbook contract is the runtime authority. Keep packet_artifact to exactly one JSON packet path, derive allowed non-packet inputs from the final writer artifact_input, and writer_forbidden_input_artifacts must not overlap the allowed list.

Make expected_trace_markers executable: the binder stage includes its exact packet path and the writer stage includes its exact receipt path.

## Stage 1

Observe the live workbook surface only. Publish the observed sink handles, checked-sink collection, and workbook layout facts needed by the note. Do not calculate the final value or prewrite later-stage artifacts.

## Stage 2

Resolve the workbook write state once. Use the designated binding table and provenance only inside this stage, then publish `resolved_workbook_state` with opaque cell/write handles, formula or value payloads, workbook render metadata, and a revision. Keep non-target checked sinks self-bound. Do not carry the binding table, source handles, candidate fragments, or target-versus-source comparisons into the stage-2 handoff.

## Stage 3

Reload only `resolved_workbook_state` from the note and write exactly packet_artifact as the primary output. Copy the resolved write state faithfully; do not dereference a source fragment, rediscover workbook layout, infer formula families, or recompute workbook truth. Any sidecar belongs inside that packet as a named field, not as an alternate packet authority.

## Stage 4

Use packet_only authority. Consume packet_artifact plus only writer_allowed_non_packet_inputs, write the output workbook, then emit writer_receipt_artifact carrying every writer_receipt_required_keys value. Do not reopen the raw source, binding note, or expected fixture.

