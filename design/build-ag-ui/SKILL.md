---
name: build-ag-ui
description: >-
  Load this skill when starting a generative-UI frontend for an AG-UI agent: a canvas where the
  agent answers by placing components from a catalogue. Trigger on "build a UI with AG-UI",
  "generative UI for my agent", or @ag-ui/client with no canvas yet.
disable-model-invocation: false
user-invocable: true
compatibility: >-
  The canvas needs Bun (or Node.js 20+) and network access for the first install; react, vite, zod
  and @ag-ui/client arrive as project dependencies. The mock agent needs uv and Python 3.11+, with
  fastapi, uvicorn and ag-ui-protocol installed by uv. Without uv, point the canvas at an existing
  AG-UI endpoint instead. Written against @ag-ui/client and ag-ui-protocol 1.0, zod 4.
license: Apache-2.0
---

# Build a generative-UI canvas on AG-UI

The user types, and the agent answers by **placing components**. It never writes the markup. The
catalogue fixes the set of components at build time, and the theme fixes how they look. The agent
chooses which component to show and fills in its content, and it controls nothing else.

How it works over AG-UI: each catalogue entry is sent to the agent as a **frontend tool** on every
run. When the agent calls one, the canvas checks the arguments against that entry's schema, renders
the component, and returns a tool result. It then runs the agent again so it can respond.

## Procedure

### 1. Pick the canvas

- **The user gave a template** (a path, a repo, or an existing app): build on it. Find its four
  seams (the table below). Add any missing seam in the template's own style instead of replacing
  its structure.
- **No template**: copy `${CLAUDE_SKILL_DIR}/assets/canvas-template/` into the project (default:
  `web/` and `agent/` at the repo root). Always copy, and never edit the files under the skill
  directory.

| Seam             | Default file          | Owns                                                                                                    |
| ---------------- | --------------------- | ------------------------------------------------------------------------------------------------------- |
| Catalogue        | `web/src/catalogue/`  | One file per component: `defineComponent({ name, description, schema, example, Component })`            |
| Agent connection | `web/src/useAgent.ts` | One `HttpAgent`, sends the catalogue as tools, validates the arguments, returns tool results, loops     |
| Canvas           | `web/src/App.tsx`     | Renders the placed blocks, an empty state with starter prompts, and the chat input that is always there |
| Theme            | `web/src/brand.css`   | Every colour, font, spacing value and component class. Nothing else sets a style                        |

The canvas starts with no components placed. It is never blank: the chat input is always there, and
the empty state offers starter prompts built from the catalogue.

### 2. Install the theme

Invoke the Skill tool with skill="ceh-ui-design:design-ui" and follow its _Theme layer_, with
one override: the theme is already chosen. Use **Tidewater** without asking, unless the user named
Meridian or brought their own token file with the same token and class contract. Copy the
`tidewater/brand.css` file from that skill's references directory to `web/src/brand.css`, which
`app.css` imports first. Switching later means replacing that one file, and no markup changes, so a
canvas build never stalls on a look-and-feel question.

### 3. Shape the catalogue

The seven default components cover most answers. Keep the ones the app needs and delete the rest,
removing each from `catalogue/index.ts` as well.

| Tool              | Shows                                                                   |
| ----------------- | ----------------------------------------------------------------------- |
| `show_note`       | A titled block of prose                                                 |
| `show_stat`       | One KPI, with an optional change whose colour comes from its sign       |
| `show_table`      | Records with named columns                                              |
| `show_list`       | Short items, ordered or not                                             |
| `show_key_values` | The labelled facts about one item                                       |
| `show_callout`    | A message with a semantic `tone`: info, success, warning or danger      |
| `show_bar_chart`  | Up to 12 values compared by length, coloured from the theme's data ramp |

For any component the app needs beyond these, invoke the Skill tool with
skill="ceh-ag-ui:add-canvas-component". It holds the rules each entry must pass.

### 4. Run it against the mock

Start both halves with the commands in the template's `README.md`, then check:

1. The empty state shows starter prompts. Clicking one places that component.
2. Every catalogue entry renders from its phrase: "show a table", "show key values", and so on.
3. Sending `show_note {"title":"t","body":"b","style":{"color":"red"}}` renders a note with no style
   applied.
4. `show_stat {"label":"x"}` is refused, and the chat shows the reason.

The mock agent (`agent/main.py`) has no LLM. A message containing a component's phrase places that
component with the `example` arguments the canvas sends in each tool's metadata. The form
`<tool> <json>` sends exact arguments.

### 5. Connect the real agent

Any AG-UI server works if it passes the frontend tools through to its model and **ends the run** as
soon as the model calls one. The canvas renders the component and starts the next run itself. To
build that server, invoke the Skill tool with skill="ceh-ag-ui:build-ag-ui-agent".

- **Dev:** set `AGENT_ORIGIN` and Vite proxies `/agent` to it, so no CORS setup is needed. If the
  real endpoint uses a different path, change the proxy key in `vite.config.ts`.
- **Deployed:** set `VITE_AGENT_URL`. The server must then allow the canvas's origin.

Keep `agent/` for testing components, and delete it only when the user asks.

## Rules

### The styling lock

The agent must never be able to change how a component looks. Three layers enforce this, and none
of them may be removed:

1. **The schema is content only.** `defineComponent` throws at startup if a schema exposes a
   style-like key (`style`, `className`, `color`, `size`, `variant`, …). When a visual choice is
   genuinely needed, it becomes a semantic enum, such as `tone` in `show_callout`, and the
   component maps it to a theme class.
2. **Arguments are parsed, not spread.** `useAgent` renders only `schema.safeParse(args).data`.
   Unknown keys are stripped, so an agent that sends `style` or `className` gets a normal render
   without them. Invalid arguments render nothing, and the agent receives an `error:` tool result
   it can correct from.
3. **Components use only theme tokens and classes.** They never use a hex value, a pixel size, or
   an inline style built from agent text. The one inline style in the template is the bar width in
   `show_bar_chart`, and that comes from a number the schema already validated.

### The loop, and how it breaks

- **Every frontend tool call needs a tool message before the next run.** An unanswered call makes
  most LLM providers reject the whole conversation.
- **Tool calls not in the catalogue are left alone.** They belong to the backend, which answers
  them itself.
- **`MAX_TOOL_ROUNDS` (5) caps the runs per message**, so an agent stuck in a render-reject loop
  stops.
- **Create the agent once** (`useMemo`) and unsubscribe in the effect's cleanup. StrictMode runs
  effects twice in development.
- **Stop is `abortRun()`.** It does not remove components that were already placed.

## Output

A canvas (`web/`) and a mock agent (`agent/`) in the project, or the same four seams added to the
user's template. The work is done when:

- The theme is installed from `design-ui`, and no component carries a hard-coded style.
- Every catalogue entry renders from the mock, rejects bad arguments, and ignores injected styling.
- The canvas runs end to end against the real agent, and no frontend tool call is left without a
  tool message.

## Hands off to

- Invoke the Skill tool with skill="ceh-ui-design:design-ui" to install the theme (step 2).
- A component beyond the seven defaults goes to `ceh-ag-ui:add-canvas-component`, and the real
  agent server to `ceh-ag-ui:build-ag-ui-agent`.
- Later, the canvas can grow **shared state**, where the agent keeps a live value the UI mirrors
  (`ceh-ag-ui:add-live-state-panel`). It can also get **approval steps**, where the agent pauses
  until the user decides (`ceh-ag-ui:add-human-approval`).
