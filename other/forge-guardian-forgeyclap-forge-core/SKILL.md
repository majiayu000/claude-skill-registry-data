---
name: forge-guardian
description: Scaffold design doctrine for an owner-gated production self-healing guardian (not live). Use only when designing auto-rollback, incident response, canary, circuit breaker automation.
---

# Forge playbook — Guardian (deploy -> monitor -> reproduce -> self-heal -> redeploy)

**STATUS: SCAFFOLD.** Nothing in this file is wired to any live production system in this project. No
`forge-bin/` tool currently deploys, monitors a live endpoint, or redeploys anything — this skill exists
so the *design* is available and reviewable, not because the capability is running. Do not report Guardian
as "active" or "monitoring" anything unless the owner has supplied real production access AND approved a
live circuit-breaker for that specific environment. Absent both, Guardian stays exactly what it is here: a
documented design.

**Do not duplicate existing tools — defer to:** `forge-actiongate.cjs` (the ONE hard-gate classifier every
deploy/redeploy step below MUST route through — never a parallel gate), `forge-checkpoint.cjs` (idempotency
for any redeploy/rollback action so a retry never double-deploys), `forge-briefing.cjs` (surfacing an
incident as a real "decision needed" item, the same evidenced pattern `forge-nightshift` uses), and this
project's existing "no mandatory security gates but hard-gates always stop" governance
(`CLAUDE.md` + `config/orchestration/hard-gates.json`).

## The loop this doctrine describes
1. **Deploy** — an explicit, owner-approved release to a named environment. Always classified through
   `forge-actiongate.cjs::classify()` (gate id `deploy`, `prod-activate`, or equivalent) BEFORE it happens;
   never a Guardian-internal deploy path that bypasses the existing gate.
2. **Monitor** — after a real deploy, watch the environment's own real signals (health checks, error rate,
   latency, a smoke test) — never fabricated or assumed-passing telemetry. If no real monitoring source is
   wired for an environment, Guardian has nothing to watch and says so honestly, rather than inventing a
   "healthy" status.
3. **Reproduce** — when a real signal indicates a regression, reproduce it with an actual failing
   check/test BEFORE attempting any fix (mirrors this project's `forge-debug` skill: reproduce → isolate →
   root-cause, never a guessed patch). A "fix" with no reproduction is not a fix, it's a guess.
4. **Self-heal** — propose (and, ONLY with the circuit-breaker below open, apply) the smallest correct fix
   for the reproduced regression: a code fix + regression test, a config rollback, or a redeploy of the last
   known-good artifact. Every one of these is itself a write/deploy action and is gated exactly like step 1.
5. **Redeploy** — the fixed/rolled-back artifact goes out through the SAME `deploy` gate as step 1. There is
   no separate, lower-scrutiny "redeploy" path — a redeploy is a deploy.

## Hard rules (non-negotiable, no exceptions)
- **Owner circuit-breaker required, per environment, before ANY step 1 or step 5 action.** Guardian never
  deploys or redeploys autonomously, ever — including "just restoring what was already there." An explicit,
  named approval (`owner_confirmed:true` on the specific `forge-actiongate.cjs` gate hit, for the specific
  environment) is required every time, not a standing blanket approval from a prior incident.
- **Every deploy/redeploy call is classified through `forge-actiongate.cjs` — never reimplemented.** If a
  proposed action does not clearly hit an existing gate id, that is treated as a gap to raise with the
  owner (add/confirm the right gate), not a loophole to act through.
- **No autonomous monitoring of a production system the owner has not explicitly granted access to.**
  Absent real credentials/read access to a real monitoring source, Guardian cannot "watch" anything —
  reporting a simulated or assumed health status would be exactly the fabrication this project's honesty
  core forbids.
- **A self-heal fix always ships with reproduction evidence + a regression test**, exactly like any other
  Forge bug fix — an incident "fixed" with no reproducing test is not verified fixed, it is a guess that
  happened to make the alert stop for now.
- **Idempotent redeploys.** Any redeploy/rollback action MUST go through `forge-checkpoint.cjs::shouldRun/
  claim` with a real idempotency key first — a flapping alert must never trigger the same redeploy twice in
  a race.
- **Incidents are reported like blockers, not hidden.** An open incident that cannot be safely auto-healed
  is exactly a `forge-briefing.cjs` "decision needed" item: retry the fix, roll back, or escalate — the
  owner decides, Guardian does not decide for them.

## What would need to exist before this stops being a scaffold
- Real, owner-granted credentials to the target production environment (deploy access + monitoring/read
  access), scoped least-privilege, never hardcoded in this repo.
- A real monitoring/alerting source Guardian can actually read (health endpoint, error-rate metric, log
  query) — not a guess about what "probably" indicates health.
- An owner-approved circuit-breaker mechanism for that specific environment (the explicit, per-use
  `owner_confirmed:true` this doctrine already requires — see Hard rules).
- A real rollback/redeploy path that has been tested at least once with the owner present, exactly the same
  "tested rollback" requirement `forge-mlops` already applies to model promotion.
None of the above exists in this project today. Until it does, Guardian's value is the reviewable design
above plus the fact that every action it describes already has to pass through `forge-actiongate.cjs` —
which is real and already enforced — the moment someone tries to wire a live version of this loop.

## Skills / commands / MCP
`forge-actiongate.cjs` (hard-gate classifier, reused not duplicated), `forge-checkpoint.cjs` (redeploy
idempotency), `forge-debug` skill (reproduce → isolate → root-cause discipline for step 3/4),
`forge-briefing.cjs` (incident-as-decision-needed reporting), `forge-mlops` skill (the closest existing
analog for "owner-gated promotion + tested rollback" if the guarded system is a served model).

## Fan-out & flow
No team spawns from this skill on its own while it remains a scaffold. If/when a real environment is wired,
the natural team is: `integration-boss` (deploy/monitoring wiring) + `build-boss` (the fix + regression
test) + `security-boss` (credential scoping review) + Head Chef as the explicit human-approval relay — never
a fully autonomous loop.

## Ship-readiness (unique)
Every deploy/redeploy in scope actually routed through `forge-actiongate.cjs` with a real, per-use
`owner_confirmed:true` (never a cached/standing approval); no fix claimed without real reproduction +
regression-test evidence; no "healthy"/"monitoring" claim without a real, owner-granted monitoring source;
no redeploy without a checked `forge-checkpoint.cjs` idempotency key; the report states plainly whether any
of this ran against a real environment or stayed entirely at the design/scaffold level — never implying live
production self-healing occurred when it did not.
