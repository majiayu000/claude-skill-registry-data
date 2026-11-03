---
name: platform-widget-generate
description: "Use this skill to author a complete HXL WidgetBundle (UEM body + schema.json + -meta.xml). TRIGGER when: user asks for a widget, mosaic, fragment, card, or rich UI surface for any subject, domain, feature, or entity noun; the prompt names only an entity or data shape without invoking Lightning Types, CLTs, or Apex-backed types. DO NOT TRIGGER when: the prompt explicitly says 'Lightning Type', 'CLT', 'Custom Lightning Type', 'Apex-backed type', or references '@apexClassType/...' (use platform-lightning-type-widget-coordinate); authoring a custom-LWC renderer for a Custom Lightning Type (use platform-custom-lightning-type-generate); or editing only an LWC component."
metadata:
  version: "1.5"
  domains: ["Platform", "Agentforce"]
  minApiVersion: "68.0"
  cliTools:
    - tool: ["sf"]
      semver: ">=2.0.0"
  relatedSkills:
    - "platform-apex-generate"
    - "platform-custom-lightning-type-generate"
    - "platform-lightning-type-widget-coordinate"
---

# Generating a Widget Bundle

Author a complete WidgetBundle: a UEM tree (`tile/widget`), a JSON Schema describing the widget's input contract, and the `.uiwidget-meta.xml` that registers the bundle.

## When to Use This Skill

Use when the user asks for a widget, mosaic, fragment, or card-style rich UI surface. Do not use this skill for custom-LWC renderers or for `renderer.json` files inside a Custom Lightning Type bundle — those belong to `platform-custom-lightning-type-generate`.

## Inputs

- **`widgetName`** (required) — `camelCase` identifier; becomes the directory name under `uiWidgets/`.
- A **shape** — what data the widget renders. The widget cannot be generated without it. The shape arrives one of two ways, in priority order:
  1. **`lightningTypeSchema`** — `{ path, apexClassFqn }` for an existing Apex-backed Lightning Type. The FQN takes one of two forms: outer-class (`<namespace>__<ClassName>`) where the outer class is the payload, or inner-class (`<namespace>__<ClassName>$<InnerClass>`) where the named inner class is the payload. Passed in by the `platform-lightning-type-widget-coordinate` orchestrator. When present, derive per `references/schema-from-lightning-type.md`.
  2. **Extracted from the user's prompt** — when no `lightningTypeSchema` is passed, infer the shape directly from what the user wrote: a pasted JSON payload, an enumerated field list ("id as string, total as number"), or descriptive prose. The output is the same ordered list of `{ name, type, required }` either way.

If neither source yields a shape, STOP and ask the user before proceeding.

## Output

Three files in `<pkgDir>/uiWidgets/<widgetName>/`:

| File | Content |
|---|---|
| `<widgetName>.json` | Widget envelope — `{ "type": "lightning__agentforceWidget", "contentBody": { "widgetBody": { UEM tree rooted at tile/widget } } }` |
| `schema.json` | JSON Schema — root has `type: "object"` + `properties.attributes` wrapper carrying `lightning:type: "lightning__objectType"` and the field `properties` |
| `<widgetName>.uiwidget-meta.xml` | `<UiWidgetBundle>` element with `<masterLabel>`, `<description>`, and `<widgetType>JSON</widgetType>` |

See `references/widget-bundle-layout.md` for the `<pkgDir>` resolution procedure and the exact `<widgetName>.uiwidget-meta.xml` shape.

---

## Composition

A widget body is a UEM tree of blocks nested under `contentBody.widgetBody`. The root node is `tile/widget`. Every node — root and non-root — has the same shape: no `type` key; just `definition`, optional `attributes`, optional `meta`, and optional `children`. Block shape:

```ts
interface Block {
  definition: string  // {namespace}/{blockName} — root is "tile/widget"
  attributes?: Record<string, any>
  meta?: { // see references/widget-meta-directives.md
    forEach?: string
    forItem?: string
    if?: string
  }
  children?: Block[]
}
```

The first child of `tile/widget.children` SHOULD be a single `tile/column`. All widget content typically goes inside that first child for predictable vertical structure across surfaces.

---

## Available Invocable Actions

Both are standard invocable actions on the target org.

### Calling Convention

Fire each action with whichever mechanism is available: the H360 MCP `dispatch` tool (a `POST` to the endpoint path with the request body) or `sf api request rest`. Use `v{version}` = this skill's `minApiVersion`. Never use `curl`, and never extract the org's access token.

```bash
sf api request rest '/services/data/v{version}/actions/standard/<actionName>' --method POST --body '<request body>' --target-org <org>
```

### Response Handling

Each response is an array with one envelope (`dispatch` nests it under `body`). Check three failure layers, in order:

| Layer | Signal | Action |
|---|---|---|
| Transport / auth | `dispatch` `status_code` is not 200, or CLI exits non-zero | Surface the error |
| Action | `[0].isSuccess` is `false`, or `[0].errors` is non-empty | Surface `errors[].message` |
| Per-entry (`getUiComponentSchemas` only) | any `componentSchemas[].success` is `false`, even when `[0].isSuccess` is `true` | Treat that block as unavailable |

On success, read `[0].outputValues`.

### discoverUiComponents

**Purpose:** Discover the palette of blocks available for composition.

**Endpoint:** `POST /services/data/v{version}/actions/standard/discoverUiComponents`

**Request body:** `{"inputs":[{"pageType":"FRAGMENT"}]}`

**Returns:** `outputValues.componentDefinitions[]` — list of `{ definition, description, label }`.

### getUiComponentSchemas

**Purpose:** Fetch schemas (property types, required vs optional, validation) for selected blocks.

**Endpoint:** `POST /services/data/v{version}/actions/standard/getUiComponentSchemas`

**Request body:** `{"inputs":[{"pageType":"FRAGMENT","componentDefinitions":["namespace/definition", ...]}]}`

**Returns:** `outputValues.componentSchemas[]` — list of `{ definition, success, schema }` (`schema` is a YAML string). Partial failures are supported.

> Never pass `tile/widget` to `getUiComponentSchemas` — it is a fixed wrapper, not a queryable component.

---

## Attribute Binding

- Bind a block property to runtime data with `{!$attrs.<attrName>}`. `<attrName>` MUST match a property name in `schema.json`.
- Inside a `forEach`, reference the loop variable instead — e.g. `"text": "{!$item.name}"`. See `references/widget-meta-directives.md`.
- A binding may be a **formula expression** instead of a bare field reference. See `references/widget-formulas.md` for the full supported-function list, syntax, and gotchas.
- **Localization:** only when the user asks for localized or translated text (or names Custom Labels / `$Label`), write static, user-visible strings as Custom Label references — `{!$Label.c.<LabelName>}`. See `references/widget-labels.md`.

---

## Actions

`tile/button` supports an `actions` attribute that dispatches an action node on an event. Two action definitions are supported:

| Action | Timing | Required attributes | Effect |
|---|---|---|---|
| `action/openLink` | synchronous | `url` (string). Optional `target` (`_blank`\|`_self`, default `_blank`) | Opens a URL |
| `action/sendMessage` | asynchronous | `content` (string) | Posts a new user message back to the agent and earns a fresh turn |

See `references/widget-actions.md` for complete `sendMessage` and `openLink` button JSON.

**A `tile/button` with no `actions` attribute renders disabled** — a button exists to trigger an action, so always attach a `click` action to a button meant to be interactive.

---

## Layout Best Practices

These conventions cover widget *structure* — how blocks are grouped and stacked.

| Primitive | Purpose | When to use |
|---|---|---|
| `tile/column` | Vertical stack of children | Root wrapper, and any group of blocks that should stack |
| `tile/row` | Horizontal stack of children | Two or more blocks that belong on the same line |
| `tile/spacer` | Whitespace between blocks | When extra space is needed between content groups |

- **Nesting:** Prefer flat layouts. Only nest a `tile/column` inside a `tile/row` (or vice versa) when the visual orientation actually changes for that subgroup.
- **Authoritative palette:** the table above lists *typical* layout primitives. Always confirm a block exists by inspecting `discoverUiComponents` output — do not assume a block name from this table without seeing it in the discovery response.

---

## Styling Best Practices

Style semantically (variants, not literal colors or pixels), one primary button per group, one `h1` per widget, Lucide icons only. Read `references/widget-styling.md` before assigning variants, sizes, or icons.

---

## Workflow

1. **Resolve the widget spec** — an ordered list of `{ name, type, required }`. Source depends on which input was provided (see *Inputs*):
   - If `lightningTypeSchema` was passed by the orchestrator → derive per `references/schema-from-lightning-type.md`.
   - Otherwise → infer the list directly from the user prompt (pasted JSON payload, enumerated field list, or descriptive prose).

2. **Discover blocks (REQUIRED — do NOT skip).** Call the `discoverUiComponents` invocable action (see *Available Invocable Actions*) and match widget-spec property types against the returned `label`/`description` values. **If `isSuccess` is `false`, `errors` is non-empty, or `componentDefinitions` is empty, STOP and surface the error verbatim — do not improvise block names from memory, prior runs, or training data.**

3. **Select blocks.** Choose one block per widget-spec property, plus structural primitives from *Layout Best Practices*.

4. **Get block schemas (REQUIRED — do NOT skip).** Call the `getUiComponentSchemas` invocable action for the selected blocks. Review property metadata, including each property's `default` — omit any attribute whose value would equal it (see `references/widget-styling.md`). **If `isSuccess` is `false`, `componentSchemas` is empty, or any entry has `success: false`, do not use that block — re-select a different one from step 2's results; if none works, STOP and surface the error. Never improvise from existing widgets in the project.**

5. **Build the UEM tree (example reads REQUIRED — do NOT skip).** First, identify which patterns match the widget spec and read each matching example file from this skill's own `examples/` directory (`<skill-root>/examples/`):

   | Pattern in the spec | Example to read |
   |---|---|
   | Single object (no iteration) | `<skill-root>/examples/single-object.json` |
   | Any list iteration (root-level array, nested list, or list embedded in a single-object widget) | `<skill-root>/examples/list-with-foreach.json` |
   | Conditional rendering (`if` bound to a boolean or formula) | `<skill-root>/examples/conditional.json` |
   | Computed values, text/number transforms, locale-formatted numbers/currency/dates, or `if` driven by a formula (not a bare boolean field) | `<skill-root>/examples/formulas.json` |
   | The user asked for localized / translated text (Custom Labels) | `<skill-root>/examples/localized-labels.json` |

   A spec may match multiple patterns (e.g. a list of items where some items render conditionally reads both `list-with-foreach.json` and `conditional.json`). **Read every matching example, and only those — do not skip the read because the pattern feels familiar.**

   **Before writing any formula**, read `references/widget-formulas.md` in full — it is the authoritative list of supported operators and functions; do not improvise a function name or operator that isn't documented there.

   **Before writing any `$Label` reference**, read `references/widget-labels.md` in full.

   Then:
   - Map each widget-spec property to a block property; preserve spec order.
   - **Decide root iteration:** single object → properties directly under root `tile/column`. Collection → wrap repeating block in `forEach`/`forItem`. See `references/widget-meta-directives.md`.
   - Bind values with `{!$attrs.X}` (or `{!$item.X}` inside `forEach`).
   - For conditional blocks, add `"if"` on `meta` — either a bare `lightning__booleanType` property, or a formula expression that evaluates to boolean. See `references/widget-formulas.md`.
   - **When the widget spec calls for a computed value** (a total, a derived label, a formatted string) rather than a raw field, express it as a formula inside `{!...}` per `references/widget-formulas.md` — do not invent a new schema property to hold a value that can be computed from existing ones.

6. **Author `schema.json`.** Build the JSON Schema from the widget spec. Fields live one level deep under an `attributes` wrapper:

   ```json
   {
     "title": "<Widget Display Name>",
     "description": "<one line about what the widget shows>",
     "type": "object",
     "properties": {
       "attributes": {
         "lightning:type": "lightning__objectType",
         "properties": {
           "<propertyName>": {
             "title": "<label>",
             "description": "<short description>",
             "lightning:type": "<lightning__textType | lightning__numberType | ...>"
           }
         }
       }
     }
   }
   ```

   **Required root keys:** `title`, `type: "object"`, `properties.attributes` (with `lightning:type: "lightning__objectType"` and a nested `properties` map). See `references/schema-from-lightning-type.md` for full primitive type guidance.

7. **Author `<widgetName>.uiwidget-meta.xml`.** See `references/widget-bundle-layout.md` for the exact shape.

8. **Resolve `<pkgDir>` and write the bundle.** Follow the procedure in `references/widget-bundle-layout.md` (`## Resolving <pkgDir>`). A widget bundle is a **three-file set** — all three files must be written in the same step; a bundle with fewer than three files is incomplete and will not deploy.

   ```text
   <pkgDir>/uiWidgets/<widgetName>/<widgetName>.json               # widget envelope — UEM tree (primary artifact)
   <pkgDir>/uiWidgets/<widgetName>/schema.json                     # attribute contract for the envelope
   <pkgDir>/uiWidgets/<widgetName>/<widgetName>.uiwidget-meta.xml  # UiWidgetBundle registration
   ```

   Each file has a distinct role:
   - `<widgetName>.json` — the widget envelope with the `tile/widget` UEM tree. This is the primary artifact; `schema.json` is its companion contract, not a substitute.
   - `schema.json` — the JSON Schema for the attributes referenced by `{!$attrs.X}` bindings in the envelope.
   - `<widgetName>.uiwidget-meta.xml` — the `UiWidgetBundle` element that registers the bundle for source tracking and deployment.

   Write all three before proceeding to self-validation.

9. **Self-validate.** Before reporting, run the checks and report each result individually (`pass` or `fail (<reason>)`). Do **not** summarize as a single "all passed" line — list every check so a reviewer can spot a silent skip.
Run every check in `references/widget-bundle-validation.md`.

10. **Report labels.** If the widget uses `$Label`, end the response with the label report described in `references/widget-labels.md`.

---

## Rules / Constraints

| Constraint | Rationale |
|---|---|
| Block definitions follow `{namespace}/{blockName}` and must match `discoverUiComponents` output | Runtime resolves blocks by exact definition string |
| Never pass `tile/widget` to `getUiComponentSchemas` | It is a fixed wrapper, not a queryable component |
| Read `references/` and `examples/` files only at the step that names them | Upfront reads waste context and precede the discovery result that determines which files are needed |
| Every `{!$attrs.X}` in the body resolves to a property in the widget `schema.json` | No invented fields |
| Every `tile/button` carries an `actions.click` entry using `action/openLink` or `action/sendMessage` only | These are the only two supported tile action definitions; an action-less button renders disabled |
| No `$(…)`, backticks, `<(…)`, brace expansion `{a,b,c}`, or `eval`/`exec` in any Bash tool call | Vibes' safe-shell filter forces manual approval on these patterns even in Bypass mode. Emit separate commands (`mkdir -p a && mkdir -p b`) or print each value with its own command and reason about the output — do not capture into a shell variable |

---

## Gotchas

Known failure modes and fixes (partial schemas, unresolved bindings, wrong output path, `if` truthiness, dead buttons, action choice): see `references/widget-gotchas.md`.

---

## Reference File Index

| File | When to read                                                                                                                                                                        |
|---|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `references/widget-meta-directives.md` | For `forEach` / `forItem` (iteration) and `if` (conditional rendering), including nested loops                                                                                      |
| `references/schema-from-lightning-type.md` | When `lightningTypeSchema` is provided; how to derive the widget `schema.json` from an Apex-backed Lightning Type                                                                   |
| `references/widget-bundle-layout.md` | Folder layout, `-meta.xml` shape, `<pkgDir>` resolution rules                                                                                                                       |
| `references/widget-bundle-validation.md` | Step 9 — the checks to run before reporting |
| `references/widget-formulas.md` | Supported formula functions and operators, including locale format functions (`FORMATNUMBER`, `FORMATCURRENCY`, `FORMATDATE`, …)                                                                                                                                           |
| `references/widget-labels.md` | Localization — `$Label` syntax, naming and reuse, allowed attributes, combining with data, creating labels, and the label report |
| `references/widget-actions.md` | Complete `tile/button` JSON for `action/sendMessage` and `action/openLink` |
| `references/widget-styling.md` | Variant, size, heading, and icon conventions |
| `references/widget-gotchas.md` | Known failure modes and their fixes |
| `examples/single-object.json` | Single-object pattern (root binding via `{!$attrs.X}`, no iteration)                                                                                                                |
| `examples/list-with-foreach.json` | Any list-iteration case — root-level collections, nested lists, and lists embedded inside a single-object widget (e.g. iterating a `List<InnerClass>` inside an outer Apex payload) |
| `examples/conditional.json` | Conditional pattern (`if` on `meta`, including `if` + `forEach` together)                                                                                                           |
| `examples/formulas.json` | Formula usage — text/arithmetic/date transforms, locale format functions, `IF`/`AND`/`NOT` driving both a `tile/text` and `meta.if`                                                                          |
| `examples/localized-labels.json` | Localization — `$Label` in a heading, caption, badge (`IF` choosing between labels), button label, and a label joined with data |
