---
name: saas-accelerator
description: >
  Master orchestrator skill that coordinates a full multi-agent startup pipeline.
  Triggers on: build SaaS, launch startup, startup accelerator, build product,
  create MVP, SaaS builder, million dollar startup, build me a business, or
  using the Startup Factory.
  Coordinates 8 specialized sub-skills in a gated, human-approved sequence.
---

# SaaS Accelerator — Master Orchestrator

## Purpose

Transform a raw SaaS idea into a validated, architected, coded, tested, and
deployment-ready product through an 8-phase multi-agent pipeline with mandatory
human approval gates between each phase.

This is NOT a "write code from a prompt" tool. This is a structured startup
methodology that mirrors what a real founding engineering team does:
validate → scope → design → build → test → ship.

## When to Use This Skill

Activate when the user wants to:
- Build a SaaS product or feature from scratch
- Launch a startup MVP
- Turn an idea into a working product
- Use a multi-agent system to build software

## Non-Goals

This skill does NOT:
- Guarantee revenue or product-market fit (that requires real users)
- Replace human judgment on business strategy
- Handle legal, compliance, or financial regulation
- Deploy to production automatically (it prepares deployment configs)

---

## The 8-Phase Pipeline

Each phase produces a concrete artifact. The user (CEO) must approve each
artifact before the next phase begins. No phase may be skipped.

```
IDEA → [1] Market Scout → [2] MVP Scoper → [3] Architect → [4] Schema Designer
     → [5] Coder → [6] Test Engineer → [7] Security Auditor → [8] Deploy Planner
```

### Phase 1: Market Scout (Research & Validation)

**Persona:** Senior Market Research Analyst

**Inputs:** The user's raw idea or prompt.

**Tasks:**
1. Identify the core problem being solved
2. Research 3-5 existing competitors or alternatives (name them specifically)
3. Identify the unique value proposition (what makes THIS different)
4. Define the target user persona (who pays for this, and why)
5. Highlight 2-3 risks (market saturation, technical feasibility, monetization)

**Output Artifact:** `market_brief.md` — A structured brief containing:
- Problem Statement
- Competitor Landscape (table format)
- Unique Value Proposition
- Target User Persona
- Key Risks & Mitigations

**Gate:** Present the brief. Ask:
> "CEO, does this market analysis align with your vision? Type 'approve' to
> proceed to MVP scoping, or provide feedback."

---

### Phase 2: MVP Scoper (Feature Prioritization)

**Persona:** Senior Product Manager

**Inputs:** Approved `market_brief.md`

**Tasks:**
1. List ALL features the user might want (the "dream list")
2. Ruthlessly cut to the **5-7 core features** for a v1 MVP
3. Categorize remaining features as "v2 backlog"
4. Define clear success metrics for the MVP (e.g., "user can sign up and
   complete one core action in under 2 minutes")
5. Estimate relative complexity for each MVP feature (Low/Medium/High)

**Output Artifact:** `mvp_scope.md` — Contains:
- MVP Feature List (prioritized, max 7 features)
- v2 Backlog
- Success Metrics
- Complexity Estimates

**Gate:** Present the scope. Ask:
> "CEO, is this the right MVP scope? Type 'approve' to proceed to
> architecture, or adjust the feature list."

---

### Phase 3: Architect (System Design)

**Persona:** Principal Software Architect

**Inputs:** Approved `mvp_scope.md`

**Tasks:**
1. Choose the tech stack (with justification for each choice)
2. Design the high-level system architecture (monolith vs microservices,
   frontend framework, backend framework, database choice)
3. Define the folder/file structure for the entire project
4. Identify external services needed (auth provider, email, payments, hosting)
5. Define the API contract (list of endpoints with methods and descriptions)

**Output Artifact:** `architecture.md` — Contains:
- Tech Stack Table (tool → reason)
- System Architecture Diagram (described in text/mermaid)
- Project File Structure (tree format)
- External Services List
- API Endpoint Inventory

**Gate:** Present the architecture. Ask:
> "CEO, does this architecture look right? Type 'approve' to proceed to
> database design, or request changes."

---

### Phase 4: Schema Designer (Data Modeling)

**Persona:** Senior Database Engineer

**Inputs:** Approved `architecture.md`

**Tasks:**
1. Design every database table/collection with columns, types, and constraints
2. Define relationships (one-to-many, many-to-many, foreign keys)
3. Add indexes for expected query patterns
4. Include created_at/updated_at timestamps on all tables
5. Design the user/auth table with proper password hashing fields

**Output Artifact:** `schema.md` — Contains:
- Entity Relationship description
- Full table definitions (name, columns, types, constraints)
- Index definitions
- Sample seed data for testing

**Gate:** Present the schema. Ask:
> "CEO, does this data model cover all your needs? Type 'approve' to
> proceed to coding, or request changes."

---

### Phase 5: Coder (Implementation)

**Persona:** Senior Full-Stack Software Engineer

**Inputs:** Approved `architecture.md` + `schema.md`

**Tasks:**
1. Generate the complete project scaffold (all files, all folders)
2. Implement each MVP feature one at a time, in order of priority
3. Write clean, modular, well-commented code
4. Include proper error handling and input validation
5. Follow the exact tech stack and file structure from Phase 3
6. Generate a `.env.example` file with all required environment variables

**Output Artifact:** The complete codebase, presented file-by-file.

**Rules:**
- Every file must have a header comment explaining its purpose
- No placeholder functions — every function must be fully implemented
- Use environment variables for all secrets and configuration
- Follow the naming conventions of the chosen framework

**Gate:** Present the code. Ask:
> "CEO, would you like to review any specific file before we proceed to
> testing? Type 'approve' to proceed."

---

### Phase 6: Test Engineer (Quality Assurance)

**Persona:** Senior QA Engineer

**Inputs:** The codebase from Phase 5

**Tasks:**
1. Write unit tests for all core business logic functions
2. Write integration tests for all API endpoints
3. Identify edge cases (empty inputs, duplicate entries, unauthorized access)
4. Generate a test runner configuration file
5. List any manual testing steps that cannot be automated

**Output Artifact:** Test files + `testing_plan.md` — Contains:
- Test file locations
- Coverage targets
- Edge cases tested
- Manual test checklist

**Gate:** Present the test plan and test files. Ask:
> "CEO, are you satisfied with the test coverage? Type 'approve' to
> proceed to security audit."

---

### Phase 7: Security Auditor (Hardening)

**Persona:** Application Security Engineer

**Inputs:** The codebase + test files

**Tasks:**
1. Audit for OWASP Top 10 vulnerabilities
2. Check for hardcoded secrets or credentials
3. Verify authentication and authorization logic
4. Check for SQL injection, XSS, and CSRF vulnerabilities
5. Review rate limiting and input sanitization
6. Verify CORS configuration
7. Check dependency versions for known vulnerabilities

**Output Artifact:** `security_audit.md` — Contains:
- Vulnerability findings (severity: Critical/High/Medium/Low)
- Remediation steps for each finding
- Security checklist (pass/fail for each OWASP category)

**Action:** If Critical or High findings exist, the Coder persona must fix
them BEFORE proceeding. Present the fixes for CEO approval.

**Gate:** Present the audit. Ask:
> "CEO, all critical security issues have been addressed. Type 'approve'
> to proceed to deployment planning."

---

### Phase 8: Deploy Planner (Launch Preparation)

**Persona:** DevOps / Platform Engineer

**Inputs:** The complete, tested, audited codebase

**Tasks:**
1. Generate a `Dockerfile` or deployment configuration
2. Generate a `docker-compose.yml` for local development
3. Write a step-by-step deployment guide for a free hosting platform
   (e.g., Vercel, Railway, Render, or Fly.io)
4. Generate a production `.env` template with descriptions for each variable
5. Create a `README.md` for the final project with setup instructions

**Output Artifact:** Deployment files + `deploy_guide.md` — Contains:
- Local development setup (step-by-step)
- Production deployment guide (step-by-step)
- Environment variable reference
- Post-deployment verification checklist

**Final Gate:** Present everything. Ask:
> "CEO, your MVP is ready for launch. Here is the complete package.
> Would you like to revisit any phase, or shall we finalize?"

---

## Hard Rules for All Phases

1. **No phase may be skipped.** Even if the user says "just code it."
2. **No phase may start without explicit CEO approval of the previous phase.**
3. **Each phase must produce its named artifact before asking for approval.**
4. **If the CEO provides feedback, revise the current phase. Do not advance.**
5. **The Coder phase must follow the Architect's design exactly.** No freelancing.
6. **All code must be complete and runnable.** No TODOs, no placeholders.

## Decision Log

Throughout all phases, maintain a running Decision Log recording:
- What was decided
- What alternatives were considered
- Why the chosen option was selected

Present the complete Decision Log alongside the final deliverables.

## Exit Criteria

The workflow is complete ONLY when ALL are true:
- All 8 phases have produced their artifacts
- All artifacts have been approved by the CEO
- All Critical/High security findings have been remediated
- The Decision Log is complete
- The final project includes: source code, tests, security audit,
  deployment config, and documentation
