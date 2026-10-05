---
name: validate-ui
description: Validate UI changes in the browser using Chrome DevTools MCP. Use when the user asks to verify, check, or validate UI changes in the browser, or mentions browser testing, visual verification, or E2E-style validation after code edits.
---

# UI Validation with Chrome DevTools

Use the `user-chrome-devtools` MCP server to validate UI in the browser after code changes.

## Prerequisites

- A dev server must be running at `http://localhost:3005`.
- Chrome must be open with the target page loaded.

## Two Modes

### Mode 1 - Auto (default)

Used when the user does not provide an expected behavior. Detects regressions from the code change and confirms that the change took effect.

> "Edit this component and check it in the browser."

### Mode 2 - Scenario-based

Used when the user provides an interaction scenario and expected outcome. Execute the scenario and compare against the expected result.

> "Edit it and verify. Clicking the first list item should open the detail modal."

---

## Workflow

### Phase 1 - Target Setup

Select the target browser tab and reset the measurement tools.

```
1. CallMcpTool: server="user-chrome-devtools", toolName="list_pages"
   → Find the pageId for the localhost:3005 page in the tab list.

2. CallMcpTool: server="user-chrome-devtools", toolName="select_page"
   arguments: { "pageId": <found_id> }

3. CallMcpTool: server="user-chrome-devtools", toolName="evaluate_script"
   arguments: { "function": "() => { console.clear(); return 'console cleared'; }" }
```

If you don't know which URL corresponds to the edited file, read `src/App.tsx` and `src/pages/story/routes.tsx` to understand the route mapping.

### Phase 2 - BEFORE Baseline

Collect the current state across four layers before the code change.

```
Layer 1 - A11y Snapshot:
  CallMcpTool: server="user-chrome-devtools", toolName="take_snapshot"
  arguments: { "verbose": true }
  → Element existence, text content, state (checked, disabled, etc.)

Layer 2 - Screenshot:
  CallMcpTool: server="user-chrome-devtools", toolName="take_screenshot"
  → Visual rendering state (layout, colors — things a11y can't capture)

Layer 3 - DOM Query (when needed):
  CallMcpTool: server="user-chrome-devtools", toolName="evaluate_script"
  arguments: { "function": "() => { return document.querySelector('.target').innerText; }" }
  → Precise inspection of specific DOM properties, CSS values, etc.

Layer 4 - Runtime Logs:
  CallMcpTool: server="user-chrome-devtools", toolName="list_console_messages"
  arguments: { "types": ["error", "warn"] }

  CallMcpTool: server="user-chrome-devtools", toolName="list_network_requests"
  arguments: { "resourceTypes": ["fetch", "xhr"] }
```

You don't need to collect every layer every time. Judge by the situation:
- Simple text change → Layer 1 + Layer 4 is enough.
- Layout/style change → add Layer 2.
- Need to verify a specific DOM state → add Layer 3.

### Phase 3 - Apply Change + Wait for HMR

1. Apply the code change.
2. Wait for Vite HMR to take effect.

```
CallMcpTool: server="user-chrome-devtools", toolName="wait_for"
arguments: { "time": 2000 }
```

When HMR does not apply (route changes, global config changes, etc.):
```
CallMcpTool: server="user-chrome-devtools", toolName="navigate_page"
arguments: { "type": "reload", "ignoreCache": true }

CallMcpTool: server="user-chrome-devtools", toolName="wait_for"
arguments: { "time": 3000 }
```

### Phase 4 - AFTER Collection + Validation

#### Mode 1 (Auto)

Collect the AFTER state using the same layers as Phase 2 and compare with BEFORE.

**Judgment criteria:**
- Did any new console error/warn appear?
- Did any network request return 4xx/5xx?
- Did the a11y snapshot lose any expected elements unexpectedly?
- Is the intent of the code change reflected in the snapshot (e.g., for a text change, is the new text visible)?
- Are there obvious rendering issues in the screenshot (blank screen, broken layout, etc.)?

#### Mode 2 (Scenario-based)

Execute the user-provided scenario step by step, validating after each step.

```
Example scenario: "Click 'New Inquiry' button → modal opens → enter title → submit"

Step 1: take_snapshot → find the uid of the 'New Inquiry' button
Step 2: click(uid) → click
Step 3: wait_for(1000) → wait for modal to render
Step 4: take_snapshot → confirm modal opened
Step 5: fill(uid, "Test title") → enter title
Step 6: click(submit button uid) → submit
Step 7: wait_for(2000) → wait for API response
Step 8: take_snapshot → verify result
Step 9: list_console_messages → check for errors
Step 10: list_network_requests → confirm API succeeded
```

Main tools used for interactions:
- `click`: arguments `{ "uid": "<snapshot uid>", "includeSnapshot": true }`
- `fill`: arguments `{ "uid": "<uid>", "value": "input value" }`
- `type_text`: arguments `{ "text": "input value", "uid": "<uid>" }`
- `hover`: arguments `{ "uid": "<uid>" }`
- `wait_for`: arguments `{ "time": <ms> }` or `{ "selector": "<css>" }`

### Phase 5 - Judgment Loop

```
FAIL conditions (any one triggers fail):
  - A new error in list_console_messages
  - A 4xx/5xx response in list_network_requests
  - An expected element missing from the a11y snapshot
  - (Mode 2) A scenario expectation not met

→ Edit code → re-run from Phase 3 (up to 3 iterations)

PASS conditions:
  - None of the FAIL conditions apply
  - (Mode 1) The intent of the code change is reflected
  - (Mode 2) All scenario steps pass

→ Report the result and finish
```

---

## Tool Reference (server: user-chrome-devtools)

| Tool | Purpose | Key Arguments |
|------|---------|---------------|
| `list_pages` | List open tabs | (none) |
| `select_page` | Select target tab | `pageId` (required) |
| `take_snapshot` | A11y tree snapshot | `verbose`: bool |
| `take_screenshot` | Visual capture | `format`, `fullPage`, `uid` |
| `evaluate_script` | Run JS | `function` (required), `args` |
| `list_console_messages` | Console messages | `types`: ["error","warn",...] |
| `list_network_requests` | Network requests | `resourceTypes`: ["fetch","xhr",...] |
| `navigate_page` | Navigate page | `type`: "url"\|"reload", `url` |
| `click` | Click an element | `uid` (required), `includeSnapshot` |
| `fill` | Fill an input field | `uid`, `value` |
| `type_text` | Type text | `uid`, `text` |
| `hover` | Hover | `uid` (required) |
| `wait_for` | Wait | `time` (ms) or `selector` (CSS) |

## Artifacts Policy (important)

**Screenshots, snapshot files, logs, and any other artifacts produced during validation must not be deleted automatically.** Only remove them when the user explicitly asks. When reporting, include the path of any file that was saved.

## Reporting

After validation, report the result in the following format:

```
## UI Validation Result: PASS / FAIL

- URL: http://localhost:3005/...
- Mode: Auto / Scenario-based
- Console errors: none / [error details]
- Network failures: none / [failed requests]
- Snapshot changes: [summary]
- (Mode 2) Scenario result: [pass/fail per step]
- Iterations: N
```
