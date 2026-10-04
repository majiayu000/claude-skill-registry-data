---
name: adic-pipeline
description: Automated SDLC pipeline executing Requirements → Architecture → Design → Implementation → Code Review → QA → Security → Deployment. Reduces one feature from 40h to 8h manual effort.
allowed-tools: All (orchestrates entire workflow)
---

# ADIC Pipeline: Automated SDLC

Runs complete sprint cycle from requirements extraction to production deployment. Designed for one-week hackathon timeline.

**ADIC** = **A**rchitecture → **D**esign → **I**mplementation → **C**ode Review (+ Requirements, QA, Security, Deployment)

---

## Trigger Phrases

Auto-invokes when detecting:
- "run SDLC"
- "full sprint"
- "adic pipeline"
- "automate feature"
- "/adic-pipeline"
- "build end-to-end"

---

## Pipeline Overview

| Stage | Duration | Agent | Output | Blocking |
|-------|----------|-------|--------|----------|
| 1. Requirements | 5 min | Architect | requirements.md | Yes |
| 2. Architecture | 10 min | Orchestrator | ARCHITECTURE.md update | Yes |
| 3. Design | 10 min | Orchestrator | design-contract.md | Yes |
| 4. Implementation | 45 min | Orchestrator | Code + Tests | Yes |
| 5. Code Review | 15 min | Reviewer | verification-report.md | Yes |
| 6. QA | 10 min | Orchestrator | test-results.json | Yes |
| 7. Security Scan | 5 min | Security Hook | security-report.md | Yes |
| 8. Deployment | 10 min | DevOps | deployment-log.txt | Yes |

**Total:** ~2 hours per feature → **3-4 features per week**

---

## Execution Steps

### Stage 1: Requirements (Reverse Prompting)

**Agent:** Architect agent
**Duration:** 5 minutes
**Purpose:** Extract clear requirements before implementation

**Process:**
1. Architect agent reads user's feature request
2. Asks 5 clarifying questions (reverse prompting pattern):
   - What is the expected input/output?
   - What are the acceptance criteria?
   - What are the edge cases?
   - What are the dependencies?
   - What are the constraints (performance, security)?
3. Wait for user responses
4. Generate `requirements.md`

**Output:** `active/adic-pipeline/<feature-name>/requirements.md`

**Example:**
```markdown
# Feature: OfferBrief Generation UI

## Objective
Build React component for marketers to enter business objectives and generate OfferBriefs.

## Clarifying Q&A

**Q1:** What is the expected input format?
**A1:** Natural language text (10-500 chars), e.g., "Reactivate lapsed high-value members"

**Q2:** What are the acceptance criteria?
**A2:**
- Validates input length (10-500 chars)
- Calls Claude API to generate OfferBrief
- Displays risk flags with color coding
- Shows loading state during generation

**Q3:** What are the edge cases?
**A3:**
- Empty input → Show validation error
- Claude API failure → Show error toast, retry button
- Network timeout → 30s timeout, show error

**Q4:** Dependencies?
**A4:**
- Claude API client (src/services/api.ts)
- OfferBrief types (src/shared/types/offer-brief.ts)
- Fraud detection skill (runs after generation)

**Q5:** Constraints?
**A5:**
- <2s p95 response time
- Accessible (keyboard navigation, ARIA labels)
- Mobile responsive
```

**Failure handling:** If user provides unclear answers, ask follow-up questions (max 2 rounds).

---

### Stage 2: Architecture (Update Diagrams)

**Agent:** Orchestrator (Claude Code)
**Duration:** 10 minutes
**Purpose:** Update ARCHITECTURE.md with new component/flow

**Process:**
1. Read current `docs/ARCHITECTURE.md`
2. Identify which diagram(s) need updates (e.g., Component Architecture, End-to-End Flow)
3. Update Mermaid diagrams to reflect new feature
4. Verify diagram syntax (test with Mermaid CLI if available)

**Output:** Updated `docs/ARCHITECTURE.md`

**Example change:**
```diff
# Component Architecture

graph LR
    subgraph Frontend
        A[React 19 App]
        A --> B[Designer UI]
+       B --> B1[OfferBriefForm]
+       B --> B2[RiskFlagDisplay]
        A --> C[Scout UI]
    end
```

---

### Stage 3: Design (Prompt Contract)

**Agent:** Orchestrator
**Duration:** 10 minutes
**Purpose:** Define explicit contract before implementation

**Process:**
1. Read requirements.md
2. Create design-contract.md with 4 sections:
   - **GOAL:** Quantifiable success metric
   - **CONSTRAINTS:** Hard limits & boundaries
   - **FORMAT:** Exact output shape
   - **FAILURE:** Explicit failure conditions

**Output:** `active/adic-pipeline/<feature-name>/design-contract.md`

**Example:**
```markdown
# Design Contract: OfferBriefForm Component

## GOAL
Build a React component that allows marketers to generate OfferBriefs with <2s p95 latency and >95% success rate.

## CONSTRAINTS
- Input: 10-500 characters (validate client-side)
- API timeout: 30 seconds max
- No PII logging (objective text only)
- Accessible: WCAG 2.1 AA compliant
- Mobile: Responsive down to 320px width

## FORMAT
### Component API
```typescript
interface OfferBriefFormProps {
  onSubmit: (objective: string) => Promise<OfferBrief>;
  onError: (error: Error) => void;
}
```

### Output
- Success: OfferBrief object with offer_id, segment, construct, kpis, risk_flags
- Error: Error object with message, code, retry function

## FAILURE
Reject implementation if ANY of:
- Response time >2s p95 (test with 10 concurrent requests)
- Missing validation (empty input, <10 chars, >500 chars)
- No loading state (user sees frozen UI during API call)
- No error handling (API failure causes component crash)
- Accessibility violations (missing ARIA labels, keyboard nav broken)
- Not mobile responsive (breaks on <768px width)
```

---

### Stage 4: Implementation

**Agent:** Orchestrator
**Duration:** 45 minutes
**Purpose:** Write code (frontend + backend + tests)

**Process:**
1. Read design-contract.md
2. Implement feature following contract
3. Write unit tests (>80% coverage)
4. Run tests locally to verify
5. Commit code

**Output:** Working code in `src/` + tests in `tests/`

**Files created (example):**
- `src/frontend/components/Designer/OfferBriefForm.tsx`
- `src/frontend/components/Designer/OfferBriefForm.test.tsx`
- `src/backend/api/designer.py` (if new endpoint)
- `tests/unit/backend/test_designer.py`

**Quality checks during implementation:**
- TypeScript strict mode (no 'any' types)
- ESLint passes
- Pytest passes
- Coverage >80%

---

### Stage 5: Code Review (Verification Loops)

**Agent:** Reviewer subagent (fresh context)
**Duration:** 15 minutes
**Purpose:** Catch mistakes implementer missed

**Process:**
1. Spawn reviewer subagent with ZERO context from implementation
2. Reviewer reads:
   - design-contract.md
   - Implemented code
   - Test results
3. Reviewer checks for:
   - Contract compliance (GOAL, CONSTRAINTS, FORMAT, FAILURE)
   - Code quality (readability, maintainability)
   - Edge cases (error handling, validation)
   - Security issues (input sanitization, PII logging)
   - Performance (unnecessary re-renders, N+1 queries)
4. Reviewer outputs verification-report.md

**Output:** `active/adic-pipeline/<feature-name>/verification-report.md`

**Example:**
```markdown
# Verification Report: OfferBriefForm

## Contract Compliance

### GOAL: <2s p95 latency ✅
- Tested with 10 concurrent requests: p95 = 1.8s

### CONSTRAINTS: Input validation ✅
- Client-side validation for 10-500 chars
- Displays error message for invalid input

### FORMAT: Component API ✅
- Props match TypeScript interface
- Returns OfferBrief on success, Error on failure

### FAILURE: No accessibility violations ✅
- ARIA labels present
- Keyboard navigation works

## Issues Found

### Issue 1: Missing loading state (SEVERITY: HIGH)
**Location:** OfferBriefForm.tsx:45
**Problem:** No loading indicator during API call
**Fix:** Add `useFormStatus()` hook and conditional button text

### Issue 2: Unhandled network timeout (SEVERITY: MEDIUM)
**Location:** api.ts:23
**Problem:** No timeout on fetch() call
**Fix:** Add `signal` with AbortController, 30s timeout

## Recommendation
**BLOCK MERGE** until Issue #1 (high severity) is fixed.
```

**Failure handling:**
- High severity issues: Block merge, implementer fixes, re-run review
- Medium/low severity: Allow merge with tracking issue

---

### Stage 6: QA (Automated Tests)

**Agent:** Orchestrator
**Duration:** 10 minutes
**Purpose:** Run full test suite (unit + integration + E2E)

**Process:**
1. Run unit tests: `npm test` (frontend), `pytest` (backend)
2. Run integration tests: `pytest -m integration`
3. Run E2E tests (critical paths only): `npm run test:e2e`
4. Generate coverage report
5. Output test-results.json

**Output:** `active/adic-pipeline/<feature-name>/test-results.json`

**Example:**
```json
{
  "timestamp": "2026-03-26T14:30:00Z",
  "test_suites": {
    "unit_frontend": {
      "total": 25,
      "passed": 25,
      "failed": 0,
      "skipped": 0,
      "coverage": 87.5
    },
    "unit_backend": {
      "total": 18,
      "passed": 18,
      "failed": 0,
      "skipped": 0,
      "coverage": 92.3
    },
    "integration": {
      "total": 8,
      "passed": 8,
      "failed": 0,
      "skipped": 0
    },
    "e2e": {
      "total": 3,
      "passed": 3,
      "failed": 0,
      "skipped": 0
    }
  },
  "overall_status": "PASS",
  "coverage_total": 89.2
}
```

**Failure handling:**
- Any test failure: Block merge, show failing test output, fix and re-run

---

### Stage 7: Security Scan (Pre-Deployment)

**Agent:** Security hook (bash script)
**Duration:** 5 minutes
**Purpose:** Catch vulnerabilities before deployment

**Process:**
1. Run `bash scripts/security-scan.sh`
2. Check for:
   - Hardcoded secrets (API keys, passwords)
   - Vulnerable dependencies (npm audit, pip-audit)
   - .env files in git
3. Output security-report.md

**Output:** `active/adic-pipeline/<feature-name>/security-report.md`

**Example:**
```markdown
# Security Scan Report

## Secrets Check ✅
No hardcoded secrets detected

## Dependency Vulnerabilities ✅
- Frontend: 0 vulnerabilities (npm audit)
- Backend: 0 vulnerabilities (pip-audit)

## .env Files ✅
No .env files in git

## Overall Status: PASS
```

**Failure handling:**
- Critical vulnerabilities: Block deployment, escalate to user
- High vulnerabilities: Require fix before deploy
- Medium/low vulnerabilities: Log warning, allow deploy

---

### Stage 8: Deployment (DevOps Agent)

**Agent:** DevOps agent
**Duration:** 10 minutes
**Purpose:** Deploy to Azure staging environment

**Process:**
1. DevOps agent reads deployment config
2. Generates Terraform plan
3. Applies infrastructure changes (if needed)
4. Deploys code:
   - Frontend: Azure App Service
   - Backend: Azure Functions
5. Runs smoke tests on staging
6. Output deployment-log.txt

**Output:** `active/adic-pipeline/<feature-name>/deployment-log.txt`

**Example:**
```
[2026-03-26 14:30:00] Starting deployment to Azure staging
[2026-03-26 14:30:05] Building frontend (npm run build)
[2026-03-26 14:31:20] Uploading to Azure App Service
[2026-03-26 14:31:45] Building backend (pip install -r requirements.txt)
[2026-03-26 14:32:00] Deploying to Azure Functions
[2026-03-26 14:32:30] Running smoke tests
[2026-03-26 14:33:00] Smoke tests passed
[2026-03-26 14:33:05] Deployment complete
[2026-03-26 14:33:05] Staging URL: https://tristar-staging.azurewebsites.net
```

**Failure handling:**
- Deployment failure: Rollback to previous version, notify user
- Smoke test failure: Rollback, show test output

---

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `skip_stages` | none | Comma-separated stages to skip (e.g., "6,7" skips QA+Security) |
| `auto_deploy` | false | Auto-deploy to staging without user approval |
| `verification_rounds` | 1 | Number of code review loops before merge |
| `timeout_minutes` | 120 | Max total pipeline duration |

**Usage:**
```bash
# Skip security scan (for demo)
claude-code --skill adic-pipeline "Build Designer UI" --skip-stages=7

# Auto-deploy without approval
claude-code --skill adic-pipeline "Build Scout activation" --auto-deploy=true
```

---

## Output Files

All pipeline artifacts saved to `active/adic-pipeline/<feature-name>/`:
```
active/adic-pipeline/designer-ui/
├── requirements.md
├── design-contract.md
├── verification-report.md
├── test-results.json
├── security-report.md
├── deployment-log.txt
└── pipeline-summary.json
```

**pipeline-summary.json:**
```json
{
  "feature": "designer-ui",
  "started_at": "2026-03-26T12:00:00Z",
  "completed_at": "2026-03-26T14:00:00Z",
  "duration_minutes": 120,
  "stages": {
    "requirements": "completed",
    "architecture": "completed",
    "design": "completed",
    "implementation": "completed",
    "code_review": "completed",
    "qa": "completed",
    "security": "completed",
    "deployment": "completed"
  },
  "status": "SUCCESS",
  "staging_url": "https://tristar-staging.azurewebsites.net"
}
```

---

## Failure Handling

### Stage 1-3 Failures (Requirements, Architecture, Design)
**Action:** Ask user for clarification, retry
**Example:** "Requirements unclear: Which API should generate offers—Claude or custom model?"

### Stage 4 Failure (Implementation)
**Action:** Rollback to last working state, retry with refined contract
**Example:** Implementation exceeds 2s latency → Refine design contract to use caching

### Stage 5-6 Failures (Code Review, QA)
**Action:** Fix issues, re-run verification loop
**Example:** Code review finds missing error handling → Add try/catch, re-run review

### Stage 7 Failure (Security)
**Action:** Block deployment, escalate to user
**Example:** Hardcoded API key found → Remove secret, add to .env, re-run scan

### Stage 8 Failure (Deployment)
**Action:** Rollback deployment, notify user
**Example:** Azure Functions deployment fails → Rollback to previous version, show error log

---

## Monitoring & Alerts

### Pipeline Metrics
- **Success rate:** % of pipelines that complete without failure
- **Average duration:** Mean time from start to deployment
- **Stage bottlenecks:** Which stages take longest (optimize first)
- **Failure rate by stage:** Where do failures occur most often

### Alerts
- **Pipeline exceeds 2h:** Investigate slow stages
- **>3 verification loops:** Design contract may be ambiguous
- **Security failures >2x/day:** Review code review process

---

## Best Practices

1. **Run pipeline early** (don't wait until feature is "done")
2. **Review design contract carefully** (saves implementation time)
3. **Don't skip security scan** (even for demos)
4. **Use auto-deploy for hackathons** (speed over safety)
5. **Archive pipeline artifacts** (audit trail + learning)

---

## Integration Example

```bash
# Full pipeline for Designer UI
claude-code --skill adic-pipeline "Build OfferBriefForm component"

# Pipeline output:
# Stage 1/8: Requirements (5 min) ✅
# Stage 2/8: Architecture (10 min) ✅
# Stage 3/8: Design (10 min) ✅
# Stage 4/8: Implementation (45 min) ✅
# Stage 5/8: Code Review (15 min) ✅
# Stage 6/8: QA (10 min) ✅
# Stage 7/8: Security (5 min) ✅
# Stage 8/8: Deployment (10 min) ✅
#
# ✅ Pipeline complete! Staging URL: https://tristar-staging.azurewebsites.net
```

---

**Last Updated:** 2026-03-26
**Version:** 1.0
**Owner:** TriStar Hackathon Team