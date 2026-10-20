---
name: spec-render
owner: baseline
description: Extract every PlantUML block from docs/specs/<slug>.md and render each to SVG under docs/specs/_rendered/<slug>/, with an index.md listing them in order. Run this before /approve-direction so the reviewer sees pictures instead of raw PlantUML.
disable-model-invocation: true
---

# spec-render — render a spec's diagrams for review

User-invokable only. This skill has side effects (writes SVGs and an index). Claude does not invoke it autonomously.

## Invocation

`/spec-render <slug>` — where `<slug>` corresponds to `docs/specs/<slug>.md`.

## Prerequisites

- `java` on PATH (JDK 8+) + the pinned `plantuml.jar` at `.claude/bin/plantuml.jar` (fetched at install time; SHA-verified). The render script invokes `java -jar .claude/bin/plantuml.jar -tsvg ...` and exits 2 with a named remedy if either dep is missing.
- The spec at `docs/specs/<slug>.md` exists and passes `spec_diagram_presence_guard` + `plantuml_syntax_guard` — otherwise rendering will surface the same errors.

## Steps

1. Validate the slug: `docs/specs/<slug>.md` must exist.
2. Run the render script:
   ```
   node .claude/skills/spec-render/render.mjs <slug>
   ```
   The script:
   - Reads `docs/specs/<slug>.md`.
   - Extracts every ```plantuml``` fenced block in source order.
   - For each block: classifies it by marker (c4_context / c4_container / c4_component / sequence / class / dependency_graph / state / other), writes `docs/specs/_rendered/<slug>/<NN>_<kind>.puml`, then renders to `<NN>_<kind>.svg`.
   - Writes `docs/specs/_rendered/<slug>/index.md` with section titles and image links in order.
3. Report the output path and a short per-kind count to the user.
4. If any block fails to render, surface the offending index + first line + stderr tail, and exit non-zero. Do **not** silently skip broken blocks.

## Output

- `docs/specs/_rendered/<slug>/<NN>_<kind>.svg` — one per diagram block.
- `docs/specs/_rendered/<slug>/<NN>_<kind>.puml` — source kept next to the SVG for easier diffs.
- `docs/specs/_rendered/<slug>/index.md` — markdown index with embedded images.

## Notes

- The render directory is a build output. Add `docs/specs/_rendered/` to `.gitignore` if you don't want the SVGs in the repo; the PlantUML sources in the spec are the source of truth.
- For offline review without Java + the pinned jar, use the `plantuml` MCP server from `.mcp.json` — it talks to a PlantUML renderer over HTTP. This skill prefers the local `java -jar` path because it's faster, keeps renders self-contained, and uses the SHA-pinned jar (so the version a consumer renders against matches what this baseline was tested with).
