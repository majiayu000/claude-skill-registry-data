---
name: fleet-accessibility-audit
description: How the UX designer audits accessibility — WCAG criteria, keyboard navigation, screen reader compatibility, color contrast, and the non-visual UX that most teams ignore
user-invocable: false
---

# Accessibility Audit

## Why This Matters for Fleet

Fleet has multiple interfaces: Mission Control web UI, IRC channels,
CLI tools, ntfy notifications, Plane pages. Accessibility isn't just
about screen readers on the web UI — it's about every surface being
usable by every human who interacts with the fleet.

## Audit Scope by Surface

### Web UI (Mission Control, The Lounge)
- Keyboard navigation: can every action be performed without a mouse?
- Screen reader: do elements have proper ARIA labels?
- Color contrast: WCAG AA minimum (4.5:1 for text, 3:1 for large text)
- Focus management: is focus visible and logical?
- Error messages: announced to screen readers, not just color-coded

### CLI Tools (fleet CLI, scripts)
- Output structure: clear headers, consistent formatting
- Color usage: information conveyed by color ALSO conveyed by text
- Error messages: specific, actionable, suggest next steps
- Help text: consistent --help format, examples included
- Exit codes: meaningful (0=success, 1=user error, 2=system error)

### Notifications (ntfy, IRC)
- Message clarity: understandable without visual context
- Priority levels: conveyed in text, not just urgency icon
- Actionability: clear what to do next

### Configuration (YAML, .env)
- Comments: every non-obvious field explained
- Defaults: sensible defaults that work out of the box
- Validation: clear error on invalid config, not silent failure

## WCAG Checklist (Web Surfaces)

### Perceivable
- [ ] Text alternatives for non-text content (images, icons)
- [ ] Captions for audio/video content
- [ ] Content can be presented in different ways without losing meaning
- [ ] Color is not the only visual means of conveying information
- [ ] Contrast ratio meets AA standards

### Operable
- [ ] All functionality available from keyboard
- [ ] No keyboard traps
- [ ] Users have enough time to read and use content
- [ ] Content does not cause seizures (no rapid flashing)
- [ ] Users can navigate, find content, and determine where they are

### Understandable
- [ ] Text is readable and understandable
- [ ] Content appears and operates in predictable ways
- [ ] Users are helped to avoid and correct mistakes

### Robust
- [ ] Content is compatible with current and future user tools
- [ ] Valid HTML/markup
- [ ] Status messages can be programmatically determined

## Fleet-Specific Accessibility Patterns

### Agent Status Display
```
Bad:  [green dot] architect   [red dot] devops
Good: architect (active, last seen 5m ago) | devops (offline since 2h)
```

### Task Priority
```
Bad:  [red] Critical  [orange] High  [blue] Normal
Good: [!!!] Critical  [!!] High  [!] Normal  [ ] Low
```

### Error Messages
```
Bad:  Error: invalid input
Good: Error: task_readiness must be 0-100, got 150.
      Set a valid readiness value: fleet_task_progress(readiness=50)
```

### IRC Communication
```
Bad:  @architect check this
Good: @architect: design_input needed for task AUTH-003
      (user authentication middleware). See context at
      /context/AUTH-003/contributions/
```

## Output: Accessibility Contribution

When contributing UX specs via `fleet_contribute`:

```
## Accessibility Requirements: {feature/component}

### Surface: {web | CLI | notification | config}

### Requirements
1. [MUST] {requirement}
   - WCAG: {criterion reference if applicable}
   - How to verify: {specific test}

2. [SHOULD] {requirement}
   ...

### Patterns to Use
- {specific pattern from fleet-ux-every-level}

### Anti-Patterns to Avoid
- {what NOT to do and why}
```
