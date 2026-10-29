---
name: docs-query
description: |
  Answer questions about the documented lakehouse from this repo's committed
  artifacts with `uv run docsnip query`: explain a model element, find the
  tested examples for a concept, find and regenerate the environment a script
  or journey runs on, explain what an environment runs and which capabilities
  and concerns it fully meets, and list what a changed module, element, or
  release pin reaches. Use when asked "what explains X", "is there an example
  of X", "how do I rerun this stack", "does this environment give full
  governance", or "what does this bump/model change affect".
argument-hint: '<explain|environment-for|examples-for|explain-selection|impact> <id>'
---

# Query the docs' committed artifacts

`docsnip query` reads only committed files: `architecture/dist/model.json`,
`content/<project>/compatibility.json`, `envs/` (plans, registry, generated
facts, Trestle pin), the Trestle catalog snapshot and role map, and the
content pages and scripts. It is internal. Answers can name draft pages and
non-public elements, so don't paste them into reader-facing text. The public
payloads go through the site projection (`site/src/content-core/projection.mjs`).

Every answer is JSON (`format: docsnip-query`, `version: 1`) and keyed by
stable IDs: model element IDs, repo-relative script and page paths,
`<project>/<journey>`, and environment names. An unknown ID exits 2.

## Queries

| Query | `<id>` | Answers |
|---|---|---|
| `explain` | model element | kind, summary, canonical and citing pages, edges, backing implementations, environments, journeys; for a concern or capability, `holds` per environment |
| `examples-for` | model element | scripts whose journey has it as asset, requirement, or interface, or whose page cites it |
| `environment-for` | script path, or `<project>/<journey>` | its environment: registry key, recipe, `regenerate` command, services, client env, bundle files |
| `explain-selection` | environment name or registry key | each service's element, role, role-map target and scope; every capability and concern it meets, as `full`, `partial`, or `missing` |
| `impact` | element, `module:<id>`, `pin:<project>/<key>`, `pin:trestle` | environments, scripts by compose key, claims, pages, citing pages, views |

## Reading the evidence

Each item lists the states that hold:

- `configured`: a generated environment's plan runs it.
- `tested`: a working proof on a ready page, and the compatibility artifacts
  are current. When they're stale, the answer says `"compat": "stale"`, and
  `tested` is withheld until `uv run docsnip compat --fix`.
- `documented`: a ready page explains, references, or `model:`-links it.
- `unknown`: none of these.

A `#partial` edge or a role-map `scope: partial` never counts as meeting a
target. A parent concern such as `lakehouse.governance` holds only when every
facet is `full` in the same environment. So "does X give full governance"
means checking `holds.<env>.holds`, and `missing` and `partial` say why not.

## Typical uses

- **Find and rerun an example:** `examples-for <concept>`, pick a script with
  `tested`, then `environment-for <script>` and run its `regenerate` command
  (the environment README covers starting it).
- **Before a release bump:** `impact pin:unitycatalog/release` gives the review
  list for the `release-bump` skill.
- **Before a model or Trestle change:** `impact <element>` or
  `impact module:<id>`, then `uv run docsnip check` after the change.
