---
name: fleet-ux-contribution-protocol
description: The structured protocol for producing ux_spec contributions — beyond the template, how to think about user experience at every level and deliver specifications engineers can implement.
---

# UX Contribution Protocol — Structured Specification Production

Your `ux_spec` contribution shapes how users experience the fleet's output. Without it, engineers optimize for the happy path and forget empty states, error messages, keyboard navigation, and the non-visual layers. This protocol ensures your specs are complete and implementable.

## The Contribution Trigger

You receive a ux_spec contribution task when:
- PM creates a contribution subtask for user-facing work
- The synergy matrix identifies UX input is needed (conditional — user-facing tasks)
- You proactively spot tasks in reasoning/work that touch user surfaces

## The 4-Step Protocol

### Step 1: Surface Inventory

Before specifying anything, identify EVERY user-facing surface this task touches. Use the 7-level UX model:

| Level | Question | Example |
|-------|---------|---------|
| Web UI | Does this change what users see in a browser? | Dashboard component, form, table |
| CLI | Does this change terminal output? | Command output format, flags, help text |
| API | Does this change what APIs return? | Response structure, error format, status codes |
| Config | Does this change what users configure? | YAML keys, env vars, defaults |
| Errors | Does this change error messages? | Error codes, recovery instructions |
| Events | Does this change notifications? | IRC messages, ntfy pushes, board memory |
| Logs | Does this change what operators read? | Log format, levels, context fields |

Most tasks touch 2-3 levels. A CLI tool change might touch CLI + errors + config. An API change might touch API + errors + logs.

### Step 2: State Definition

For EACH surface identified, define ALL states:

```
Surface: CLI output for `fleet status`

| State | What User Sees | When |
|-------|---------------|------|
| Loading | "Checking fleet status..." with spinner | API call in flight |
| Success | Formatted table: agent, status, task, last seen | Normal operation |
| Partial | Table with ⚠️ for unreachable agents | Some agents offline |
| Empty | "No agents registered. Run setup.sh first." | Fresh install |
| Error | "Cannot connect to MC at localhost:8000. Is it running?" + error code | MC down |
| Auth Error | "Authentication failed. Run `fleet auth refresh`." | Token expired |
```

The common mistake: only defining Success. Engineers implement what you specify. If you don't specify Empty, they'll show a blank screen.

### Step 3: Interaction + Accessibility

For interactive elements (not just display):

**Interactions:**
```
- User types `fleet status --watch` → refreshes every 5s, shows delta
- User presses Ctrl+C → clean exit, shows final state
- User pipes to grep → output is grep-friendly (no color codes, consistent columns)
```

**Accessibility:**
```
- Screen reader: table headers announced, row content in logical order
- Keyboard: Tab navigates rows, Enter opens task detail
- Color: status indicators use both color AND symbol (✓/✗/⚠️)
- No animation that can't be disabled
```

### Step 4: Deliver via fleet_contribute

```
fleet_contribute(
    task_id=TARGET_TASK_ID,
    contribution_type="ux_spec",
    content="""
    ## UX Specification: fleet status command

    ### Surfaces Affected: CLI, Errors

    ### CLI: `fleet status` output
    
    States: [table from Step 2]
    
    Interactions:
    - --watch flag: refresh every 5s
    - Pipe-safe: no ANSI codes when stdout is not a TTY
    
    Accessibility:
    - Columns aligned for screen readers
    - Status uses symbol + color (not color alone)
    
    ### Errors
    - Connection refused → "Cannot connect to MC at {url}. Is it running?" [E-MC-001]
    - Auth failed → "Authentication failed. Run `fleet auth refresh`." [E-AUTH-001]
    - Timeout → "MC responded slowly ({time}ms). Check load." [E-MC-002]
    
    ### NOT in scope (this phase):
    - Interactive mode (future)
    - JSON output format (future)
    """
)
```

## Quality Checklist

Before submitting your contribution, verify:

- [ ] All affected surfaces identified (not just the obvious one)
- [ ] All states defined for each surface (loading, success, empty, error, partial)
- [ ] Error messages include: what failed + error code + what to do
- [ ] Accessibility addressed: keyboard, screen reader, color independence
- [ ] Phase-appropriate depth (POC = minimal, production = comprehensive)
- [ ] Specific enough that the engineer can implement without guessing

## What Makes a Good ux_spec vs a Bad One

**Bad:** "Make it user-friendly"
**Bad:** "Add good error messages"
**Bad:** "Should be accessible"

**Good:** "Error on auth failure: 'Authentication failed. Token expired at {time}. Run `fleet auth refresh` to get a new token.' Error code: E-AUTH-001"
**Good:** "Empty state: 'No tasks assigned. Waiting for PM to dispatch work.' (not a blank screen)"
**Good:** "Keyboard nav: Tab moves between table rows. Enter opens task detail. Escape returns to table."

Specific. Implementable. Verifiable.
