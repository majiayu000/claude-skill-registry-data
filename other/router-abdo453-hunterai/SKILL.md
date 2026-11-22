---
name: "router"
description: ">"
---

# Router

*Sourced from aetherdz-huntpack*

# Master Router — Bug Bounty Skill Dispatcher

The entry point for bug-bounty hunting. It fingerprints the target and classifies the task,
names the **minimal** set of specialized skills, and tells you to read them before acting.
It **dispatches and composes** — it does not re-teach hunting techniques.

## When to use

- At the **start of any authorized security assessment** — decide which skill(s) to load.
- When the user names a target, says "test this", "look for bugs", or asks "which skill should I use?".
- When switching targets or rotating.

**When *not* to use:** once the right skill is loaded and the task is squarely inside it, work
from that skill — don't re-run the router every turn. Re-route only when the task **pivots** to a
new stage (router step 3).

## Routing algorithm

1. **Classify the task** — is it "understand the target", "map the surface", "hunt a bug class",
   "stay disciplined", "prove a finding", or "write the report"?
2. **Detect the target** — web app? API? which archetype? (see `skills/understand/application-archetypes`)
3. **Read the routing table below** → load the minimal skill set for that stage.
4. **Read the chosen skill(s) fully** before acting.
5. **Re-route on pivot** — new evidence that moves you to another stage loads that stage's skills.

## Routing table

| Stage | Skills (read before acting) |
|---|---|
| **Understand** | `application-archetypes` → `application-model-builder` |
| **Map surface** | `web2-recon` |
| **Hunt** | `web2-vuln-classes` · `business-logic-hunter` · `api-security` |
| **Discipline** | `domain-scoped-hunting` (load **before** any hunt) |
| **Prove** | `false-positive-killer` → `triage-validation` |
| **Deliver** | `attack-path-builder` → `report-writing` |

Default session order: Understand → Map → Discipline → Hunt → Prove → Deliver.
Every output uses the shared evidence schema below (stage 5 of this file).

## RESPONSE-DRIVEN NEXT ACTIONS

| You See | You Are In | Next Move |
|---------|-----------|-----------|
| 403 on all requests to endpoint | Recon/Discovery | Run 403 bypass checklist (headers, method swap, path variation). 5 min → skip. |
| 200 but body is SPA catch-all | Recon | Not a real endpoint. Try `.json`, `/api` prefix, format param. |
| Error stack trace on bad input | Discovery → Prove | Deepen error probe, chain to info disclosure, look for debug endpoints. |
| Timing diff on user-exists | Discovery → Prove | Automate enumeration → password spray or ATO chain. |
| WAF block page (403/406/429) | Discovery | Try Content-Type switch, HTTP/2→1.1, IP rotation. 5 min → kill path. |
| IDOR-confirmed (A reads B data) | Prove → Chain | Check if same IDOR affects PUT/DELETE → chain to data mod or ATO. |
| Race condition success (2x200, 2x change) | Prove | Verify ledger — both changes persisted? → financial impact chain. |
| 401 without token, 200 with any token | Mapping | Auth exists but weak ACL. Focus on IDOR, BOLA, mass assignment. |
| JWT in response with `role` field | Mapping → Prove | None-alg, weak secret, role tamper → chain to admin access. |
| GraphQL introspection on | Mapping → Discovery | Schema leak → field auth bypass → batching for mass PII. |
| Sibling endpoint found mid-session | Mapping | Re-score, add to model, generate new hypotheses. |

## WEAK PATH CANCELLATION (Stop Early, Save Time)

Kill the current path immediately when:
- 3 consecutive 403s with no bypass → STOP (auth gated)
- 5 min of recon on a host → SKIP (5-minute rule)
- 20 min on an endpoint with no signal → ROTATE (20-minute rule)
- A vs B sessions return identical data → STOP (no IDOR)
- `unique constraint` on race test → STOP (serialized)
- Confirmed intended behavior → STOP
- Score < 40 after 2 clean tests → STOP
- WAF blocking 3 different payload approaches → STOP

DEFER (don't kill) when:
- New technology detected mid-session → re-evaluate
- Score jumps 15+ points from new evidence → re-prioritize
- Chain opportunity appears for a low-sev finding
- Target just deployed an update

## EVIDENCE SCHEMA INTEGRATION

Every phase output must use the shared evidence schema below:
```yaml
evidence_id: "OBS-NNN" | phase: "recon"|"model"|"hunt"|"chain"|"validate"
type: "request"|"response"|"diff"|"observation"
source: "header"|"JS"|"API"|"curl"|"diff" | actor: "guest"|"user_a"|"user_b"|"admin"
signal: "sequential_id"|"missing_403"|"role_field"|"error_stack"|"timing_diff"
action: "exact curl/request" | expected: "what should happen" | actual: "what happened"
confidence: 0.3-1.0 | impact: "real" | reproducible: true|false
chain_candidate: false
```

No evidence → no claim → kill it.
