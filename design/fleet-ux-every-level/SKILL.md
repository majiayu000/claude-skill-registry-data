---
name: fleet-ux-every-level
description: UX is not just UI — UX at every level. CLI output, API responses, error messages, config structure, events, notifications, logs, code ergonomics.
user-invocable: false
---

# UX at Every Level

## The PO's Words

> "UX is not just about the UI, UX is at every level, even the core
> and module or CLI and AST"

## Where UX Lives

### Web UI
Components, layouts, interactions, visual states (loading, empty, error,
success, partial), transitions, responsiveness, accessibility.

### CLI
- Output formatting (tables, colors, progress indicators)
- Error messages (what went wrong, what to do, specific not vague)
- Help text (discoverable, complete, with examples)
- Progress display (long operations show progress, not silence)
- Exit codes (machine-readable for scripts)

### API Responses
- Response structure (consistent envelope, predictable shape)
- Error formats (code, message, details — not stack traces)
- Pagination (cursor-based for stability, clear next/prev)
- Status codes (correct HTTP semantics, not everything 200)
- Content negotiation (JSON by default, clear headers)

### Configuration
- File structure (logical grouping, not flat dump)
- Naming (clear, consistent, no abbreviations without context)
- Defaults (sensible — works out of box for common case)
- Validation messages (which field, what's wrong, what's valid)
- Documentation within config (comments explaining each section)

### Error Messages
- **What** went wrong (specific, not "An error occurred")
- **Why** it went wrong (cause, not just symptom)
- **What to do** (actionable fix, not "contact support")
- **Context** (which operation, which input, which state)

### Events & Notifications
- Scannable (emoji prefix for quick visual categorization)
- Actionable (what should the reader DO?)
- Linked (URLs to task, PR, dashboard — not bare IDs)
- Prioritized (urgent vs informational is immediately clear)

### Logs
- Structured (JSON or consistent format, grep-friendly)
- Contextual (request ID, agent name, task ID in every line)
- Leveled (DEBUG/INFO/WARN/ERROR used correctly)
- Useful (tells a story when read in sequence)

### Code Ergonomics (Developer UX)
- API surface (minimal, clear, hard to misuse)
- Naming conventions (intent-revealing, consistent)
- Error handling (clear return types, no silent failures)
- Documentation (docstrings for public API, not obvious code)

## Contribution: ux_spec

When you receive a UX contribution task:

1. Call `ux_spec_contribution(task_id)` — gathers task context
2. Identify ALL user-facing elements at EVERY level (not just UI)
3. For EACH element, specify:
   - **States**: loading, empty, error, success, partial, disabled
   - **Interactions**: what the user does, what happens
   - **Accessibility**: keyboard nav, screen reader, color contrast
   - **Existing patterns**: reuse what exists, don't reinvent
4. Deliver: `fleet_contribute(task_id, "ux_spec", your_spec)`

### What Makes a Good UX Spec

**Bad:** "Make it look nice"
**Good:**
```
SearchBar component:
  States: empty (placeholder "Search..."), typing (live character count),
          loading (spinner in input), results (dropdown), no-results
          ("No results for '{query}'"), error ("Search failed. Retry?")
  Interactions: type → debounce 300ms → search, Enter → immediate,
                Escape → close dropdown, click outside → close
  Accessibility: aria-label="Search tasks", role="combobox",
                 aria-expanded on dropdown, keyboard nav in results
  Pattern: matches existing fleet SearchBar in MC frontend
```

## Group Calls

| Call | When |
|------|------|
| `ux_spec_contribution(task_id)` | Contribution task — UX spec for a feature |
| `ux_accessibility_audit()` | Review — check WCAG compliance |

## The Test: Would the PO Be Satisfied?

For every interface (UI, CLI, API, config, error, event, log):
- Is it clear what's happening?
- Is it clear what to do next?
- Does it respect the user's time?
- Would the PO use this and feel it's professional?

If any answer is no, the UX needs work.
