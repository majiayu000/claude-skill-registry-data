---
name: adr
description: >
  Create an Architecture Decision Record in docs/decisions/ and optionally
  sync to Confluence for business projects. Use when making significant
  technical decisions. Triggers on: architecture decision, ADR, technical decision.
---

## Architecture Decision Record

### Step 1: Determine Next ADR Number
```bash
ls docs/decisions/ADR-*.md 2>/dev/null | sort -t- -k2 -n | tail -1
```
Increment by 1. Start at 001 if none exist.

### Step 2: Create ADR
Create `docs/decisions/ADR-<NNN>-<kebab-case-title>.md` with sections:
- **Status**: Proposed / Accepted / Deprecated / Superseded
- **Date**: YYYY-MM-DD
- **Context**: The challenge or decision point
- **Decision**: What was decided and why
- **Consequences**: Positive, Negative, Risks
- **Alternatives Considered**: Each with reason for rejection

### Step 3: Update Architecture Docs
Add reference in `docs/context/ARCHITECTURE.md`.

### Step 4: Sync to Confluence (Business Only)
If Confluence MCP is available, create a child page under "Architecture Decisions".
Note: canonical version is always the repo file.

### Step 5: Commit
`docs(adr): ADR-<NNN> <title>`
