---
name: to-issues
description: Breaks a PRD, plan, or feature document into local-first vertical slice issues with clear implementation notes. Use when work needs to become independently implementable markdown issues before TDD, prototyping, or scoped execution.
---

# To Issues

Break a PRD, plan, or feature document into small vertical slice issues that can be implemented without rediscovering the whole product context.

Default output is local markdown under `docs/agents/issues/`.

Remote issue publishing is optional and requires explicit user request.

## Read First

Gather source material:

- PRD or plan path provided by the user,
- current conversation,
- `docs/agents/issue-tracker.md`,
- `docs/agents/domain.md`,
- `docs/agents/test-commands.md`,
- `CONTEXT.md`,
- relevant ADRs,
- existing issues if the repo already has local issue docs.

If the source PRD or plan is missing, ask for it. Do not invent scope.

## Output Location

Default directory:

```txt
docs/agents/issues/
```

Recommended file naming:

```txt
0001-short-action-title.md
0002-short-action-title.md
```

If the repo already has a local issue convention, use it.

Before creating files:

- present the issue list,
- present target paths,
- ask for approval.

## Workflow

### 1. Understand The Source

Summarize:

- product goal,
- acceptance criteria,
- constraints,
- known non-goals,
- verification expectations.

If source material conflicts with repo docs or ADRs, surface the conflict before slicing.

### 2. Draft Vertical Slices

Create slices that deliver narrow end-to-end value.

Each issue should usually include:

- user-visible or caller-visible behavior,
- data or state change if relevant,
- API, UI, CLI, or module surface if relevant,
- test or verification path,
- documentation update if needed.

Avoid horizontal layer issues such as:

- backend only,
- frontend only,
- tests only,
- schema only,
- refactor only,
- documentation only.

Exceptions are allowed only when a dependency is genuinely standalone, such as a migration prerequisite or shared test harness. Explain the exception.

See `references/vertical-slice-guide.md`.

### 3. Order And Dependencies

Order issues so each one can be implemented with minimal blocked work.

For each issue, identify:

- dependencies,
- whether it can start immediately,
- whether it needs human decision before implementation,
- whether it should be a prototype instead of production work.

Prefer many small slices over a few large ones.

### 4. Present Before Writing

Show a numbered list:

```md
1. <title>
   Type: implementation / prototype / decision
   Depends on: none or issue title
   Value: one sentence
   Verification: one sentence
   Target path: docs/agents/issues/0001-title.md
```

Ask:

- Is the granularity right?
- Are dependencies correct?
- Should any issue split, merge, or move out of scope?

Do not write files until the list is approved.

### 5. Write Issue Files

Each issue file must include:

```md
# <Issue Title>

## Problem

## User Impact

## Scope

## Out Of Scope

## Acceptance Criteria

## Suggested Implementation Notes

## Verification Commands
```

Use `references/local-issue-template.md` for the full template.

### 6. Suggested Implementation Notes

Every issue should include practical implementation notes:

- likely files or areas,
- important constraints,
- allowed scope,
- forbidden scope,
- suggested order of work,
- expected output.

The notes should be specific enough to reduce rediscovery, but not so rigid that they block reasonable implementation choices.

### 7. Keep Issues Independent

Each issue should:

- reference parent PRD or plan,
- include its own acceptance criteria,
- include verification commands or unknowns,
- avoid relying on hidden conversation context,
- state dependencies explicitly.

If an issue cannot stand alone, rewrite or merge it.

## Safety Rules

- Do not publish remote issues unless explicitly asked.
- Do not overwrite existing local issue files without approval.
- Do not run destructive git or filesystem commands.
- Do not close or modify parent documents.
- Keep Windows paths quoted when showing commands.

## Verification

Before finishing:

- List created or proposed issue files.
- Confirm every issue has all required sections.
- Confirm no horizontal slices remain without explanation.
- Confirm verification commands are present or marked unknown.
- Recommend next step: usually `tdd`, `prototype`, or `handoff`.
