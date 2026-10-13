---
name: tradecraft-attack-path-mapping
description: >
  Model the target as an attack graph — nodes (assets, identities, trust) and edges (a technique
  that gets you from one to the next) — and find the shortest path to the objective. Load when many
  findings need to be assembled into a route, on "how do these bugs connect", AD/cloud lateral-
  movement planning, or to explain how a foothold reaches crown jewels.
domain: tradecraft
type: methodology
stability: learning
modes: [pentest, defense]
mitre: []
tools: [bloodhound, cartography, pmapper]
schema_version: 1
---

# Attack-path mapping

## When it applies
You have several footholds/findings and need to see how they combine into a route to the objective
— or you're defending and want to know which single edge, if cut, breaks the most paths.

## Why it works
Attackers think in graphs; defenders who do too find the choke points. Modelling
principals → permissions → resources as edges makes "can A reach D?" a reachability query, and
surfaces multi-step paths no single finding reveals (this is why BloodHound changed AD assessment).

## Method
1. **Nodes**: assets (hosts, buckets, DBs), identities (users, roles, service accounts), and secrets.
2. **Edges = a technique you can actually run**: "user→host" (valid creds / RCE), "host→identity"
   (token/cred theft — `privesc-*`, `cloud-imds-ssrf`), "identity→identity" (delegation, role assumption —
   `ad-*`, `cloud-iam-privesc`), "identity→data" (read access). Label each edge with its skill.
3. **Build the graph**: BloodHound (AD), PMapper/Cartography (AWS/cloud IAM), or a hand-drawn graph
   in `notes.md` for smaller scopes.
4. **Query for paths**: shortest path from a controlled node to the objective; enumerate alternates.
5. **Pick the path**: lowest cost/noise, highest reliability. Each edge becomes an ordered lead in
   the scenario (`tradecraft-attack-scenarios`).
6. **Defensive read**: rank edges by how many objective-paths traverse them — those are the
   remediation priorities (kill the edge, not just the node).

## Gotchas
- An edge you can't actually execute is not an edge — validate the technique, don't assume it.
- Graphs go stale as you change the environment (new creds, revoked tokens); re-query after each win.
- Don't collect the whole graph when one path proves impact — least action.

## Verify success
You can state the full path — node by node, edge by edge, each edge a runnable technique — from a
starting position to the objective, and name the one edge whose removal breaks it.

## References
BloodHound / SharpHound; NCC PMapper; AWS/GCP Cartography; MITRE ATT&CK flow.
