---
name: tokens-to-figma
description: "Push a codebase's design tokens into Figma as variables and modes. Use when the user says \"sync tokens to Figma\", \"create Figma variables from code\" or \"push design tokens to Figma\"."
license: MIT
metadata:
  author: Tony Gorb
  source: https://github.com/tonygorb/skills
  category: figma
  cover: "2 modes"
---

# Tokens to Figma

Mirror the code's tokens in a Figma file as variables: primitives as raw values, semantic tokens
as aliases with a Light and a Dark mode. Code stays the source of truth. Figma follows it, by name,
and every write is checked by reading it back.

## What it needs

Check all of these first. If one is missing, say what and stop.

1. **The Figma MCP server, connected, with its `use_figma` tool.** That tool runs Plugin API
   scripts in the file; it is how variables get written. Read-only Figma access is not enough.
2. **Figma's `figma-use` skill, if your agent has it.** Load it before the first `use_figma` call,
   every session. Skipping it causes failures that are hard to trace.
3. **A Figma file URL with edit access.** This skill writes into an existing file; it doesn't
   create one. With some setups the file must also be open in the Figma desktop app.
4. **A Figma plan with variable modes** (Professional or above). Starter files can't add a Dark
   mode, so `02 Semantic` can't hold Light and Dark there. On Starter, say so and stop.
5. **Tokens in the code**, readable: a tokens JSON file, a Tailwind v4 `@theme` block, or `:root`
   and dark-mode custom properties. Ideally already split into primitives and semantic tokens
   (see `token-foundations`).

If the MCP server or `use_figma` isn't available, write a short status ("not synced: Figma MCP
unavailable") and stop. Never describe a sync that didn't happen.

## Steps

### 1. Read the tokens from code

Collect every token with its value per mode:

- **Primitives:** colour scales, spacing, radius, container widths, durations, easings.
- **Semantic tokens:** each colour role with its light and dark value, recorded as a reference to
  a primitive (`--color-action-primary` → `brand-600` light, `brand-500` dark).
- **Component tokens:** button and input heights, card padding, component radii.

Resolve `var(…)` chains so you know which primitive each semantic token points at. If a semantic
token holds a raw value instead (`white`, a hex), list it. It can't become an alias until a
primitive for it exists in code.

### 2. Build the name map

Code uses kebab-case CSS variables; Figma uses slash-separated PascalCase. One token, one
variable, one name in each place:

| Code | Figma |
|---|---|
| `--color-brand-500` | `Color/Brand/500` |
| `--color-background` | `Color/Background` |
| `--color-surface-default` | `Color/Surface/Default` |
| `--color-action-primary-hover` | `Color/Action/Primary Hover` |
| `--spacing-4` | `Spacing/4` |
| `--radius-md` | `Radius/Md` |
| `--duration-fast` | `Duration/Fast` |

Show the map. Offer to save it in the repo (for example `design-system/figma-map.json`) so later
runs and drift checks match by the same names. Ask before adding the file.

### 3. Inspect the file

With `use_figma`, list the file's variable collections, their modes and their variables. Sort every
token into one of three:

- **Exists and matches:** skip it.
- **Exists and differs:** update it, matched by name.
- **Missing:** create it.

If the file already holds variables, ask which it is: **update in place**, or **create only** (leave
every difference alone and list it for review). Never touch variables that aren't in the map.

### 4. Plan the collections

| Collection | Holds | Modes |
|---|---|---|
| `01 Brand` | Primitive colour scales: brand, neutral, accent, state | one |
| `02 Semantic` | Semantic colour roles, each an alias to a `01 Brand` variable | Light, Dark |
| `03 Component` | Button and input sizes, card and section padding, component radii | one, or Light and Dark if values differ by theme |
| `04 Layout` | Spacing, radius scale, container widths | one |
| `05 Motion` | Durations (number), easings (string) | one |

Types: colours are COLOR, sizes and durations are FLOAT, easings and font families are STRING.

Scopes, so each variable only shows up where it belongs:

| Variables | Scopes |
|---|---|
| Colour (default) | `FRAME_FILL`, `SHAPE_FILL`, `TEXT_FILL`, `STROKE_COLOR`, `EFFECT_COLOR` |
| `Color/Text/*` | `TEXT_FILL` |
| `Color/Border/*` | `STROKE_COLOR` |
| `Color/Background`, `Color/Surface/*` | `FRAME_FILL`, `SHAPE_FILL` |
| `Spacing/*` | `GAP` |
| `Radius/*` | `CORNER_RADIUS` |
| `Container/*` | `WIDTH_HEIGHT` |

Show the plan with counts (create, update, skip, conflicts) and wait for a yes.

### 5. Write, one collection per call

Order: collections, then modes, then `01 Brand`, `02 Semantic`, `03 Component`, `04 Layout`,
`05 Motion`, then scopes. One `use_figma` call per collection keeps each call small and each
failure contained.

A new collection starts with one mode. Rename it `Light` and add `Dark` where the plan says two.

Figma stores colour as sRGB from 0 to 1, so convert each OKLCH value inside the script. The plugin
runtime has no colour library; ship the conversion inline:

```js
function oklchToRgb(L, C, H) { // L in %, returns Figma {r, g, b, a} plus clamped: true if out of sRGB
  const Lp = L / 100, a = C * Math.cos(H * Math.PI / 180), b = C * Math.sin(H * Math.PI / 180);
  const l = (Lp + 0.3963377774 * a + 0.2158037573 * b) ** 3;
  const m = (Lp - 0.1055613458 * a - 0.0638541728 * b) ** 3;
  const s = (Lp - 0.0894841775 * a - 1.2914855480 * b) ** 3;
  const lin = [4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
              -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
              -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s];
  const enc = v => v <= 0.0031308 ? 12.92 * v : 1.055 * v ** (1 / 2.4) - 0.055;
  const clamped = lin.some(v => v < -1e-4 || v > 1 + 1e-4);
  const [r, g, bl] = lin.map(v => Math.max(0, Math.min(1, enc(v))));
  return { r, g, b: bl, a: 1, clamped };
}
```

Pass Figma only `{ r, g, b, a }`. Where `clamped` is true, the value was outside sRGB: list it in
the report.

Find or create by name, never blindly create:

```js
const cols = await figma.variables.getLocalVariableCollectionsAsync();
const brand = cols.find(c => c.name === "01 Brand")
  ?? figma.variables.createVariableCollection("01 Brand");
const vars = await figma.variables.getLocalVariablesAsync("COLOR");
const find = name => vars.find(v => v.name === name && v.variableCollectionId === brand.id);

const v = find("Color/Brand/500") ?? figma.variables.createVariable("Color/Brand/500", brand, "COLOR");
const { clamped, ...rgba } = oklchToRgb(60, 0.18, 250);
v.setValueForMode(brand.defaultModeId, rgba);
v.scopes = ["FRAME_FILL", "SHAPE_FILL", "TEXT_FILL", "STROKE_COLOR", "EFFECT_COLOR"];
```

Semantic variables hold aliases, never raw colours. Set one per mode:

```js
semanticVar.setValueForMode(lightModeId, figma.variables.createVariableAlias(brand600));
semanticVar.setValueForMode(darkModeId, figma.variables.createVariableAlias(brand500));
```

That way a change to a brand primitive flows through every role that uses it.

### 6. Read back after every call

After each collection, read the variables again with `use_figma` and confirm:

- each variable exists, in the right collection;
- every mode has a value;
- scopes match the plan;
- each semantic alias resolves to the right primitive, in both modes.

Mark anything that fails as failed. Count only what the read-back confirmed.

### 7. Styles, only if asked

Variables carry single values. If the user also wants local styles, the same rules apply:

- **Text styles** (Display, Heading, Body, Caption, Label) match the code's type scale exactly:
  same sizes, line heights, weights and letter spacing.
- **Effect styles** (Shadow Xs to Xl, Focus Ring) take their colour from a variable, never a raw
  value.

Match by name, write, read back, as above.

### 8. Report

```
## Tokens to Figma

File: <url>
Mode: <update in place | create only>

| Collection | Created | Updated | Skipped | Failed |
|---|---:|---:|---:|---:|
| 01 Brand | | | | |
| 02 Semantic | | | | |
| ... | | | | |

Verified by read-back: <N of M>
Conflicts left for review: <list, or "none">
Out-of-gamut colours clamped: <list, or "none">
Raw values that couldn't alias: <list, or "none">
Tokens Figma has that code doesn't: <list, or "none">
```

## Checking drift later

Read-only. Compare the file against the name map and today's code:

- **Missing in Figma:** in code, not in the file.
- **Extra in Figma:** in the file, not in code.
- **Value mismatches:** different value, missing mode, wrong scope, or an alias pointing at the
  wrong primitive.

Report every item, even minor ones. Partial is not in sync. Fix drift by changing code first and
re-running, never by editing Figma alone.

## Never

- Call `use_figma` before loading `figma-use`, when your agent has it.
- Claim a variable was written without reading it back.
- Pretend to sync when the MCP server is unavailable.
- Create a duplicate. Match by name and update in place.
- Invent a Figma-only token. Add it in code and the name map first.
- Store a raw colour in a semantic variable. Alias it to a primitive.
- Overwrite or delete Figma variables that aren't in the map.
- Ship a semantic collection without both Light and Dark modes.

## Red flags: you're about to fake a sync

- "The script ran without errors." That isn't proof. Read the variables back.
- "I'll create them all fresh, it's quicker." That duplicates. Find by name first.
- "This one colour is only for Figma." Then it isn't a token yet. Put it in code first.
