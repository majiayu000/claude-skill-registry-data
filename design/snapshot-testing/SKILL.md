---
name: snapshot-testing
description: Snapshot testing — when to use, maintenance, CI integration.
---

## When to Use

| Use snapshots for | Do NOT use snapshots for |
|---|---|
| UI components with stable, complex render output | Business logic with frequently changing return values |
| Serialized data structures (API response shape) | Anything that changes on every run (timestamps, random IDs) |
| Error message strings that must stay stable | Core algorithm correctness — use explicit assertions |
| CLI command output format | Database query results in integration tests |

**Rule of thumb:** if a snapshot update is expected more than once per sprint for a given component, snapshots are the wrong tool for that component.

---

## Snapshot Rules

- **Always review snapshot diffs in PR.** A snapshot diff is a behavioral change — treat it like a code change, not noise.
- **Never auto-accept snapshots** with `--updateSnapshot` without visually confirming the new output is correct.
- **Delete stale snapshots immediately.** A snapshot for a deleted component is dead weight and can mask regressions.
- **Snapshots are not a substitute for behavioral assertions.** They verify structure; they do not verify correctness. Pair snapshots with explicit `expect(value).toBe(...)` assertions for critical logic.

### Size limit

If a snapshot file exceeds **50 lines**, the component under test is too complex. Options:
1. Break the component into smaller units and snapshot each independently
2. Test the component's behavior with targeted assertions instead of a full render snapshot
3. Extract sub-components and snapshot them separately

---

## Updating Snapshots

```bash
# Jest
jest --updateSnapshot

# Vitest
vitest --update

# Run only tests for a specific component
jest src/components/Button --updateSnapshot
```

**Before running update:**
1. Confirm the visual/structural change was intentional (design change, new feature)
2. Run the app locally and visually verify the component
3. After updating, re-run tests without `--updateSnapshot` to confirm they pass clean

**Commit message when updating snapshots:**
```
test(Button): update snapshot after adding disabled state variant
```

Always explain WHY the snapshot changed — not just "update snapshots".

---

## CI Integration

- Snapshots must be committed to the repository — never `.gitignore` snapshot directories
- CI runs tests **without** `--updateSnapshot`; if a snapshot changed without an update commit, the build fails
- A failing snapshot in CI means either:
  1. A developer forgot to commit the updated snapshot, OR
  2. An unintended regression — investigate before accepting

### Jest config example
```js
// jest.config.js
module.exports = {
  snapshotSerializers: ['@emotion/jest/serializer'],  // if using CSS-in-JS
  // CI will fail automatically if snapshots are outdated — no extra config needed
};
```

### Snapshot file location
- Keep snapshot files co-located with tests: `src/components/__snapshots__/Button.test.tsx.snap`
- Do not move snapshots to a central directory — co-location makes ownership clear

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Snapshotting the entire page/route | Snapshot only the component under test |
| Not seeding deterministic test data | Mock `Date.now()`, UUIDs, and random values |
| Leaving obsolete snapshots after component rename | Run `jest --ci` with `--verbose` to find orphaned snapshots |
| Committing `--updateSnapshot` in CI script | CI must never auto-update; only developers update locally |

---

## Checklist

- [ ] Snapshots reviewed in every PR that touches UI components
- [ ] No snapshot file exceeds 50 lines
- [ ] Snapshots committed alongside test files
- [ ] CI does not pass `--updateSnapshot`
- [ ] All snapshot updates have a commit message explaining the change
