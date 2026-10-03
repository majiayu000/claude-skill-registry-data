---
name: verify
description: Curation review pass — Capabilities or Functionalities with confidence='extracted' awaiting Alex's verification.
allowed-tools:
  - "mcp__bigweld__find_capabilities_by_state"
  - "mcp__bigweld__find_nodes"
  - "mcp__bigweld__mark_verified"
  - "mcp__bigweld__get_node"
---

# /verify [label]

Find nodes still at `confidence='extracted'` and walk them with Alex one at a time per his interview-mode preference. Default to Capability; ask if he wants Functionality too.

For Capabilities: call `find_capabilities_by_state(state="current")` then filter results client-side for `confidence == "extracted"`. For Functionalities: call `find_nodes(label="Functionality", filters={"confidence": "extracted"})`.

For each candidate, show name + description + cliff_notes (use `get_node()` if cliff_notes isn't in the find result). Ask Alex: verify, edit, or skip. On verify: call `mark_verified(slug, label, notes=<short>)`. On edit: switch to `edit_node(label, slug, patch)` flow. On skip: move to next.

`mark_verified` is NOT confirm-gated — Alex's "yes" in conversation is the authorization.
