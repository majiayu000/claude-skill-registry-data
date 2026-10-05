---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
---

# Verification Before Completion

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

Claiming work is complete without verification is dishonesty, not efficiency. If you haven't run the verification command in this message, you cannot claim it passes.

**Violating the letter of this rule is violating the spirit of this rule.**

---

## When This Fires

- ANY claim that work is done, fixed, passing, deployed, or ready
- ANY expression of satisfaction about work state
- Before committing, pushing, or creating PRs
- Before moving to the next task
- Before telling Josh something works
- After delegating to agents (verify their output independently)

**If Josh finds something broken that you called done, that's a trust violation.**

---

## The Gate Function

```
BEFORE claiming any status:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete, in THIS message)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output actually confirm the claim?
   - If NO → State actual status with evidence
   - If YES → State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

---

## Stage 1: Code Quality (Before Commit)

### Build & Lint
```
□ Build/compile passes — zero errors, zero warnings
□ Linter passes (ruff, eslint, tsc --noEmit, etc.) — show output
□ No debug code, print statements, or commented-out blocks
□ No hardcoded secrets (IPs only where config-appropriate)
```

### Tests
```
□ Full test suite ran — show actual output, not "should pass"
□ Record result: "X/Y tests pass, 0 failures"
□ New/changed code has test coverage for happy path + edge cases
□ If TDD: red-green-refactor verified (test fails without fix, passes with)
□ Integration tests if touching DB, APIs, or cross-service boundaries
```

### Self-Review
```
□ git diff — read every changed line as if reviewing someone else's code
□ Clear variable/function names, no unnecessary duplication
□ No N+1 queries, unbounded loops, or resource leaks
□ Error handling at system boundaries (user input, external APIs, file I/O)
□ No security issues: injection, XSS, auth bypass, secrets in code
□ Changes match task scope — no unrelated "improvements"
□ Dependencies only bumped if necessary, breaking changes checked
```

---

## Stage 2: Commit & Push

```
□ Commit message explains WHY, not just WHAT
□ Each commit is one logical unit of work
□ No unrelated files staged (check git status)
□ No secrets committed (.env, credentials, wallet addresses)
□ Push succeeds — no rejected refs, no hook failures
□ If CI exists: wait for green, don't assume
```

---

## Stage 3: Deploy Verification

**This is where trust gets broken most often. HTTP 200 ≠ working.**

### Pre-Deploy
```
□ Target host reachable (SSH, retry on first failure)
□ Port conflicts checked: ss -tlnp on target
□ Config uses correct IPs for DEPLOYMENT context, not dev
  - Client-side URLs reachable FROM THE BROWSER, not from the container
  - NEXT_PUBLIC_* are BUILD-TIME in Next.js — must be correct at docker build
  - CORS origins include the origin the browser will actually use
□ Secrets/env files exist on target with correct values
□ Sufficient disk, memory, VRAM on target
□ Docker images built successfully — read the build output, don't assume
```

### Container Health
```
□ ALL containers show "Up" and "(healthy)" — not "starting", not missing
□ Health check commands work inside the container
  - curl may not exist in slim images — use python3 urllib or wget
□ Container logs show clean startup — no tracebacks, no warnings
□ docker compose ps — all services running, correct port mappings
```

### End-to-End Functional Proof (NON-NEGOTIABLE)

**Test from the USER's perspective, not from inside the container.**

```
□ API responds from LAN IP (not 127.0.0.1):
    curl http://<HOST_IP>:<PORT>/api/health

□ Frontend loads from LAN IP:
    curl -s http://<HOST_IP>:<PORT> | verify expected HTML content

□ Frontend can actually reach backend:
    - Verify API URL in JS bundles points to LAN-reachable backend
    - Verify CORS: curl with Origin header, check access-control-allow-origin
    - NOT JUST "page loads" — verify the client-server connection works

□ Data is present:
    - API returns real data, not empty arrays
    - If migrated: row counts match source
    - If seeded: seed data loads correctly

□ Key user journey works:
    - Can a user DO the thing the service is for?
    - Not "page renders" — "user can complete the workflow"
    - Auth flows work if applicable (register, login, protected endpoints)
```

### Network
```
□ Service accessible from other fleet hosts, not just localhost
□ Ports bound to correct interface:
    - 0.0.0.0 for LAN-accessible
    - 127.0.0.1 for internal-only (databases, admin)
□ Firewall allows traffic if UFW active
```

---

## Stage 4: Production Readiness

```
□ Service restarts cleanly (docker compose restart)
□ Service survives host reboot (restart policy or systemd enabled)
□ Data persists across restarts (volumes, not ephemeral)
□ Rollback plan exists — know how to revert
□ Logs accessible (docker logs, journalctl)
□ GPU VRAM verified (nvidia-smi) if GPU workload
□ Port registered in your project's port registry documentation
□ README/docs updated, session summary includes deploy details
```

---

## Stage 5: Report With Evidence

When reporting completion, include proof:

```
✅ GOOD:
"ExamForge deployed on <gpu-host>:
  - docker ps: 3/3 healthy
  - curl http://<service-ip>:<api-port>/api/health → {"status":"ok"}
  - curl http://<service-ip>:<frontend-port> → 93KB HTML, contains 'ExamForge'
  - JS bundles contain http://<service-ip>:<api-port> (verified grep)
  - CORS: access-control-allow-origin: http://<service-ip>:<frontend-port>
  - API returns 7 certifications, 2399 questions"

❌ BAD:
"ExamForge deployed on <gpu-host>. Backend returns 200, frontend returns 200.
 All systems go."
```

---

## Verification Matrix

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build output: exit 0 | Linter passing |
| Bug fixed | Original symptom gone | Code changed, assumed fixed |
| Deployed | All containers healthy + E2E proof | Health check 200 |
| Frontend works | Browser can load AND call backend | HTML returns 200 |
| Data migrated | Row counts match on both sides | Script ran without errors |
| Service accessible | curl from LAN IP succeeds | curl from localhost succeeds |
| Agent completed | VCS diff verified independently | Agent reports "success" |
| Requirements met | Line-by-line checklist with evidence | Tests passing |

---

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Health check passed" | Health check ≠ functional |
| "200 OK" | 200 ≠ working |
| "Linter passed" | Linter ≠ compiler ≠ functional |
| "Agent said success" | Verify independently |
| "Partial check is enough" | Partial proves nothing |
| "I already verified earlier" | Verify AGAIN, fresh |
| "It works from localhost" | Test from the user's machine |

---

## Anti-Patterns From Real Incidents

| What Happened | What Should Have Happened |
|---|---|
| Claimed ExamForge "deployed and working" from 200 health check | Verified frontend→backend connection from browser perspective |
| NEXT_PUBLIC_API_URL pointed to 127.0.0.1 in Docker build | Used deployment host LAN IP in build args, verified in JS bundle |
| Backend bound to 127.0.0.1 only | Bound to 0.0.0.0, tested from LAN |
| Health check used curl (not in slim Python image) | Used python3 urllib (always available) |
| Didn't run plan's own verification steps | Execute every verification step listed in the plan |
| Said "all containers healthy" when frontend hadn't started | Verified ALL containers in docker ps, not just some |
| Expressed satisfaction before running verification | Gate function: evidence first, claims second |

---

## Minimum Gate (Quick Reference)

Before saying "done", answer each with evidence — not "I think so":

```
1. BUILT?      → Build output, zero errors
2. TESTED?     → Test output, zero failures
3. LINTED?     → Linter output, zero errors
4. DEPLOYED?   → All containers healthy (show docker ps)
5. REACHABLE?  → curl from LAN IP returns expected content
6. FUNCTIONAL? → End-to-end user journey works
7. DATA?       → Real data present, not empty
8. DOCUMENTED? → Ports, docs, session summary updated
```

---

## The Bottom Line

**Working code that's verified beats shipped code that's assumed.**

Run the command. Read the output. Test from the user's perspective. THEN claim the result.

This is non-negotiable.
