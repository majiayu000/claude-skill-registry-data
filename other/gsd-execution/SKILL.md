---
description: Execute work in GSD order — triage, map, plan, decide, implement, validate, close
---

# GSD Execution

## Workflow Sequence

1. **Triage**: `/project:gsd-triage` — create NID, classify, break down
2. **Map**: `/project:mapcodebase` — understand repo context
3. **Spec**: `/project:bmad-spec` — define scope and acceptance criteria
4. **Decide**: `/project:arch-adr` — record architectural decisions
5. **Implement**: `/project:impl` — make the changes
6. **Validate**: `/project:test-full` — run tests and verify
7. **Close**: `/project:session-close` — persist state, write handoff

## Rules

- Every phase must leave state behind in `vault/`
- No phase should depend on chat history alone
- Each commit should be atomic and independently deployable
- Always check `.planning/REQUIREMENTS.md` for alignment
- Update `.planning/STATE.md` when project-level progress is made

## State Files

| File | Updated By |
|------|-----------|
| `vault/10-Queue/<NID>.md` | gsd-triage, impl |
| `vault/20-Specs/<NID>-spec.md` | bmad-spec |
| `vault/30-Architecture/ADR-*.md` | arch-adr |
| `vault/90-Index/Active NIDs.md` | gsd-triage, session-close |
| `.planning/STATE.md` | session-close (if project progress) |

## Alternative Workflows

**Quick fix** (no spec/ADR needed):
1. `/project:gsd-triage`
2. `/project:impl`
3. `/project:test-full`
4. `/project:session-close`

**Audit only** (no implementation):
1. `/project:start`
2. `/project:gsd-triage`
3. `/project:docker-doctor` or `/project:workflow-audit` or `/project:secrets-scan`
4. `/project:session-close`
