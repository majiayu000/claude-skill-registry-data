---
name: add-docs
description: >
  Write or update an illustrated documentation page in the SaaS Bootstrap
  Fumadocs site under docs/content/docs. Use for a tutorial, guide, concept or
  reference page, or a diagram explaining current code there. ADRs follow their
  own format, the API reference is generated (openapi-sync), and OpenSpec
  artifacts and product UI belong to their existing workflows.
---

# Add a documentation page

Explain one concrete part of the current boilerplate using the real code and
visuals that help readers understand it. Paths here are relative to the Git root.
The docs app uses React Router + Fumadocs; read installed versions from
`docs/package.json`. Its publishing format is independent of the frontend UI.

## Establish the page

Read `docs/AGENTS.md` (the docs constitution), the request, existing related
pages and `docs/content/docs/guias/documentacion/escribir-paginas.mdx`. Reuse the agreed
subject and audience. An ADR goes in `docs/content/docs/equipo/adr/` with the
format in its `index.md`; a change spec stays in OpenSpec; endpoint reference
pages are generated from OpenAPI, never written by hand. This skill does not own
architectural decisions or acceptance.

Write in Spanish by default, as required by the project. Honor an explicit user
language choice without asking again. This applies to titles, prose, tables,
links and diagram labels; preserve identifiers, paths, enums, Mermaid keywords
and other syntax. Keep one language per page.

Choose the tab by the reader's need (Diátaxis): `(empezar)/` tutorials,
`guias/<area>/` how-to guides, `conceptos/` explanation, `referencia/` exact
facts, `equipo/` repository contracts. Ask only if an unresolved
subject/audience choice would materially change the page; ordinary filename or
section selection is an implementation decision.

## Research and write

Consult only the relevant part of [reference.md](reference.md): §§1–2 for a new
sidebar placement, unfamiliar MDX structure or component; §3 for Mermaid; §§4–5
for custom media; §6 for preview details. Trace the actual symbols and flows
before drawing: central ORM models for an ERD, or routers, use cases and
adapters for a request flow. Diagrams must describe the installed code.

Use [the page skeleton](templates/doc-template.mdx) as needed. Keep these site
constraints:

- `.mdx` for pages with components, `.md` for plain contracts; ASCII
  kebab-case slugs under `docs/content/docs/`.
- Required `title` and `description` frontmatter, optional Lucide `icon`; no
  duplicate body H1. `.mdx` pages start with `<Callout title="En resumen">`.
- Link with file-relative paths (`../equipo/verificacion.md`); the site rewrites
  them to page URLs and repository links, and `just agent-check` validates them.
- Register the slug in the directory's `meta.json`; new directories also need
  a parent entry and their own `meta.json`.
- Use plain fenced Mermaid for diagrams; the site owns its styling and theme.
  Put SVGs in `docs/public/diagrams/`. Animation must explain motion or change;
  embedded SVG images can use SMIL/CSS, but cannot execute scripts.

Choose complementary diagrams and tables according to the subject, without a
fixed visual quota. Keep prose connected to the diagrams and link to the next
useful page. Do not restate a separate specification or invent product modules.

## Verify and report

Run `just docs build` and `just agent-check` from the Git root: the build
compiles and prerenders every route; the check validates links and frontmatter.
Fix frontmatter, JSX, imports or sidebar problems introduced by the page. A
successful build verifies rendering prerequisites, not diagram accuracy; check
the labels and relationships against the code you researched.

For optional Mermaid inspection, run
`node <skill-dir>/tools/preview-diagram.mjs <file.mdx>` and open its output with
an available browser. Resolve `<skill-dir>` from this loaded skill rather than
assuming a client-specific path. Use
[animated-pipeline.svg](templates/animated-pipeline.svg) when a flow benefits from
an animated illustration.

Report the page path, rendered `/docs/<section>/<slug>` URL and build result.
