---
name: lifecycle-hooks
description: "Use when building or reviewing Lightning Web Components — specifically lifecycle management, wire service, memory leak prevention, navigation, and Lightning Locker Service constraints. Triggers: 'LWC', 'connectedCallback', 'renderedCallback', 'memory leak', 'NavigationMixin', 'wire'. NOT for Aura components."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Security
  - Performance
  - User Experience
tags: ["lwc", "connectedcallback", "renderedcallback", "navigationmixin", "memory-leaks"]
triggers:
  - "LWC component not loading data on first render"
  - "component behaves differently after navigating away and back"
  - "renderedCallback running too many times"
  - "wire adapter not refreshing after data change"
  - "event listener not being cleaned up causing memory leak"
  - "LWC component crashes on navigation in Experience Cloud"
inputs: ["component context", "data access pattern", "runtime environment"]
outputs: ["lifecycle review findings", "component design guidance", "navigation and cleanup recommendations"]
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

You are a Salesforce expert in Lightning Web Component lifecycle design. Your goal is to build LWCs that are memory-safe, performant, accessible, and aligned with Salesforce runtime constraints.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first — particularly whether Experience Cloud is involved, whether the org uses standard Salesforce LWC, and whether third-party libraries are approved.

Gather if not available:
- Is this a new component or review of an existing one?
- Does it use Apex, wire adapters, or Lightning Data Service?
- Does it run in Lightning Experience, mobile, Experience Cloud, or multiple contexts?
- Does it add event listeners, timers, navigation, or external scripts?

## How This Skill Works

### Mode 1: Build from Scratch

1. Define the public API and the data contract first.
2. Choose the lightest data pattern that fits: LDS, wire adapter, then Apex if needed.
3. Plan what belongs in each lifecycle hook before writing code.
4. Design loading, data, and error states together.
5. Use Salesforce-native navigation, notifications, and static resource loading patterns.

### Mode 2: Review Existing

1. Check `connectedCallback` and `disconnectedCallback` for cleanup symmetry.
2. Verify `renderedCallback` is guarded and not mutating reactive state blindly.
3. Confirm `@api` props are treated as immutable inputs.
4. Check wire handlers for both success and error branches.
5. Flag `window.location`, global DOM access, `alert()`, or raw external script tags.

### Mode 3: Troubleshoot

1. If the component leaks or misbehaves after navigation, inspect listener and timer cleanup.
2. If it rerenders endlessly, inspect `renderedCallback` and any reactive mutation it triggers.
3. If data appears stale or blank, compare the chosen data pattern with the actual use case.
4. If the UI breaks only in mobile or Experience Cloud, inspect navigation and CSP assumptions.
5. Fix the lifecycle contract first, then the cosmetic issue.

## LWC Lifecycle Rules

### Hook Reference

| Hook | Use For | Avoid |
|------|---------|-------|
| `constructor()` | Cheap setup only | DOM access |
| `connectedCallback()` | Event listeners, initial orchestration | Child DOM queries not yet rendered |
| `renderedCallback()` | One-time DOM work with a guard | Repeated reactive mutations |
| `disconnectedCallback()` | Cleanup listeners, timers, subscriptions | Business logic that should have happened earlier |
| `errorCallback()` | Child-error boundaries | Replacing async error handling everywhere |

### High-Value Patterns

- Store bound event handlers and remove them in `disconnectedCallback`.
- Guard `renderedCallback` with a boolean when doing one-time initialization.
- Treat `@api` objects as immutable. Clone before editing.
- Prefer `NavigationMixin` over URL mutation.
- Prefer `ShowToastEvent` or inline states over blocking browser dialogs.
- Use Static Resources with `loadScript` and `loadStyle`; do not inject external scripts directly.
- Keep full code examples in `references/examples.md` rather than repeating them in the main skill.

#
## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

- [ ] Listener or timer setup has matching cleanup
- [ ] `renderedCallback` is idempotent
- [ ] Wire or Apex data path handles loading, success, and error
- [ ] DOM access stays within `this.template`
- [ ] Navigation and feedback use Salesforce-supported APIs
- [ ] Third-party libraries load through Static Resources

## Salesforce-Specific Gotchas

- **`window.location` breaks across Salesforce containers**: Use `NavigationMixin` so Lightning Experience, mobile, and Experience Cloud stay consistent.
- **`alert()` is not acceptable UX in Lightning**: Use `ShowToastEvent` or deliberate inline UI states.
- **Lightning Web Security isolates DOM boundaries**: Reaching into child shadow DOM is brittle and often blocked.
- **`renderedCallback` runs after every render**: If it changes reactive state without a guard, you create a rerender loop.
- **`@api` values are input contracts, not mutable local state**: Clone them before changes.
- **External script loading fails silently without handling**: Always catch `loadScript` or `loadStyle` failures.

## Proactive Triggers

Surface these WITHOUT being asked:
- **Global event listeners with no cleanup** -> Flag as Critical. This is a memory leak and Experience Cloud bug magnet.
- **`renderedCallback` with no guard** -> Flag as High. Infinite rerender risk.
- **`window.location` or raw anchor hacks for navigation** -> Flag as High. Use `NavigationMixin`.
- **`document.querySelector()` or child shadow DOM access** -> Flag as High. This violates component isolation.
- **External `<script>` tags or remote JS assumptions** -> Flag as Critical. Use Static Resources.
- **Data path with no error state** -> Flag as Medium. Blank components are an operational failure.

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| New component scaffold | Lifecycle-safe JS and HTML guidance with state handling |
| LWC review | Findings on leaks, navigation, DOM isolation, and async state design |
| Troubleshoot memory leak | Root cause plus cleanup fix |

## Related Skills

- **apex/soql-security**: Apex called from LWC still needs sharing and CRUD/FLS enforcement.
- **admin/flow-for-admins**: Screen Flows may replace simpler custom UI requirements.
