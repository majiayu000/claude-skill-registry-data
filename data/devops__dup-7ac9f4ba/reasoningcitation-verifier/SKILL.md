---
name: reasoning/citation-verifier
description: Verify each generated claim against provided sources, enforce inline citations, and prune unsupported text. Use when outputs must be strictly grounded.
---

# Citation Verifier

Capabilities
- extract_claim_atoms: split output into verifiable claim units.
- locate_source_span: find supporting spans in scoped sources.
- generate_inline_citation: attach [Source: file:line] style tags.
- prune_unsupported_claims: drop or flag claims without support.

Dependencies
- constrained-decoding (to force citation format)
- S2 (optional multi-scale selection)
- guardrails-control (optional enforcement)

Inputs
- claims or draft text, plus source chunks with refs (path + lines).

Outputs
- validated_text with inline citations
- unsupported_claims list (if any)

Usage
- Use after context-boundary-manager has produced scoped chunks; enforce that every claim cites a known span or is removed.
