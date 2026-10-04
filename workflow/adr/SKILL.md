---
name: adr
description: Scaffold an architecture decision record in architecture/decisions/ using the repo's governed ID conventions. Use when a decision needs recording or the user says /adr.
---

# /adr — record an architecture decision

1. Read `architecture/decisions/README.md` for conventions.
2. **ID selection (critical):** use `ADR-KOA-DEV-NNN` (next sequential number) for
   decisions local to this repository — harness, CI, tooling, repo layout. The
   governed `ADR-KOA-NNN` range belongs to the Koʻa baseline amendment process and
   must NOT be minted here.
3. Create `architecture/decisions/ADR-KOA-DEV-NNN-<slug>.md`:

```markdown
# ADR-KOA-DEV-NNN — <Title>

**Status:** proposed | accepted
**Date:** <YYYY-MM-DD>
**Deciders:** <who>

## Context
Why this decision is needed; constraints from the governance baseline
(architecture/governance/) that bear on it.

## Decision
The decision, stated actively. Numbered points if there are several.

## Consequences
What becomes easier/harder; follow-ups; what would trigger revisiting.
```

4. Add a row to the index table in `architecture/decisions/README.md`.
5. If the decision touches naming, include the cultural-review caveat; if it promotes
   the placeholder workflow toward a real capability, say so explicitly and reference
   ADR-KOA-DEV-001.
