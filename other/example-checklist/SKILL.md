---
name: "phase-complete"
description: "Phase completion checklist -- verifies tests, integration, state, and PR readiness before marking a phase done."
---

# Phase Completion Checklist

<!-- WHY THIS SKILL EXISTS:
Agents under-report failures. When an agent says "Phase 3 complete," it often means
"I wrote the code and it looks right." This skill forces a mechanical verification
sequence that catches the gap between "looks right" and "actually works." Invoke it
at the end of every implementation phase BEFORE declaring the phase complete. -->

You have been asked to verify that the current implementation phase is ready to close.
Run through every section below in order. Do NOT skip steps. Record results inline.

---

## 1. Code Completeness

- [ ] All tasks listed in the phase scope (from your agent definition) are implemented.
- [ ] No TODO, FIXME, or HACK comments were left behind (unless explicitly deferred).
- [ ] No placeholder or stub implementations remain (empty function bodies, `pass` statements, `// TODO`).
- [ ] All new files have been staged. Run `git status` and verify nothing is untracked.

## 2. Tests Pass

Run the full test suite for your territory. Record the output.

**Backend:**
```bash
cd apps/backend && python -m pytest tests/ -v --tb=short
```

**Frontend:**
```bash
cd apps/frontend && npm run test
```

- [ ] All tests pass (zero failures, zero errors).
- [ ] No tests were skipped unless documented in your agent memory with a reason.
- [ ] New code has corresponding test coverage (endpoints have happy + error path tests, components have render tests).

## 3. Lint and Type Check

**Backend:**
```bash
cd apps/backend && ruff check . && ruff format --check .
```

**Frontend:**
```bash
cd apps/frontend && npx tsc --noEmit
```

- [ ] Zero lint errors.
- [ ] Zero type errors.

## 4. Build Verification

- [ ] Docker image builds successfully: `docker compose build <service>`
- [ ] Application starts without errors: `docker compose up -d && docker compose logs <service> | tail -20`
- [ ] Database migrations run cleanly: `docker compose run --rm backend alembic upgrade head`

## 5. Integration Smoke Test

<!-- WHY: Unit tests mock system boundaries. This catches the failures that only appear
when real services talk to each other. -->

```bash
./scripts/integration-smoke-test.sh
```

- [ ] All checks pass.
- [ ] If any check fails, the failure is investigated and fixed before proceeding.

## 6. API Contract Compliance

If this phase touched any API surface (endpoints, schemas, frontend API calls):

- [ ] Implementation matches `contracts/openapi.yaml` exactly.
- [ ] No undocumented endpoints or response fields were added.
- [ ] Any necessary deviations are recorded in your agent memory under "Contract Deviations."

## 7. Agent Memory Updated

Update your agent memory with:

- [ ] Current phase marked as complete.
- [ ] Completed tasks checklist filled in.
- [ ] Files modified this session listed.
- [ ] Test results recorded (pass count, any notable findings).
- [ ] Integration verification results recorded.

## 8. PR Readiness

- [ ] All changes are committed to a feature branch (not `main`).
- [ ] Commit messages are descriptive (not "wip" or "fix stuff").
- [ ] Branch is pushed to remote.
- [ ] PR is created with a summary of changes and test results.

---

## Result

After completing all sections, summarize:
- **Phase:** [name]
- **Status:** PASS / FAIL
- **Blockers:** [list any, or "None"]
- **Notes:** [anything the next phase needs to know]

If any section fails, do NOT declare the phase complete. Fix the issue first.
