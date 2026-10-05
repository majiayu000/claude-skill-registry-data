---
name: do-tech-docs
description: Technical documentation standards — document structure, writing style, file organisation, mermaid diagrams, and validation. Referenced by do-docs and tech-docs-writer.
user-invocable: false
disable-model-invocation: true
---

# Technical Documentation

Produce technical documentation that explains **what** systems do, **how** they interact, and **why** specific choices were made.

**Primary audience: LLMs.** These docs will be loaded into LLM context windows during development tasks. Every token must earn its place. Write for machine comprehension first — dense, precise, and structurally consistent. Avoid prose padding, narrative flow, and filler sentences that a human might appreciate but an LLM gains nothing from.

Avoid documenting business processes or product capabilities.

## Repository Type Detection

A project is a **mono-repo** if any of the following are present:

- `package.json` with a `workspaces` field
- `pnpm-workspace.yaml`
- `lerna.json`
- `Cargo.toml` with a `[workspace]` section
- `go.work` file
- Multiple `pyproject.toml` files in subdirectories
- `nx.json`
- `rush.json`

If none of these indicators are found, treat the project as a **single-repo**.

This determination controls where documentation is stored — see [File Organisation](#file-organisation).

## Documentation Principles

### Include

- **Purpose and function**: What each component does and why it exists
- **Technology choices**: What is used and why it was selected
- **Integration points**: How components communicate and depend on each other
- **Data flow**: How data moves through the system
- **Architectural patterns**: Design patterns employed and their rationale
- **Accessibility patterns**: ARIA attribute usage, focus management, keyboard navigation, screen reader support, and WCAG compliance level. Especially important for government or public-sector projects.
- **Validation and business rules**: Form validation logic, required field rules, conditional visibility, and domain constraints that the application enforces
- **Mermaid diagrams**: Every document describing interactions or flows must include at least one diagram

### Exclude

- **Implementation code**: No function bodies, algorithms, or internal logic as code blocks
- **Infrastructure configuration**: No CDK, Terraform, Docker Compose, or config file content
- **CLI commands**: No terminal commands or deployment scripts (see exception below)
- **API endpoint definitions**: No route paths, request/response schemas, or curl examples

### Include as Structured Tables (Not Code Blocks)

- **Component/module public API**: Props, parameters, exported types, and return values — documented as tables, not code snippets
- **Context/hook API surface**: What a context provider or hook exposes to consumers

### Optional: Developer Onboarding Section

When documenting a full project (not a single component), include a brief onboarding section in `architecture-overview.md` or a dedicated `getting-started.md`:

- Prerequisites (runtime versions, package manager)
- Install and run commands
- Key scripts (build, test, lint)

Keep to under 20 lines. This is the one context where CLI commands are acceptable.

## Document Structure

Every document must start with a YAML frontmatter block. This gives an LLM immediate context about what the document covers without reading the full body.

```markdown
---
title: <descriptive title>
scope: <component | service | architecture | decision>
relates-to: [list of other doc filenames this connects to]
last-verified: <YYYY-MM-DD when last checked against source code>
---

## Overview

<1-2 sentences: what this covers, stated as facts not narrative.>

## <Core Content>

<Main documentation. Use H2/H3 headings as section labels. Prefer bullet points and tables over paragraphs. Each section should be independently useful — an LLM may retrieve a single section, not the whole document.>

## Integration Points

<How this component connects to others. Include a Mermaid diagram.>

## Design Decisions

<Decision: rationale format. No preamble.>
```

### Token Budget

Docs are loaded into LLM context alongside code, conversation history, and tool results. Context is finite and expensive.

- **Target: 200-500 lines per document.** If a document exceeds this, split it.
- Use bullet points and tables instead of paragraphs — same information, fewer tokens
- State facts directly: "Auth uses JWT with RS256" not "The authentication system has been designed to utilise JSON Web Tokens using the RS256 algorithm"
- Define terms inline on first use with parenthetical notation: "The gateway (API entry point handling routing and auth) forwards requests to..."
- Omit transition sentences, introductory phrasing, and summaries of what was just said
- Prefer structured lists over prose for enumerating components, dependencies, or flows

### File Organisation

#### Root-level directory structure (all projects)

```
docs/
  technical/     — root-level / cross-cutting technical docs
  product/       — product documentation (features, user guides, business context)
  maverick/      — maverick-generated project skills (if applicable)
```

#### Single-repo projects

All technical docs go in `docs/technical/` — no additional nesting required.

#### Mono-repo projects

- Cross-cutting and architectural docs go in `docs/technical/` at the repo root
- Package-specific technical docs go in `<package>/docs/` (no `technical/` subdirectory needed since package docs are inherently technical)
- Each `<package>/docs/` maintains its own `index.md` listing that package's documents
- Product docs are **never** stored at the package level — always in root `docs/product/`

#### General rules

- Create **separate files** for distinct topics rather than monolithic documents
- Use `kebab-case.md` naming (e.g. `authentication-architecture.md`)
- Each file should be self-contained but may cross-reference others via `relates-to` in frontmatter
- Maintain an `index.md` in `docs/technical/` listing all documents with one-line descriptions — this serves as the entry point for LLM context loading
- In mono-repos, root `docs/technical/index.md` should link to each `<package>/docs/index.md`

### Sizing

| Task size                           | Documentation depth                                |
| ----------------------------------- | -------------------------------------------------- |
| Trivial (config, minor change)      | 2-3 sentences in an existing doc or commit message |
| Small (single component)            | Overview + core content (under 200 lines)          |
| Medium (feature, service)           | Full document structure (200-500 lines)            |
| Large (cross-cutting, architecture) | Split into multiple focused documents              |

### Within a Document

Scale section depth to component complexity. Indicators that a component needs deeper coverage:

- File exceeds 300 lines
- Contains business/domain logic (rule engines, calculations, transformations)
- Has multiple distinct output modes (e.g., screen rendering, PDF export, print view)
- Serves as an aggregation point for data from multiple sources

For these components, document each distinct responsibility separately rather than summarising the whole.

## Mermaid Diagram Standards

Use diagrams to visualise:

- **Service interactions**: `sequenceDiagram` or `flowchart`
- **Data flows**: `flowchart` or `sequenceDiagram`
- **Architecture overviews**: `flowchart` or `C4Context`
- **State transitions**: `stateDiagram-v2`

Guidelines:

- Every diagram must have a descriptive title
- Use clear, descriptive node labels — not abbreviations or internal variable names
- Keep diagrams focused on one concept; prefer multiple simple diagrams over one complex one
- Aim for no more than 15-20 nodes per diagram

## Writing Style

- **Dense, not verbose**: State facts. Skip introductions, transitions, and conclusions. An LLM does not need to be "eased into" a topic.
- **Precise**: Use exact technology names and versions. "PostgreSQL 16 with row-level security" not "a relational database with access controls".
- **Consistent terminology**: Use the same term for the same concept everywhere. Define domain terms inline on first use.
- **Structured over narrative**: Prefer `key: value` patterns, bullet lists, and tables. Reserve prose for explaining *why* — rationale that cannot be expressed as a list.

## Validation Checklist

Before finalising documentation:

- [ ] All factual claims verified against source code
- [ ] Mermaid diagrams render correctly (valid syntax)
- [ ] No implementation code, config snippets, or CLI commands included (API surface tables are acceptable)
- [ ] Cross-references use correct relative paths
- [ ] Document is under 500 lines (split if larger)
- [ ] YAML frontmatter present with title, scope, relates-to, last-verified
- [ ] `docs/technical/index.md` updated if this is a new document (and `<package>/docs/index.md` for mono-repo package docs)
- [ ] Bullet points and tables used instead of prose where possible
- [ ] All public exports from documented modules are covered (check for multiple exports per file)
- [ ] Numbering, terminology, and facts are consistent across all documents in the set

<!-- maverick-plugin-version: 4.0.2-dev -->
