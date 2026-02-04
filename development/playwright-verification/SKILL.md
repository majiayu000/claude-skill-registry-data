---
name: playwright-verification
description: Automated feature verification using Playwright MCP and Claude Code CLI. Use when verifying UI features, running acceptance tests, checking feature completion status, or validating features.json verification steps. Integrates with agentic-development workflow for progress tracking.
---

# Playwright Verification Skill

Automated browser-based verification of features.json using Microsoft's Playwright MCP server and Claude Code CLI.

## Quick Start

```bash
# In Claude Code CLI
claude
> /project:verify p6-sound-list      # Verify single feature
> /project:verify-all                 # Verify all incomplete features
```

## Prerequisites

```bash
# One-time setup
npm install -D @playwright/test
npx playwright install chromium

# Add MCP to Claude Code (per-project)
claude mcp add playwright -- npx @playwright/mcp@latest --headless
```

## Core Concepts

### Verification Flow

```
features.json           Claude Code              Playwright MCP
     │                      │                         │
     │  verification: [     │                         │
     │    "Click X",        │  Parse steps            │
     │    "Panel opens"     │────────────────────────>│
     │  ]                   │                         │
     │                      │  browser_click("X")     │
     │                      │────────────────────────>│
     │                      │                         │ Execute
     │                      │  browser_snapshot()     │
     │                      │<────────────────────────│
     │                      │                         │
     │  passes: true        │  Update JSON            │
     │<─────────────────────│                         │
```

### Verification Step Patterns

Map plain English verification steps to Playwright MCP actions:

| Step Pattern | Playwright Action | Example |
|--------------|-------------------|---------|
| "Click X button/toggle" | `browser_click` | "Click Sound Browser toggle" |
| "Panel opens/closes" | `browser_snapshot` + assert | "Panel opens showing categories" |
| "X visible/shown" | `browser_snapshot` + find element | "Search input visible" |
| "X hidden/not visible" | `browser_snapshot` + assert absent | "Panel closes on click-away" |
| "Typing X filters Y" | `browser_type` + `browser_snapshot` | "Typing filters samples" |
| "Persists via localStorage" | `browser_evaluate` | "Theme persists via localStorage" |
| "Shortcut X does Y" | `browser_press_key` + verify | "Escape stops all audio" |
| "Works when X not focused" | `browser_click` outside + action | "Works when REPL not focused" |
| "Double-click X" | `browser_click` with count:2 | "Double-click inserts name" |

### Feature Dependencies

Features with dependencies are skipped if dependencies haven't passed:

```json
{
  "id": "p6-sound-search",
  "dependencies": ["p6-sound-list"],  // Must pass first
  "passes": false
}
```

Verification order respects dependency graph automatically.

## Commands Reference

### /project:verify

Verify a single feature by ID.

**Usage:**
```
/project:verify p6-sound-list
```

**Process:**
1. Read feature from features.json
2. Check dependencies (skip if not met)
3. Navigate to localhost:5173
4. Execute each verification step
5. Report pass/fail per step
6. Update features.json if ALL pass

**Output:**
```
=== Verifying: p6-sound-list ===
✓ Click Sound Browser toggle button
✓ Panel opens showing sample categories
✓ Each category expands to show sample names
✗ Sample count displayed per category
✓ Panel closes on toggle or click-away

Result: 4/5 passed - FAIL
```

### /project:verify-all

Verify all incomplete features in current phase.

**Usage:**
```
/project:verify-all
```

**Process:**
1. Read currentPhase from features.json meta
2. Filter: phase === currentPhase AND passes === false
3. Sort by dependency order
4. Run verification on each
5. Generate summary report
6. Update claude-progress.txt

**Output:**
```
=== Phase 6 Verification Summary ===

Passing: 3/16
├── p6-sound-list ✓
├── p6-shortcut-halt ✓
└── p6-hud-fps ✓

Failed: 1/16
└── p6-sound-search ✗ (step 3)

Skipped: 2/16 (dependencies not met)
├── p6-sound-preview
└── p6-sound-insert

Next priority: p6-sound-search
```

## Playwright MCP Tools

Available tools when Playwright MCP is connected:

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Go to URL |
| `browser_click` | Click element by name/role |
| `browser_type` | Type into focused element |
| `browser_press_key` | Press keyboard key |
| `browser_snapshot` | Get accessibility tree |
| `browser_evaluate` | Run JavaScript in page |
| `browser_scroll` | Scroll page/element |
| `browser_wait` | Wait for condition |

### Accessibility Tree

Playwright MCP uses accessibility tree, not screenshots. Element identification via:
- Role: `button`, `textbox`, `heading`, etc.
- Name: visible text or aria-label
- State: `checked`, `expanded`, `disabled`

Example snapshot fragment:
```
- button "Sound Browser" [ref=btn1]
- region "Sound Panel" [ref=panel1]
  - heading "Drums"
  - list
    - listitem "bd" [ref=item1]
    - listitem "sd" [ref=item2]
```

## File Structure

```
basilisk-av/
├── .claude/
│   ├── settings.json          # MCP config
│   └── commands/
│       ├── verify.md          # Single feature command
│       └── verify-all.md      # Batch command
├── features.json              # Feature definitions
├── claude-progress.txt        # Session tracking
└── init.sh                    # Dev startup
```

### features.json Schema

```json
{
  "meta": {
    "project": "basilisk-av",
    "currentPhase": 6,
    "lastUpdated": "2025-12-12"
  },
  "features": [
    {
      "id": "p6-feature-name",
      "phase": 6,
      "category": "category-name",
      "description": "What it does",
      "priority": "high|medium|low",
      "dependencies": ["p6-other-feature"],
      "verification": [
        "Step 1 in plain English",
        "Step 2 in plain English"
      ],
      "passes": false
    }
  ]
}
```

**Rules:**
- Only modify `passes` field during verification
- Never edit verification steps mid-session
- Dependencies must use exact feature IDs

## Debugging

### Headed Mode (Watch Browser)

```bash
# Remove headless flag
claude mcp remove playwright
claude mcp add playwright -- npx @playwright/mcp@latest

# Now browser window visible during verification
```

### Check MCP Connection

```bash
claude
> /mcp
# Should list: playwright
```

### Manual Snapshot

```bash
claude
> Use playwright to navigate to localhost:5173 and take a snapshot
```

### Common Issues

| Issue | Solution |
|-------|----------|
| MCP not found | `claude mcp add playwright -- npx @playwright/mcp@latest` |
| Browser won't launch | `npx playwright install chromium` |
| Element not found | Check accessibility tree with `browser_snapshot` |
| Timeout | Increase wait, check dev server running |
| WSL display issues | Use `--headless` or set `DISPLAY=:0` |

## Integration with Agentic Development

This skill extends the agentic-development workflow:

1. **Session Start**: `init.sh` shows feature status
2. **Development**: Implement feature code
3. **Verification**: `/project:verify <id>` runs automated checks
4. **Progress**: `claude-progress.txt` updated automatically
5. **Handoff**: Clean state for next session

### Workflow Example

```bash
# Start session
./init.sh

# Check what to work on
# → Shows: "Next incomplete: p6-sound-list"

# Implement feature...

# Verify implementation
claude
> /project:verify p6-sound-list

# If passing, move to next
> /project:verify p6-sound-search

# End session - progress auto-tracked
```

## Writing Good Verification Steps

### Do

- Use specific, observable actions: "Click Sound Browser button"
- Reference visible UI text: "Panel shows 'No results' message"
- One assertion per step: "Search input visible at top"
- Include edge cases: "Works when REPL not focused"

### Don't

- Vague steps: "It should work"
- Multiple assertions: "Panel opens and shows categories and count"
- Implementation details: "useState updates correctly"
- Non-observable: "Performance is good"

### Examples

**Good:**
```json
"verification": [
  "Click Sound Browser toggle button",
  "Panel opens showing sample categories",
  "Click 'Drums' category header",
  "Category expands showing sample names",
  "Click toggle button again",
  "Panel closes"
]
```

**Bad:**
```json
"verification": [
  "Sound browser works",
  "Categories load from Strudel API and render in React state",
  "UX is intuitive"
]
```

## CI Integration (Future)

```yaml
# .github/workflows/verify.yml
name: Feature Verification
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx playwright install chromium
      - run: npm run dev &
      - run: sleep 5
      - run: |
          # Run verification via Playwright test file
          npx playwright test verify.spec.ts
```

## References

- [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- [Playwright Accessibility](https://playwright.dev/docs/accessibility-testing)
- [MCP Protocol](https://modelcontextprotocol.io/)
