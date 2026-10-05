---
name: agentic-markdown
description: "Maintains Markdown docs as explicit agent-readable context trees. Use when the user asks to create or update Markdown docs, split a large Markdown file, normalize or improve documentation structure, repair broken document trees, or make agent navigation explicit. Do not use for general prose editing, marketing copy, or unlinked repo-wide documentation cleanup."
metadata:
  version: "2.1.0"
  last_updated: "2026-06-02"
---

# Agentic Markdown

A simple way to organize and navigate Markdown so humans and agents can quickly find what matters without guesswork. It reveals details step by step, keeps structure clear and connections explicit, and helps you focus only on what’s relevant instead of reading everything.

## Model

- unit: one logical context block with exactly one entrypoint
- entrypoint: exactly one of `name.md` or `name/index.md`, never both
- child unit: a unit reached by one structural `Source:` link from its parent
- context link: a non-child link outside the current unit's owned `Source:` tree
- inline section: short content that remains in the current entrypoint
- extracted section: content moved to a child unit, leaving heading, description, and `Source:`

No implicit discovery. File proximity, sibling files, directory contents, and backlinks do not define structure.

## Entrypoints

Every unit entrypoint must use this format:

```md
---
title: Human Title
tags: [tag-a, tag-b]
---

# Human Title

Short overview of this unit.

## Section Name
One or two lines describing the child content.
Source: [Readable Title](./child.md)
```

Frontmatter rules:

- `title` is required, string, human-readable
- `tags` is required, flat list; it may be empty
- frontmatter title and top `#` heading should match unless preserving an existing public title is more important
- do not add frontmatter to agent-instruction files such as `SKILL.md`, `AGENTS.md`, `CLAUDE.md`, or similar agentic control files unless an explicit stronger local convention already requires it

Child targets are also entrypoints and must follow the same format.

## Source Links

`Source:` is the only structural child directive.

Required form:

```md
## Section Name
One or two lines explaining why this child exists.
Source: [Readable Title](./relative-entrypoint.md)
```

Rules:

- must be under a section header
- must have a useful one- or two-line description before it
- must use a Markdown link with readable label text
- must use a relative path
- must point to a valid unit entrypoint
- must not point to non-child context documents, independent sibling units, URLs, anchors, or unlinked nearby files

Semantics:

- defines the tree hierarchy for owned child units only
- participates in primary traversal
- is only for owned child units in the primary traversal tree
- is eligible for recursive descent when relevant
- order follows the `Source:` line order in the file

## Context Links

Context links are explicit and not part of the current unit's owned `Source:` tree. They may point inside or outside the wiki.

Use `Dependencies` for non-child documents required for correct interpretation:

```md
## Dependencies

| Document | Purpose |
|---|---|
| [Glossary](../glossary.md) | Defines required terms |
```

Use `Related` for non-child documents that provide optional expansion:

```md
## Related

| Document | Purpose |
|---|---|
| [Patterns](../patterns.md) | Alternative approaches |
```

Rules for both tables:

- must be Markdown tables with exactly `Document` and `Purpose` columns
- each row must include one relative Markdown link and a short purpose
- links must not be children of the current unit
- links may point inside or outside the wiki
- links are context links, not structural hierarchy

### Inline Links

Ordinary Markdown inline links are allowed for local references, citations, examples, or supporting material that do not define a unit-level relationship.

Do not force every non-child link into `Dependencies` or `Related`.

- promote an inline link to `Dependencies` when the linked document is required to correctly understand the unit
- promote an inline link to `Related` when it is useful optional context for the whole unit or section
- promote an inline link to `Source:` only when it is an owned child unit

Read `Dependencies` only when ambiguity, undefined terms, or correctness needs require them. Read `Related` only when more context, comparison, or exploration is useful.

## Traversal

Follow this algorithm:

1. Open the entrypoint.
2. Read frontmatter, overview, section headers, descriptions, and link labels.
3. If sufficient, stop.
4. For each relevant `Source:`, open the child entrypoint.
5. If ambiguity or missing prerequisite remains, open relevant `Dependencies`.
6. If still incomplete or expansion is useful, open relevant `Related`.
7. Never scan sibling files, directories, or unlinked files.

Choose relevance from section headers, descriptions, link text, target tags, and the current task. Do not auto-expand every child, dependency, or related document.

## Transform Procedure

1. Check the user request, explicit local constraints, and current linked graph for contradictions. If a real conflict remains, stop and ask for resolution.
2. Identify the unit boundary from the requested entrypoint and explicit links only.
3. Choose the canonical entrypoint; if both `name.md` and `name/index.md` exist for one unit, keep one and remove or convert the duplicate.
4. Add or repair required frontmatter on every unit entrypoint.
5. Inventory sections in order. Keep short sections inline; extract only coherent topics that improve scanability.
6. Choose merge, reference, or create by this rule:

| Situation | Action |
|---|---|
| An existing owned child already matches the topic | Merge the new material into that child |
| A non-child linked document already owns the truth | Reference it with inline links, `Dependencies`, or `Related`; do not copy facts |
| The content is new, owned by the current tree, and does not fit cleanly into an existing linked document | Create a new child |
| Ownership is unclear or multiple linked documents could plausibly own the topic | Stop and ask |

7. Create a new child only when the decision rule above resolves to create.
8. For extracted topics, preserve heading identity, choose descriptive relative paths, move content into child entrypoints, and leave description plus `Source:`.
9. Convert non-child context references to `Dependencies` or `Related` tables when they are needed.
10. Validate in the order below and fix failures before finishing.

Do not split for symmetry. Do not invent missing children only to satisfy a broken link; either create the child from real inline content or remove/inline the stub.

### Contradiction Stops

When step 1 finds mutually exclusive requirements:

- make no structural edits
- name the conflicting requirements concretely
- ask the user which requirement wins
- report validation as skipped because the transform intentionally stopped
- do not treat later transform steps as ambiguous; they are not applicable until the conflict is resolved

Read an unlinked local constraint file only when the user request, brief, or entrypoint explicitly identifies it. Otherwise, unlinked nearby files remain outside the unit.

### Legacy Markdown

When converting legacy Markdown that uses multiple top-level `#` headings:

- keep or create one document-level `#` heading from the canonical entrypoint title
- convert remaining top-level topic headings to `##` sections unless they become child entrypoints
- preserve the visible heading text when extracting; only sanitize filenames
- keep heading order stable unless validation requires moving a child link

## Splitting

- keep one file by default
- split when the entrypoint becomes hard to scan or a section is a coherent reusable topic
- keep short residual sections inline when they are easy to scan and not reusable
- prefer `./topic.md` for one coherent topic
- use `./topic/index.md` only when that topic has multiple substantial subtopics that should be explicit children
- never create vague files like `part-1.md`
- sanitize filenames, not headings; `FAQ / Edge Cases` may become `faq-edge-cases.md`
- preserve source order and meaning
- never keep substantial duplicate truth inline and in a child

Folder-backed topics are just units whose entrypoint is `index.md`; directories are never traversed implicitly.

Shared reference files that are needed for interpretation but are not owned by the current tree should stay outside the tree and be listed in `Dependencies`. Do not absorb or duplicate them only to avoid a context section.

## Choosing a Content Format

Pick the simplest format that makes the content easier to scan, compare, or reuse.

| Need | Use | Good for | Avoid when |
|---|---|---|---|
| Explain one idea or give context | Prose paragraph | Overview, rationale, caveats | The content has many parallel items |
| Show a small set of related points | Bullet list | Rules, examples, properties, options | Order matters |
| Show ordered steps | Numbered list | Procedures, algorithms, setup steps | Steps are independent |
| Show pass/fail items | Checklist | Validation, review, completion criteria | Items need explanation or comparison |
| Compare things across the same fields | Table | Options, tradeoffs, decision matrices with meaningful cell values | Cells become long paragraphs or most cells are empty/unknown |
| Define terms | Definition list or table | Glossaries, field meanings, concepts | Definitions are long enough to need sections |
| Show hierarchy | Tree or nested list | File structure, ownership, parent/child relations | Relationships are not hierarchical |
| Show flow over time | Flowchart | Workflows, traversal, decision paths | The sequence is simple enough for a numbered list |
| Show states and transitions | State diagram | Lifecycle, statuses, process states | States are informal or few |
| Show many-to-many relationships | Graph diagram | Dependencies, references, system links | The graph is too dense to read |
| Show exact syntax | Code block | Templates, examples, commands, frontmatter | The content is conceptual, not literal |
| Highlight a rule or warning | Callout / short note | Constraints, exceptions, safety rules | Everything is becoming a callout |
| Present rich or sortable data | Markdown table (add a `mermaid` diagram if the shape matters) | Dashboards, large or scannable datasets, reports | A sentence conveys it |

Follow this rules:

- **Absent data is not a table.** When a comparison or dataset is named but its values are absent, write prose plus a clearly labeled data gap or measurement stub. Do not create a table skeleton with blank, `—`, `TBD`, `N/A`, or “not provided” cells, and do not invent figures.

## Validation

Before finishing, read and apply [validation checklist](./references/validation-checklist.md). This is the required final pass. Do not finish without using it.

## Backlinks

Backlinks are optional and non-canonical. If needed, generate them outside source files. They must never affect traversal or validation.

## Output

Report:

- final tree
- context sections touched
- reused existing docs
- new docs created
- validation result
- files changed
- any intentionally inline large section and why it stayed inline
