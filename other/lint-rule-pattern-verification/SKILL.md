---
name: lint-rule-pattern-verification
description: >-
  Use when a gate matches source with a regex or an AST selector — a check script under
  `scripts/ci/`, an esquery `no-restricted-syntax` entry, a drift guard that greps source for a
  helper call — and it may miss a spelling (bracket access, quoted or shorthand key, namespace
  import) or count a commented-out or quoted occurrence as executable, letting the gate pass while
  enforcing nothing.
---

# Lint rule pattern verification

## Profile keys consumed

- `make.lint_eslint`
- `make.lint_deps`

The esquery half of a pattern gate runs through the target mapped by `make.lint_eslint` and the
dependency-cruiser half through `make.lint_deps`; skip the corresponding half with a recorded note
when the key maps to `null`. A gate script that is not wired to either target is still in scope —
this skill is about the pattern, not the runner.

## Overview

A pattern-based gate has two failure modes and both are silent. It can miss a spelling of the
construct it polices (false negative), or it can match text that never executes — a commented-out
call, a documented example, a string literal — and certify coverage that does not exist. Neither
shows up as a red build.

## When to use

- Adding or editing any regex, glob or AST selector that decides whether a gate fires.
- A gate has never failed since it was added — check that it can fail at all.
- A rule is about to police a _call_ or a _statement_ rather than a token.
- Reviewing an allowlist or manifest gate where a missed spelling excuses a stale entry.
- Not for: pattern matching that only formats or reports and gates nothing.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — gate scripts under `scripts/ci/` (route-coverage inventory, ESLint and
  dependency-cruiser fixture runners) and must-fail fixtures under `tests/unit/tooling/`.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — the same pattern; its
  interaction-state drift guard parses the TypeScript AST and ships fail-closed cases for
  commented-out and quoted calls.
- **Component-library shape** (Storybook-first, no bootable app, published package): partial — shell
  gate scripts and Bats contracts exist; no AST-based guard yet, so the AST half is guidance rather
  than an existing example.

## Prefer the AST when matching code structure

Regex over raw source cannot tell executable code from a comment or a string, and it fails open in
the direction that matters: commenting a call out is the cheapest way to disable it, and the text
stays on disk.

```ts
const visit = (node: ts.Node): void => {
  if (
    ts.isCallExpression(node) &&
    ts.isIdentifier(node.expression) &&
    node.expression.text === SCAN_CALLEE
  ) {
    found.push(node.arguments[1]?.getText(source).trim() ?? '');
  }
  ts.forEachChild(node, visit);
};
```

Comments never become nodes and a call spelled inside a string literal is a string, so only real
calls count. Keep the parser in a pure function taking `(fileName, sourceText)` so its fail-closed
behaviour can be asserted on sources the repository never has to ship.

## Three cases every such guard needs

- **A real call** returns the captured argument.
- **A commented-out call**, both line and block form, returns nothing.
- **A quoted call**, in a plain string and a template literal, returns nothing.

Add a fourth that guards the guard: assert the walk found at least as many calls as the registry
requires, so the other assertions cannot pass vacuously over an empty list.

## When a regex is the right tool, enumerate the spellings

Grep the codebase for the construct first and write down every form found, then a must-fail fixture
per form. Recurring misses:

- Member access — `obj.key` versus `obj['key']` versus `obj[variable]`.
- Object keys — bare, quoted, computed, and shorthand `{ x }` against explicit `{ x: value }`. A
  formatter may normalise one spelling and leave the others.
- Imports — default, namespace, named, side-effect, dynamic `import()`, `require()`.
- Declarations — `function f()`, `const f = () =>`, method shorthand, `f: function ()`.

## Remediation

Widen the pattern to include the missed spelling, re-check the negative fixtures so the wider
pattern does not fire on unintended code, and add the spelling to the fixture set. Where a variant
is excluded on purpose, say so next to the pattern with the reason, so a reviewer can tell a
deliberate boundary from a hole. Never narrow the gate's scope, exclude the offending file, or
annotate the finding away — the rule itself is the bug.

## Common mistakes

- Testing only the spelling the author had in mind, so the gate encodes one example.
- Matching a call name as text and treating a commented-out call as coverage.
- Broad matchers like `\w+` that quietly stop at a bracket or a dot.
- Shipping a gate with no failing fixture, so nobody ever observes it firing.
