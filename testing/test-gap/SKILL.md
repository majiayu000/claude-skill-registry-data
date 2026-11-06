---
name: test-gap
description: >-
  User-invoked as /test-gap [path]. Spawns the qa agent to analyse test
  coverage and returns a prioritised list of missing tests, risk-ranked
  (consensus/payload-parsing logic first). Use to decide what to test next.
allowed-tools: Read, Grep, Glob, Bash, Agent
invocation: /test-gap [path]
---

# Test Gap Analysis

Identify the highest-value missing tests for `$ARGUMENTS` (a module/dir, or the
whole package if empty).

## Steps

1. Establish current coverage:
   `uv run pytest tests/unit/ -q --cov=aegis_swr --cov-report=term-missing`
   (scope with `--cov=aegis_swr.<subpkg>` when a path is given).
2. Spawn the **`testing-expert`** agent with the coverage output and the target path. Ask it
   to map uncovered lines to behaviours and **risk-rank** them:
   - **P0**: consensus/skeptic logic, payload/dump/log parsing, escalation &
     HITL paths, security-relevant branches.
   - **P1**: backend strategies, orchestrator transitions, schema validation.
   - **P2**: CLI/view formatting, logging.
3. Return the qa agent's prioritised list.

## Output

```
## Test Gap - <target> (coverage: NN%)
### P0 - must test
- path:line-range - <untested behaviour> - <why risky> - <suggested test>
### P1 - should test
### P2 - nice to have
```
Offer to have `testing-expert` write the P0 tests next.
