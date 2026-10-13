---
name: tradecraft-pivot-decisions
description: >
  Decide what to do next after a result — the branching logic that turns a single outcome into the
  next lead. Load whenever a step just finished (success, partial, or dead end) and it's unclear
  where to go: "what now", "I got a shell/creds/a hash", "this didn't work", triaging which of
  several leads to pursue. This is the decision engine between techniques.
domain: tradecraft
type: methodology
stability: locked
modes: [pentest, bugbounty, defense]
mitre: []
tools: []
schema_version: 1
---

# Pivoting: deciding the next move

## When it applies
A step just produced a result and you must choose the next action instead of blindly running the
next tool. Applies after every meaningful step — this is what keeps an engagement adaptive.

## Why it works
Value comes from routing on evidence: a result changes the probability and payoff of every other
lead. Making the routing explicit (what the result unlocks, what it rules out) avoids both
tunnel-vision and aimless scanning, and produces the `decision` + `rationale` entries the Attack
Map is built from.

## Method
1. **Classify the result**: confirmed / partial / blocked / failed. Record it as the lead's `status`.
2. **Ask what it unlocks** (route by artifact — the signal → skill map):
   - creds / hash → crack or spray (`network-credential-cracking`, `network-password-spraying`)
   - a shell → enumerate & escalate (`privesc-enumeration` → `privesc-*`)
   - SSRF / file read → reach internal services, metadata (`cloud-imds-ssrf`, `web-ssrf`)
   - a token / key → what identity does it become? (`cloud-iam-privesc`, `ad-*`)
   - two small bugs that combine → `exploit-chaining`
   - internal foothold → `network-pivoting-tunneling`, map the graph (`tradecraft-attack-path-mapping`)
3. **Score the candidates**: impact toward the objective × likelihood × cost/noise; pick the top one.
4. **On a dead end**, don't just stop: record *why* (so it's not retried), then fall back to the
   next-best lead from the scenario. "Blocked by infra" ≠ "not vulnerable" — say which.
5. **Update the plan**: re-order remaining leads; note the new pivot. Then act on the single top lead.

## Gotchas
- Sunk cost: abandon a low-yield lead even after effort if a better one appeared.
- "It failed" without a reason is a lost lesson — always record the mechanism of the failure.
- Chasing novelty over objective: the next move is the one that best advances the stated goal.

## Verify success
After each result there is a recorded decision (status + rationale) and exactly one chosen next
lead that advances the objective — the engagement never stalls on "what now".

## References
OODA loop applied to offense; MITRE ATT&CK tactic transitions; the `exploit-chaining` skill.
