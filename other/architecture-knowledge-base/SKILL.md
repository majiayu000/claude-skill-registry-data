---
name: architecture-knowledge-base
description: Creates source-backed architecture documentation shaped around the codebase and its readers. Use when asked to document a system, explain project architecture, map important flows, or turn an implementation into a navigable knowledge base.
metadata:
  category: planning-architecture
---

# Architecture Knowledge Base

Build the documentation that best explains this codebase. Do not reproduce a standard architecture pack by default. Let the system's real boundaries, risks, and reader needs determine the result.

## Use supporting skills as lenses

Load relevant skills when they are available. Useful options include:

- `domain-modeling` to resolve domain terms and maintain the shared glossary as described below
- `type-breakdown` for types, execution, effects, and errors
- `adr` for durable decisions
- `technical-writing` for structure and plain language
- `mermaid-diagrams` for visual explanations
- `coding-standards` for boundaries, dependencies, and failures
- `deslopify` or `unslop` for editing
- a knowledge-base skill for navigation and progressive disclosure

These skills offer methods, not mandatory deliverables. Use only what helps. Do not install missing skills or block the work because one is unavailable.

## Start with the codebase

Read the repository instructions, existing docs, source, tests, configuration, and relevant history. Find the questions a new maintainer would struggle to answer. Trace important behavior from real entry points to real effects.

Document the system as it exists. Use exact names from the repository. Distinguish confirmed behavior from inference, recommendation, and uncertainty whenever readers could confuse them.

Ask the user only when a missing product or architecture decision would force speculation. Answer repository questions by inspecting the repository.

## Build shared domain language

Read any existing `ai-artifacts/CONTEXT.md` or `ai-artifacts/CONTEXT-MAP.md` before naming concepts. When terms are overloaded or distinctions matter to understanding the system, load `domain-modeling` if available and use it during the source trace, not only as a final writing check.

Test the terms against concrete edge cases. Can a candidate exist without a selection? Can a target lie outside the search root? Use scenarios from the codebase to distinguish concepts that sound interchangeable. Check the answers against source and tests. Surface contradictions with existing definitions; ask only when resolving them requires a product decision.

Record resolved terms as you go in the relevant context glossary. For a single context, create `ai-artifacts/CONTEXT.md` when the first useful distinction is resolved. Keep definitions short, choose canonical names, and identify misleading alternatives. Follow `domain-modeling`'s `CONTEXT-FORMAT.md` when available. Keep runtime details in the architecture explanation, not the glossary.

Link the glossary from the architecture explanation and use its terms consistently in prose and conceptual diagrams. A small embedded domain diagram can clarify relationships without repeating the implementation flow. Create a context map only for genuinely separate contexts. Do not force a glossary, context map, or ADR when none adds useful knowledge.

## Choose the right shape

Keep agent-authored project knowledge under `ai-artifacts/` unless the user or repository requires another location.

Choose the smallest structure that explains the system well. A compact project may need one document. A larger system may benefit from separate domain context, architecture explanations, flow references, decision records, or an index. Create a navigation page only when there is enough material to navigate.

Possible artifacts include:

- a map of the system and its boundaries
- a glossary of terms that are easy to confuse
- an explanation of an important runtime flow
- a reference for types, states, effects, and failures
- a record of a durable architectural decision
- a guide that routes readers to existing documentation

This list is a menu, not a checklist. Combine, split, rename, or omit artifacts according to the codebase. Do not create empty sections, speculative prose, or documents whose only purpose is to satisfy a template.

## Follow the important ideas

Spend detail where the system earns it. Look for:

- boundaries where data, control, trust, or ownership changes
- entry points and effects that define the product's behavior
- state transitions, concurrency, retries, cancellation, or recovery
- types and validation that protect important invariants
- failure paths that operators or callers need to understand
- dependencies that constrain future changes
- decisions whose rationale is not obvious from the code

Do not give every module equal coverage. Explain the architecture, not the directory tree.

## Make evidence visible

Ground claims in source, tests, configuration, or repository history. Link to files or name symbols when that helps readers verify a statement.

Use explicit evidence labels when a document mixes different confidence levels:

```text
[existing]  Confirmed in the repository
[inferred]  Implied by the implementation
[proposed]  A recommendation, not current behavior
[?]         Unresolved
```

Do not force these markers into prose when the distinction is already clear. Never invent rationale, alternatives, line numbers, or behavior.

## Use visuals when they clarify

Add Mermaid or ASCII diagrams when a relationship, sequence, state model, boundary, or data flow is easier to understand visually. Choose the diagram from the explanation. Do not start with a required diagram inventory.

Keep each visual close to the prose it supports. Use domain language for conceptual views and implementation names for technical views. Prefer a small diagram that answers one question over a complete diagram nobody can read. Validate Mermaid that you add.

## Record decisions only when the evidence supports them

Create an ADR when a decision is hard to reverse, surprising without context, and based on a real trade-off. Keep one decision per record and connect it to related documentation.

If the repository proves what was implemented but not why it was chosen, document the implementation elsewhere or mark the rationale unresolved. Do not manufacture alternatives to complete an ADR template.

## Build useful navigation

When the work produces multiple documents, connect them with normal GitHub-compatible relative Markdown links. Put links in sentences that explain what the reader will find and why it matters. Use progressive disclosure so an entry page routes readers without repeating the detailed documents.

Add concise YAML `description` frontmatter when the repository or knowledge-base convention uses it. Keep terminology and claims consistent across the set.

Consider adding a short link from the main `README.md` when the new documentation is useful to the README's audience. Do not rewrite unrelated README content or expose secrets, credentials, private setup details, internal release procedures, or sensitive operations.

## Write for maintainers

Use plain, precise technical English. Prefer real symbols and concrete behavior over generic architecture language. Use active voice, focused paragraphs, and headings that help readers answer questions. Explain important limitations and failures directly.

The documentation should help someone reason about a change. It should not merely prove that documentation exists.

## Review the result

Review the work against its purpose rather than a fixed inventory:

- Does the structure fit this codebase and its likely readers?
- Are the important boundaries and flows easier to understand?
- Do the glossary, architecture prose, and conceptual diagrams use the same resolved domain terms?
- Can readers tell evidence from inference or advice?
- Do links, paths, symbols, and diagrams work?
- Does each artifact earn its place?
- Did the work preserve existing documentation and user changes?

Run the narrowest relevant formatting, documentation, lint, type, or test checks. Fix failures caused by the documentation change. Report unrelated or pre-existing failures without changing unrelated code.

Finish with a short account of what you created, what it helps readers understand, what you verified, and what remains uncertain. Do not commit or push unless the user explicitly asks.
