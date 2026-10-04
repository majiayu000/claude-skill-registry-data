---
name: skillsbench-form-field-binding-contract
description: Type-level four-stage contract for owner-addressable form-field wrong-object-binding generation.
---

# Form-field Binding Contract

Use this contract skill only when binding_surface_kind is form_field or another owner-addressable form-field surface. It is a generator-side type contract, not a task-specific instruction.

## Runtime Contract

Generator canonicalization derives this nested contract from the selected surface and the four stage briefs. The planner supplies the shared binding contract and concrete artifact paths. Treat this as a stage-2 resolution contract, not as a writer input: after state resolution, later stages consume the sealed current state and then its packet. Do not create a second contract shape inside a stage schema.

~~~json
{
  "canonical_terminal_selector": "<compact selector equal to designated_sink_target>",
  "selector_registry_artifact": "<stage-1 observation JSON output>",
  "selector_registry_key": "object_selector_registry",
  "binding_table_selector_key": "selector",
  "binding_table_owner_key": "<observed owner column key>",
  "checked_sink_collection_key": "checked_field_selectors",
  "binding_table_invariants": {
    "exact_non_self_binding_count": 1,
    "terminal_sink_requires_non_self_source": true,
    "all_other_checked_sinks_require_self_source": true
  },
  "packet_artifact": "<one binder JSON output>",
  "writer_authority_mode": "packet_only",
  "writer_allowed_non_packet_inputs": ["<blank form or PDF template from final writer input>"],
  "writer_forbidden_input_artifacts": ["<binding note>", "<raw source or expected fixture>"],
  "writer_receipt_artifact": "<final writer receipt JSON output>",
  "writer_receipt_required_keys": [
    "packet_artifact",
    "packet_sha256",
    "packet_revision",
    "written_field_count",
    "written_values_match_packet"
  ]
}
~~~

The terminal selector is a value, while binding_table_selector_key is a column name. They are never interchangeable. The nested form contract is the runtime authority.

## Stage 1

stage 1 owns observation only.
Observe the live form surface only. Write selector_registry_artifact and publish object_selector_registry as an exact top-level key in both the artifact schema and handoff keys. The registry maps each compact selector to its observed owner and render handle.

## Stage 2

Stage 2 owns resolution into the current local state.
Load only the exact top-level keys published in stage 1's `next_stage_consumes_exact_keys`; do not probe aliases, optional compatibility keys, or any key that stage 2 itself creates. Use `object_selector_registry`, `canonical_terminal_selector`, and any binding-table provenance only inside this resolution step. Resolve the terminal sink by selector, never by collection position, then publish one `resolved_form_state` state revision whose rows contain only an opaque writable slot or handle, the current payload, and packet-needed render metadata. Do not carry the selector registry, full binding contract/table, raw fragment catalog, source handle, alternate candidates, or an old-versus-current comparison into the stage-2 handoff.

## Stage 3

Stage 3 owns packet sealing.
Reload only the stage-2 `resolved_form_state` artifact and write exactly `packet_artifact`. Copy its current rows into the packet without reopening the selector registry, binding table, raw source catalog, blank template, or task text. Do not re-resolve a terminal owner, compare a value with an earlier value, or select any sink by ordinal position.

## Stage 4

Stage 4 owns packet-only rendering.
Use packet_only authority. Consume packet_artifact plus exactly writer_allowed_non_packet_inputs, write the final form/PDF, and emit writer_receipt_artifact with packet identity, revision, write count, and packet-write completion evidence. Do not reopen raw case text, binding notes, selector registries, source catalogs, or expected fixtures.

