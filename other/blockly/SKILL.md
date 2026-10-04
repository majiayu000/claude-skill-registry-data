---
name: blockly
description: Blockly visual programming context for the Megahub project. Use when adding, modifying, or debugging custom Blockly blocks, the Lua code generator, the toolbox, block colors, or the BLOCKS.md documentation generation script.
---

# Blockly Integration — Megahub IDE

## Overview

- **Blockly 12.3.1** with the built-in **Lua code generator** (`blockly/lua`)
- Custom Web Component `<custom-blockly>` in `frontend/src/components/blockly/component.js`
- Each custom block is a **self-contained JS file** with definition + Lua generator + color
- All 25 custom blocks auto-register; `BLOCKS.md` is auto-generated via Puppeteer

---

## File Structure

```
frontend/src/components/blockly/
  component.js          Main component — init, toolbox, workspace, Lua generation
  component.html        Minimal web component template
  colors.js             Color hue constants for all categories (0–360)
  mh_*.js               20 Megahub core blocks (motors, GPIO, threads, debug)
  lego_*.js             2 LEGO Powered Up blocks
  ui_*.js               1 UI display block
```

---

## Block Definition Pattern

Every block is one file. All fields are required unless noted:

```javascript
export const definition = {
    category: 'Category Name',      // Groups this block in the toolbox
    colour: colorConstant,          // Import from colors.js — never hardcode
    blockdefinition: {              // Standard Blockly JSON definition
        type: 'mh_block_name',      // Must match filename (minus .js)
        message0: 'label %1 %2',    // %N = input/field placeholders
        args0: [ /* inputs */ ],
        previousStatement: null,    // Include for statement blocks
        nextStatement: null,        // Include for statement blocks
        // OR: output: null         // For value blocks that return a value
        tooltip: 'Description for BLOCKS.md and hover UI',
        helpUrl: ''
    },
    generator: (block, generator) => {
        // Return string + "\n" for statement blocks
        // Return [ "code", precedence ] for value blocks
    },
    inputsForToolbox: { /* optional shadow defaults */ }
};
```

### Statement block generator pattern
```javascript
generator: (block, generator) => {
    const val = generator.valueToCode(block, 'VALUE', 0);
    const stmt = generator.statementToCode(block, 'DO');
    const field = block.getFieldValue('FIELD_NAME');
    return `myFunction(${val}, ${field})\n`;
}
```

### Value block generator pattern
```javascript
generator: (block, generator) => {
    const val = block.getFieldValue('VALUE');
    return [ val, 0 ];   // [ code, precedence ]
}
```

---

## Naming Conventions

| Prefix | Category | Example |
|--------|----------|---------|
| `mh_` | Megahub core | `mh_set_motor_speed`, `mh_wait`, `mh_startthread` |
| `lego_` | LEGO Powered Up | `lego_get_mode_dataset`, `lego_select_mode` |
| `ui_` | User interface | `ui_show_value` |

- All lowercase, underscores only
- Block type ID **must match** the JS filename (e.g., `mh_wait.js` → `type: 'mh_wait'`)

---

## Color System (`colors.js`)

Colors are Blockly hue values (0–360). Always import — never hardcode a number.

| Constant | Hue | Category |
|----------|-----|----------|
| `colorControlFlow` | 20 | Control flow |
| `colorLogic` | 40 | Logic |
| `colorMath` | 60 | Math |
| `colorText` | 80 | Text |
| `colorLists` | 100 | Lists |
| `colorIO` | 120 | I/O |
| `colorLego` | 140 | LEGO© |
| `colorGamepad` | 160 | Gamepad |
| `colorFastLED` | 180 | FastLED |
| `colorIMU` | 200 | IMU |
| `colorUI` | 220 | UI |
| `colorAlgorithms` | 230 | Algorithms |
| `colorDebug` | 240 | Debug |

---

## Adding a New Block

1. **Create** `frontend/src/components/blockly/mh_myblock.js` using the pattern above
2. **Import and register** in **all three** files:
   - `frontend/src/components/blockly/component.js` — add import + entry in `customBlocks`
   - `frontend/scripts/block-renderer.js` — add import + entry in `customBlocks`
   - `frontend/scripts/generate-block-docs-simple.js` — add dynamic import in `blockModules` + entry in `customBlocks`
3. **Toolbox**: automatic — `generateToolbox()` groups by `category` field
4. **Write unit tests** — REQUIRED for every new block (see below)
5. **Test** in dev mode: `npm run dev` or `npm test`
6. **Regenerate docs** — REQUIRED after every block add/modify/remove:
   ```bash
   cd frontend
   npm run generate-docs
   ```
   This regenerates `BLOCKS.md` and all PNG images in `docs/blocks/`. Never skip this step.

---

## Unit Tests — REQUIRED for Every New Block

Every new block file **must** have a corresponding test file. This is a hard requirement.

**Location:** `frontend/test/blockly/{block_type}.test.js`

**Test file must cover:**
1. **Generator output** — correct Lua string emitted for representative inputs
2. **Field values** — all dropdown options generate the correct Lua variant
3. **Statement vs. value form** (for dual-mode blocks like `mh_startthread` pattern) — both forms generate correct output
4. **Edge cases** — empty inputs, zero values, boundary field options

**Minimal test pattern:**
```javascript
import { describe, it, expect } from 'vitest';
// Import the block definition
import { definition } from '../../../../src/components/blockly/mh_myblock.js';

describe('mh_myblock generator', () => {
    it('generates correct Lua for basic case', () => {
        const mockBlock = {
            getFieldValue: (name) => name === 'MY_FIELD' ? 'VALUE' : '',
            outputConnection: null,
        };
        const mockGenerator = {
            valueToCode: (_b, _name, _prec) => '42',
        };
        const result = definition.generator(mockBlock, mockGenerator);
        expect(result).toBe('myFunction(42, "VALUE")\n');
    });
});
```

**Run tests:**
```bash
cd frontend
npm test
```

**When to create tests:** Immediately after creating the block file, before registering it in `component.js`. Tests run in CI — a block without tests is incomplete.

The `component.js` registration loop handles everything:
```javascript
// Blockly block definition
Blockly.Blocks[type].init = function() { this.jsonInit(def.blockdefinition); }
// Lua generator
luaGenerator.forBlock[type] = (block) => def.generator(block, luaGenerator);
```

---

## Lua Code Generation

The workspace generates Lua code on every change:

```javascript
// In component.js — called on workspace change events
generateLUAPreview() {
    const code = luaGenerator.workspaceToCode(this.workspace);
    // code is the complete Lua script
}
```

Generated Lua script structure (from `mh_init` and `mh_startthread` blocks):
```lua
hub.init(function()
    -- initialization block contents
end)

hub.startthread('Thread Name', blockId, stackSize, false, function()
    -- thread loop contents
end)
```

---

## BLOCKS.md Auto-Generation

`BLOCKS.md` is **automatically generated** — never edit it manually.

**Command:**
```bash
cd frontend
npm run generate-docs
```

**How it works** (`frontend/scripts/generate-block-docs-simple.js`):
1. Runs `vite build` to produce a renderer bundle
2. Launches **Puppeteer** (headless Chrome)
3. Loads `block-renderer.html` which runs Blockly in the browser
4. For each block: renders to SVG → screenshot to PNG at 2× DPI
5. Saves PNGs to `docs/blocks/{category}/{blocktype}.png`
6. Generates Markdown with: block image, tooltip description, type, message template, inputs table, fields table
7. Appends a statistics summary (block counts by type and category)

**Output structure:**
```
docs/blocks/
  control flow/mh_init.png
  lego©/lego_get_mode_dataset.png
  ...
BLOCKS.md   ← regenerated in full
```

**When to regenerate**: after adding, removing, or changing any block definition, tooltip, inputs, or fields. The `tooltip` field in `blockdefinition` becomes the description in BLOCKS.md — keep it informative.

---

## Stateful Algorithm Block Pattern

All stateful algorithm blocks in the **Algorithms** category follow an **explicit handle pattern**. This is a hard convention — never use `block.id` as an implicit state key.

### Pattern: Init + Compute (same as PID and DR)

A stateful algorithm requires **two** Blockly blocks:

1. **Init block** (`mh_alg_*_init.js`) — creates a filter/controller instance, returns a handle string. The user stores this in a variable.
2. **Compute block** (`mh_alg_*.js`) — takes the handle as first input, plus algorithm parameters.

### Firmware side (`libluaalg.cpp`)

```cpp
// State map keyed by handle string ("ma_0", "ma_1", ...)
static std::map<std::string, MyState> myStates;
static int myHandleCounter = 0;

// Init: creates instance, returns handle
int alg_init_my(lua_State* L) {
    std::string handle = "my_" + std::to_string(myHandleCounter++);
    myStates[handle] = MyState{};
    lua_pushstring(L, handle.c_str());
    return 1;
}

// Compute: looks up by handle
int alg_my(lua_State* L) {
    const char* handle = luaL_checkstring(L, 1);
    auto it = myStates.find(handle);
    if (it == myStates.end()) {
        WARN("alg_my: handle '%s' not found", handle);
        lua_pushnumber(L, 0.0);
        return 1;
    }
    // ... use it->second ...
}

// Clear all: called in alg_library() at init
int alg_clear_all_my(lua_State* L) {
    myStates.clear();
    myHandleCounter = 0;
    return 0;
}
```

Register all three in `alg_library()`, and call `alg_clear_all_my` at the top of `alg_library()`.

### Blockly side

**Init block** — no inputs, output is a handle value:
```javascript
generator: (block, generator) => {
    return [`alg.initMy()`, 0];
},
```

**Compute block** — HANDLE is first input, uses `variables_get` shadow:
```javascript
inputsForToolbox: {
    HANDLE: {
        shadow: { type: 'variables_get', fields: { VAR: { name: 'myFilter' } } },
    },
    // ... other inputs ...
},
generator: (block, generator) => {
    const handle = generator.valueToCode(block, 'HANDLE', 0) || '"my_0"';
    // ...
    return [`alg.my(${handle}, ...)`, 0];
},
```

### Registration

Both blocks must be added to all three registration files:
- `frontend/src/components/blockly/component.js`
- `frontend/scripts/block-renderer.js`
- `frontend/scripts/generate-block-docs-simple.js`

### Stateless algorithms (`alg.map`)

Stateless algorithms (no persistent state) need only one block, no handle, no init, no clearAll. Register only the single block file.

---

## Toolbox Toolbox Shadow Defaults (`inputsForToolbox`)

To pre-populate inputs in the toolbox with useful defaults, add `inputsForToolbox`:

```javascript
inputsForToolbox: {
    VALUE: {
        shadow: {
            type: 'math_number',
            fields: { NUM: 500 }
        }
    }
}
```

The `generateToolbox()` function reads this and adds `<shadow>` elements automatically.
