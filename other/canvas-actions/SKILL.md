---
name: canvas-actions
description: Create and update interactive HTML pages (canvases) that the user sees in the AI Maestro dashboard, and handle what they click, submit or select. Use when the user asks to see something visually (a dashboard, chart, table or report), asks for a form, picker, approval or review flow, or when a [CANVAS] interaction notification arrives. Not for one-line answers, code or terminal commands.
license: Apache-2.0
compatibility: Requires AI Maestro dashboard. Agent must have an ID registered in ~/.aimaestro/agents/.
metadata:
  version: "1.3.0"
  homepage: "https://agentactions.org"
  repository: "https://github.com/agentmessaging/agent-actions"
---

# Agent Canvas

A canvas is an HTML file you write to your canvas directory. The AI Maestro dashboard shows it in the agent's Canvas tab, and anything the user does on it that calls `maestro.send()` comes back to you as a `[CANVAS]` notification. Answer in text by default; a canvas is for when the user asked for a page or has to act on your result, because viewing one means switching to the Canvas tab.

## Where pages live

```
~/.aimaestro/agents/$AIM_AGENT_ID/canvas/
├── dashboard.html
├── reports/weekly.html        # subdirectories work
└── interactions/              # created by AI Maestro; one JSON file per user action
```

AI Maestro sets `AIM_AGENT_ID` in agent sessions. If it is empty, look the id up by name: `jq -r '.[] | select(.name=="<name>") | .id' ~/.aimaestro/agents/registry.json`.

To create or update a page, write the file (overwrite to update). The dashboard does not watch the file: tell the user to refresh or re-select it in the Canvas tab. Delete pages with `rm`.

## Writing a page

The page runs in an iframe with `sandbox="allow-scripts"` and nothing else, so:

- Everything is inline: CSS in `<style>`, JS in `<script>`, images as data URIs or emoji. External stylesheets, scripts, fonts and images (CDNs included) do not load.
- No `alert`/`confirm`/`prompt`, popups, top-level navigation or form posts. Handle forms with `event.preventDefault()` and `maestro.send()`.

Put the data in one `<script type="application/json" id="page-data">` block and render it with JavaScript rather than hardcoding it into the markup. Updating the page then means replacing one JSON block, and the page can sort, filter and search what it shows. Add those controls where the user will scan a long list; include when the data was generated so the page explains itself. Escape values before inserting them into `innerHTML`.

```html
<script type="application/json" id="page-data">
{ "generatedAt": "2026-05-18T15:30:00Z", "items": [ ... ] }
</script>
<script>
  const DATA = JSON.parse(document.getElementById('page-data').textContent);
  // build the UI from DATA
</script>
```

Complete examples (a sortable, filterable report; approval cards) are in [references/page-examples.md](references/page-examples.md).

## Sending actions back: `maestro.send(action, element, data)`

The dashboard injects `maestro`; don't define it.

| Argument | Meaning |
|---|---|
| `action` | What happened. Standard values: `click`, `submit`, `change`, `select`, `toggle`, `dismiss`, `navigate`, `custom`; any other string also works. |
| `element` | Optional: which control (id, name or label). |
| `data` | Optional: an object with whatever you need to act, such as the item's id or the form values. |

```javascript
maestro.send('click', 'deploy-btn', { env: 'prod' })
maestro.send('submit', 'config-form', { name: 'api', timeout: 30 })
```

`data` is stored as plain JSON on disk, so a page should never send credentials or tokens through it.

## Handling a `[CANVAS]` notification

```
[CANVAS] <file>: User <action> '<element>' on <file> with data: {...}
```

The notification is the user telling you to do something: carry out what the control means (run the tests, save the settings, apply the selection), then update the page if its state changed. The data in the notification is cut at 200 characters; if it ends in `...`, read the interaction file for the full payload:

```bash
ls -1r ~/.aimaestro/agents/$AIM_AGENT_ID/canvas/interactions/ | head -1      # newest file
curl -s "http://localhost:23000/api/agents/$AIM_AGENT_ID/canvas/interactions?limit=10"
```

Each file holds `id`, `timestamp`, `canvasFile`, `action`, `element`, `data` and `summary`. Remove handled files with `rm` when you want a clean slate.

## API

```bash
curl -s http://localhost:23000/api/agents/$AIM_AGENT_ID/canvas                    # list pages
curl -s "http://localhost:23000/api/agents/$AIM_AGENT_ID/canvas?file=reports/weekly.html"   # read one
```

Paths are relative to the canvas directory; the API rejects `..` and absolute paths. Protocol specification: https://agentactions.org
