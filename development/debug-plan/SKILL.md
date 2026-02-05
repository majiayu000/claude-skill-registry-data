---
name: debug-plan
description: Create debug test plan from user input. Use when planning browser debug sessions with Chrome DevTools. Parses prompt for URL/target, identifies interactions to test (clicks, inputs, flows), confirms plan with user via HITL, creates specific test steps (navigate, click, fill, verify). Outputs URL and test plan for debug execution.
---

# Debug Plan Skill

> **ROOT AGENT ONLY** - Runs only from root Claude Code agent, initiates debug workflow.

**Purpose:** Parse user request and create test plan for browser debugging
**Trigger:** Phase 1 of `/debug` command workflow
**Input:** User prompt describing what to debug
**Output:** Confirmed URL + test plan with specific steps

---

## Workflow

**1. Parse prompt for URL/target**

- Extract target URL from prompt:
  - Explicit URLs: `http://localhost:5173/login`, `https://example.com/checkout`
  - Implicit paths: `/login`, `/settings`, `/users`
  - Named targets: "the login form", "settings page", "modal on users page"
- Identify environment:
  - `localhost:*` → local dev server
  - `*.local`, `127.0.0.1` → local environment
  - Production URLs → external site
- Default port: 5173 (Vite) if not specified

**2. Identify what to test**

Analyze prompt for interaction types:

| Interaction Type | Keywords                              | Example Steps                     |
| ---------------- | ------------------------------------- | --------------------------------- |
| Navigation       | "load page", "visit", "navigate to"   | Navigate to URL, wait for load    |
| Form interaction | "fill", "submit", "login", "sign up"  | Fill email, fill password, submit |
| Click actions    | "click", "button", "link", "toggle"   | Click button, click link          |
| Visual testing   | "layout", "centered", "responsive"    | Resize viewport, capture layout   |
| Console errors   | "error", "warning", "console"         | Capture console messages          |
| Flow testing     | "checkout", "workflow", "end-to-end"  | Multi-step sequence               |
| Network testing  | "API", "request", "response", "fetch" | Monitor network calls             |

**3. HITL: Confirm target + test plan**

Present concise plan to user:

```
Debug Plan:
  Target: http://localhost:5173/login
  Test: Login form with test credentials
  Steps:
    1. Navigate to /login
    2. Fill email field with test@test.com
    3. Fill password field with password123
    4. Click submit button
    5. Verify redirect to /dashboard
    6. Capture console errors

Proceed? (y/n)
```

**4. Create debug steps**

Based on confirmation, structure test plan:

```json
{
  "url": "http://localhost:5173/login",
  "viewport": { "width": 1280, "height": 720 },
  "steps": [
    {
      "id": "step-1",
      "action": "navigate",
      "description": "Navigate to login page",
      "target": "http://localhost:5173/login"
    },
    {
      "id": "step-2",
      "action": "fill",
      "description": "Enter email",
      "selector": "input[type='email']",
      "value": "test@test.com"
    },
    {
      "id": "step-3",
      "action": "fill",
      "description": "Enter password",
      "selector": "input[type='password']",
      "value": "password123"
    },
    {
      "id": "step-4",
      "action": "click",
      "description": "Submit login form",
      "selector": "button[type='submit']"
    },
    {
      "id": "step-5",
      "action": "verify",
      "description": "Check redirect to dashboard",
      "expected": "url contains '/dashboard'"
    }
  ],
  "capture": {
    "screenshots": true,
    "console": true,
    "network": true
  }
}
```

---

## Action Types

| Action     | Description             | Parameters                      |
| ---------- | ----------------------- | ------------------------------- |
| `navigate` | Load URL                | `target` (URL)                  |
| `click`    | Click element           | `selector` (CSS)                |
| `fill`     | Fill input field        | `selector`, `value`             |
| `hover`    | Hover over element      | `selector`                      |
| `press`    | Press keyboard key      | `key` (e.g., "Enter", "Escape") |
| `resize`   | Change viewport size    | `width`, `height`               |
| `scroll`   | Scroll to element       | `selector` or `x`, `y`          |
| `wait`     | Wait for condition      | `duration` or `selector`        |
| `verify`   | Assert expected outcome | `expected` (condition)          |

---

## URL Resolution Rules

| User Input                   | Resolved URL                      | Notes                            |
| ---------------------------- | --------------------------------- | -------------------------------- |
| `localhost:5173/login`       | `http://localhost:5173/login`     | Add http:// if missing           |
| `/login`                     | `http://localhost:5173/login`     | Assume Vite dev server           |
| `the login form`             | `http://localhost:5173/login`     | Infer path from context          |
| `https://example.com/page`   | `https://example.com/page`        | Use as-is                        |
| `settings page on mobile`    | `http://localhost:5173/settings`  | Extract path, note viewport need |
| `modal isn't centered`       | **ASK USER** for specific URL     | Ambiguous - needs clarification  |
| `checkout flow`              | `http://localhost:5173/cart`      | Infer starting point             |
| `React error on settings`    | `http://localhost:5173/settings`  | Extract page from error context  |
| `localhost:3000/api/users`   | `http://localhost:3000/api/users` | Different port                   |
| `http://192.168.1.100:8080/` | `http://192.168.1.100:8080/`      | Use as-is                        |
| Empty/unclear                | **ASK USER** for URL              | Cannot proceed without target    |

**Default ports:**

- Vite: 5173
- Next.js: 3000
- Create React App: 3000
- Backend APIs: 3000-8080 range

If URL is ambiguous, ALWAYS ask user for clarification.

---

## Viewport Presets

| Preset      | Size         | Use Case            |
| ----------- | ------------ | ------------------- |
| Desktop     | 1280 x 720   | Default             |
| Tablet      | 768 x 1024   | iPad portrait       |
| Mobile      | 375 x 667    | iPhone SE           |
| Large Phone | 414 x 896    | iPhone 11 Pro       |
| Wide        | 1920 x 1080  | Large desktop       |
| Custom      | User-defined | Specific breakpoint |

If prompt mentions "mobile", "tablet", or specific device, set viewport accordingly.

---

## Test Plan Patterns

### Pattern 1: Form Submission

```
Steps:
  1. Navigate to form page
  2. Fill all required fields
  3. Click submit
  4. Verify success message or redirect
  5. Capture console for errors
```

### Pattern 2: Visual Layout

```
Steps:
  1. Navigate to page
  2. Set viewport to target size
  3. Take baseline screenshot
  4. Identify visual issue (offset, overflow, etc.)
  5. Capture DOM snapshot for analysis
```

### Pattern 3: E2E Flow

```
Steps:
  1. Navigate to starting page
  2. Complete step 1 (e.g., add to cart)
  3. Navigate to step 2 (e.g., checkout)
  4. Fill payment info
  5. Submit order
  6. Verify confirmation page
  7. Capture network requests
```

### Pattern 4: Console Error Investigation

```
Steps:
  1. Navigate to page
  2. Perform action that triggers error
  3. Capture console messages
  4. Take DOM snapshot at error state
  5. Identify error source (component, line number)
```

### Pattern 5: Network Monitoring

```
Steps:
  1. Navigate to page
  2. Trigger API call (click button, submit form)
  3. Monitor network requests
  4. Verify request payload
  5. Verify response data
  6. Capture failed requests
```

---

## Output Format

**JSON structure passed to chrome-devtools-testing:**

```json
{
  "url": "string",
  "viewport": { "width": number, "height": number },
  "steps": [
    {
      "id": "string",
      "action": "navigate|click|fill|hover|press|resize|scroll|wait|verify",
      "description": "string",
      "selector": "string (optional)",
      "target": "string (optional)",
      "value": "string (optional)",
      "key": "string (optional)",
      "expected": "string (optional)",
      "duration": "number (optional)"
    }
  ],
  "capture": {
    "screenshots": boolean,
    "console": boolean,
    "network": boolean
  }
}
```

---

## Validation Rules

**WARN if:**

- No URL provided and cannot infer from prompt
- More than 15 steps (too complex, suggest breaking into multiple tests)
- No verification steps (missing success criteria)
- Selectors are too generic (`button`, `div`) - suggest more specific ones

**PASS if:**

- URL is valid and accessible
- Steps are clear and actionable
- Verification criteria defined
- User confirmed plan via HITL

---

## Integration

**Called by:**

- `/debug` command (Phase 1)

**Calls:**

- None (planning only)

**Next step:** `/skill chrome-devtools-testing` (Phase 2 - Setup)

---

## Examples

### Example 1: Login Form Test

**Input:** `/debug "check if the login form works"`

**Output:**

```json
{
  "url": "http://localhost:5173/login",
  "viewport": { "width": 1280, "height": 720 },
  "steps": [
    {
      "id": "step-1",
      "action": "navigate",
      "description": "Navigate to login page",
      "target": "http://localhost:5173/login"
    },
    {
      "id": "step-2",
      "action": "fill",
      "description": "Enter email",
      "selector": "input[type='email']",
      "value": "test@test.com"
    },
    {
      "id": "step-3",
      "action": "fill",
      "description": "Enter password",
      "selector": "input[type='password']",
      "value": "password123"
    },
    {
      "id": "step-4",
      "action": "click",
      "description": "Click login button",
      "selector": "button[type='submit']"
    },
    {
      "id": "step-5",
      "action": "verify",
      "description": "Verify redirect to dashboard",
      "expected": "url contains '/dashboard'"
    }
  ],
  "capture": {
    "screenshots": true,
    "console": true,
    "network": true
  }
}
```

### Example 2: Mobile Layout Issue

**Input:** `/debug "the modal isn't centered on mobile"`

**HITL:** "Which page has the modal? (e.g., /users, /settings)"

**User:** "/users"

**Output:**

```json
{
  "url": "http://localhost:5173/users",
  "viewport": { "width": 375, "height": 667 },
  "steps": [
    {
      "id": "step-1",
      "action": "navigate",
      "description": "Navigate to users page",
      "target": "http://localhost:5173/users"
    },
    {
      "id": "step-2",
      "action": "resize",
      "description": "Set mobile viewport",
      "width": 375,
      "height": 667
    },
    {
      "id": "step-3",
      "action": "click",
      "description": "Open modal",
      "selector": "button[data-testid='open-modal']"
    },
    {
      "id": "step-4",
      "action": "wait",
      "description": "Wait for modal animation",
      "duration": 500
    },
    {
      "id": "step-5",
      "action": "verify",
      "description": "Check modal centering",
      "expected": "modal has left offset ~0px"
    }
  ],
  "capture": {
    "screenshots": true,
    "console": true,
    "network": false
  }
}
```

### Example 3: Console Error Investigation

**Input:** `/debug "there's a React error on the settings page"`

**Output:**

```json
{
  "url": "http://localhost:5173/settings",
  "viewport": { "width": 1280, "height": 720 },
  "steps": [
    {
      "id": "step-1",
      "action": "navigate",
      "description": "Navigate to settings page",
      "target": "http://localhost:5173/settings"
    },
    {
      "id": "step-2",
      "action": "wait",
      "description": "Wait for page load",
      "duration": 1000
    },
    {
      "id": "step-3",
      "action": "click",
      "description": "Click Save button (trigger error)",
      "selector": "button[data-testid='save-settings']"
    },
    {
      "id": "step-4",
      "action": "verify",
      "description": "Capture console errors",
      "expected": "console has React error messages"
    }
  ],
  "capture": {
    "screenshots": true,
    "console": true,
    "network": false
  }
}
```
