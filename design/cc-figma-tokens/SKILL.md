---
name: cc-figma-tokens
description: "Build or update Figma variable collections (Primitives and Semantic) from component-contracts token files. Use when the user wants to sync their design token definitions into Figma as native variables — e.g. 'build the token library', 'sync tokens to Figma', 'create Figma variables from tokens', 'update the variable collections'. This skill is a PREREQUISITE for cc-figma-component — tokens must exist in Figma before components can be built. Requires the figma-use and figma-generate-library skills."
---

# cc-figma-tokens — Component Contracts Token Skill

Build Figma variable collections from component-contracts token files. This skill creates the Primitive and Semantic variable collections that all components bind to.

**Prerequisites — load these skills first:**
- `figma-use` — Plugin API syntax rules (mandatory before every `use_figma` call)
- `figma-generate-library` — Design system workflow and variable creation patterns

**Always pass `skillNames: "cc-figma-tokens"` when calling `use_figma` as part of this skill.**

---

## 1. Configuration

Before anything else, read `.component-contracts` from the project root. This file contains all required configuration. Never output `FIGMA_ACCESS_TOKEN` in any response.

```
FIGMA_ACCESS_TOKEN=...       # never output this value
FIGMA_FILE_KEY=...           # use for all use_figma calls
TOKENS_DIR=...               # root directory of token files
CONTRACTS_DIR=...            # root directory of contract files
```

If `.component-contracts` is missing, stop before any Figma write and ask the user for the Figma file key plus token/contract directories, or create a safe `.component-contracts.example` in a separate setup step. Do not reference a non-existent example file as if it already exists.

---

## 2. Token File Structure

Component-contracts uses W3C DTCG token format organized in two tiers:

```
{TOKENS_DIR}/
  primitive/
    color.tokens.json
    motion.tokens.json
    shape.tokens.json
    space.tokens.json
    typography.tokens.json
  semantic/
    semantic.tokens.json
```

**Tier 1 — Primitives**: Raw values. Named with scale suffixes (`color/blue/500`, `space/4`). No aliases. Single mode: `Value`.

**Tier 2 — Semantic**: Aliases into Primitives. Named with roles (`brand/500`, `surface/default`, `text/primary`). Single mode: `Value`.

Read all token files before creating anything in Figma. Build a complete in-memory map of all tokens and their values/aliases before making any `use_figma` calls.

---

## 3. Figma Variable Architecture

### Collections

Create exactly two collections in this order:

| Collection | Modes | Purpose |
|-----------|-------|---------|
| `Primitives` | `Value` | Raw token values — never bound directly to components |
| `Semantic` | `Value` | Aliases into Primitives — this is what components bind to |

### Variable naming

Use `/` as the group separator, matching W3C DTCG path structure:

```
Primitives:  color/blue/500, space/4, radius/md
Semantic:    brand/500, surface/default, text/primary, focus/default
```

### Variable scopes

**NEVER use `ALL_SCOPES`.** Assign scopes based on the token's semantic role:

| Token role | Scope |
|-----------|-------|
| Color — background/fill | `FRAME_FILL`, `SHAPE_FILL` |
| Color — text | `TEXT_FILL` |
| Color — border/stroke | `STROKE_COLOR` |
| Color — focus ring | `FRAME_FILL`, `SHAPE_FILL`, `STROKE_COLOR` |
| Spacing — padding, gap | `GAP` |
| Spacing — border width | `STROKE_WIDTH` |
| Border radius | `CORNER_RADIUS` |
| Typography — font size | `FONT_SIZE` |
| Typography — font weight | `FONT_WEIGHT` |
| Typography — line height | `LINE_HEIGHT` |
| Primitives (all) | `[]` — hidden from property panels |

> **Note:** `HORIZONTAL_PADDING` and `VERTICAL_PADDING` are NOT valid `VariableScope` enum values in the Figma Plugin API. Use `GAP` only for all spacing variables.

### Code syntax

Every variable MUST have WEB code syntax set. Use the `var()` wrapper with the CSS custom property name:

```
Primitive color/blue/500  →  var(--ds-color-blue-500)
Semantic brand/500        →  var(--ds-brand-500)
Semantic surface/default  →  var(--ds-surface-default)
```

CSS naming convention: `--ds-{path-with-dashes}` where `/` becomes `-`.

ANDROID and iOS do NOT use a `var()` wrapper.

---

## 4. Execution Modes

**Default (fast):** Present the Phase 0 plan and await approval, then run Phases 1–4 sequentially without stopping. This is the default for all runs.

**Debug mode:** Stop after each phase and await explicit approval before proceeding. Use when diagnosing issues or validating intermediate output. Activate by including "debug mode" in your prompt.

---

## 5. Workflow

### Batching requirement (critical for performance)

**Create ALL variables in a single `use_figma` call per collection.** Never create variables one at a time or category by category.

- One `use_figma` call creates the Primitives collection + all variables
- One `use_figma` call creates the Semantic collection + all aliases
- Do NOT write intermediate state files between variables
- Do NOT validate between individual variables
- Validate ONCE after the entire collection is created

Token creation is deterministic and low-risk. The state ledger and intermediate file-writing pattern from `figma-generate-library` is NOT appropriate here — skip it entirely. Read all token files first, build the complete variable map in memory, then execute in one call per collection.

If a collection exceeds ~80 variables and must be split across two calls, split by category (e.g. color in one call, everything else in another) — never by individual variable.

---

### Phase 0 — Inspect (read-only)

Before creating anything:

1. Read all token files from `TOKENS_DIR`
2. Inspect the Figma file — check for existing variable collections named `Primitives` or `Semantic`
3. If collections exist, check whether this is a create or update operation
4. Present a summary to the user: token counts per tier, existing vs. new collections, any conflicts
5. **Await explicit user approval before proceeding**

### Phase 1 — Primitives collection

1. Read all primitive token files and build complete variable map in memory
2. Create the `Primitives` collection with a single `Value` mode
3. Create ALL primitive variables in a single `use_figma` call — color, space, motion, shape, typography
4. Set scopes to `[]` on all primitives (hidden)
5. Set WEB code syntax on all primitives
6. Validate: `get_metadata` to confirm variable count matches token file count
7. In debug mode: **Await user checkpoint before proceeding**

### Phase 2 — Semantic collection

1. Read semantic token file and resolve all `{token.path}` references to Primitive variable IDs
2. Handle creation order — variables that alias other semantic variables (e.g. `border/brand → brand/500`) must be created after their targets
3. Create the `Semantic` collection with a single `Value` mode
4. Create ALL semantic variables in a single `use_figma` call using `figma.variables.createVariableAlias`
5. Set scopes based on semantic role (see §3 scope table)
6. Set WEB code syntax on all semantic variables
7. Validate: `get_metadata` — confirm all aliases resolve correctly
8. In debug mode: **Await user checkpoint before proceeding**

### Phase 3 — Explicit mode assignment

After both collections exist, call `setExplicitVariableModeForCollection` on every node in the file to force the `Value` mode. This prevents ghost mode issues where variables appear unresolved.

```js
// Apply to every node recursively
function applyModes(node, collection, modeId) {
  node.setExplicitVariableModeForCollection(collection, modeId);
  if ('children' in node) {
    for (const child of node.children) {
      applyModes(child, collection, modeId);
    }
  }
}
```

In debug mode: **Await user checkpoint before proceeding**

### Phase 4 — Validation

Run a final validation pass:
- `get_metadata` — confirm both collections exist with correct variable counts
- `get_screenshot` — visually confirm variables appear correctly in Figma

Return a structured summary:
```json
{
  "collections": {
    "Primitives": { "variableCount": N, "modeCount": 1 },
    "Semantic": { "variableCount": N, "modeCount": 1 }
  },
  "status": "complete"
}
```

---

## 6. Update vs. Create

If variable collections already exist:

- **Add new variables**: create and alias, do not touch existing variables
- **Update values**: modify the raw value of the Primitive, the Semantic alias chain updates automatically
- **Never delete existing variables** without explicit user confirmation — components may be bound to them
- Use idempotency check before every create: `getLocalVariables().find(v => v.name === name && v.variableCollectionId === collId)`

---

## 7. Known Constraints

- **Always use `setSharedPluginData` / `getSharedPluginData` — never `setPluginData` / `getPluginData`**. The non-shared version uses a debug UUID as the plugin identifier that changes on each tool execution, making stored data permanently unretrievable and causing file bloat. Always use the `component_contracts` namespace:
  ```js
  // CORRECT
  node.setSharedPluginData('component_contracts', 'dsb_key', value);
  node.getSharedPluginData('component_contracts', 'dsb_key');

  // WRONG — UUID changes per execution, data becomes orphaned
  node.setPluginData('dsb_key', value);
  ```

- **Letter-spacing cannot be stored as a Figma variable** — Figma FLOAT variables are unitless integers; em-based letter-spacing values are incompatible. Handle letter-spacing via Text Styles only, not variables.
- **`HORIZONTAL_PADDING` and `VERTICAL_PADDING` are not valid `VariableScope` values** — the Plugin API does not expose these as enum members. Use `GAP` only for all spacing variables.
- **Typography variables** — font size and weight can be stored as FLOAT variables. Font family must use a STRING variable.
- **Chained aliases are permitted**: `Semantic/brand/500 → Primitive/color/blue/500`. Do not flatten the chain.
- **Creation order matters for chained semantic aliases** — create the aliased variable first. E.g. create `brand/500` before `border/brand` which aliases it.
- **Ghost mode**: Figma creates an empty ghost mode automatically when a collection is created. This is expected. Always call explicit mode assignment (Phase 3) to suppress it.
