---
name: design-preflight-with-docs
description: Use when the user wants design-preflight with durable documentation, combining focused design questions with updates to the domain glossary and selective ADRs.
---

# Design Preflight With Docs

Use `design-preflight` and `domain-modeling` together. Read both skills before starting; `design-preflight` supplies the `grilling` workflow. Do not run a second interview through `grill-with-docs`.

## Composition

Forward `durable`, `conservative`, `quick`, or `open`, along with the user's context and limits, to `design-preflight`. With no mode, use its default `durable` mode. Inherit its design principles, question budget, and completion rules rather than redefining them here.

Use `domain-modeling` for terminology, glossary updates, and selective ADRs. In every mode except `open`, its proposed questions must meet the selected preflight question bar and count toward the same session budget. Documentation does not create a separate interview or justify reopening settled decisions. In `open`, retain the underlying `grilling` scope and completion rules.

When a delivery coordinator asks for a draft, forward that request so
`design-preflight` returns its questions instead of asking. Include
`domain-modeling`'s proposed questions in the same draft, and write
documentation only after the coordinator returns the user's answers.

## Documentation

Read the existing context map, relevant glossary, and ADRs when present; follow the repository's documentation locations and conventions. Missing documents are not a blocker and do not require placeholders.

As terms are resolved, record stable domain definitions using `domain-modeling`'s glossary rules and format. Offer ADRs only when its criteria are met, using its ADR format. Distinguish the chosen design from current behavior when migration or implementation is still pending.

Before writing, state the artifact's classification and location. Preserve stable terminology and decision rationale in durable documentation; keep interview transcripts, question counts, progress, and unresolved working assumptions in the conversation or temporary agent-work storage. Do not turn tentative recommendations into accepted decisions or force a document when nothing durable emerged.

## Handoff

Include links to documents created or updated alongside the preflight handoff. If none were warranted, say so briefly. Documentation does not authorize implementation, commits, or other actions beyond the user's request.
