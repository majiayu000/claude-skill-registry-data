---
name: dep-lifecycle
description: Full dependency lifecycle composite — audit known vulnerabilities, triage by severity and breaking-change risk, upgrade targeted packages, verify tests pass, ship PR. Use monthly, before releases, or when dependency alerts are stacking. Never do a blanket upgrade; always triage first.
triggers:
  - dep lifecycle
  - dependency audit
  - update dependencies
  - dependabot triage
  - bump deps
  - audit dependencies
---

# dep-lifecycle

Full dependency lifecycle: audit → triage → upgrade → verify → ship.

## Phases

### Phase 1 — Audit
Run the scanner: `npm audit --json` (Node), `pip-audit` (Python), `cargo audit` (Rust).
Fetch open dependency PRs: `gh pr list --label "dependencies" --json number,title,headRefName`.
Output: vulnerabilities ranked by severity + stale packages by version lag.

### Phase 2 — Triage

| Class | Trigger | Action |
|---|---|---|
| CVE critical/high | CVSS ≥7 | Upgrade now |
| Breaking major | semver major | Separate PR; read migration guide first |
| Routine minor/patch | semver minor/patch | Batch into one PR |
| No upstream fix | vuln with no fix | Document + open issue; do not block sweep |

Skip any dependency where the vulnerable API is provably not called (grep for usage; zero hits → dismiss).

### Phase 3 — Upgrade (targeted, not blanket)
Upgrade each targeted package individually. Run a smoke check after each upgrade.
Do NOT run `npm update` or `pip install --upgrade-all`.

### Phase 4 — Verify
Run full quality gates. If tests fail after an upgrade: isolate → revert → open follow-up issue. Do not block the whole sweep for one hard upgrade.

### Phase 5 — Ship
- **Patches + minors:** one PR with all low-risk upgrades
- **Majors:** one PR per major (separate review context)

PR title: `chore(deps): bump <package(s)> to <version(s)>`

## Reconciliation

```
DEP LIFECYCLE — <date>

Phase 1 Audit:   N vulnerabilities, M stale packages ✅
Phase 2 Triage:  X critical/high, Y routine, Z dismissed ✅
Phase 3 Upgrade: <packages + versions> ✅
Phase 4 Verify:  PASS | <N packages reverted> ✅
Phase 5 Ship:    PR(s) <numbers> ✅
```

## Failure / Stop Conditions

- Phase 2: CVE with no upstream fix IS actively called → halt, escalate to user.
- Phase 3: major upgrade breaks >2 test files → revert, document, continue with rest.
- Phase 4: do not ship if any required gate is red due to an upgrade in this sweep.
- Never batch a major upgrade with routine patches.
