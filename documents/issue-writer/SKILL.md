---
name: issue-writer
description: Write or groom GitHub issues to the "executable cold" standard — template sections, testable acceptance criteria, correct labels and blocked-by links. Use when filing issues, promoting stubs, or grooming the backlog.
---

# issue-writer

CLAUDE.md rule 7: every issue must be executable by a fresh session with zero
chat context. The task template (`.github/ISSUE_TEMPLATE/task.md`) is
normative; this skill is how to fill it so that's actually true. All GitHub
work goes through `gh`.

## The five sections

1. **Context** — why this exists, linking the governing ADR or design doc. The
   test: could a session with no chat history make the right judgment calls
   from this section alone? Decisions already made (and by whom) go here, not
   in chat.
2. **Files** — the files/packages expected to change. This also determines
   `area/*` labeling, which is what makes parallel dispatch safe (disjoint
   areas only).
3. **Acceptance criteria** — testable statements, checkboxed. "Works
   correctly" is not a criterion; "`conch approve <id>` on a terminal-state
   approval exits nonzero with one error line" is.
4. **Required tests** — the tests the change must ship with. Approval-path
   changes always include the full request → notify → resolve → audit chain
   test (rule 3) — say so explicitly.
5. **Blocked by** — links to open issues that must merge first, or the word
   "nothing". Keep these true: stale blocked-by chains stall the unattended
   runner.

## Labels and milestones

- `area/*` — always, from the Files section; it gates parallel dispatch.
- `approval-path` — whenever the approval chain is touched (Nick merges).
- `agent/todo` is **human-only** (Nick's approval signal for the unattended
  runner) — never apply it yourself. `agent/ready` is machine-managed by
  `conch-agent sync` — never touch it. (Two-tag model: agent-dispatch.md.)
- Milestone: the phase it belongs to. Stubs stay stubs until their milestone
  is next (promotion rule, principal-review skill); promote by rewriting to
  this standard, not by relabeling.

## Worked example

```sh
gh issue create \
  --title "REST: GET /v1/approvals/{id} — single-approval read parity" \
  --label area/server --milestone "P2 Hardening" \
  --body-file issue.md   # the five sections above
```

Before filing, self-check: cold-executable Context; testable criteria;
Files ↔ labels agree; Blocked-by verified against open issues.
