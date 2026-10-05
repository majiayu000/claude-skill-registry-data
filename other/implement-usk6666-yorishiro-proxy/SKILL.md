---
description: "Load a Linear Issue and execute the full workflow from branch creation to implementation, testing, commit, and PR creation"
user-invokable: true
---

# /implement

An end-to-end workflow skill for implementing a Linear Issue through to PR creation.

## Arguments

- `/implement <Issue ID>` — Implement the specified Issue (e.g., `/implement USK-12`)

## Steps

1. **Load Issue**: Fetch Issue details with `mcp__linear-server__get_issue`
2. **Update Issue status**: Update status to "In Progress"
3. **Create branch**: Generate an appropriate branch name from the Issue
   - feat: `feat/<id>-<short-desc>`
   - fix: `fix/<id>-<short-desc>`
   - other: `chore/<id>-<short-desc>`
4. **Design review** (mandatory for any Issue that introduces a new public type, modifies an interface, or touches more than one package; **skip for** docstring-only / test-only / single-call-site fixes — note the skip reason in the user-facing plan): launch the design-reviewer agent. See "Design Review Invocation" below.
5. **Present plan to user**: Issue summary, file actions (new / modified / untouched), key resolved decisions from the design review, deferred items, unresolved questions. Get user confirmation before implementing. For trivial Issues that skipped Step 4, present a one-paragraph plan instead.
6. **Implement**: Implement code based on the plan
7. **Write tests**: Write tests for the implementation
8. **Verify**:
   - Auto-format with `gofmt -w .`
   - `make lint` (gofmt check + golangci-lint: govet / staticcheck / unused / ineffassign / gocyclo)
   - `make build`
   - `make test`
9. **Commit**: Commit in Conventional Commits format
   - Include `Refs: <Issue ID>` in the commit message footer
10. **Push**: Push to remote with `git push -u origin <branch-name>`
11. **Create PR**:
    - Review changes with `git diff main...HEAD`
    - PR title in Conventional Commits format (e.g., `feat(protocol): add HTTP handler`)
    - PR body follows the template below
    - Create PR with `gh pr create`
12. **Update Issue status**: Update status to "In Review"
13. **Report results**: Display implementation summary + PR URL

## Design Review Invocation

Read `.claude/agents/design-reviewer.md` and replace the placeholders before launching:

| Placeholder | Value |
|---|---|
| `{{SCOPE_DESCRIPTION}}` | Issue title + description + tentative file action list (new / modified) inferred from the Issue |
| `{{SPEC_REFERENCES}}` | Paths to relevant spec/design docs (`docs/rfc/envelope.md` for data path; protocol-specific RFCs; `docs/rfc/plugin-migration.md` for plugin work). Cite specific sections, not whole files. |
| `{{PACKAGES_TO_SURVEY}}` | Packages the new code creates, modifies, or depends on |
| `{{COMPLETED_CONTEXT}}` | One-paragraph summary of relevant existing public surface this Issue will integrate with (types/functions, not the whole architecture) |
| `{{PRODUCT_IDENTITY}}` | Read from `.claude/skills/review-gate/SKILL.md` Phase 1-4 "Product context" block — single source of truth |
| `{{PRINCIPLES}}` | The MITM Implementation Principles from `CLAUDE.md` (the 6-item list). Quote verbatim. |

Launch:
```
Agent(
  description="Design review: <Issue ID>",
  subagent_type="general-purpose",
  prompt=<composed prompt>
)
```

Process the result:
- **All resolved** → fold the resolved decisions table into the Step 5 plan
- **Unresolved items exist** → present **only** the unresolved questions to the user in Step 5 with the agent's proposed answers and trade-offs. Do not ask the user about resolved questions.
- **Fitness check FAIL** → stop and report. Do not proceed to Step 5 until the scope is adjusted.

## PR Body Template

```markdown
## Summary
- <bulleted list of changes>

## Test plan
- [ ] Test items

Resolves <Issue ID>
Linear: https://linear.app/usk6666/issue/<Issue ID>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Notes

- If build or tests fail, fix the issues before re-running
- Determine implementation scope from Issue labels and description
- The design review in Step 4 already serves as the implementation plan for non-trivial Issues — Step 5 just relays it to the user
- Since build/test verification was done in Step 8, do not re-run when creating the PR
- If PR creation fails, guide the user to manually run `/pr`
- Before completing implementation, verify that the feature is accessible from the config file (no missing config struct, validation, or init function changes)
