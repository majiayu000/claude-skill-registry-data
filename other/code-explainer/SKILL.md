---
name: code-explainer
description: Create source-backed, Notion-style standalone HTML explainers for repository features by inspecting live code first, separating implemented behavior from docs or assumptions, and validating the generated page.
---

# Code Explainer

Create polished, source-backed HTML explainers for codebase features. Use this when the user asks to explain a feature, subsystem, mode, workflow, or internal implementation as an HTML page, Notion-style page, visual doc, or shareable local artifact.

## Core Contract

Base the explainer on the live code first. Docs can support the explanation, but they do not override implementation behavior unless the user explicitly asks for a spec or product-plan explanation.

Before writing, identify:

- the feature or subsystem being explained
- the repository or checkout that actually contains the implementation
- the code paths that define behavior
- supporting docs, if any, and whether they describe implementation or intent
- the requested artifact location and format

If the implementation is not in the current working directory, inspect nearby or user-provided paths before concluding it is absent. State the source checkout used.

## Source-Backed Workflow

1. Search for feature names, command names, mode names, API method names, labels, and user-facing strings with `rg`.
2. Read entrypoints first: CLI command definitions, public crate/module exports, app routes, protocol types, feature registries, or UI command wiring.
3. Follow the behavior path from input to output: user entrypoint, config or policy loading, routing or dispatch, runtime execution, persistence or side effects, and completion, failure, or delivery paths.
4. Read tests when behavior is subtle, safety-related, or enforced indirectly.
5. Separate implemented behavior, documented intent, known limitations, and inferred architecture.

## HTML Output

Default to a standalone `.html` file with embedded CSS.

The page should feel like a Notion-style technical brief:

- clear title and concise subtitle
- metadata cards for implementation, inputs, and outputs
- short mental model section
- code-backed flow from trigger to result
- sections for configuration, runtime behavior, state, boundaries, and failure modes when relevant
- compact tables for surfaces, commands, APIs, or states
- callouts for important constraints
- final `Code Sources Used` section listing inspected files

Keep the page readable and useful. Avoid marketing copy, decorative filler, large hero layouts, or vague claims.

## Visual Style

Use restrained, document-like styling: a single centered page container, warm neutral background, white page surface, 8px border radius or less, readable system font stack, embedded responsive CSS, and tables, callouts, pills, or flow steps when they clarify the system.

Cards and compact panels must never truncate their content. Metadata cards often contain long repository paths, command names, socket paths, plugin IDs, or API names, so default card and code styling must allow wrapping:

- set `min-width: 0` on grid/flex children that contain text
- allow long inline code and path-like strings to wrap with `overflow-wrap: anywhere` or an equivalent rule
- avoid fixed-height cards for text content
- prefer wrapping over horizontal clipping for metadata, pills, labels, and callouts
- keep `pre` blocks horizontally scrollable when preserving code formatting matters

When using CSS grid for card rows, assume each card may contain a long unbroken source path or command. Confirm that the content remains readable at normal desktop widths, not only that the overall page avoids document-level overflow.

Do not use external assets, CDN dependencies, or JavaScript unless the user asks for interactivity.

## Validation

After creating or editing the page:

1. For tracked modifications, run `git diff --check -- <file>`. For new/untracked artifacts or output outside Git, inspect the generated file directly; a clean Git diff does not validate an untracked file.
2. Confirm the file exists and contains the expected title and key sections.
3. Inspect the top viewport, especially metadata cards, pills, and any inline `code` in compact panels, for clipped or truncated text.
4. If the user has the in-app browser open or asks to view it, open the local `file://` URL in the Codex in-app browser when that workflow is available.
5. Report the page path, validation result, and whether the page is untracked or modified.

Do not run unrelated test suites for an HTML-only explainer unless the page is part of an app build.

## Guardrails

- Do not cite memory as source truth for the explainer unless the user explicitly asks for prior context.
- Do not present design docs as implemented behavior without checking code.
- Do not personalize generated UI or sample copy with the user's name unless they explicitly ask.
- Do not mutate product code while creating an explainer page.
- Preserve unrelated worktree changes.
