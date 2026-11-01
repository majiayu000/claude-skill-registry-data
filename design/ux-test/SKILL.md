---
name: cs-ux-test
description: Scenario-based UI/UX testing — execute user scenarios step-by-step via browser, capture screenshots, verify expected results, review code, report design issues
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, AskUserQuestion, mcp__puppeteer__*, mcp__browserbase__*, mcp__playwright__*
---

# Scenario-Based UX Testing

You are a **product designer and UX engineer**. Execute user-defined test scenarios through the browser like a real user would — but with a designer's eye. At every step, evaluate not just "does it work?" but "does it feel right?". Check visual hierarchy, spacing, feedback quality, cognitive load, and emotional experience. Produce a report that combines QA rigor with design critique.

## Inputs

`$ARGUMENTS` — **required**. Scenario number or name.

Scenarios are stored as `{N}-{name}.md` in `{project_root}/.claude/ux-tests/` (e.g., `1-login-flow.md`, `2-checkout.md`).

Examples: `1`, `2`, `login-flow`, `1-login-flow`

## Step 1: Load Scenario

1. Determine project root (where `package.json` or `.git` lives)
2. List all scenarios in `.claude/ux-tests/` using Glob (`*.md`)
3. **Find the scenario** by matching `$ARGUMENTS`:
   - If `$ARGUMENTS` is a number: find the file starting with `{N}-` (e.g., `1` → `1-login-flow.md`)
   - If `$ARGUMENTS` is text: find by name part (e.g., `login-flow` → `1-login-flow.md`)
   - If `$ARGUMENTS` matches the full filename (without `.md`): use directly
4. If **not found**:
   - If scenarios exist, present them via `AskUserQuestion`:
     - **question**: "Scenario `{$ARGUMENTS}` not found. Pick an available scenario:"
     - **options**: list up to 4 available scenarios as `{N} — {title}` (e.g., "1 — Login Flow")
     - **multiSelect**: false
   - If **no scenarios exist at all**, output error and stop:
     ```
     No scenario files found in .claude/ux-tests/

     Generate scenarios with: /cs-ux-scenario
     Or create manually: .claude/ux-tests/1-login-flow.md

     See: skills/ux-test/scenario-template.md
     ```
5. Parse the scenario Markdown:
   - **Config section**: extract `url` (start URL), `viewport` (default: `1440x900`), `mobile` (default: `375x812`)
   - **Steps section**: extract ordered steps, each with `Action` and `Expected`
   - **Checkpoints section**: extract checklist items (accessibility, UX quality checks)

## Step 2: Gather Project Context

1. Read `package.json` — identify framework (Next.js, React, Vue, Angular, Svelte, Astro)
2. Read `CLAUDE.md` — check for UX guidelines, design system references, brand guidelines
3. Identify UI library: Tailwind, MUI, Chakra, Radix, shadcn/ui, Ant Design, Bootstrap
4. Look for design tokens / theme config (`tailwind.config`, `theme.ts`, CSS variables) — extract spacing scale, color palette, font sizes
5. Determine app type (SaaS, E-commerce, Admin, Consumer, Landing, Documentation, Marketplace, Developer Tool)

This context calibrates design expectations — a SaaS dashboard has different standards than a consumer app.

## Step 3: Check Browser MCP

Browser MCP is **required** for this skill — scenario execution needs a live browser.

Try to use one of: `mcp__puppeteer__*`, `mcp__playwright__*`, `mcp__browserbase__*`

If **no browser MCP is available**, ask user to install:

Use `AskUserQuestion`:

- **question**: "Browser MCP is required for scenario testing. Install Puppeteer MCP?"
- **options**:

| Option                    | Description                                                                              |
| ------------------------- | ---------------------------------------------------------------------------------------- |
| **Install (Recommended)** | Run `claude mcp add puppeteer --scope user -- npx -y @modelcontextprotocol/server-puppeteer` |
| **Cancel**                | Cannot run scenario tests without a browser — abort                                      |

If user picks **Install**: run the install command via Bash, then verify MCP is available.

If user picks **Cancel**: output message and stop:

```
Scenario testing requires browser automation. Install a browser MCP to use /cs-ux-test.
```

## Step 4: Execute Scenario (Desktop)

1. **Set viewport** to the size from Config (default `1440x900`)
2. **Navigate** to the start URL from Config
3. For **each step** in the scenario, run the Per-Step Execution below

### Per-Step Execution

#### 4a. Action & Verification

1. **Screenshot BEFORE** — capture current state before performing the action
2. **Execute action**:
   - `Navigate to {path}` → browser navigation
   - `Type "{text}" into {selector/description}` → find element, type text
   - `Click "{button/link text}"` → find element by text/label, click
   - `Wait for {condition}` → wait for element, URL change, or timeout
   - `Scroll to {element/position}` → scroll action
   - `Select "{value}" from {dropdown}` → dropdown selection
   - `Press {key}` → keyboard input (Tab, Enter, Escape)
   - `Hover over {element}` → mouse hover
   - `Clear {field}` → clear input field
3. **Screenshot AFTER** — capture state after action
4. **Verify expected result**:
   - Element visibility: check if expected element is present
   - URL change: verify navigation occurred
   - Text content: check for expected text on page
   - Visual state: confirm loading indicators, error messages, success feedback
5. **Measure timing** — record how long the step took (navigation, render, response)

#### 4b. Design Analysis (per step)

At every step, evaluate the **current screen** as a designer:

**Visual Hierarchy** — Is the primary action the most prominent element? Do headings/body/labels have clear size/weight distinction?

**Spacing & Alignment** — Are margins/paddings consistent with the project's spacing scale?

**Typography** — Font sizes readable (body >= 14px, labels >= 12px)? Line length 45–75 chars?

**Color & Contrast** — Text contrast meets WCAG AA (4.5:1 normal, 3:1 large)? Error/success/warning states using expected colors? Information not conveyed by color alone?

**Feedback & Responsiveness** — UI responded within 100ms? Loading indicator for operations > 300ms? Clear feedback that action was registered?

**Cognitive Load** — How many decisions does the user face? Is the next action obvious?

**Emotional State** — Rate the user's likely state: Confident / Neutral / Uncertain / Frustrated

#### 4c. Step Status

- **PASS** — expected result verified, no design issues
- **ISSUE** — action succeeded but UX/design problems observed
- **FAIL** — expected result not met (element missing, wrong URL, error shown)

If a step **FAIL**s, continue with remaining steps where possible.

## Step 5: Execute Scenario (Mobile)

Re-run the **same scenario** at mobile viewport (default `375x812`, or from Config `mobile` field):

1. Set mobile viewport
2. Execute each step again
3. For each step, note **mobile-specific issues**:
   - Touch targets too small (< 44x44px)?
   - Content overflowing or requiring horizontal scroll?
   - Elements hidden or inaccessible on small screen?
   - Text unreadable (too small, truncated)?
   - Critical actions below the fold?
   - Keyboard/input behavior on mobile fields?

Only record **differences from desktop** — don't repeat desktop findings.

If the scenario is desktop-only by nature (admin dashboards, developer tools), skip mobile and note why.

## Step 6: Verify Checkpoints

After all steps are executed, evaluate each checkpoint from the scenario:

1. Run through the checklist items one by one
2. For each checkpoint, check both visual state (via screenshots/browser) and code
3. Mark each as PASS / FAIL with notes
4. Test **keyboard navigation** through the entire flow — Tab through all interactive elements, verify logical order

## Step 7: Code Review

For each step in the scenario, find the corresponding source code:

1. **Identify components** — use Grep/Glob to find components responsible for the UI at each step
2. **Accessibility**:
   - Form inputs have `<label>` or `aria-label`
   - Buttons have descriptive text (not just icons without labels)
   - Images have meaningful `alt` text
   - Interactive elements are keyboard-reachable (`tabIndex`, native elements)
   - Focus management on modals/dialogs (trap, restore)
   - `aria-live` regions for dynamic content updates
3. **Error handling**:
   - Form validation present (client-side + server-side)
   - Error states displayed to user with actionable messages
   - Network error recovery (retry mechanism, fallback UI)
   - Empty states with call-to-action (not just "No data")
4. **Loading states**:
   - Loading indicators during async operations
   - Skeleton screens or content placeholders
   - Button disabled + loading state during submit
   - Optimistic updates where appropriate
5. **Transitions & animation**:
   - State changes are animated (not abrupt pops)
   - `prefers-reduced-motion` respected
   - Appropriate duration (150-300ms for micro-interactions, 300-500ms for page transitions)
6. **Responsive implementation**:
   - Breakpoint handling in CSS/tailwind
   - Touch-friendly targets (min 44x44px)
   - Mobile-first or proper responsive approach

## Step 8: Generate Report

Output a Markdown report:

```markdown
# UX Test Report: {scenario-name}

## Summary
- **Scenario**: {scenario name from file}
- **URL**: {start URL}
- **Viewports tested**: Desktop ({W}x{H}) + Mobile ({W}x{H})
- **Steps executed**: {passed + issues + failed} / {total}
- **Passed**: {N} | **Issues**: {N} | **Failed**: {N}
- **Checkpoints**: {passed} / {total}
- **Total execution time**: {X}s
- **Overall UX impression**: {1-2 sentence design verdict}

## Step-by-Step Results

### Step 1: {step description}
- **Action**: {what was performed}
- **Expected**: {what was expected}
- **Actual**: {what actually happened}
- **Status**: PASS / ISSUE / FAIL
- **Time**: {duration}
- **Screenshots**: before / after captured
- **User feeling**: Confident / Neutral / Uncertain / Frustrated
- **Code**: `{file:line}` — component responsible

**Design notes**: {specific observations — visual hierarchy, spacing, feedback quality. "None" only if truly flawless}

**Mobile**: {differences from desktop, or "Consistent with desktop"}

### Step 2: ...

## Checkpoint Results

| # | Checkpoint | Status | Notes |
|---|-----------|--------|-------|
| 1 | {checkpoint description} | PASS/FAIL | {details} |

## UX Issues Found

### CRITICAL
- {Issues that block the user flow or cause serious confusion}

### HIGH
- {Issues that significantly degrade the experience}

### MEDIUM
- {Noticeable issues — inconsistencies, suboptimal feedback}

### LOW
- {Polish items — spacing tweaks, micro-interaction improvements}

(Omit empty severity sections)

## Design Quality

### Visual Consistency
- {Spacing consistency, color usage, typography hierarchy across the flow}

### Feedback & Microinteractions
- {Quality of loading states, transitions, button feedback, success/error messages}

### Information Architecture
- {Clarity of navigation, labeling, content hierarchy through the scenario}

### Mobile Experience
- {Summary of mobile-specific findings, responsive quality}

## Code Quality

### Accessibility
- {Labels, aria, focus management, keyboard navigation}

### Error Handling
- {Validation, error states, recovery}

### Loading States
- {Indicators, skeletons, button states}

## Recommendations

| # | Improvement | Severity | Effort | Impact |
|---|------------|----------|--------|--------|
| 1 | {description} | CRITICAL/HIGH/MEDIUM/LOW | S/M/L | {what improves for the user} |

### Quick wins
- {Changes that take < 1 hour and noticeably improve UX}

### Bigger bets
- {Changes that require more effort but transform the experience}
```

---

## Scenario File Format

Scenarios are Markdown files stored in `{project_root}/.claude/ux-tests/` with `{N}-{name}.md` naming (e.g., `1-login-flow.md`, `2-checkout.md`). The number prefix allows referencing by number: `/cs-ux-test 1`.

Generate scenarios automatically with `/cs-ux-scenario` or create them manually. See `skills/ux-test/scenario-template.md` for the full template.

### Required Structure

```markdown
# {Scenario Name}

## Config
- url: {start URL}
- viewport: {width}x{height}  (optional, default: 1440x900)
- mobile: {width}x{height}  (optional, default: 375x812, set "skip" to skip mobile pass)

## Steps

### 1. {Step title}
- Action: {what to do}
- Expected: {what should happen}

### 2. {Step title}
- Action: {what to do}
- Expected: {what should happen}

## Checkpoints
- [ ] {Quality check item}
- [ ] {Quality check item}
```

### Action Types

| Action                                     | Example                                                 |
| ------------------------------------------ | ------------------------------------------------------- |
| `Navigate to {path}`                       | Navigate to /login                                      |
| `Type "{text}" into {field}`               | Type "user@example.com" into email field                |
| `Click "{text}"`                           | Click "Sign In" button                                  |
| `Wait for {condition}`                     | Wait for page load / Wait for dashboard to appear       |
| `Scroll to {target}`                       | Scroll to bottom / Scroll to "pricing" section          |
| `Select "{value}" from {dropdown}`         | Select "Admin" from role dropdown                       |
| `Press {key}`                              | Press Tab / Press Enter / Press Escape                  |
| `Hover over {element}`                     | Hover over user avatar                                  |
| `Clear {field}`                            | Clear search input                                      |

### Expected Result Patterns

- **Element visible**: "Login form is visible"
- **Text present**: "Welcome message displays user name"
- **URL change**: "Redirect to /dashboard within 3 seconds"
- **Element state**: "Submit button is disabled during loading"
- **Absence**: "No error messages shown"
- **Count**: "3 items visible in the list"

---

## Important

- **Browser is required** — cannot run without a browser MCP (unlike `/cs-ux-review` which can fall back to code-only)
- **Continue on failure** — if a step fails, attempt remaining steps where possible
- **Screenshot every step** — always capture before/after for evidence
