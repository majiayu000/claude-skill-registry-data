---
name: penpot-mcp-operator
description: Use when working with Penpot through MCP, including remote or local Penpot MCP setup, reading or modifying active Penpot design files, creating pages, boards, shapes, text, tokens, components, exports, imports, or diagnosing Penpot MCP API behavior. USE FOR "work in Penpot", "create a Penpot board", "use Penpot MCP", "upload images to Penpot", "inspect this Penpot file", and "fix Penpot MCP API guessing".
---

# Penpot MCP Operator

Use this skill to operate Penpot through MCP without guessing the API.

## Operating Rule

Penpot MCP acts on the currently focused Penpot file and page. Always inspect before writing.

1. Confirm whether the available server is remote or local.
2. Read the Penpot high-level overview once per session if it has not already been read.
3. Use `penpot_api_info` for every object type and member you plan to rely on before write operations.
4. Run a read-only probe with `execute_code`.
5. Make the smallest requested mutation.
6. Verify with a structural readback and, when possible, `export_shape`.
7. Report exact proof level and limitations.

## Remote Versus Local

Remote MCP is simplest for Penpot Cloud and usually exposes:

- `execute_code`
- `high_level_overview`
- `penpot_api_info`
- `export_shape`

Remote MCP does not provide full local filesystem access. Do not assume local-path image import or local export writes work.

For remote MCP image upload, local asset import, file picker work, plugin UI work, or drag-and-drop style workflows, use browser control with Chrome or computer-use. Remote MCP alone should not be treated as a local asset bridge.

For PDF/image-heavy workflows, check the Penpot plugin path before rebuilding assets manually. The Penpot plugin hub includes plugins such as Import PDF, bitmap vectorization, design token management, color export and HTML-to-design. Use Chrome or computer-use for plugin install/UI steps when MCP remote cannot perform the browser interaction.

For brand typography, use Penpot custom fonts before approximating with system fonts. Custom fonts are uploaded at team/dashboard level, then become available inside files for that team. Supported formats include TTF, OTF, WOFF and WOFF2. Use Chrome or computer-use for the dashboard upload flow when MCP cannot operate that UI.

Local MCP requires a running local server and Penpot plugin connection. It can expose local-resource workflows such as local image import and stronger export paths, depending on configuration.

Never paste, log, commit, or screenshot a remote MCP `userToken`.

## Illustrator Source Reconstructions

When the Penpot task is a 1:1 recreation of an Illustrator file, brandbook, logo sheet, or layered `.ai` source, use this skill together with `adobe-illustrator-operator`.

Penpot MCP is the execution surface. Illustrator remains the canonical source for artboards, visual stacking, layer order, object names, text and export references.

Before writing Penpot objects:

1. read the Illustrator tree through the Illustrator workflow;
2. create or select the matching Penpot file;
3. recreate boards in Illustrator artboard order;
4. import or recreate child objects in Illustrator tree order;
5. recreate Illustrator TextFrames as Penpot text wherever technically possible;
6. replace generic imported names with semantic names tied to the Illustrator tree;
7. verify each board visually and structurally before moving to the next board.

Do not use a flattened page SVG as final proof for a 1:1 reconstruction.

## Required Read Probe

Start with:

```js
return {
  page: penpot.currentPage ? {
    id: penpot.currentPage.id,
    name: penpot.currentPage.name,
    keys: Object.keys(penpot.currentPage)
  } : null,
  root: penpot.root ? {
    id: penpot.root.id,
    name: penpot.root.name,
    type: penpot.root.type,
    keys: Object.keys(penpot.root)
  } : null
};
```

If the task needs child traversal, query the specific container type and member first. Do not assume `children`, `remove`, or `findShapes` exist globally.

## API-First Write Workflow

Before writing a board, text, token, image, or component:

1. Ask `penpot_api_info` for the creator method, such as `Penpot.createBoard`.
2. Ask `penpot_api_info` for the concrete shape type methods you will use, such as `Board.resize`, `Rectangle.resize`, `Text.growType`, `Group.appendChild`.
3. Use only confirmed members.
4. Keep code idempotent by naming generated nodes clearly.
5. If deletion or replacement is needed, confirm the delete/remove API exists before using it.

## Safe Creation Pattern

Use append-only creation when the delete API is not confirmed.

```js
const board = penpot.createBoard();
board.name = "REVIEW__Example";
board.x = 0;
board.y = 0;
board.resize(1440, 900);
board.fills = [{ fillColor: "#050505", fillOpacity: 1 }];
penpot.root.appendChild(board);

const text = penpot.createText("Example Brand");
text.name = "TITLE__Example_Brand";
text.x = 80;
text.y = 80;
text.resize(600, 90);
text.growType = "fixed";
text.fontSize = "72";
text.fills = [{ fillColor: "#FFDF00", fillOpacity: 1 }];
board.appendChild(text);

penpot.viewport.zoomIntoView([board]);
return { ok: true, boardId: board.id, boardName: board.name };
```

## Verification

After mutation, run a structural readback that returns:

- active page name
- generated board or node ids
- generated node names
- count of direct elements when the API supports it
- any known limitation, such as remote export or local import unavailable

Use `export_shape` for visual proof when available. If export fails in remote mode, say that visual proof is pending in the Penpot canvas and do not claim screenshot proof.

## References

Use `references/penpot-mcp-api-map.md` for command map, known limitations, setup modes, and safe snippets.

Use `references/upstream-penpot-ai-kit.md` when the task needs a fuller Penpot agent workflow, such as tokens, components, screen building, audits, migration, routing, approval checkpoints or prompt templates.
