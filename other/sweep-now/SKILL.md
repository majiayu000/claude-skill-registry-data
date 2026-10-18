---
name: sweep-now
agent: none
description: Run the three read-mostly vault sweeps for stale tracker items, dormant-note candidates, and broken wikilinks, then append one dated result to SWEEP_LOG.md.
allowed-tools: Read, Edit, Bash, Grep, Glob
user-invocable: true
triggers:
  - sweep now
  - vault sweep
  - clean the vault
  - sweep stale
  - broken links
---

# /sweep-now

Run all three sweeps in sequence and append one result to
`vault/memory/SWEEP_LOG.md`.

## Checks

1. Scan active Delegation Tracker items. Flag live items whose last meaningful
   update is older than 14 days.
2. Read `HEAT_INDEX.json` `cold_bottom_20`. For each note last touched more than
   60 days ago, propose a dormant flip. Do not apply it unattended.
3. Scan vault wikilinks and list references whose target does not exist.

## Output

Append:

```markdown
### YYYY-MM-DD - full sweep
- Delegation tracker: <N> stale items flagged (<stable references>)
- Dormant-note candidates: <N> proposed
- Broken wikilinks: <N>
- Notes inspected: <wikilink list or none>
- Open issues for the operator: <list or none>
```

Append only after all three scans complete. The nightly controller independently
checks the newest real H3 date header.

## Cadence

The default cadence is seven days. A nightly skip is legal only when
`SWEEP_LOG.md` exists, contains a valid real dated H3 header, and the controller
derives that it is within cadence. Missing or malformed evidence is failure.

## Boundaries

- Do not auto-fix broken links.
- Do not auto-flip dormant notes.
- Do not auto-close stale work.
- Keep every proposal human-reviewable.
