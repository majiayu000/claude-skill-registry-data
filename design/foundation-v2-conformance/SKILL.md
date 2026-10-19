---
name: foundation-v2-conformance
description: "Enforce correct usage of the Foundation v2 UI packages: token-only styling, named imports, no bypass of abstraction layers, tracked workaround markers, and fresh-consumer tests that fail when a consumer drifts. Use when a UI component is built outside the design system, imports a raw token, bypasses a wrapper, or a fresh-consumer test starts to fail."
license: MIT-compat
compatibility: "Node.js or Python host; Foundation v2 packages installed; Linux"
metadata: {}
allowed-tools: []
---

Standard: name/description/length rules — [agentskills.io standard](../references/agentskills-standard.md).
# Foundation v2 Conformance Skill (body <500 lines)

Full procedure: references/foundation-v2-conformance-procedure.md
Sources: references/SOURCES.md
Evals: references/EVALS.md
Helpers: scripts/

## When to use this skill
- You import or build on top of a Foundation v2 UI package.
- You need to prove a consumer (app, micro-frontend, library) uses the package the way it was designed.
- You have added a workaround and need to track it until a proper fix lands.
- A reviewer asks "is this component actually conformant, or is it bypassing the tokens?"

## Disambiguation
- Fires: building on @ottili/foundation-ui, proving a consumer uses the public API, tracking an FV2-WA workaround, reviewing a component for token drift.
- Does NOT fire for: styling a non-Foundation app, reviewing backend code, or checking a11y conformance (use playwright-a11y-e2e).

## When NOT to use this skill (neighbour prompts — do not fire)
- Styling that lives only in a theme file and is never referenced by a component — the skill governs component imports and literals, not the token library itself.
- A brand-new component that is not yet consumed by anything — there is no consumer to test yet; the skill fires once the first consumer lands.
- A one-off prototype in a scratch directory that is deleted this week — track it with a marker anyway, but the fresh-consumer test is out of scope.
- A component that legitimately needs a raw value (e.g. a dynamically computed gradient) — file the `FV2-WA:` ticket and name the owner; the skill does not ban exceptions, it tracks them.
- An axe-only accessibility review — that is the playwright-a11y-e2e skill; this skill is about the package surface, not the criteria.

## Worked examples
Good (named import from the public package, token-derived values, tracked workaround):
```tsx
import { Button, Card } from '@ottili/foundation-ui';
import { duration, density } from '@ottili/foundation-ui/tokens';
export function OrderCard() {
  return (
    <Card padded tone="elevated">
      <Button variant="primary" style={{ transitionDuration: duration('fast') }}>
        Save
      </Button>
    </Card>
  );
}
```
Verified 2026-10-16 against `packages/foundation-ui/src/primitives/display.ts:30` (`CardProps` carries `padded?: boolean`, not `padding`) and `packages/foundation-ui/src/primitives/tokens.ts` (exports `duration(token)`, `density(token)`, `MOTION_REDUCE_VAR` — there is no `tokens` object and no `tokens.spacing` namespace).
Bad (deep import into internals — breaks when the package restructures):
```tsx
import { Button } from '@ottili/foundation-ui/dist/components/Button';
// dist/ is not part of the public contract; this import will break on the next release
```
Bad (raw literal instead of a token — drifts when the design system changes):
```tsx
<div style={{ color: '#ff0000', padding: '99px' }} />
// no token, no ALLOWED marker; check_foundation_tokens.py fails this
```
Good (tracked workaround — marker + ISSUE ticket, checker passes):
```tsx
<div style={{ color: '#ff0000' }} /* ALLOWED: FV2-WA ISSUE-1234 */ />
// the marker names a ticket; the checker exempts the line; the ticket owns the fix
```

## Pitfalls from research
- Deep imports into `dist/` or package internals are not part of the public contract and break on the next release.
- Raw design values drift silently when the token file changes; the checker catches them only if it runs.
- An `ALLOWED` marker without an `ISSUE-<digits>` ticket is a stale escape hatch, not a tracked workaround.
- A fresh-consumer test that reaches into internals is a unit test in disguise and gives no conformance signal.

## Near-miss triggers (act before the incident)
- "I need a specific prop the component does not export" — raise it with the package owner; do not reach into internals.
- "It is just a one-off colour" — put it in the token file or file an `ALLOWED` ticket; never ship raw.
- "The fresh-consumer test is slow" — it is the point; a fast test that reaches into internals proves nothing.
- "The workaround has been there for months" — check the ISSUE ticket is still open; a closed ticket means the marker is stale.

## Verification checklist (all must pass before you finish)
- [ ] All imports are from the public package surface, never `dist/` or internals.
- [ ] All design values resolve to a token or carry an `ALLOWED` marker with an `ISSUE-<digits>` ticket.
- [ ] Every workaround marker has an open ticket and a review date.
- [ ] Fresh-consumer test runs against a clean install and fails when the package changes.
- [ ] `scripts/check_foundation_tokens.py` exits 0 in CI.

## Related skills
- [acceptance-harness](../acceptance-harness/SKILL.md) — conformance is an acceptance scenario with PASS evidence.
- [module-contract-first](../module-contract-first/SKILL.md) — the Foundation `exports` map is itself a module contract; enumerate it, do not hand-wave it.
- [problem-json-contracts](../problem-json-contracts/SKILL.md) — a conformance failure is reported as a problem detail, not a silent row.
- [playwright-a11y-e2e](../playwright-a11y-e2e/SKILL.md) — axe assertions must not be weakened for token drift.
- [honest-status](../honest-status/SKILL.md) — a conformance failure is a status item; mark it VERIFIED only after the checker ran green, not after the code is written.
- [long-test-discipline](../long-test-discipline/SKILL.md) — the fresh-consumer install + test cycle takes minutes; run it in the foreground with a recorded seed.
- [shared-tree-git](../shared-tree-git/SKILL.md) — the conformance report and the fresh-consumer test are committed with a task-id prefix.
