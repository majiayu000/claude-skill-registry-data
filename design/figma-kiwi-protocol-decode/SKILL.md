---
name: figma-kiwi-protocol-decode
description: Decode Figma's binary Kiwi wire protocol to extract scenegraph, SVGs, and CSS from WebSocket frames, and write mutations back to live files.
triggers:
  - extract data from a Figma file
  - decode Figma scenegraph without REST API
  - get SVG paths from Figma vectors
  - write changes to Figma files programmatically
  - bypass Figma API rate limits
  - capture Figma WebSocket frames
  - clone Figma components via protocol
  - extract CSS from Figma nodes
---

# Figma Kiwi Protocol Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## What This Does

Figma uses Kiwi (binary serialization by Evan Wallace) over WebSocket for real-time sync. This library decodes those binary frames to extract the full scenegraph, SVG vectors, and CSS — then writes mutations back to live files. No REST API rate limits, no paid plan required.

**Read path**: Intercept WebSocket frames via Chrome DevTools Protocol, decode binary data.
**Write path**: Open standalone Node WebSocket to Figma's multiplayer endpoint, apply mutations that propagate live.

Ships as lib, CLI, MCP server, and Claude Code plugin.

## Installation

```bash
npm install figma-kiwi-protocol
```

## CLI Quick Start

### Read: Capture and Decode

```bash
# 1. Open Figma file in Chrome with remote debugging enabled
chrome --remote-debugging-port=9222

# 2. Set environment variables
export CDP_WS_URL="ws://localhost:9222/devtools/browser/<id>"
export FIGMA_TOKEN="figd_..."
export FIGMA_FILE_KEY="abc123def"  # from Figma URL

# 3. Capture all pages (auto-discovers pages via REST API)
npx figma-kiwi-protocol capture-all-pages

# 4. Decode binary frames to JSON scenegraph
npx figma-kiwi-protocol decode

# 5. Extract SVG files from vector nodes
npx figma-kiwi-protocol extract-svgs

# 6. Decode individual frames for inspection
npx figma-kiwi-protocol decode-frames

# 7. Extract all comments (with threaded replies and flattened metadata)
npx figma-kiwi-protocol comments $FIGMA_FILE_KEY --threads --flat
```

### Write: Mutations and Cloning

```bash
# 1. One-time recon: steal cookies + multiplayer URL from Chrome
#    Writes /tmp/figma_handshake.json (rerun when cookies expire)
npx figma-kiwi-protocol recon-handshake

# 2. Rename a layer by guid (format: sessionID:localID)
npx figma-kiwi-protocol write rename 2004:16177 "NEW_NAME"

# 3. Enable auto-layout on a frame
npx figma-kiwi-protocol write enable-al 2010:16169 \
    --direction HORIZONTAL --hug both --padding 16 --spacing 8

# 4. Deep-clone a component (creates new guids, independent subtree)
npx figma-kiwi-protocol clone 41:1923 --name-suffix " (clone)"

# 5. Batch mutations from JSON file (dry-run first)
npx figma-kiwi-protocol write batch ./changes.json --dry-run
```

## Library Usage

### Read: Decode Binary Data

```javascript
import {
  commandsBlobToPath,
  vectorNetworkBlobToPath,
  extractSvgs,
  extractCSSFromKiwi,
  isFigWireFrame,
  extractCompressedSchema,
  mergePages,
  buildTree
} from 'figma-kiwi-protocol';

// Decode commandsBlob (pre-computed SVG path) to SVG path string
const blobBytes = Buffer.from(node.commandsBlob);
const svgPath = commandsBlobToPath(blobBytes);
// Returns: "M 0.00 0.00 L 24.00 0.00 L 24.00 24.00 Z"

// Decode vectorNetworkBlob (editable path data) to SVG
const vectorBlob = Buffer.from(node.vectorNetworkBlob);
const editablePath = vectorNetworkBlobToPath(vectorBlob);

// Extract CSS from decoded scenegraph node
const nodeChange = scenegraph.nodeChanges.find(n => n.guid === '41:1923');
const css = extractCSSFromKiwi(nodeChange);
// Returns: { width: "100px", display: "flex", background: "#1a1a1a", ... }

// Check if binary frame contains Kiwi schema
const frameBytes = fs.readFileSync('/tmp/figma_kiwi/frame_000.bin');
if (isFigWireFrame(frameBytes)) {
  const compressedSchema = extractCompressedSchema(frameBytes);
  // Decompress with zstd, generate decoder with kiwi CLI
}

// Merge multiple page captures into single scenegraph
const page1 = JSON.parse(fs.readFileSync('/tmp/figma_kiwi/page1.json'));
const page2 = JSON.parse(fs.readFileSync('/tmp/figma_kiwi/page2.json'));
const merged = mergePages([page1, page2]);

// Build tree structure from flat nodeChanges
const tree = buildTree(merged.nodeChanges);
```

### Write: Mutations and Session Management

```javascript
import { FigmaSession } from 'figma-kiwi-protocol/session';

// Connect using handshake data from recon-handshake command
const session = await FigmaSession.connect();
// Reads /tmp/figma_handshake.json by default

// High-level mutation helpers (each resolves when server echoes)
await session.rename(
  { sessionID: 2004, localID: 16177 },
  'ButtonPrimary'
);

await session.setStackMode(
  { sessionID: 2010, localID: 16169 },
  'HORIZONTAL'
);

await session.setPadding(
  { sessionID: 2010, localID: 16169 },
  { all: 16 }
);

await session.setSpacing(
  { sessionID: 2010, localID: 16169 },
  8
);

await session.setSizing(
  { sessionID: 2010, localID: 16169 },
  'HORIZONTAL',
  'HUG'
);

// Low-level mutate: send raw nodeChanges and blobs
await session.mutate({
  nodeChanges: [
    {
      guid: '2004:16177',
      guidState: 'SYNCED',
      properties: { name: 'Footer' }
    }
  ],
  blobs: []
});

// Close connection
await session.close();
```

### Clone: Deep Copy Components

```javascript
import { cloneSubtree } from 'figma-kiwi-protocol/clone';
import { FigmaSession } from 'figma-kiwi-protocol/session';
import fs from 'fs';

// Load decoded scenegraph
const scenegraph = JSON.parse(
  fs.readFileSync('/tmp/figma_kiwi/scenegraph.json')
);

const session = await FigmaSession.connect();

// Deep-clone a component with all children (generates new guids)
const { nodeChanges, blobs } = cloneSubtree({
  scenegraph,
  sourceGuid: '41:1923',  // Component to clone
  sessionID: session.sessionID,
  nameSuffix: ' (Clone)'
});

// Apply clone mutation (propagates live to all connected editors)
await session.mutate({ nodeChanges, blobs });

await session.close();
```

### Builder: Author Nodes from Scratch

```javascript
import { FigmaBuilder } from 'figma-kiwi-protocol/builder';
import { FigmaSession } from 'figma-kiwi-protocol/session';

const session = await FigmaSession.connect();
const b = new FigmaBuilder({ sessionID: session.sessionID });

// Create vertical auto-layout frame
const card = b.frame({
  name: 'Card',
  stackMode: 'VERTICAL',
  padding: { all: 16 },
  spacing: 12,
  size: { x: 320, y: 200 }
});

// Add rectangle child (builder handles parentIndex uniqueness)
b.rectangle({
  parent: card,
  size: { x: 288, y: 120 },
  fills: [{ type: 'SOLID', color: { r: 0.1, g: 0.1, b: 0.1, a: 1 } }]
});

// Add text child
b.text({
  parent: card,
  name: 'Title',
  characters: 'Hello World',
  fontSize: 24,
  fontName: { family: 'Inter', style: 'Bold' }
});

// Build and apply
const nodeChanges = b.build();
await session.mutate({ nodeChanges });

await session.close();
```

## Configuration

### Environment Variables

```bash
# CDP capture (read path)
CDP_WS_URL="ws://localhost:9222/devtools/browser/<id>"
FIGMA_TOKEN="figd_..."      # For page discovery
FIGMA_FILE_KEY="abc123def"  # From Figma URL

# Write path (after recon-handshake)
# Reads /tmp/figma_handshake.json by default
# Override with:
FIGMA_HANDSHAKE_PATH="/custom/path/handshake.json"

# MCP server
FIGMA_KIWI_DIR="/tmp/figma_kiwi"  # Where decoded data lives
```

### MCP Server Setup

Add to `.mcp.json` or `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "figma": {
      "command": "node",
      "args": ["/path/to/figma-kiwi-protocol/mcp/server.mjs"],
      "env": {
        "FIGMA_KIWI_DIR": "/tmp/figma_kiwi"
      }
    }
  }
}
```

MCP tools: `figma_pages`, `figma_page`, `figma_node`, `figma_search`, `figma_css`, `figma_texts`, `figma_components`.

## Common Patterns

### Extract All Text Content

```javascript
import { buildTree } from 'figma-kiwi-protocol';
import fs from 'fs';

const scenegraph = JSON.parse(
  fs.readFileSync('/tmp/figma_kiwi/scenegraph.json')
);

const tree = buildTree(scenegraph.nodeChanges);

function extractText(node, texts = []) {
  if (node.type === 'TEXT' && node.characters) {
    texts.push({
      name: node.name,
      text: node.characters,
      fontSize: node.fontSize,
      guid: node.guid
    });
  }
  if (node.children) {
    node.children.forEach(child => extractText(child, texts));
  }
  return texts;
}

const allTexts = extractText(tree);
console.log(JSON.stringify(allTexts, null, 2));
```

### Batch Rename Layers

```javascript
import { FigmaSession } from 'figma-kiwi-protocol/session';
import fs from 'fs';

const session = await FigmaSession.connect();

// Load changes from JSON
const changes = JSON.parse(fs.readFileSync('./renames.json'));
// Format: [{ guid: "2004:16177", newName: "Header" }, ...]

for (const { guid, newName } of changes) {
  const [sessionID, localID] = guid.split(':').map(Number);
  await session.rename({ sessionID, localID }, newName);
  console.log(`Renamed ${guid} → ${newName}`);
}

await session.close();
```

### Find Components by Name

```javascript
import { buildTree } from 'figma-kiwi-protocol';
import fs from 'fs';

const scenegraph = JSON.parse(
  fs.readFileSync('/tmp/figma_kiwi/scenegraph.json')
);

function findByName(node, search, results = []) {
  if (node.name && node.name.toLowerCase().includes(search.toLowerCase())) {
    results.push({
      guid: node.guid,
      name: node.name,
      type: node.type
    });
  }
  if (node.children) {
    node.children.forEach(child => findByName(child, search, results));
  }
  return results;
}

const tree = buildTree(scenegraph.nodeChanges);
const buttons = findByName(tree, 'button');
console.log(buttons);
```

### Convert Auto-Layout Frame

```javascript
import { FigmaSession } from 'figma-kiwi-protocol/session';

const session = await FigmaSession.connect();
const guid = { sessionID: 2010, localID: 16169 };

// Enable horizontal auto-layout
await session.setStackMode(guid, 'HORIZONTAL');

// Set padding
await session.setPadding(guid, { all: 16 });

// Set spacing between children
await session.setSpacing(guid, 12);

// Hug contents in both directions
await session.setSizing(guid, 'HORIZONTAL', 'HUG');
await session.setSizing(guid, 'VERTICAL', 'HUG');

await session.close();
```

## Binary Format Reference

### commandsBlob Structure

```
Byte  Command      Parameters
0x01  MoveTo       x(f32) y(f32)
0x02  LineTo       x(f32) y(f32)
0x03  ClosePath    (none)
0x04  CubicBezier  x1(f32) y1(f32) x2(f32) y2(f32) x(f32) y(f32)
0x00  (separator)  subpath boundary
```

### vectorNetworkBlob Structure

```
Header: vertexCount(u32) segmentCount(u32) regionCount(u32)

Per vertex (12 bytes):
  flags(u32) x(f32) y(f32)

Per segment (28 bytes):
  flags(u32) startVertexIdx(u32) tangentStartX(f32) tangentStartY(f32)
  endVertexIdx(u32) tangentEndX(f32) tangentEndY(f32)
```

## Troubleshooting

### "CDP WebSocket connection failed"

- Ensure Chrome is running with `--remote-debugging-port=9222`
- Get correct CDP URL from `chrome://inspect` or `http://localhost:9222/json/version`
- Check no other process is using port 9222

### "No frames captured"

- Verify Figma file is open in Chrome tab
- Reload Figma page after starting capture
- Check CDP_WS_URL points to browser, not a specific tab

### "Handshake failed" (write path)

- Run `recon-handshake` first to capture cookies
- Cookies expire — rerun recon if writes fail with auth errors
- Ensure Figma file is open in Chrome during recon

### "Invalid guid format"

- Guids are `sessionID:localID` format (e.g. `2004:16177`)
- Find guids in decoded scenegraph JSON
- Session ID changes per Figma session; use current decoded data

### SVG paths look incorrect

- Composite icons need transform composition (known limitation)
- For SYMBOL nodes with VECTOR children, extract each VECTOR separately
- Check if node has rotation/translation transforms applied

### Mutations not appearing in Figma

- Ensure Figma file is open in browser (WebSocket must be connected)
- Check session.mutate() resolved (server echoed ack)
- Verify guid exists in current scenegraph
- Some properties require specific node types (e.g. stackMode only on FRAME)

### MCP tools return empty data

- Run `capture-all-pages` and `decode` first
- Check FIGMA_KIWI_DIR points to directory with scenegraph.json
- Ensure scenegraph.json is valid JSON (run `jq . scenegraph.json`)
