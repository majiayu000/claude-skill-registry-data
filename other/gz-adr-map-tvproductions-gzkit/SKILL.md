---
name: gz-adr-map
description: Use to trace an ADR to its artifacts with gz state and repository search.
category: adr-operations
compatibility: GovZero v6 framework; manual mapping workflow
metadata:
  skill-version: "1.2.3"
  govzero-framework-version: "v6"
  govzero-author: "GovZero governance team"
  govzero_layer: "Layer 1 - Evidence Gathering"
gz_command: state
invocation: uv run gz state --json
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
model: haiku
---

# gz-adr-map

Construct ADR traceability with the available `gz` and repo-local tooling.

## Procedure

```bash
# 1) ADR/OBPI graph from ledger
uv run gz state --json

# 2) ADR -> REQ -> test coverage hop
#    Decorators are REQ-level (`@covers("REQ-X.Y.Z-NN-MM")`), not ADR-level.
#    Traceability hop is ADR -> OBPI briefs (Acceptance Criteria REQ IDs) -> @covers(REQ-...).
uv run gz covers ADR-0.3.0            # canonical traceability walker (replace with target ADR)
rg -n '@covers\("REQ-' tests          # raw REQ-decorator survey across the repo

# 3) Validate a target ADR's linked briefs
uv run gz adr audit-check ADR-0.3.0 --json
```

## Notes

<!-- gz-validate-skip: command-shape -->
- There is no dedicated `gz adr map` subcommand in this repository.
- This skill is intentionally workflow-based instead of a single command.

## References

- Command implementation: `src/gzkit/cli/` (parsers) and `src/gzkit/commands/` (command bodies)
- User docs: `docs/user/manpages/state.md`, `docs/user/manpages/adr-audit-check.md`
