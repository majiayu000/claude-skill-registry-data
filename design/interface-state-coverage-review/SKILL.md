---
name: interface-state-coverage-review
description: Reviews an interface, component library, or user flow for missing, inconsistent, or poorly communicated UI states. Use when the user asks to audit loading, empty, error, success, validation, disabled, offline, permission, destructive-action, asynchronous, or transition states.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: review
  audience: product-designers-and-frontend-developers
  tags:
    - ui
    - ux
    - interface-states
    - user-flows
    - feedback
    - error-handling
  status: draft
  side_effects: none
---

# Interface State Coverage Review

## Purpose

Review an interface, component, or user flow for state completeness.

The skill identifies states that are missing, visually inconsistent, difficult to understand, inaccessible, or unable to help the user recover. It evaluates more than the ideal path and checks what happens before, during, after, and when an interaction fails.

The goal is not to require every possible state for every component. The goal is to identify the states that are relevant to the actual interface and ensure they are deliberately designed.

## When to use this skill

Use this skill when:

- The user asks to review loading, empty, success, error, disabled, or validation states.
- A UI looks polished in screenshots but may not handle real-world conditions.
- A user flow includes asynchronous requests, uploads, submissions, filtering, authentication, permissions, or destructive actions.
- A component library needs consistent interaction-state behavior.
- The user asks what states a feature or component should support.
- A design or implementation needs a state matrix before development.
- QA has found inconsistent feedback, unclear errors, or dead-end screens.
- The interface uses optimistic updates, background synchronization, live data, or delayed operations.
- The user asks for a UX review before release.

Do not use this skill when:

- The request is only about branding, typography, color direction, or visual identity.
- The user only needs a full WCAG audit.
- The task is limited to one isolated CSS pseudo-class.
- Another specialized skill already covers the specific workflow in greater depth.
- There is no interface, component, flow, prototype, or implementation to inspect.

## Inputs to inspect

Inspect the available evidence that represents the interface:

- Application source files
- Page and component templates
- Routes and user-flow definitions
- CSS, design tokens, and component variants
- Screenshots and screen recordings
- Figma exports or design specifications
- Storybook stories
- Tests and fixtures
- API integration code
- Form validation rules
- Error-handling utilities
- Loading and synchronization logic
- Empty-state and fallback components
- Product requirements or acceptance criteria
- Existing issue reports
- Analytics or support evidence, when supplied

Relevant repository locations may include:

- `src/components/`
- `src/pages/`
- `src/routes/`
- `src/features/`
- `src/styles/`
- `src/stories/`
- `tests/`
- `e2e/`
- `docs/`
- `examples/`
- `demo/`

Do not assume a specific framework or directory structure.

## State categories

Consider only categories relevant to the inspected interface.

### Entry states

Examples:

- First use
- Empty account
- Empty collection
- Prefilled data
- Returning user
- Restored session
- Missing permission
- Expired session
- Unavailable feature

### Data states

Examples:

- Initial loading
- Background refresh
- Stale data
- Partial data
- Cached data
- No results
- Filtered zero results
- Pagination end
- Delayed response
- Timeout
- Offline
- Synchronization conflict

### Action states

Examples:

- Idle
- Hover
- Focus
- Active or pressed
- Selected
- Expanded
- Disabled
- Read-only
- Submitting
- Uploading
- Processing
- Cancelling
- Retrying
- Completed
- Failed
- Undo available

### Form states

Examples:

- Unmodified
- Modified
- Valid
- Invalid
- Required but empty
- Validation pending
- Server-rejected
- Partially completed
- Autosaved
- Unsaved
- Restored draft
- Submission successful
- Submission failed

### Outcome states

Examples:

- Success
- Partial success
- Recoverable error
- Blocking error
- Permission denied
- Resource not found
- Conflict
- Rate limited
- Cancelled
- Destructive action completed
- Destructive action reversed

### System states

Examples:

- Offline
- Reconnecting
- Maintenance
- Unsupported environment
- Feature unavailable
- Service degradation
- Authentication expired
- Background operation continuing
- Cross-device synchronization pending

## Workflow

1. Define the review scope

   Identify:

   - The target screen, component, feature, or user flow
   - The user’s primary goal
   - The critical actions
   - External dependencies
   - Destructive or irreversible actions
   - Asynchronous operations
   - Places where users can become blocked

   State explicitly what is and is not being reviewed.

2. Map the primary user flow

   Describe the expected path from entry to completion.

   For each step, record:

   - What the user sees
   - What action is available
   - What system response is expected
   - What data or service dependency exists
   - What can fail
   - How the user proceeds or recovers

   Do not evaluate only static screens. Include transitions between states.

3. Build a relevant state inventory

   For each important screen or component, identify applicable states.

   Classify each state as:

   - `covered`
   - `partially-covered`
   - `missing`
   - `inconsistent`
   - `not-applicable`
   - `not-verifiable`

   Do not mark a state as missing merely because it is not visible in the inspected screenshot. Check the implementation or available documentation first.

4. Review state communication

   For each relevant state, verify whether the interface clearly communicates:

   - What is happening
   - Why it is happening
   - Whether the user needs to act
   - Whether the action succeeded
   - Whether data was saved
   - Whether the operation is still running
   - Whether the user can cancel
   - Whether the user can retry
   - Whether progress is determinate or indeterminate
   - What happens next

   Review visible text, icons, layout, control availability, focus behavior, status announcements, and state changes.

   Do not rely on color, animation, or icons as the only communication method.

5. Review loading and asynchronous behavior

   Check:

   - Whether the loading indicator appears at the correct time
   - Whether existing content unnecessarily disappears
   - Whether controls prevent accidental duplicate actions
   - Whether the user can distinguish loading from failure
   - Whether long operations provide useful progress
   - Whether cancellation is supported when appropriate
   - Whether optimistic updates can be reversed after failure
   - Whether background refreshes avoid disrupting the current task
   - Whether skeleton content resembles the final layout
   - Whether loading motion respects reduced-motion preferences
   - Whether focus and reading position remain stable

   Flag fake precision, endless spinners, layout shifts, and silent background failures.

6. Review empty and zero-result states

   Distinguish between:

   - A genuinely empty account or collection
   - No search results
   - No results after filtering
   - Data that failed to load
   - Content hidden by permissions
   - Content that does not yet exist
   - Content removed or archived

   Check whether the state explains why the area is empty and offers a meaningful next action.

   Avoid generic messages such as “Nothing here” when the interface can provide a more useful explanation.

7. Review errors and recovery

   For each likely failure, determine whether the interface:

   - Explains the problem in user-facing language
   - Preserves entered data
   - Avoids blaming the user
   - Identifies the affected action or field
   - Offers retry, edit, undo, reconnect, or support options
   - Distinguishes temporary from permanent failures
   - Avoids exposing raw stack traces or internal codes
   - Keeps unaffected parts of the interface usable
   - Returns focus to a useful location
   - Announces important errors when appropriate

   Prioritize failures that can cause data loss, duplicate actions, or blocked completion.

8. Review disabled, unavailable, and permission states

   Check whether unavailable controls are:

   - Hidden only when the action is irrelevant
   - Disabled when users benefit from discovering the action
   - Accompanied by an explanation when the reason is not obvious
   - Visually distinguishable without becoming unreadable
   - Excluded from focus only when truly disabled
   - Re-enabled when the blocking condition changes

   Do not recommend disabled controls as the default solution for every unavailable action.

9. Review destructive actions

   For delete, overwrite, revoke, reset, remove, cancel, or discard actions, check:

   - Whether the consequence is clear
   - Whether the scope of the action is named
   - Whether confirmation is proportional to the risk
   - Whether repeated confirmations create unnecessary friction
   - Whether undo is safer than confirmation
   - Whether irreversible actions are explicitly identified
   - Whether success and failure states are communicated
   - Whether accidental repeated activation is prevented

10. Review transitions and continuity

    Check what happens when the interface changes state.

    Verify whether it preserves:

    - Focus
    - Scroll position
    - Entered data
    - Selection
    - Expanded sections
    - Filters and sorting
    - Navigation context
    - User orientation
    - Back-button behavior
    - URL state, when relevant

    Flag transitions that visually succeed but leave keyboard or assistive-technology users in an outdated context.

11. Review cross-component consistency

    Compare similar states across the interface:

    - Loading indicators
    - Empty-state layout
    - Error placement
    - Success feedback
    - Disabled controls
    - Retry actions
    - Status language
    - Icon meaning
    - Progress representation
    - Motion behavior
    - Spacing and hierarchy

    Identify accidental inconsistencies separately from intentional contextual differences.

12. Prioritize findings

    Assign each finding one priority:

    - `critical` — blocks completion, risks data loss, or hides a serious failure
    - `high` — creates a dead end, major confusion, or unreliable recovery
    - `medium` — weakens clarity, consistency, or confidence
    - `low` — minor polish or consistency improvement

    Prioritize functional clarity and recovery before decorative polish.

13. Recommend the smallest effective change

    For each finding, recommend:

    - The state to add or revise
    - The information it must communicate
    - The action the user should be able to take
    - The component or flow affected
    - Any accessibility consideration
    - A practical validation method

    Do not redesign the entire interface when a targeted state improvement is sufficient.

14. Validate the proposed coverage

    Check the reviewed flow against realistic scenarios such as:

    - Slow connection
    - Empty account
    - Invalid input
    - Server rejection
    - Interrupted request
    - Permission loss
    - Duplicate activation
    - Partial response
    - Offline transition
    - Retry after failure
    - Successful completion
    - Returning to the interface later

    Do not claim a state is implemented unless evidence confirms it.

## Output format

Return:

```md
## Interface state review

### Scope

- Target:
- Primary user goal:
- Critical flow:
- Evidence inspected:
- Not reviewed:

### Summary

Brief assessment of overall state coverage and the most important risk.

### State coverage matrix

| Area or component | State | Status | Evidence | UX risk |
|---|---|---|---|---|
| Example form | submitting | covered | Submit button displays progress text | Low |
| Example form | server error | missing | No error branch found | High |

Use these status values:

- covered
- partially-covered
- missing
- inconsistent
- not-applicable
- not-verifiable

### Findings

| Priority | Area | Problem | User impact | Recommendation |
|---|---|---|---|---|

### Critical flow gaps

1. ...
2. ...

### Recommended implementation order

1. Blocking and data-loss states
2. Error recovery
3. Loading and asynchronous feedback
4. Empty and permission states
5. Cross-component consistency
6. Visual polish

### Suggested validation scenarios

- [ ] ...
- [ ] ...

### Remaining unknowns

- ...
```

If the task is a planning request rather than a review, replace evidence-based findings with a proposed state matrix and clearly label it as a recommendation.

## Quality bar

The task is complete only when:

- The review covers the actual interface rather than a generic checklist.
- The primary user flow is identified.
- Relevant states are distinguished from irrelevant ones.
- Empty, loading, error, and success states are not treated as interchangeable.
- Findings include evidence or are marked as not verifiable.
- Missing states are connected to a concrete user impact.
- Recommendations explain communication and recovery behavior.
- Critical and destructive actions receive proportionate attention.
- Transitions preserve user context where possible.
- Accessibility considerations are integrated without pretending this is a full WCAG audit.
- Recommendations are prioritized.
- No implementation is claimed without validation.
- Side effects are avoided unless the user explicitly requests changes.

## Edge cases

- For static content sites, many asynchronous and data states may be irrelevant.
- For prototypes, distinguish designed states from implemented states.
- For screenshots, mark interaction behavior as not verifiable.
- For native controls, do not replace reliable platform behavior merely to create custom states.
- For optimistic interfaces, inspect both immediate success feedback and rollback behavior.
- For real-time interfaces, include reconnecting, stale, conflicting, and partial-update states.
- For uploads, include file rejection, interruption, retry, cancellation, partial completion, and duplicate files.
- For search and filtering, distinguish empty datasets from zero matching results.
- For authentication flows, include expired sessions, interrupted redirects, denied access, and recovery.
- For destructive operations, prefer recoverability where technically and legally appropriate.
- For offline-first interfaces, inspect synchronization and conflict states rather than only a generic offline banner.
- If state logic is generated by a third-party component, verify how the application configures and communicates those states.
- If no implementation exists yet, produce a proposed state model rather than presenting assumptions as findings.

## Related skills

- `design-system-consistency-review`
- `interaction-polish-review`
- `frontend-accessibility-review`
- `form-ux-review`
- `user-flow-friction-review`
