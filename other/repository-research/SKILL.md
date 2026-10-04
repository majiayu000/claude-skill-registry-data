---
name: repository-research
description: Use when tracing local code, behavior, dependencies, seams, tests, or repository conventions before a substantial change or technical plan. Do not use for implementation, open-ended web research, technical proposals, or delivery planning.
---

# Repository Research

Trace local code and produce reviewable evidence before substantial planning.
The default workflow is read-only and works without background delegation.

## Boundaries

- Do not implement, refactor, format, generate files, or change configuration.
- Do not propose architecture or APIs beyond the evidence needed to hand off to
  `technical-design`.
- Do not create tickets, estimates, milestones, or delivery sequencing; hand
  an approved in-chat research brief to `spec-workflow` when the work needs a
  durable SPEC.
- Do not become open-ended web research. Use external sources only to verify a
  named dependency, API, or claim when local evidence is insufficient.
- Never inspect, quote, infer from, or reproduce credentials, tokens, private
  keys, `.env` contents, auth/session data, personal data, or sensitive logs.

## Research workflow

### 1. Set scope and stopping criteria

State the question, affected behavior, likely repository area, and what decision
the findings must support. Identify the smallest evidence set that will answer
the question. Do not explore unrelated code merely because it is nearby.

### 2. Establish repository context

Read applicable instructions, architecture/context documents, ADRs, entry
points, configuration, and tests. Use existing names and conventions. Record
the repository revision when it materially affects the finding.

### 3. Trace evidence

Trace relevant symbols through callers, data flow, boundaries, dependencies,
error paths, configuration, and tests. Identify the observable seam and classify
dependencies as in-process, locally substitutable, remote-but-owned, or
external when that distinction affects planning.

For each material claim, retain a path and line reference or a stable primary
source URL. Label it as a fact, inference, assumption, or unknown. Validate
claims with the narrowest safe search, inspection, or existing test evidence.

### 4. Propose the reviewable artifact

Before writing, present the proposed Markdown path, purpose, scope, and
sensitivity assessment. Preview the artifact outline and request explicit
approval for that target. Do not create directories, temporary files, notes, or
reports implicitly.

If approval is denied, return the evidence in chat and state that no artifact
was written. Do not claim persistence that did not occur.

### 5. Write once after approval

When approved, create one reviewable Markdown artifact using the repository's
existing notes convention. If none exists, ask the user to approve a sensible
path. Include only sanitized evidence:

```markdown
# Research: <question>

## Scope and Revision

## Evidence

## Trace and Dependencies

## Tests and Observable Seams

## Facts, Inferences, and Unknowns

## Planning Implications

## Open Risks and Follow-Ups
```

Do not include secret-derived values, hashes, lengths, distinctive substrings,
or raw sensitive logs. Use a typed placeholder such as `[REDACTED_TOKEN]` only
when the omission itself is necessary to explain a boundary.

### 6. Hand off without planning prematurely

Summarize what is known, what remains uncertain, and whether evidence is enough
to proceed. Hand off technical proposals to `technical-design` and a durable
work request to `spec-workflow` only after the artifact or approved in-chat
brief is reviewable, and only when those companion skills are available.
