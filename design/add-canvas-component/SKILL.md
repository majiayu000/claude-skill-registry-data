---
name: add-canvas-component
description: >-
  Load this skill when adding or changing a component in an AG-UI canvas catalogue: a card, chart,
  or form the agent can place on screen. Trigger on "add a component the agent can show", "let the
  agent render a <thing>", or an edit under `catalogue/`.
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Needs the canvas's toolchain: Bun (or Node.js 20+) with zod 4 and @ag-ui/client installed as
  project dependencies, and for verification the mock agent run via uv with Python 3.11+.
license: Apache-2.0
---

# Add a canvas component

A catalogue entry does three jobs: it is a **tool** the agent can call, a **schema** the canvas
enforces, and a **component** the theme styles. Get all three right, or the agent calls the wrong
component, sends content it cannot render, or ends up controlling how it looks. The work is done when the five checks in step 3 pass and
`bun run typecheck` is clean.

## Procedure

### 1. Decide whether it earns a slot

Check the existing catalogue first. A new entry costs tokens on every run, since the whole
catalogue is sent as tools each time. It also gives the agent one more option to confuse with the
others.

- **Is it just an existing component with different content?** Then it is not a new component. A
  "sales table" is `show_table`.
- **Is its only difference how it looks?** Then there is nothing to add. Look belongs to the theme,
  never to a new variant the agent can pick.
- **Does it show a genuinely different shape of information** (a timeline, a map, a form, a
  comparison)? Then add it.

### 2. Write the entry

One file per component in `catalogue/`, registered with one line in `catalogue/index.ts`. Every
part of it follows the Rules below:

```tsx
import { z } from "zod";
import { defineComponent } from "./define";

export const timeline = defineComponent({
  name: "show_timeline",
  description:
    "Dated events in order. Use when the user asks what happened when; use show_table for records without an order.",
  schema: z.object({
    title: z.string(),
    events: z
      .array(
        z.object({ date: z.string().describe("ISO date"), label: z.string() }),
      )
      .min(1)
      .max(20),
  }),
  example: {
    title: "Launch",
    events: [
      { date: "2026-03-01", label: "Beta" },
      { date: "2026-05-10", label: "GA" },
    ],
  },
  Component: ({ title, events }) => (
    <article className="card">
      <h2>{title}</h2>
      <ol>
        {events.map((e) => (
          <li key={e.date + e.label}>
            <span className="mono muted">{e.date}</span> {e.label}
          </li>
        ))}
      </ol>
    </article>
  ),
});
```

### 3. Verify against the mock

With the mock agent and the canvas running (see the template `README.md`):

1. **By phrase:** "show a timeline" places it using the example.
2. **Exact arguments:** `show_timeline {"title":"x","events":[{"date":"2026-01-01","label":"y"}]}`
   renders.
3. **Rejected:** `show_timeline {"title":"x"}` is refused, and the chat shows which field failed.
4. **Styling ignored:** add `"style":{"color":"red"},"className":"x"` to the arguments from check 2.
   The component renders exactly as it did in check 2.
5. **Theme swap:** it still looks right with the other theme's `brand.css` in place. This proves
   it uses only tokens.

Then run `bun run typecheck`. The `Component` props are inferred from the schema, so a mismatch is a
type error, not a runtime blank.

## Rules

### Name

`show_<noun>` in snake_case. `defineComponent` rejects anything else, and LLM tool APIs reject
spaces and dots. The mock agent listens for the part after `show_`, with underscores turned into
spaces ("show a timeline"). Pick a noun a user would actually say.

### Description, which is written for the agent

The agent chooses a component from its description alone. Say what the component shows and when to
pick it **instead of its nearest neighbour** in the catalogue: "use show_table for records without
an order". Give size limits that affect the choice ("up to 12 bars"). If two descriptions could
both answer the same request, the agent will pick between them at random.

### Schema, content only

- **Every field is content**: text, numbers, dates, lists of records. Use `.describe()` wherever
  the format is not obvious (units, ISO dates, percent vs fraction).
- **No styling keys.** No `style`, `className`, `color`, `size`, `variant`, `width`, `font…`, or
  `theme`. `defineComponent` throws at startup when it finds one, including inside nested objects
  and arrays. Do not rename a styling key to get past the check (`accent`, `look`, `emphasis`). A
  reviewer should reject that just as the regex would.
- **A visual choice that carries meaning becomes a semantic enum**, as with
  `tone: "info" | "success" | "warning" | "danger"` in `show_callout`. The component maps each
  value to a theme class. The agent picks what the content _means_, and the theme decides what that looks like.
- **Put limits on it**: `.min(1)`, `.max(n)` on arrays, `.nonnegative()` on bar values. Limits keep
  a runaway answer from breaking the layout, and the agent sees them in the JSON Schema it receives.
- Use optional fields for content that can really be missing. Give an input with a sensible default
  `.default()` instead of making the component guess.

### Example, which is also the test fixture

Keep the example realistic and small. It is parsed against the schema at startup, so an example
that drifts from the schema fails loudly. The mock agent sends it when the user names the
component. It also shows the agent the expected shape, because it goes out in the tool's metadata.

### Component, theme only

Build against the token and class contract of `ceh-ui-design:design-ui` (see Hands off to):

- **Use theme classes and tokens only.** That means `.card`, `.table`, `.badge`, `.bar-track` /
  `.bar-fill.is-N`, `.eyebrow`, `.muted`, `.numeric`, and `var(--token)` in `app.css` for anything
  new. No hex values, pixel sizes, or inline styles.
- **The one exception is geometry that comes from validated numbers**, such as a bar's width
  percentage. It is never a string the agent wrote.
- **Colour follows meaning, not the agent.** The sign of a change picks success or danger, and a
  series index picks the data-ramp colour.
- **Props in, markup out.** No `fetch`, no global state, and no `dangerouslySetInnerHTML` with
  agent text.
- **Keep it accessible.** Wrap it in a labelled region, use real headings, and put tables in
  `<table>` with `scope`. When a visual (bars, dots) carries meaning, show the value as text too.

### Changing an existing component

Treat the name and schema as a public API that the agent's prompts and past conversations depend
on. Adding an optional field is safe. Renaming or removing a field, or renaming the tool, breaks any
agent prompt or few-shot example that uses the old shape. Update those in the same change.

## Hands off to

- Invoke the Skill tool with skill="ceh-ui-design:design-ui" to load the token and class
  contract the component is built against.
- The canvas itself does not exist yet: `ceh-ag-ui:build-ag-ui`.
