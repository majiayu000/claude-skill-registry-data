---
name: game-qa
description: "Testing methodology for web games using Playwright MCP. Invoked by game-orchestra when code needs testing. Documents what to test, how to test, and how to interpret results. The game-tester agent executes these tests."
---

> **Note:** This is a methodology reference document. The game-tester agent executes these tests. This skill does not use gated steps.

# Game QA

Testing methodology for web games. This skill documents WHAT to test
and HOW. The **game-tester agent** PERFORMS the tests.

## When Invoked

By game-orchestra when code exists and needs testing.

## Playwright MCP Tools

Use these Playwright MCP tools for game testing:

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Load the game URL |
| `browser_snapshot` | Capture DOM state |
| `browser_take_screenshot` | Visual verification |
| `browser_evaluate` | Call render_game_to_text(), advanceTime() |
| `browser_click` | Simulate mouse input |
| `browser_press_key` | Simulate keyboard input |
| `browser_fill_form` | Text input (for name entry, etc.) |
| `browser_console_messages` | Error tracking |

## Testing Workflow

1. **Navigate** to game URL (`browser_navigate`)
2. **Screenshot** initial state (`browser_take_screenshot`)
3. **Capture baseline state** via `browser_evaluate`:
   ```javascript
   window.render_game_to_text()
   ```
4. **Simulate inputs** via `browser_click` or `browser_press_key`
5. **Advance time** deterministically:
   ```javascript
   window.advanceTime(1000)  // Advance 1 second
   ```
6. **Capture post-action state** and screenshot
7. **Compare** expected vs actual state
8. **Report** findings: what worked, what broke, visual anomalies

## Testing Checklist

### Core Gameplay
- [ ] Primary movement/interaction inputs work
- [ ] Win/lose/success/fail transitions trigger correctly
- [ ] Score/health/resource changes reflect actions
- [ ] Boundary conditions: edges, min/max values
- [ ] Collisions: player-enemy, player-item, player-boundary

### UI & Navigation
- [ ] Menu → game → pause → resume → gameover flow
- [ ] Buttons/links respond to clicks
- [ ] Text is readable (not truncated, overlapping, or invisible)
- [ ] Responsive: game works at 375px, 768px, 1024px widths

### Integration Hooks
- [ ] `window.render_game_to_text()` returns valid JSON
- [ ] `window.advanceTime(ms)` advances state correctly
- [ ] State from render_game_to_text matches visual state

### Error Tracking
- [ ] No console errors during normal gameplay
- [ ] No console errors during edge cases (rapid input, resize)
- **Rule:** Fix the FIRST console error before testing anything else

## Interpreting Results

- **State matches visual:** PASS
- **State exists but visual wrong:** Rendering bug
- **Visual right but state wrong:** State tracking bug
- **Both wrong:** Logic bug — check game loop
- **Console error:** Stop testing, fix error first

## See Also
- `action-payloads.md` — Input simulation patterns
- `game-integration.md` — Required hook implementations
