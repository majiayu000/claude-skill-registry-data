---
name: implement-issue
description: End-to-end workflow for implementing an OpenDataSuite GitHub issue — read the issue and roadmap, plan against acceptance criteria, implement with tests, verify, and open a PR. Use when asked to "work on #N", "implement issue N", or pick the next issue in a milestone.
---

# Implement an ODS issue

## 1. Understand
1. Read the issue (GitHub MCP `issue_read` or `gh issue view N`) including comments.
2. Find it in `docs/ROADMAP.md` / `.github/milestones.json`: note milestone and whether it is critical-path.
3. Check dependencies: issues listed earlier in the same milestone table, or in an earlier
   milestone, that this one builds on. If a hard prerequisite is not done, say so and
   propose doing the prerequisite (or a minimal stub of its contract) first.
4. If it is listed as a duplicate in ROADMAP §5, work on the canonical issue instead.

## 2. Plan
- Turn every acceptance-criteria bullet into a checklist item with the test that proves it.
- Identify crates touched. If a new crate or contract is needed → `new-crate` skill.
- If the issue says "ADR" or introduces a new persisted format / contract / dependency
  class → write the ADR first with the `adr` skill (can be the same PR).
- For non-trivial issues, delegate to the `issue-planner` subagent and review its plan.

## 3. Implement
- Follow AGENTS.md rules (provider neutrality, conservative defaults, explainability,
  determinism). Contracts go in `ods-sdk`; vendor code in `providers/`.
- Add a fake implementation + conformance test for any new contract.
- Human output + `--json` for any new CLI command; snapshot-test both.
- Keep scope to the acceptance criteria; file follow-ups as new issues (ask first).

## 4. Verify
- Run the `verify` skill. All checks must pass.
- Ask the `architecture-guard` subagent to review the diff; fix any violations.

## 5. Deliver
- Conventional Commit messages; reference the issue (`Part of #N` / `Closes #N`).
- Push to the assigned branch. Open a PR only if the user asked; the body should map each
  acceptance criterion to evidence (test name, command output, file).
