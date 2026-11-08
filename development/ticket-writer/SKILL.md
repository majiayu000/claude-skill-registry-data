---
name: ticket-writer
description: Create GitHub Issues from a plan document (research checklist, testing plan, or implementation plan). Uses the issue templates in .github/ISSUE_TEMPLATE/. Sets labels, milestones, and blocked-by references.
---

# Ticket writer

Create GitHub Issues from a plan document.

## Input

One of:
- `dev/versions/vN/builds/UC-XXX-label/research-checklist.md` → creates research tickets
- `dev/versions/vN/builds/UC-XXX-label/testing-plan.md` → creates test stub tickets
- `dev/versions/vN/builds/UC-XXX-label/implementation-plan.md` → creates implementation and post-impl tickets

Or a single light build (bug fix or small change) → one `light-build.md` issue.

Also needs:
- The flow tracker issue number of the build (not for a light build).
- The UC identifier (e.g., UC-001) for the `uc:XXX` label.
- The active version (`dev/versions/README.md`) for the milestone `vN`.

## Process

### 1. Read the plan document

Extract each item that needs a ticket: questions, test stubs, implementation steps,
or post-impl tests.

### 2. Create issues using `gh`

Use the GitHub CLI to create issues. For each item:

```bash
gh issue create \
  --title "Phase: description" \
  --label "phase:xxx,uc:XXX" \
  --milestone "vN" \
  --body "..."
```

The body follows the matching template in `.github/ISSUE_TEMPLATE/`:
- Research questions → `research-ticket.md` (includes a Mermaid sequence diagram
  showing the UC flow with the relevant step highlighted)
- Test stubs → `test-stub-ticket.md`, plus the label `tier:ci` or `tier:eval` from the
  testing plan. Manual-tier ACs get no ticket.
- Implementation steps → `implementation-ticket.md`. Fill **Test author** from the
  matrix and the **LLM boundary** block from the plan's LLM boundary table.
- Post-impl tests → `post-impl-test-ticket.md`
- Light build → `light-build.md`, label `build:light`; add its row to
  `dev/versions/vN/builds/_light/traceability-matrix.md`.

For **research tickets**, the flow diagram is generated from the flow model in the
research checklist. The same base diagram is reused across related questions — only
the highlighted `rect` moves to the step each question comes from.

### 3. Set dependencies

Add `Blocked by #N, #N` in the issue body, referencing:
- Research tickets blocked by other research tickets
- Test stub tickets blocked by research decisions
- Implementation tickets blocked by test stubs and other implementation tickets
- Post-impl test tickets blocked by implementation tickets

### 4. Update the flow tracker

Add each created issue to the flow tracker issue body under the correct phase.

### 5. Update the local mirror

Update `dev/versions/vN/builds/UC-XXX-label/flow-tracker.md` with the new ticket numbers.
Update the source plan document's ticket column with issue numbers.
Update `dev/versions/vN/builds/UC-XXX-label/traceability-matrix.md`: fill the Test and Impl columns with
the new ticket links. Before finishing, run the matrix's no-orphan check — no test
or implementation ticket may exist without a matrix row (see WORKFLOW.md
"Traceability"). Keep ticket bodies to a matrix-row reference (FR/AC id + link)
rather than restating requirement text (WORKFLOW.md "Document rules").

## Ticket rules

Implementation tickets must be executable by a flash model or by a developer who does
not check their own work (WORKFLOW.md "Ticket rules"):

1. One concern per ticket.
2. Exact file paths.
3. Input/output contract with types.
4. Test command as acceptance criteria.
5. Do NOT section with explicit boundaries.
6. Blocked by prerequisites.
7. Context section with the existing files the implementer needs.
8. Maximum 3 files changed.
9. Test author named.

## Separation rule

The test author of an FR must not implement it (WORKFLOW.md "Phase 4"). When the PO
assigns tickets, or when asked to suggest assignees, check every implementation ticket
against the matrix's Test author column and flag any conflict. Light builds are exempt.

## Linking convention

All cross-references must be clickable Markdown links (see WORKFLOW.md "Linking
convention"). At the start, derive the repo base URL:

```bash
git remote get-url origin
# https://github.com/{owner}/{repo}.git → base = https://github.com/{owner}/{repo}
```

Apply to every output:

- **Issue bodies — Deliverable section:** use
  `[dev/research/topic.md]({base}/blob/main/dev/research/topic.md)`.
- **Local plan files** (checklist, flow tracker): update Ticket column and `#N`
  references to `[#N]({base}/issues/N)`.
- Issue-to-issue references (`Blocked by #N`) stay as `#N` in issue bodies because
  GitHub auto-links them. Only local `.md` files need full links.

## Rules

- One milestone per version, `vN`. Create it if it does not exist (normally done in
  Phase 0): `gh api repos/{owner}/{repo}/milestones -f title="vN"`.
- Create labels first if they do not exist (WORKFLOW.md "Labels").
- The agent writes the tickets; the PO approves them before any is assigned.
- Always reference the flow tracker issue in every ticket body.
- Number tickets in dependency order so that blocked-by references point to
  lower-numbered issues.
