---
name: orchestration-workflow
description: "Practical step-by-step walkthrough for orchestrating features end-to-end using the multi-agent system, from planning through deployment"
context: fork
globs: ["**/AGENTS.md", "**/agents/*.agent.md"]
alwaysApply: false
---

# Orchestration Workflow: Step-by-Step Guide

Practical walkthrough for using the multi-agent system end-to-end. This is your "how-to" guide for orchestrating features from planning through production deployment.

---

## Your First Feature (Real Example)

**Scenario:** You want to add JWT authentication to your app.  
**Time:** ~6-8 hours total (spread across 1-2 days)  
**Team:** All agents working together  
**Result:** Complete feature with 95% coverage, security audit passed, ready to deploy

---

## Step 1: Plan the Feature (30 minutes)

### What You Do

Open VS Code, start a chat with Copilot:

```
@athena: Plan JWT authentication with refresh tokens

Requirements:
- User login with email + password
- JWT access token (15 min expiry)
- Refresh token (7 day expiry)
- Secure token storage (httpOnly cookies)
- Token verification on protected routes
- Rate limiting (5 attempts/min)
- OWASP Top 10 compliant

Please create a detailed 3-4 phase implementation plan.
```

### What Athena Does

Athena researches patterns, calls Apollo for existing auth code, and creates:

```
📋 Plan: JWT Authentication
├─ Phase 1: Database Schema (Demeter)
│  ├─ Tasks: Create user + token tables
│  ├─ Test requirements: 5 test cases
│  └─ Risk: Zero-downtime migration
├─ Phase 2: Backend Services (Hermes)
│  ├─ Tasks: JWT service + endpoints
│  ├─ Test requirements: 8 test cases
│  └─ Risk: Token expiry edge cases
├─ Phase 3: Frontend Integration (Aphrodite)
│  ├─ Tasks: LoginForm + useAuth hook
│  ├─ Test requirements: 6 test cases
│  └─ Risk: Token refresh race condition
└─ FAQ: Answers to common questions
```

### What You Do

1. Review the plan presented by Athena in chat
2. **Ask questions or approve**
   - If concerns: `@athena: Please adjust plan because...`
   - If approved: "Plan looks good, let's proceed"

### ⏸️ PAUSE POINT 1: Plan Approval

```
Athena: ✅ Plan approved! Ready to orchestrate implementation
Zeus: Starting Phase 1 - Database Schema
```

---

## Step 2: Orchestrate Implementation

### Phase 1: Database Schema

**Zeus delegates to Demeter:**
```
@demeter: Implement database schema for JWT auth

Requirements:
- User table: id, email, hashed_password
- Token table: id, user_id, token, issued_at, expires_at, revoked_at
- Indexes: user(email), token(user_id, token)

TDD: RED → GREEN → REFACTOR
Coverage target: >80%
```

**Demeter does:**
1. Write FAILING migration test (RED)
2. Write minimal migration (GREEN)
3. Refactor (REFACTOR) — add types, indexes, constraints, timestamps

**Demeter delivers:** Schema files + tests, >80% coverage

**Themis reviews:** Coverage, security, performance, tests → APPROVED

**Background dispatch for independent phases (OpenCode v1.16.2+):**
If Phase 2 (backend) and Phase 3 (frontend) have no file dependencies, Zeus can dispatch both in **background** simultaneously and continue working while they execute. This eliminates the sequential wait.

### ⏸️ PAUSE POINT 2: Phase Review

```
Zeus: "Phase 1 complete! Coverage: >80% ✅ Security: ✅ Tests: passing ✅
Ready to continue to Phase 2?"

User: "continue"
```

### Phase 2: Backend Services

**Zeus delegates to Hermes:**
```
@hermes: Implement backend services for JWT auth

Create:
1. JWTService: generate, verify, refresh JWT
2. AuthService: handle login/logout
3. Auth endpoints: POST /auth/login, POST /auth/refresh, GET /auth/verify

TDD: RED → GREEN → REFACTOR
Coverage target: >80%
```

**Hermes does (TDD):**
1. Write failing test for JWT generation (RED)
2. Write minimal JWT service (GREEN)
3. Refactor with proper types, error handling (REFACTOR)
4. Repeat for all endpoints

**Hermes delivers:** Services + tests, >80% coverage

**Themis reviews:** Coverage, security (OWASP), performance → APPROVED

### ⏸️ PAUSE POINT 2: Phase Review

```
Zeus: "Phase 2 complete! Coverage: >80% ✅ Security: OWASP ✅ Tests: passing ✅
Ready to continue to Phase 3?"

User: "continue"
```

### Phase 3: Frontend Integration

**Zeus delegates to Aphrodite:**
```
@aphrodite: Implement frontend for JWT auth

Create:
1. LoginForm component
2. useAuth hook for state management
3. Protected route wrapper

TDD: RED → GREEN → REFACTOR
Coverage target: >80%
```

**Aphrodite does (TDD):**
1. Write failing component test (RED)
2. Write minimal component (GREEN)
3. Refactor with proper accessibility, error handling (REFACTOR)

**Aphrodite delivers:** Components + tests, >80% coverage

**Themis reviews:** Coverage, accessibility, security → APPROVED

### ⏸️ PAUSE POINT 2: Phase Review

```
Zeus: "Phase 3 complete! Coverage: >80% ✅ Accessibility: ✅ Tests: passing ✅
All phases approved!"
```

---

## Step 3: Final Summary

```
✅ JWT Authentication Complete

📊 Metrics:
- 3 phases: Database, Backend, Frontend
- >80% coverage across all layers
- Security: OWASP compliant ✅
- All tests passing ✅

🚀 Ready to commit
```

---

## Step 4: Git Commit

### ⏸️ PAUSE POINT 3: Git Commit

```
Zeus: "All phases approved! Ready to commit."

Suggested commit message:
feat: Add JWT authentication with refresh tokens

- Create User + Token database schema
- Implement JWTService + AuthService
- Add login, refresh, verify endpoints
- Create LoginForm + useAuth hook
- Full TDD: >80% coverage
- Security: OWASP Top 10 compliant

User: git add -A && git commit -m "..."
```

---

## Quick Reference: Workflow Commands

```bash
# Step 1: Plan
@athena: Plan [feature description]

# Step 2: Orchestrate
@zeus: Implement feature using plan

# Step 3: At pause points
# - Review phase results
# - Approve before proceeding

# Step 4: Commit
git add -A
git commit -m "feat: ..."

# Step 5: Deploy
git push origin [branch]
```

---

## Troubleshooting

### Problem: Phase coverage is <80%
**Solution:** Implementer adds missing test cases, re-runs coverage, Themis re-reviews.

### Problem: Security audit found issue
**Solution:** Relevant agent fixes (parameterized queries, input validation), re-audit, Themis approves.

### Problem: Frontend accessibility below target
**Solution:** Aphrodite improves ARIA labels, keyboard navigation, re-checks, Themis approves.

---

## Common Patterns

### Pattern 1: Simple Bug Fix (Skip Athena)
```
Discovery: @apollo: Find bug in authentication
Fix:      @hermes: Fix the validation error
Review:   @themis: Auto-invoked after fix
Result:   Minimal change, minimal risk (~30 min)
```

### Pattern 2: Complex Feature (Full System)
```
Plan:        @athena: Plan architecture
Orchestrate: @zeus: Implement using plan
Result:      Complete feature, >80% coverage (1-2 days)
```

### Pattern 3: Database Optimization
```
Discovery:   @apollo: Find N+1 queries
Optimize:    @demeter: Add indexes + optimize
Review:      @themis: Auto-invoked
Result:      10x faster queries (~2 hours)
```

---

## Pro Tips

🎯 **Plan First** — Saves 2-3x rework time  
🎯 **Use Pause Points** — You control when to proceed  
🎯 **Trust Themis** — Code review catches issues early  
🎯 **Commit Atomically** — One phase = one commit  
🎯 **Test First** — RED tests before code  
🎯 **Coverage Matters** — <80% = blocked, no exceptions  
🎯 **Security First** — Themis enforces OWASP compliance  
🎯 **Background Dispatch** — Use OpenCode v1.16.2+ background agents to run independent phases in parallel without polling  

---

## Next Steps

1. ✅ Read this guide
2. ✅ Review agent reference in `agent-coordination/SKILL.md`
3. ✅ Review TDD standards in `tdd-with-agents/SKILL.md`
4. 🚀 Start your first feature: `@athena: Plan [your idea]`

---

**Philosophy:** Plan → Orchestrate → Review → Commit → Deploy
Every phase has a pause point where YOU control the outcome.
