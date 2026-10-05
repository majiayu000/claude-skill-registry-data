---
name: excalidraw
description: "Generate Excalidraw architecture diagrams (.excalidraw JSON files) from your codebase. Triggers: you need whiteboard-style sketches that read as a thinking artifact rather than a polished spec — ideal for design."
version: "1.0.1"
category: docs
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Analyze the project codebase and generate Excalidraw architecture diagrams as `.excalidraw` JSON files.

INPUT:
$ARGUMENTS

Accepted arguments:

- No arguments: generate all applicable diagram types.
- `c4`: generate C4 Context and Container diagrams only.
- `sequence`: generate sequence diagrams for key flows only.
- `er`: generate ER diagram from database schema only.
- `deps` or `dependency`: generate module dependency graph only.
- A specific flow description (e.g., "user login flow"): generate a sequence diagram for that flow only.

============================================================
PHASE 1: CODEBASE ANALYSIS
============================================================

Step 1.1 — Tech Stack and Architecture Detection

Scan config files to determine: project type (web app, API, mobile, CLI, library, monorepo), primary language/framework, database(s), external services (auth, payment, email, storage), message queues, caching layers, and API gateway config.

Step 1.2 — Service and Module Mapping

For monorepos/microservices: read `docker-compose.yml` or K8s manifests for service definitions, map inter-service communication, identify external deps per service.

For monoliths: read directory structure to identify modules/domains, trace import statements to map module dependencies, identify layer boundaries.

Step 1.3 — Database Schema Extraction

Scan for schema definitions in: `schema.prisma`, `*.entity.ts` (TypeORM/MikroORM), `models/*.js` (Sequelize), `models.py` (Django), `db/schema.rb` (Rails), `models/*.py` (SQLAlchemy), `schema.ts` (Drizzle), `migrations/*.sql`, `*.model.ts` (Mongoose).

Extract: table/collection names, columns with types, primary/foreign keys, relationships (1:1, 1:N, M:N), indexes, and enums.

Step 1.4 — Key Flow Identification

Identify the most important flows to diagram:

- Authentication flow (login, signup, token refresh)
- Primary business flow (main use case)
- Data write flow (create/update through layers)
- API request lifecycle (middleware, validation, handler, response)
- Background job flow (if applicable)

For each flow, trace: entry point, middleware, service layer, data access, external calls, and response construction.

============================================================
PHASE 2: EXCALIDRAW FILE FORMAT
============================================================

Each `.excalidraw` file is a single JSON document with this top-level shape:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "gridSize": 20,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

Every element MUST include: `id` (random nanoid-like string), `type`, `x`, `y`, `width`, `height`, `angle` (default `0`), `strokeColor`, `backgroundColor`, `fillStyle` (`hachure` | `cross-hatch` | `solid`), `strokeWidth` (`1` thin, `2` bold, `4` extra-bold), `strokeStyle` (`solid` | `dashed` | `dotted`), `roughness` (`0` smooth, `1` normal, `2` cartoonist), `opacity` (0–100), `groupIds` (`[]`), `frameId` (`null`), `roundness` (`null` or `{ "type": 3 }` for rounded rectangles), `seed` (random int), `version` (`1`), `versionNonce` (random int), `isDeleted` (`false`), `boundElements` (`null` or array), `updated` (epoch ms), `link` (`null`), `locked` (`false`).

Type-specific extras:

- **rectangle / ellipse / diamond**: no extra required fields beyond the base. Use `roundness: { "type": 3 }` for rounded rectangles.
- **text**: `text` (string), `fontSize` (16/20/28/36), `fontFamily` (`1` = Virgil hand-drawn, `2` = Helvetica, `3` = Cascadia mono — prefer `1` for sketch feel), `textAlign` (`left`|`center`|`right`), `verticalAlign` (`top`|`middle`|`bottom`), `baseline` (`fontSize * 0.85` rounded), `containerId` (`null` or the id of a shape it labels), `originalText` (same as `text`), `lineHeight` (`1.25`).
- **arrow / line**: `points` (array of `[x,y]` offsets from element origin, first is `[0,0]`), `lastCommittedPoint` (`null`), `startBinding` and `endBinding` (`null` or `{ "elementId": "<id>", "focus": 0, "gap": 8 }` to attach to shapes), `startArrowhead` (`null` or `"arrow"`), `endArrowhead` (`"arrow"`), `elbowed` (`false`).

Color palette — use the Excalidraw default-ish set so files open cleanly:

- Stroke: `#1e1e1e` (default), `#2f9e44` (success/db), `#e03131` (external/danger), `#1971c2` (api/services), `#f08c00` (queue/cache).
- Background fills: `#ffffff` (none), `#b2f2bb` (db), `#ffc9c9` (external), `#a5d8ff` (service), `#ffec99` (queue/cache).
- Default `fillStyle: "hachure"` for that hand-drawn shading.

Layout rules (avoid overlap and produce a readable canvas):

- Pick a grid: 240px column step, 140px row step.
- Label text elements should be centered inside their container — set `containerId` and place `x`/`y`/`width`/`height` to match.
- Arrows must reference both endpoints via `startBinding`/`endBinding` so they reflow if a shape moves.
- Add each shape's id to the other endpoint's `boundElements` array as `{ "id": "<arrowId>", "type": "arrow" }`.

============================================================
PHASE 3: DIAGRAM GENERATION
============================================================

Step 3.1 — C4 Context Diagram (`docs/diagrams/excalidraw/c4-context.excalidraw`)

Center the System under test as a rounded rectangle with a bold label. Place users/actors as ellipses on the left, external systems as rectangles with `strokeStyle: "dashed"` on the right. Arrows labeled with the relationship verb ("uses", "sends events to"). Keep it under 12 shapes.

Step 3.2 — C4 Container Diagram (`docs/diagrams/excalidraw/c4-container.excalidraw`)

Inside a large dashed rectangle representing the system boundary, draw each container (web app, API, worker, db, cache, queue) as a labeled rounded rectangle. Use the color palette above. Annotate arrows with protocol (`HTTPS`, `SQL`, `AMQP`, `gRPC`).

Step 3.3 — Sequence Diagrams (`docs/diagrams/excalidraw/sequence-<flow>.excalidraw`)

Lay participants out as labeled rectangles along the top edge (x stepped by 200, y = 40). Drop a vertical dashed line beneath each as the lifeline. Messages are horizontal arrows between lifelines, stepping y by 80 per message. Always generate the auth flow if auth exists, plus the primary business flow.

Step 3.4 — ER Diagram (`docs/diagrams/excalidraw/er-diagram.excalidraw`)

Each table is a rounded rectangle with two text rows: bold table name (fontSize 20) on top, then a multi-line column list (fontSize 16) listing `name: type` with `(PK)` / `(FK)` markers. Relationships are arrows with cardinality labels (`1`, `0..1`, `*`).

Step 3.5 — Module Dependency Graph (`docs/diagrams/excalidraw/dependency-graph.excalidraw`)

Top-down layout: entry points (routes/controllers) at the top, data stores at the bottom, external systems on the sides. Use background-fill color to encode the layer (api / domain / data / external). Highlight circular dependencies with red dashed arrows.

============================================================
PHASE 4: OUTPUT AND ORGANIZATION
============================================================

Create `docs/diagrams/excalidraw/` if it does not exist. Skip diagram types with no underlying data (no ER if no database).

For every `.excalidraw` file, also write a sibling `.md` file with the same stem containing: heading, brief explanation of the diagram, and a fenced link `[Open in Excalidraw](./<file>.excalidraw)`. The `.excalidraw` file can be opened directly at https://excalidraw.com (File → Open) or via the VS Code Excalidraw extension.

Generate `docs/diagrams/excalidraw/README.md` listing every diagram with a one-line description and a link to both the JSON file and the explanation.

============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing each `.excalidraw` file, validate:

1. The file is valid JSON (`jq empty <file>` exits 0). If `jq` is unavailable, parse with `node -e "JSON.parse(require('fs').readFileSync('<file>','utf8'))"`.
2. `type === "excalidraw"`, `version === 2`, `elements` is a non-empty array.
3. Every element has all required base fields listed in Phase 2.
4. Every arrow's `startBinding.elementId` and `endBinding.elementId` resolve to an existing element id.
5. No two non-arrow shapes overlap by more than 50% of either's bounding box.
6. No element has `x` or `y` greater than 4000 or less than -2000 (keeps the canvas reasonable).

If validation fails, regenerate only the offending file and re-validate. Stop after 2 iterations and report which file is still failing.

============================================================
OUTPUT
============================================================

## Excalidraw Diagrams Generated

### System Profile

- **Type:** [monolith / microservices / monorepo]
- **Services:** [count]
- **Database Tables:** [count]
- **External Systems:** [count]

### Diagrams Created

| Diagram        | File                                                 | Elements |
| -------------- | ---------------------------------------------------- | -------- |
| C4 Context     | docs/diagrams/excalidraw/c4-context.excalidraw       | N        |
| C4 Container   | docs/diagrams/excalidraw/c4-container.excalidraw     | N        |
| Sequence: Auth | docs/diagrams/excalidraw/sequence-auth.excalidraw    | N        |
| ER Diagram     | docs/diagrams/excalidraw/er-diagram.excalidraw       | N        |
| Dependencies   | docs/diagrams/excalidraw/dependency-graph.excalidraw | N        |

### How to View

- Drag any `.excalidraw` file onto https://excalidraw.com
- Or install the `pomdtr.excalidraw-editor` VS Code extension and open in-editor

### Observations

- [Circular dependencies detected]
- [Isolated modules with no connections]
- [Missing relationships that could not be determined]

============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists at `~/.claude/projects/<project>/`. If found, append to `skill-telemetry.md`:

```
### /excalidraw — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / 2 max
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Skip silently if the memory directory does not exist.

============================================================
DO NOT
============================================================

- Do NOT fabricate components, services, or tables. Only diagram what exists.
- Do NOT include internal implementation details in C4 Context diagrams.
- Do NOT generate diagrams for types with no data (no ER if no database).
- Do NOT include sensitive info (credentials, internal URLs, IPs) in diagrams.
- Do NOT overwrite existing `.excalidraw` files without reading them first.
- Do NOT emit broken arrow bindings — every binding must reference an element that exists in the same file.
- Do NOT use `fontFamily` outside `1`, `2`, or `3`. Other values render as boxes.

NEXT STEPS:

After generating diagrams:

- "Run `/diagram` to also produce Mermaid versions for inline rendering in Markdown."
- "Run `/document` to check overall documentation health."
- "Run `/adr` to create ADRs explaining architectural decisions shown in the diagrams."
- "Run `/onboarding` to include these diagrams in the developer onboarding guide."
