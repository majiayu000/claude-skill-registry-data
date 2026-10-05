---
name: oncokb-datastar-review
description: Review Datastar code for Tao-aligned architecture, correct attributes/actions usage, and maintainable server-driven UI patterns.
---

## Scope

- Use when a change adds or modifies Datastar attributes, actions, signals, or Datastar-driven SSE flows.
- Focus on review findings, not feature implementation.

## Workflow

1. Detect Datastar surface area in the change.
   - Identify changed files using `data-*` Datastar attributes, `@action(...)` expressions, SSE patch events, and Datastar-specific JS/plugin code.
   - Completion criterion: Datastar-affected files and interaction paths are explicitly listed.

2. Check Tao principles first.
   - Apply `reference/the-tao-of-datastar.md` as architecture-level guardrails.
   - Verify backend-as-source-of-truth, minimal frontend state, and server-driven patching.
   - Completion criterion: each applicable Tao principle has a pass/fail note with evidence.

3. Check attribute/action correctness.
   - Verify attribute semantics, modifiers, casing, and order-sensitive patterns.
   - Verify backend action method/option usage (`@get`, `@post`, retries, cancellation, signal filtering).
   - Completion criterion: no undocumented or incorrect Datastar attribute/action usage remains unreported.

4. Check interaction quality and reliability.
   - Flag optimistic updates that claim success before backend confirmation.
   - Confirm loading states/indicators for long-running operations.
   - Confirm morph/patch behavior preserves intended state (`data-ignore-morph`, `data-preserve-attr` when required).
   - Completion criterion: UX and reliability risks are either accepted explicitly or documented as findings.

5. Report actionable review findings.
   - Separate blockers from non-blocking improvements.
   - Include file paths, principle/rule violated, and a concrete fix direction.
   - Completion criterion: author can apply each finding without additional discovery.

## Output format

- `Blockers`: incorrect Datastar semantics, architecture violations, or high-risk UX/reliability defects.
- `Non-blocking`: maintainability and clarity improvements.
- `Checked`: Tao principles reviewed, attribute/action correctness reviewed, and reliability checks completed.

## Quality bar

- Prefer Tao-aligned server-driven patterns over frontend state accumulation.
- Do not approve speculative/optimistic-success UI without explicit product agreement.
- Keep findings concrete and tied to changed code.

## Reference

- `reference/the-tao-of-datastar.md`
- `../oncokb-datastar/reference/datastar-attributes.md`
- `../oncokb-datastar/reference/datastar-actions.md`
- `../oncokb-datastar/reference/examples/index.md`
