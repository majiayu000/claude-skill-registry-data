---
name: fleet-interaction-design
description: How UX produces ux_spec contributions — all states, all interactions, all UX levels (not just UI). The structured protocol for user experience at CLI, API, config, error, and notification levels.
---

# Interaction Design — UX's Contribution Protocol

Your ux_spec contribution ensures the engineer builds user-facing elements correctly the FIRST time. Without your input, engineers optimize for the happy path — they forget loading states, error messages, empty states, keyboard navigation, and the non-visual UX layers.

## UX at Every Level — Not Just UI

The fleet builds CLI tools, APIs, configs, notifications, and logs — not just web UIs. Your ux_spec covers ALL user-facing surfaces:

| Level | User-Facing Element | UX Concerns |
|-------|-------------------|-------------|
| CLI | Command output, flags, help text | Consistent format, progressive disclosure, error messages with next steps |
| API | Endpoints, responses, errors | Consistent structure, meaningful error codes, pagination, rate limit feedback |
| Config | YAML files, env vars, settings | Discoverability, validation feedback, sensible defaults, migration path |
| Errors | Error messages, exceptions | What went wrong, what to do, error code for search |
| Events | IRC messages, board memory | Consistent format, actionable content, right channel |
| Notifications | ntfy pushes, alerts | Priority-appropriate urgency, clickable context, no noise |
| Logs | Structured logging | Grep-friendly, level-appropriate, context included |

## The ux_spec Contribution Structure

When you call `ux_spec_contribution(task_id)`, prepare:

```
## UX Specification for: {task title}

### Surfaces Affected:
- {list which levels this task touches}

### For Each Surface:

#### {Surface}: {component/endpoint/command}

**States:**
| State | What User Sees | Trigger |
|-------|---------------|---------|
| Loading | {description} | Request in flight |
| Empty | {description — not just blank} | No data yet |
| Success | {description} | Operation completed |
| Error | {description — with error code + next step} | Operation failed |
| Partial | {description} | Some items loaded, some failed |

**Interactions:**
- {action} → {result} → {feedback to user}
- {keyboard shortcut} → {what it does}

**Accessibility:**
- Keyboard-only navigation: {how}
- Screen reader: {what's announced}
- Color contrast: {WCAG level}
- Focus management: {where focus goes after action}

### NOT in scope:
- {what you're deliberately deferring for this phase}
```

## Phase-Appropriate UX Depth

| Phase | UX Scope |
|-------|---------|
| poc | Happy path states only. Error = generic message. No accessibility. |
| mvp | All states (loading, empty, success, error). Basic keyboard nav. Consistent error format. |
| staging | Full states + partial states. Keyboard nav complete. Screen reader tested. Error codes. |
| production | Everything above + performance UX (loading indicators, progressive loading). WCAG AA compliance. |

## Deliver via fleet_contribute

```
fleet_contribute(
    task_id=TARGET_TASK_ID,
    contribution_type="ux_spec",
    content=your_spec
)
```

The engineer sees your spec in their context during work stage. They implement the states, interactions, and accessibility you defined. During review, fleet-ops checks that the implementation matches your spec.

## Common UX Mistakes to Prevent

1. **No empty state** — screen is blank when there's no data. Add: "No tasks yet. Create one with fleet_task_create."
2. **No error context** — "Error occurred" tells the user nothing. Add: error code + what failed + what to do.
3. **Inconsistent format** — CLI output changes structure between commands. Establish: consistent sections, headers, spacing.
4. **No loading feedback** — user waits with no indication. Add: progress indicator or status message.
5. **Keyboard dead end** — focus gets trapped or lost. Define: focus flow for every interaction.

Your contribution catches these BEFORE implementation, when they're cheap to fix — not during review, when they require rework.
