---
name: module-contract-first
description: "Designs and enforces module contracts in one working tree: public API surface, versioned schemas, drift tests against reference snapshots, and boundary rules between sibling modules. Use when defining a new module's public API, reviewing a breaking change, or diagnosing cross-module breakage in a shared tree."
license: MIT-compat
compatibility: "framework-agnostic; Python/TypeScript/Postgres; Ottili modules"
metadata: {}
allowed-tools: []
---

Standard: name/description/length rules — [agentskills.io standard](../references/agentskills-standard.md).
# Module Contract First Skill — Quick Reference (body <500 lines; full procedure in references/module-contract-procedure.md)

## When to use this skill (trigger)
- You are starting a new module or adding public exports to an existing one.
- A consumer imports a symbol that is not in the committed contract snapshot.
- You need to decide whether a change is breaking (major bump) or non-breaking (minor/patch).
- Sibling modules import each other and you must enforce a boundary (no cycles).
- CI is red with "DRIFT DETECTED" or "CYCLE DETECTED".

## Disambiguation
- Fires: starting a new module or public exports, a consumer imports an unlisted symbol, deciding breaking vs non-breaking, sibling-module cycle detection, CI red with DRIFT/CYCLE.
- Does NOT fire for: an HTTP API error contract (use problem-json-contracts) or a single internal helper with no consumers.

## When NOT to use this skill
- Private/internal helpers that no consumer imports — they are not part of the public surface, so no snapshot covers them.
- A change to a private helper that no symbol table can see — the skill governs the public surface, not your local functions.
- Single-file scripts with no consumers and no planned exports — no snapshot is needed, but if the file *might* be imported later, snapshot it anyway.
- Fully greenfield work where no other module depends on the output yet — the skill still fires once the first consumer lands; until then, snapshot the surface anyway so the first import is not a surprise.
- A pre-release version bump (1.2.3-alpha.1) — the decision table still applies; a pre-release is not a free pass to break the API, and the snapshot is regenerated alongside the bump.

## Decision table — change classification
| Change | Semver | Action |
|--------|--------|--------|
| Add new export, route, table, or message | minor | regenerate snapshot, commit both together |
| Rename export, change signature, remove export | major | bump major, notify all consumers, regenerate snapshot |
| Add optional field to a request object | patch | regenerate snapshot only |
| Change field type or required->optional | major | bump major, regenerate snapshot, update consumers |

## Numbered procedure (summary; full recipe in references/module-contract-procedure.md)
1. **Enumerate the public surface** — run `python3 scripts/check_contract_drift.py --enumerate <module-dir>` and commit the generated snapshot as the source of truth.
2. **Freeze and version** — tag the snapshot commit with semver per the decision table; never hand-edit a committed snapshot.
3. **Write the drift test** — `python3 scripts/check_contract_drift.py --check <module-dir>` must run in CI on every PR; exit 1 on any drift.
4. **Enforce boundaries** — run `python3 scripts/check_contract_drift.py --cycles <root>`; any back-edge is an automatic fail.
5. **Document the boundary** — write a boundary doc listing allowed importers and forbidden import directions.

## Worked examples
Good (additive change — minor bump, regenerate snapshot in the same PR):
```bash
$ python3 scripts/check_contract_drift.py --enumerate src/users
ok: enumerated 15 symbols -> src/users/module-contracts/users.json
$ python3 scripts/check_contract_drift.py --classify src/users/module-contracts/users.json src/users/module-contracts/users.json
{
  "bump": "patch",
  "added": [],
  "removed": [],
  "old_count": 15,
  "new_count": 15
}
```
Bad (breaking rename without a major bump — consumer breaks at import time):
```python
# before: public export get_user(id)
# after:  public export fetch_user(id)
$ python3 scripts/check_contract_drift.py --classify old.json new.json
{
  "bump": "major",
  "added": ["fetch_user"],
  "removed": ["get_user"],
  ...
}
# Do NOT ship this as a patch. Bump major, notify consumers, regenerate snapshot.
```
Bad (hand-edited snapshot to make CI green — hides a real breaking change for weeks):
```json
// users.json hand-edited to add "fetch_user" without removing "get_user"
{"symbols": ["fetch_user", "get_user", ...]}
# --check now passes, but the live code no longer exports get_user.
# Rule: never hand-edit; always regenerate with --enumerate.
```

## Pitfalls from research (real incidents)
- Hand-edited snapshots hide new exports; the next `--check` shows full-add drift and CI goes red until regenerated honestly alongside the code change in the same PR.
- A snapshot that is not regenerated on every PR touching public API surface is the #1 cause of silent breakage across Ottili modules.
- Import cycles break static analysis tooling downstream even when snapshots match; cycle detection is an automatic fail regardless of snapshot state.
- An empty module must have an empty snapshot; a missing snapshot file is treated as full-add drift, not an error.

## Near-miss trigger prompts (act on these immediately)
- "I added an export but forgot to update the snapshot" — run `--check` before committing; if drift, regenerate then commit both files together.
- "Module A imports B and B imports A" — run `--cycles` immediately; extract shared types into an internal-only module.
- "The snapshot looks right but CI is red" — diff spans >5 lines with no corresponding code change = probable manual edit; block merge.

## Verification checklist (all must pass before you finish)
- [ ] Snapshot regenerated via `--enumerate`, never hand-edited
- [ ] `--check` exits 0 against the committed snapshot
- [ ] `--cycles` reports no back-edges
- [ ] Semver bump matches the change classification in the decision table
- [ ] Boundary doc lists allowed importers and forbidden directions
- [ ] Drift test is wired into CI config
- [ ] Enumeration completes in <2s for modules under 500 symbols

- [problem-json-contracts](../problem-json-contracts/SKILL.md)

## References
- Full procedure, decision table and worked examples: `references/module-contract-procedure.md`.
- Eval prompts with expected behaviour and failure signs: `references/EVALS.md`.
- Primary sources with URLs and retrieval dates: `references/SOURCES.md`.

## Related skills
- [problem-json-contracts](../problem-json-contracts/SKILL.md) — contract shapes are also problem-detail shapes.
- [honest-status](../honest-status/SKILL.md) — a contract that drifts is a status item; mark it VERIFIED only after `--check` ran green.
- [long-test-discipline](../long-test-discipline/SKILL.md) — the snapshot enumeration and the drift check are long tests; run them in the foreground with a recorded seed.
- [shared-tree-git](../shared-tree-git/SKILL.md) — snapshot and boundary doc are committed with a task-id prefix.
