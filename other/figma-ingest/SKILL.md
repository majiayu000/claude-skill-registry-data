---
name: figma-ingest
description: Use when a Figma frame URL has to become kivo-creator section specs - reading the frame through the official Figma MCP server in the main session (get_metadata for the tree, get_design_context per section, get_variable_defs for tokens, get_screenshot to look, get_code_connect_map for mapped components), writing exact or inferred values only, and stopping with connection steps when the server is missing. For HTML sources use html-ingest; for creating Code Connect mappings use code-connect.
license: MIT
compatibility: Main session only (subagents do not inherit MCP servers). Needs the official Figma MCP server; reference images for the pixel diff also need FIGMA_TOKEN in the environment. Node 20+.
---

# Figma ingest

Read a Figma frame into neutral section specs. The MCP output is a reference to read, never code to copy: its arbitrary classes and literal values are not carried into the project.

## When to use

- A `figma.com/design/...` (or `/file/`) link with a `node-id`, from `/creator` or on its own.
- Not for HTML (`html-ingest`) and not for writing Code Connect mappings (`code-connect`).

## Inputs required

1. The frame URL with `node-id` (a page link without it is ambiguous: ask for the frame).
2. The Figma MCP tools in this session. Their names end in `get_metadata`, `get_design_context`, `get_variable_defs`, `get_screenshot` and `get_code_connect_map`; the prefix depends on how the server was connected.
3. The target project root with `.roots-stack.json`, and the kivo-creator plugin root (two levels above this skill's folder).
4. Optional: `FIGMA_TOKEN` (a Figma personal access token) exported in the shell. **Without it, reference images cannot be fetched**: the specs are still written, but the pixel diff has nothing to compare against.

## Procedure

1. **Check the server.** If none of the tools above is available, stop and say: the official Figma MCP server is not connected in this session; add the remote server `https://mcp.figma.com/mcp` (HTTP transport) in the assistant's MCP settings, or enable the local server of the Figma desktop app, sign in, and start a new session. Do not fall back to screenshots, the REST API or guessing.
2. **Metadata.** Call `get_metadata` with the file key and node id from the URL (`node-id=1-2` means `1:2`). Save the response text to `.creator/figma-metadata.xml`, then:

   ```bash
   node <kivo-creator>/scripts/figma-sections.mjs --url="<figma URL>" --metadata=.creator/figma-metadata.xml --project=.
   ```

   It creates `.creator/<run>/` with `figma-sections.json`: one entry per top-level frame (`id`, `nodeId`, `kind` from the layer name, `chrome`, geometry).
3. **Variables.** Call `get_variable_defs` for the frame; save the result as `.creator/<run>/figma-variables.json`.
4. **Code Connect.** Call `get_code_connect_map` for the frame; save it as `.creator/<run>/figma-code-connect.json`. When a section's node is mapped to a block in the catalog (`node <kivo-creator>/scripts/match.mjs --catalog --project=.`), set `"codeConnect": { "block": "<block name>", "component": "<component name>" }` in that section's spec.
5. **One spec per section.** For each non-chrome entry, call `get_design_context` with its `nodeId` (and `get_screenshot` when you need to look at it), then write `.creator/<run>/specs/<id>.json` following `schemas/section-spec.schema.json`:
   - `source`: `{ "kind": "figma", "ref": "<nodeId>", "url": "<figma URL>" }`; `kind` from `figma-sections.json`, corrected when the content clearly says otherwise (add a note).
   - `slots`: literal texts, image and link targets that appear in the design context are `exact`; a repeated card becomes one `list` slot named `items`. Leave out anything that is not in the design.
   - `layout`: columns, alignment, media position and repeat count from the geometry and auto layout; mark it in `notes` as inferred.
   - `tokens`: colours, font family, size, weight, line height and padding per role (`section`, `heading`, `text`, `link`, `button`), `exact` when the design context or a variable gives the value. Write the value as CSS (`#0a84ff`, `56px`); never copy a Tailwind class from the reference code.
   - `refs`: leave `{}`; step 7 fills it.
   Chrome entries get a spec with `"chrome": true`, empty `slots` and `tokens`, `layout` `{ "columns": 1, "align": "left", "media": "none", "repeat": 0 }` and the note "chrome: not read". They are never matched.
6. **Validate**: `node <kivo-creator>/scripts/validate-spec.mjs .creator/<run>/specs`.
7. **References.** The MCP screenshot reaches you, not the disk, so pixel references come from the Figma REST API and need `FIGMA_TOKEN`.
   - With the token exported: `node <kivo-creator>/scripts/figma-ref.mjs --run=.creator/<run>` saves one PNG per section at the frame's width and records it in each spec's `refs`.
   - Without it (exit code 2, `FIGMA_TOKEN is not set`): say plainly that reference images cannot be fetched, so the pixel diff will report "no reference" for every section and only the style check and lint will run. Ask the person to export a token in their shell if they want the diff.
   - The token is read from the environment only. Never ask for it in the conversation, never pass it on a command line, never print or echo it.
8. Hand over to `section-matching`.

## Verification

- `validate-spec.mjs` prints `ok` for every spec.
- Every slot value can be found in a saved MCP response or in the design context you read.
- No Tailwind class, `px-[…]` value or `var(--…)` fallback from the reference code appears in any spec.
- The reply says whether reference images were saved; it never claims references exist when `figma-ref.mjs` did not run.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Figma tools missing | Server not connected, or running inside a subagent | Stop with the connection steps; run in the main session |
| `get_metadata` returns one huge frame | The link points at a page or a wrapper | Ask for the frame link, or pass the inner frame's node id |
| Design context truncated | Very large section | Call it for the children of that section and merge the slots |
| `FIGMA_TOKEN is not set` | No token in the environment | Reference images cannot be fetched; ask the person to export one, or accept a report without pixel diff |
| `Figma images API answered 403` | Token expired or without access to the file | Ask for a token with read access to that file; the specs stay valid |
| Values only in the screenshot | Raster image or flattened text | Leave them out; note that the source is a raster |

## Escalation

Ask when the frame has variants for several breakpoints (which one is canonical), when text is rasterised, or when a component mapped by Code Connect points at code that does not exist in the project.
