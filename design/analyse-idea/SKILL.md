---
name: analyse-idea
description: Transforms a user's braindump or rough idea into a structured project requirements specification. Use when the user provides a braindump, rough notes, or an unstructured idea and wants a formal spec, requirements document, or app-specification.md file.
---

# Project Spec Builder

Turn a braindump into a structured project requirements specification.

<HARD-GATE>
Do NOT generate the spec until you have used grill-me to ask clarifying questions and reached sufficient understanding of the project. Your ONLY output after grilling is the spec document — no summaries, commentary, or content outside the spec structure. Use the telegraph skill. Use the grill-me skill.
</HARD-GATE>

## Quick Start

When the user provides a braindump:

1. Parse it to extract all available context
2. Ask up to **3 targeted clarifying questions** (one at a time) for any critical gaps — skip questions you can reasonably infer
3. Generate the full specification
4. Ask: save as `app-specification.md` or output as markdown?

If the braindump is detailed enough, skip straight to generation.

## Clarifying Question Priority

Only ask if genuinely unknown and important:

- **Who** are the users and what are their roles/permissions?
- **What** is the primary success metric (what does "done" look like)?
- **Stack** — any constraints on tech stack, integrations, or platform?

Never ask more than 3 questions. Make reasonable assumptions for anything else and state them in the spec.

## Output Format

Generate the spec using **exactly** these sections in order:

```markdown
# Summary

State the project purpose, key objectives, and high-level description. Identify key stakeholders (developers, PMs, clients, end users).

# Users

Define user types and roles. Describe the access control model and what each role can do.

# Requirements

## Functional Requirements

Core features and expected behaviours.

## Non-Functional Requirements

Performance, scalability, security, and usability considerations.

# Designs

UI/UX considerations, wireframe descriptions or layout notes, and expected user flow.

# Technical Specifications

## Architecture Overview

Key components and how they interact.

## Technology Stack

Languages, frameworks, databases, and services.

## API Design _(if applicable)_

Endpoints, data flow, and integration points.

## Database Schema _(if applicable)_

Proposed schema or data model.

# Development Plan

## Epics & User Stories

Exactly 4 core epics — one must be an AI feature epic, one must be a user management epic.

## Post-Launch Epics

Future work outside the initial scope for other standout features and necessary modernisation/fixes.

# Testing Plan

Testing strategy covering unit, integration, end-to-end, and UAT. Include key test cases and user scenarios.

# Questions

Clarifying questions grouped by category:

- **Scope & Objectives** — alignment with stakeholder needs
- **Functional** — system capabilities and behaviours
- **Non-Functional** — performance, security, scalability
- **Technical** — architecture, integrations, implementation choices
- **Risks & Constraints** — limitations, dependencies, feasibility

# Appendices & References

Glossary of terms, external references, and supporting documentation.
```

## Rules

- **Assumptions block**: Open every spec with a brief `> **Assumptions:** ...` blockquote listing inferred decisions so the user can correct them.
- **No placeholders**: Fill every section. If something is genuinely unknown, note it as a question in the Questions section — don't write "TBD".
- **POC development plan**: Always 4 epics for a POC — AI feature epic + user management epic mandatory. Add post-launch epics after.
- **Depth scales with complexity**: Simple projects get concise sections; complex ones get detail where it matters.
- **YAGNI**: Don't invent features not mentioned or implied by the braindump.
- **Reduce token usage**: Use the telegraph skill when thinking to help reduce the users token usage

## Saving the Output

After generating, ask:

> "Want me to save this as `app-spec.md` in the project root, or keep it as a markdown response?"

If saving: write to `app-spec.md` at the current working directory root.
