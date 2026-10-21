---
name: audit-baseline
owner: baseline
description: Drift check between the baseline implementation on disk and the claims in `docs/init/seed.md` + cross-references in CLAUDE.md, README.md, and the rendered docs site. Verifies hook/agent/skill/command names + counts, settings.json wiring, project.json key presence, .mcp.json servers, vendored license files, and helper script presence. Exit 0 PASS / 1 FAIL — suitable for CI. Read-only; safe to invoke any time.
---

# audit-baseline — drift defender

Mechanical check that the baseline implementation matches its specification. Deterministic, not LLM judgment — pattern matches and file presence only. Run on demand, by `/init-project` Step 8, or in CI.

## What it checks

| Category | Check |
|---|---|
| **Counts** | Hooks, agents, skills, commands on disk match the count claimed in `seed.md` |
| **Names** | Each component's name matches the canonical list in `seed.md` §4 |
| **Helper scripts** | `validate.mjs`, `swarm_merge.mjs`, `render.mjs`, `lint.mjs`, `archive.sh` present + executable |
| **settings.json** | Every baseline hook is wired in the correct event/matcher block |
| **project.json** | Every key listed in `seed.md` §13 Step 8 exists (values may be null pre-init) |
| **.mcp.json** | the declared documentation provider and the `plantuml` server present |
| **Vendored licenses** | `claude-automation-recommender/{LICENSE,NOTICE}` present (Apache 2.0 attribution) |
| **Cross-doc counts** | Numeric claims in `CLAUDE.md`, `README.md`, and `docs/init/seed.md` match disk |

## Invocation

`/audit-baseline` — model-invocable and user-invocable.

Calls `audit.mjs`. Output is a compact pass/fail table with a final verdict. Exits `0` on a clean audit, `1` on any failure. WARN-level findings (advisory; e.g., a doc with no relevant claims) don't fail the audit.

## When to run

- **End of `/init-project`** — Step 8. A fresh baseline should pass.
- **Before `/approve-direction`** — confirm the baseline hasn't drifted.
- **In CI** — fail the build on drift.
- **On demand** — when something feels off, when adding a component, or after a long gap in baseline maintenance.

## When the audit reports drift

- **Counts mismatch** → add the missing component or update `seed.md` to match the new count. Don't update one without the other.
- **Name mismatch** → a component was renamed, added, or removed. Update the canonical lists in `seed.md` §4 and the expected sets in `audit.mjs`.
- **Helper missing or non-executable** → `chmod +x` or restore from history.
- **Hook unwired** → add the entry to `.claude/settings.json`.
- **project.json key missing** → re-run `/init-project`, or add the key manually.
- **License missing** (vendored skills) → restore from upstream; this is a license-compliance gap.
- **Cross-doc stale numbers** → update the docs. `seed.md` is the source of truth.

## Maintenance

Expected name sets live in `expected-baseline.mjs` (the `EXPECTED_*` constants). Adding a new hook, agent, skill, or command means updating both `expected-baseline.mjs` and `seed.md`. The audit catches the drift; fix the implementation, not the audit.

`audit.mjs` is a thin orchestrator: it builds the shared audit context in `checks/context.mjs`, then runs one check module per concern from `checks/*.mjs` (each returns `[name, status, detail]` rows) and prints the table. To add a check, write a new `checks/<concern>.mjs` exporting `run(ctx)` and list it in the orchestrator's `CHECKS` array; pure surface helpers shared across checks live in `checks/surface-helpers.mjs`.

## Output format

```
check                                      status  detail
------------------------------------------ ------  ---------------------------
hooks count (seed vs baseline)             PASS    17
agents count (seed vs baseline)            PASS    1
skills count (seed vs baseline)            PASS    36
commands count (seed vs disk)              PASS    4
hooks names match seed §4.1                PASS
agents names match seed §4.2               PASS
skills names match seed §4.3               PASS
commands names match seed §4.4             PASS
helper swarm-plan/validate.mjs             PASS
…
hook wired: setup_guard                    PASS
…
project.json: test.cmd                     PASS
…
mcp server: gitmcp                         PASS
mcp server: plantuml                       PASS
mcp server: playwright                     PASS
recommender LICENSE                        PASS
recommender NOTICE                         PASS
CLAUDE.md count claims                     PASS
README.md count claims                     PASS
docs/init/seed.md count claims             PASS
------------------------------------------ ------
overall                                    PASS    fails=0 warns=0
```
