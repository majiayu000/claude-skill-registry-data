---
name: oncokb-datastar
description: Build and review Datastar-based HTML interactions using correct `data-*` attributes, modifiers, and expression patterns.
---

## Purpose

Use this skill when implementing or reviewing Datastar UI behavior in HTML templates.

## When to use this skill

- Adding or changing Datastar attributes in markup.
- Debugging signal flow, event handlers, or attribute evaluation order.
- Reviewing whether Datastar usage matches documented attribute semantics.

## Workflow

1. Identify intended interaction behavior.
   - List expected signals, events, visibility toggles, class/style updates, and side effects.
   - Completion criterion: target runtime behavior is explicit before coding.

2. Map behavior to canonical Datastar attributes.
   - Prefer documented attributes and modifiers over ad-hoc JavaScript.
   - Distinguish read/write signal setup (`data-signals`, `data-bind`, `data-computed`) from side effects (`data-effect`, `data-on:*`).
   - Completion criterion: each behavior maps to a documented attribute pattern.

3. Validate syntax and ordering.
   - Check casing and modifier usage (for example `__case`, `__delay`, `__debounce`, `__throttle`).
   - Ensure order-sensitive attributes are sequenced correctly on the same element.
   - Completion criterion: no invalid key/modifier usage and no order-related defects.

4. Confirm free vs Pro compatibility.
   - Use Pro-only attributes only when the project has a Datastar Pro license.
   - Completion criterion: no accidental Pro dependency in OSS-only contexts.

5. Report or implement changes with concrete examples.
   - Provide direct attribute-level recommendations and updated markup snippets.
   - Completion criterion: another engineer can apply the guidance without guessing.

## Quality bar

- Use attribute semantics exactly as documented.
- Avoid replacing Datastar declarative patterns with unnecessary imperative code.
- Call out invalid attributes early (for example malformed `data-on:*` keys or unsupported modifiers).
- Prefer small, composable signal patterns over monolithic expressions.

## Reference

- `reference/datastar-attributes.md`
- `reference/datastar-actions.md`
- `reference/examples/index.md`
