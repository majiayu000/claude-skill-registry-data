---
name: feature-doc-splitter
description: Use when splitting rough feature notes into overview, frontend, and backend implementation docs with codebase context and contracts.
---

# Feature Doc Splitter

## Overview

Use this skill to turn an early feature note into a small documentation set that engineers can implement independently. The output is three build-ready documents: an overview document, a frontend implementation document, and a backend implementation document.

The documentation must connect the request to the real codebase, separate frontend and backend responsibilities, define shared contracts, include required Mermaid diagrams, and make unknowns explicit. For new UI surfaces, the workflow also decides whether optional Pencil placeholders should be reserved.

## When to Use

Use this skill when the user asks to:

- Split an initial feature requirement document into overview, frontend, and backend implementation documents.
- Convert rough product notes into build-ready technical documentation.
- Inspect an existing codebase before writing feature implementation docs.
- Add Mermaid business flows, interaction flows, sequence diagrams, or API contract indexes.
- Ask whether new frontend UI surfaces should reserve optional Pencil design placeholders.

## Do not use

Do not use this skill for:

- Implementing the feature code itself.
- Writing a single unsplit PRD or marketing brief.
- Designing UI visuals in Pencil.
- Backend-only API design that does not require a three-document feature split.
- Frontend-only component work that does not require overview and backend implementation docs.

## Instructions

Follow this workflow and keep the three output documents separated by owner responsibility.

## Required Output

Create or update three documents:

- Overview document: goal, background, scope, non-goals, business objects, end-to-end flow, cross-team contracts, required Mermaid diagrams, rollout plan, risks, and acceptance criteria.
- Frontend implementation document: frontend-only routes, pages, sections, components, state, hooks, API integration points, interaction states, Mermaid flows, tests, and optional Pencil placeholders for new UI surfaces.
- Backend implementation document: backend-only data model, migrations, API routes, schemas, services, validation rules, statistics formulas, jobs, notification or event creation, Mermaid flows, tests, and acceptance criteria.

The overview document must link to the frontend and backend implementation documents by project-relative paths, and it must contain Mermaid diagram code blocks.

## Workflow

1. Read repository instructions first.
   - Read the relevant `AGENTS.md` files before editing.
   - Follow local documentation style, file placement, naming, and package conventions.
   - Preserve unrelated user changes.

2. Read the initial feature note completely.
   - Identify the user goal, affected actors, business terms, ranking or statistics rules, visible UI, backend data needs, notification needs, and implied permissions.
   - Record ambiguous points as assumptions or open questions in the documents instead of hiding them.

3. Inspect the codebase before writing.
   - Use `rg` and targeted file reads to find existing pages, routes, components, hooks, generated API clients, models, schemas, services, tests, notification code, and statistics or ranking logic.
   - Prefer existing modules and conventions over new abstractions.
   - If an existing component or module can be reused, document the reuse path and do not create a design placeholder for it.

4. Define the documentation set.
   - Keep names consistent across all three documents.
   - Use project-relative links.
   - Keep frontend and backend documents independently actionable: each should be implementable by its owner without reading internal details from the other side.
   - Put shared contract facts in the overview and repeat only the consumer-facing subset needed in each implementation document.

5. Write the overview document.
   - Include total goal, business background, scope, non-goals, terminology, actor list, data ownership, API contract index, rollout phases, acceptance criteria, risks, and dependencies.
   - Always include at least one Mermaid end-to-end business flow in the overview document.
   - Include a Mermaid sequence or interaction flow when multiple systems or roles participate.

6. Write the frontend document.
   - Include routes or entry points, page or panel changes, component inventory, state model, data loading, API client usage, empty/loading/error states, permissions, i18n or copy needs, analytics if relevant, and tests.
   - Include a Mermaid frontend business logic flow and a Mermaid user interaction flow.
   - Before defining or creating any Pencil placeholders, ask the user whether they want placeholders reserved unless they already explicitly opted in or out.
   - If the user does not need Pencil placeholders, do not create `.pen` files and document the decision briefly.
   - If the user wants Pencil placeholders, define them only for genuinely new pages, views, sections, panels, blocks, or components.
   - Mark reused existing UI explicitly as "reuse existing component, no design placeholder".

7. Write the backend document.
   - Include models, migrations, API endpoints, request and response schemas, operation IDs, service classes, validation, deduplication or idempotency, permission checks, statistics formulas, events, jobs, and tests.
   - Include a Mermaid backend business or statistics flow.
   - Include a Mermaid sequence diagram when API, service, database, and event or notification systems interact.
   - Specify OpenAPI generation impact when the project uses generated clients.

8. Create design placeholders only after user opt-in.
   - Ask a concise yes/no question before creating placeholder files if the user has not already stated a preference.
   - If the user declines or says placeholders are not needed, do not create `.pen` files.
   - Create `.pen` files only for new frontend UI surfaces that require manual design later and that the user wants reserved.
   - Do not create `.pen` files for reused existing components, simple text changes, existing list rows, existing tabs, or existing entry buttons.
   - Place placeholders near the feature docs, for example `docs/features/<feature>/pencil/<surface>.pen`.
   - When the project uses Pencil `.pen` JSON files, an empty placeholder may contain only:

```json
{"version":"2.13","children":[]}
```

9. Verify the result.
   - Check links, heading consistency, Mermaid syntax, document split boundaries, and that the overview document contains Mermaid code blocks.
   - Confirm no machine-specific absolute paths were introduced unless the user explicitly requested them.
   - Validate `.pen` JSON if placeholders were created.
   - Run repository documentation or skill validators when available; otherwise run at least `git diff --check`.
   - Report the checks that were run.

## Separation Rules

- Do not put backend implementation internals in the frontend document.
- Do not put frontend component or layout decisions in the backend document.
- Do not invent new backend APIs when an existing contract is sufficient.
- When a new API is required, document method, path, operation ID, auth, request schema, response schema, errors, pagination, sorting, and frontend consumption expectations.
- When the frontend uses generated API code, require the generated client path and regeneration command instead of scattered handwritten API calls.
- Keep all paths project-relative in documentation.

## Mermaid Requirements

Use quoted Mermaid node labels when labels contain punctuation.

Minimum diagrams:

- Overview: required end-to-end business flow.
- Overview: sequence or interaction flow when multiple systems or roles participate.
- Frontend: user interaction flow.
- Frontend: frontend business logic or state flow.
- Backend: backend API/service/data flow.
- Backend: sequence or statistics flow when persistence, jobs, or events are involved.

## Final Response

Summarize the created or updated documents, list any Pencil placeholders created or intentionally removed, and report validation results. Keep the response concise.
