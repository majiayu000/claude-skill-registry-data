---
name: debug-execution
description: Execute browser debug steps using Chrome DevTools MCP. Navigate to URL, capture baseline snapshots/screenshots, perform interactions (click, fill, hover, press_key), collect console messages and network requests, validate results. Use when executing planned debug interactions with visual/DOM evidence capture.
---

# Debug Execution - Chrome DevTools MCP Workflow

**Purpose:** Execute debug plan using Chrome DevTools MCP tools with evidence capture
**Trigger:** After debug-plan and chrome-devtools-testing complete
**Input:** Debug plan (URL, interactions, expectations)
**Output:** Evidence bundle (screenshots, snapshots, console logs, network requests, validation results)

---

## Workflow Steps

### 1. Navigate and Establish Baseline

1. **Navigate to target URL:**
   - Use `navigate_page(url)` MCP tool
   - Wait for page load complete
   - Record navigation success/failure

2. **Capture baseline state:**
   - Use `take_snapshot()` to capture initial DOM structure
   - Use `take_screenshot()` to capture initial visual state
   - Record baseline timestamp
   - Store snapshots for comparison

### 2. Execute Interaction Loop

For each interaction in the debug plan:

**a. Execute Interaction:**

- Choose appropriate MCP tool based on interaction type:
  - `click(element)` - Click element (button, link, etc.)
  - `fill(element, text)` - Input text into field
  - `hover(element)` - Hover over element
  - `press_key(key)` - Keyboard input (Enter, Escape, Tab, etc.)
- Wait for interaction effects to complete
- Record interaction execution status

**b. Capture Post-Interaction Evidence:**

- Use `take_screenshot()` to capture visual state after interaction
- Use `take_snapshot()` to capture DOM changes
- Label evidence with interaction step number
- Store for comparison against expectations

**c. Validate Interaction Result:**

- Compare actual vs expected state
- Check for visual changes (screenshots)
- Check for DOM changes (snapshots)
- Record validation status (pass/fail)

### 3. Collect Diagnostic Evidence

After all interactions complete:

1. **Collect console messages:**
   - Use `list_console_messages()` to retrieve all console output
   - Filter by type (error, warning, info, log)
   - Identify critical errors
   - Record console state

2. **Collect network activity:**
   - Use `list_network_requests()` to retrieve all network requests
   - Check for failed requests (4xx, 5xx)
   - Identify slow requests
   - Record network state

### 4. Validate Against Expectations

1. **Compare results to debug plan expectations:**
   - Visual state matches expected
   - DOM state matches expected
   - Console errors match expected (or none if not expected)
   - Network requests successful (or match expected failures)

2. **Generate validation summary:**
   - List expectations met
   - List expectations failed
   - Identify unexpected behaviors
   - Categorize severity (critical, warning, info)

### 5. Bundle Evidence for Report

Organize all captured evidence:

```
Evidence Bundle:
  - Baseline: screenshot + snapshot
  - Interactions: [
      {step: 1, action: "click login", screenshot, snapshot},
      {step: 2, action: "fill email", screenshot, snapshot},
      {step: 3, action: "submit form", screenshot, snapshot}
    ]
  - Console: {errors, warnings, logs}
  - Network: {requests, failures, slow}
  - Validation: {met, failed, unexpected}
```

---

## Execution Logic

```
plan = {url, interactions, expectations}
evidence = {baseline: {}, interactions: [], console: [], network: [], validation: {}}

// Step 1: Navigate and baseline
navigate_page(plan.url)
evidence.baseline.snapshot = take_snapshot()
evidence.baseline.screenshot = take_screenshot()

// Step 2: Execute interactions
for each interaction in plan.interactions:
  // Execute
  result = execute_mcp_tool(interaction.type, interaction.params)

  // Capture evidence
  screenshot = take_screenshot()
  snapshot = take_snapshot()

  evidence.interactions.push({
    step: interaction.step,
    action: interaction.description,
    screenshot: screenshot,
    snapshot: snapshot,
    status: result.status
  })

  // Validate
  validation = compare_to_expected(interaction.expected, snapshot, screenshot)
  evidence.validation.interactions.push(validation)

// Step 3: Collect diagnostics
evidence.console = list_console_messages()
evidence.network = list_network_requests()

// Step 4: Final validation
evidence.validation.summary = validate_against_expectations(plan.expectations, evidence)

return evidence
```

---

## MCP Tools Reference

| Tool                    | Purpose               | Parameters                 |
| ----------------------- | --------------------- | -------------------------- |
| `navigate_page`         | Navigate to URL       | `url: string`              |
| `take_snapshot`         | Capture DOM structure | None                       |
| `take_screenshot`       | Capture visual state  | None                       |
| `click`                 | Click element         | `element: selector/coords` |
| `fill`                  | Input text            | `element, text`            |
| `hover`                 | Hover over element    | `element: selector/coords` |
| `press_key`             | Keyboard input        | `key: string`              |
| `list_console_messages` | Get console logs      | None                       |
| `list_network_requests` | Get network activity  | None                       |

---

## Evidence Capture Rules

1. **Always capture baseline** - Before any interaction
2. **Always capture after each interaction** - Screenshot + snapshot pair
3. **Always collect console messages** - Full log with timestamps
4. **Always collect network requests** - Full request/response metadata
5. **Label all evidence** - Step number, timestamp, description
6. **Store sequentially** - Maintain interaction order for timeline reconstruction

---

## Validation Logic

**Compare to expectations:**

```
for each expectation in plan.expectations:
  if expectation.type == "visual":
    check screenshots for expected change

  if expectation.type == "dom":
    check snapshots for expected elements/attributes

  if expectation.type == "console":
    check console logs for expected messages/errors

  if expectation.type == "network":
    check network requests for expected calls/responses

  record validation.status (pass/fail)
  record validation.details (what matched/failed)
```

**Categorize findings:**

- CRITICAL - Blocking errors, crashes, failed expectations
- WARNING - Non-blocking issues, unexpected behaviors
- INFO - Observations, performance notes

---

## Output Format

```json
{
  "url": "http://localhost:5173/login",
  "navigation": { "status": "success", "timestamp": "2025-01-15T10:30:00Z" },
  "baseline": {
    "screenshot": "baseline.png",
    "snapshot": "baseline-dom.json",
    "timestamp": "2025-01-15T10:30:01Z"
  },
  "interactions": [
    {
      "step": 1,
      "action": "Click login button",
      "type": "click",
      "element": "#login-btn",
      "status": "success",
      "screenshot": "step-1-after.png",
      "snapshot": "step-1-dom.json",
      "validation": {
        "status": "pass",
        "details": "Button clicked, form submitted"
      }
    }
  ],
  "console": {
    "errors": ["Uncaught TypeError at login.js:42"],
    "warnings": ["Deprecated API usage"],
    "logs": ["User login initiated"],
    "count": { "error": 1, "warning": 1, "log": 1 }
  },
  "network": {
    "requests": [
      {
        "url": "/api/auth/login",
        "method": "POST",
        "status": 200,
        "duration": 150
      }
    ],
    "failures": [],
    "slow": []
  },
  "validation": {
    "summary": {
      "total": 5,
      "met": 4,
      "failed": 1,
      "unexpected": 0
    },
    "critical": ["Console error: Uncaught TypeError"],
    "warnings": ["Deprecated API usage"],
    "info": ["Login flow completed in 2.5s"]
  }
}
```

---

## Error Handling

**On navigation failure:**

- Record error details
- Capture any partial page load
- Abort execution, return partial evidence

**On interaction failure:**

- Record error details
- Capture current state
- Continue to next interaction (resilient execution)
- Mark interaction as failed in evidence

**On MCP tool failure:**

- Record tool error
- Log to console
- Continue execution where possible
- Include tool errors in final report

---

## Integration

**Called by:** /debug command (Phase 3)
**Requires:** chrome-devtools-testing (MCP connection verified)
**Calls:** Chrome DevTools MCP tools (navigate_page, click, fill, take_screenshot, etc.)
**Next phase:** report-phase (format evidence into debug report)

---

## Example

```
/debug "test login form validation"

Debug Plan:
  URL: http://localhost:5173/login
  Interactions:
    1. Fill email with invalid format
    2. Click submit
    3. Check for validation error
  Expectations:
    - Validation error displayed
    - Form not submitted
    - No console errors

Debug Execution (this skill):
  → navigate_page(http://localhost:5173/login)
  → take_snapshot() - baseline DOM
  → take_screenshot() - baseline visual

  → fill(#email, "invalid-email")
  → take_screenshot() - after fill
  → take_snapshot() - DOM state

  → click(#submit-btn)
  → take_screenshot() - after submit
  → take_snapshot() - validation error visible

  → list_console_messages() - no errors (✓)
  → list_network_requests() - no requests (✓)

  Validation:
    ✓ Validation error displayed
    ✓ Form not submitted (no POST request)
    ✓ No console errors

  Output: Evidence bundle with 3 screenshots, 3 snapshots, console logs, network logs
```

---

## Success Criteria

- Navigation successful
- All interactions executed
- Evidence captured for each step
- Console messages collected
- Network requests collected
- Validation completed against expectations
- Evidence bundle ready for reporting
