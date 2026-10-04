---
name: architecture-viewer
description: Open or update an architecture diagram with the selected builtin or custom viewer, preserving a neutral session handoff. Use when asked to inspect architecture interactively or continue an existing diagram session.
---

# Architecture viewer

1. Inspect selection with citizen integrations show architecture-viewer --json. Use an explicit
   invocation override only when requested. Report unavailable implementations; never silently
   change the selection or install an alternative.
2. Run citizen integrations doctor architecture-viewer to obtain the selected adapter's actual
   capabilities. Missing required capabilities are errors, not evidence that a different viewer
   was selected.
3. Prepare an authorized immutable snapshot. For the upstream adapter use architecture-diagram
   profile 1, an explicit project root, optional source/metrics roots, and the SHA-256 of the exact
   profile bytes. Keep the profile and roots inside that project unless the user pre-authorized an
   additional adapter root. Preserve missing observations; report projection omissions.
4. Validate with citizen viewer validate --input INPUT_JSON, then invoke citizen viewer open
   --input INPUT_JSON. Record the returned session_reference, adapter, document identity,
   revision, digest, actual capabilities and mapping/evidence paths.
5. For an update, query citizen viewer status --session REFERENCE, prepare a new immutable input,
   then use citizen viewer replace-document --session REFERENCE --input REPLACEMENT_JSON
   --request-id REQUEST_UUID. Include the observed expected_revision. Only an acknowledged
   successful result means the viewer accepted the document.
6. Preserve the request ID when inspecting uncertain outcomes. A timeout is not cancellation.
   Conflicts, stale epochs, expired claims and indeterminate generation require explicit
   reconciliation; do not automatically reopen or replay source-changing work.
7. A regeneration request belongs to the current authorized workflow owner. Claim it only with
   the configured consumer identity and required capability, capture source identity, run the
   normal source-change gates, and publish with the claimed revision. Selection and viewing do
   not authorize edits. A detached viewer remains useful for viewing.
8. Put session and evidence references in the shared task handoff. Continue using the pinned
   session across runtimes, establishing native permissions anew. Close with citizen viewer
   close --session REFERENCE when the user is finished.

The complete configuration, adapter envelope, profile mapping and limitations are documented in
docs/viewer-integrations.md in the harness checkout. Runtime bindings share this procedure;
viewer selection is independent of model/provider selection.
