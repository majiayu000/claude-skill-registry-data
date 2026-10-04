---
name: "open-knowledge-format"
description: "Use when creating, inspecting, validating, converting, or maintaining Open Knowledge Format (OKF) knowledge bundles made of Markdown files with YAML frontmatter, index files, logs, citations, and cross-links for human and AI-agent consumption."
---

# Open Knowledge Format Skill

## Purpose

Use this skill to create, inspect, validate, convert, and maintain knowledge bases that follow the Open Knowledge Format, abbreviated as OKF.

OKF represents knowledge as a directory of Markdown files with YAML frontmatter, normal Markdown links, optional directory indexes, optional update logs, and citations. Keep outputs useful for both humans and agents.

## When to use

Use this skill when the user asks to:

- Create an OKF bundle from project docs, schemas, APIs, metrics, runbooks, wiki pages, or notes.
- Convert existing material into OKF concept files.
- Validate whether a directory follows OKF v0.1.
- Generate OKF concept documents.
- Generate or update `index.md` files.
- Generate or update `log.md` files.
- Add citations, cross-links, examples, tags, or schema sections to OKF documents.
- Design an agent-readable knowledge catalog for software, data, product, or enterprise knowledge.

Do not use this skill for ordinary Markdown writing unless the user explicitly wants OKF-compatible knowledge files or bundle design.

## Source of truth

Use the OKF v0.1 rules below as the working baseline. When exact format details matter, consult the upstream OKF references linked from `README.md`.

Prefer local package files for reusable content:

- `templates/concept.md` for the full concept document template.
- `examples/software-project-okf/` for a minimal OKF bundle example.

## OKF v0.1 essentials

### Bundle

An OKF bundle is a self-contained directory tree of Markdown files. It can live in a Git repository, a subdirectory, a zip/tar archive, or a static filesystem location.

### Concept document

A concept is one unit of knowledge represented by one Markdown file.

The concept ID is the file path inside the bundle without the `.md` suffix.

Example:

```text
tables/orders.md -> tables/orders
```

Every non-reserved `.md` concept file must begin with parseable YAML frontmatter.

Required frontmatter:

```yaml
type: <Concept Type>
```

Recommended frontmatter:

```yaml
title: <Human-readable title>
description: <One-sentence summary>
resource: <Optional URI for the underlying asset>
tags: [<tag1>, <tag2>]
timestamp: <ISO 8601 datetime>
```

Unknown frontmatter fields are allowed and should be preserved.

### Reserved files

The following filenames are reserved and must not be treated as normal concept documents:

- `index.md`: directory listing for progressive disclosure.
- `log.md`: chronological update history.

Hard rule for `index.md` frontmatter:

- The bundle-root `index.md` may include YAML frontmatter only to declare `okf_version`.
- Non-root `index.md` files must not contain frontmatter.
- Do not generate `okf_version` in subdirectory indexes such as `concepts/index.md`, `references/index.md`, or `insights/index.md`.

Valid bundle-root `index.md` version declaration:

```yaml
---
okf_version: "0.1"
---
```

Valid subdirectory `index.md` shape:

```markdown
# Concepts

## Business Concepts

- [Compliance Checking](./compliance_checking.md) - Compliance checking related concept.
```

`index.md` should primarily provide navigation. Do not place concept body content, long explanations, or source material in `index.md`; create concept files instead and link to them.

### Links

Use standard Markdown links to connect concepts.

Prefer bundle-relative links for cross-directory references because they are stable when documents move:

```markdown
[Customers](/tables/customers.md)
```

Relative links are also valid for nearby files:

```markdown
[Neighbor](./neighbor.md)
```

When generating or editing a bundle, verify internal Markdown links against the actual file tree. Broken links are warnings for consumers, but production-quality bundles should fix them before delivery.

Common path mistake to avoid:

```markdown
<!-- Wrong when target is inside the same concepts subtree -->
[Calculation Validation](../industry/calculation_validation.md)

<!-- Prefer -->
[Calculation Validation](/concepts/industry/calculation_validation.md)
```

### Citations

When a concept makes factual claims based on external or source material, add a `# Citations` section at the bottom.

Citation links may point to external URLs, bundle-relative files, or files under a `references/` directory.

## Workflows

### Create an OKF bundle

1. Identify the knowledge domain and intended consumers.
2. Propose a compact directory structure.
3. Extract candidate concepts.
4. Create one Markdown file per concept.
5. Add YAML frontmatter with at least `type`.
6. Add concise body sections such as Overview, Details, Schema, Examples, Relationships, and Citations when useful.
7. Add links between related concepts; prefer bundle-relative links for cross-directory references.
8. Generate directory-level `index.md` files when navigation matters.
9. Ensure only the bundle-root `index.md` has optional `okf_version` frontmatter; subdirectory indexes must not have frontmatter.
10. Generate or update `log.md`.
11. Validate the bundle before reporting completion.

### Convert existing material to OKF

1. Inventory the provided sources.
2. Split large documents into atomic concepts.
3. Map each concept to a file path and `type`.
4. Preserve source references in `# Citations`.
5. Add `title`, `description`, `tags`, and `resource` where available.
6. Add cross-links rather than duplicating repeated explanations.
7. Generate indexes and logs.
8. Verify generated links against the final file tree.
9. Report converted files, skipped material, assumptions, and follow-up gaps.

### Validate an OKF bundle

Check these items:

- All Markdown files are UTF-8.
- Reserved files are handled as `index.md` or `log.md`.
- Every concept file starts with parseable YAML frontmatter.
- Every concept frontmatter has a non-empty `type`.
- Recommended fields are present where useful.
- The bundle-root `index.md` may have `okf_version` frontmatter.
- Non-root `index.md` files do not have frontmatter.
- `index.md` files focus on navigation and progressive disclosure.
- Markdown links are syntactically valid.
- Internal links resolve against the actual bundle file tree.
- Broken links are warnings for consumption, but should be fixed before delivery when possible.
- `log.md` date headings use `YYYY-MM-DD`.
- External claims have citations.

Return validation results using this structure:

```markdown
# OKF Validation Report

## Summary

## Errors

## Warnings

## Recommendations
```

### Generate index.md

For each directory:

1. Read direct child concept files and subdirectories.
2. Extract `title` and `description` from frontmatter where available.
3. Group entries by type or subdirectory.
4. Use relative links within the same directory and bundle-relative links for cross-directory references.
5. Keep entries concise.
6. Do not add frontmatter to non-root `index.md` files.
7. Do not use `index.md` as a concept article or long-form content page.

### Generate log.md

For each relevant directory:

1. Put newest entries first.
2. Use ISO date headings, for example `## 2026-06-16`.
3. Use short bullets.
4. Link to affected concept files.

## Output rules

- Keep one concept per file.
- Keep concept bodies concise and structured.
- Use clear Markdown headings, tables, and lists.
- Preserve producer-defined frontmatter fields.
- Tolerate unknown `type` values.
- Do not invent a mandatory type registry.
- Do not replace domain-specific formats such as OpenAPI, SQL DDL, Protobuf, or Avro; link to or cite them instead.
- Do not embed secrets, credentials, private tokens, or sensitive internal URLs.
- Use citations for source-backed claims.
- Prefer links over duplicated content.
- Prefer bundle-relative links for cross-directory concept references.
- Treat `index.md` as navigation and `log.md` as traceability.
- Never add YAML frontmatter to non-root `index.md` files.

## Recommended type names

OKF does not require a central type registry. Use descriptive type names, such as:

- `Database Table`
- `BigQuery Table`
- `Dataset`
- `Metric`
- `API Endpoint`
- `API Schema`
- `Business Concept`
- `System`
- `Module`
- `Component`
- `Runbook`
- `Playbook`
- `Decision`
- `Reference`
- `Policy`
- `SOP`

When reading an OKF bundle, treat unknown types as generic concepts.

## Quality checklist

Before finalizing OKF output, verify:

- The bundle or file paths are clear.
- Concept files have required frontmatter.
- Reserved files are not accidentally treated as concepts.
- Only the bundle-root `index.md` has optional `okf_version` frontmatter.
- Subdirectory `index.md` files have no frontmatter.
- `index.md` files are navigational and not concept bodies.
- Internal links resolve correctly.
- Links are useful and not excessive.
- Citations are present for factual source material.
- The result can be read by humans and selectively loaded by agents.
- Long examples or templates are placed in `templates/` or `examples/`, not duplicated inside this skill file.
