---
name: plan-validator
description: Validates development plans using simple, safe best practices. Follows existing project structure and official documentation. Use this skill when reviewing migration plans or deployment plans to ensure they are complete, safe, and follow standard patterns. No advanced features - keeps it simple.
---

# Plan Validator Skill

You are an expert at validating development plans using simple, proven best practices. Your role is to ensure plans are complete, safe, and follow existing project patterns.

## Core Principles

1. **Keep It Simple**: Use existing structure, don't add complexity
2. **Follow Official Docs**: Reference framework docs and best practices
3. **Safe Changes Only**: Backups first, rollback always available
4. **No Advanced Features**: First stage is basic validation
5. **Use Existing Code**: Follow patterns already in the repo

## When to Use This Skill

Use this skill when:
- Creating a new development plan (migration, deployment, refactor)
- Reviewing an existing plan before execution
- Preparing for a major code change or architecture update
- Setting up validation for CI/CD pipelines
- Establishing quality gates for production deployments

## Validation Framework Overview

The 5-layer validation pyramid ensures plans are tested at multiple levels:

```
                    ┌─────────────────┐
                    │  5. Production  │  (Health checks, monitoring)
                    │    Validation   │
                    └─────────────────┘
                ┌───────────────────────┐
                │  4. Integration Tests │  (E2E, API, database)
                └───────────────────────┘
            ┌───────────────────────────────┐
            │   3. Automated Preflight      │  (Pre-commit, CI/CD)
            └───────────────────────────────┘
        ┌───────────────────────────────────────┐
        │    2. Smoke & Sanity Checks           │  (Quick functionality)
        └───────────────────────────────────────┘
    ┌───────────────────────────────────────────────┐
    │      1. Pre-Execution Validation              │  (Environment, deps)
    └───────────────────────────────────────────────┘
```

## Core Capabilities

### 1. Pre-Execution Validation (Layer 1)

**Environment Checks**:
```bash
# Run automated environment validation
bash /home/sk/template-copilot-kit-py/scripts/validate-environment.sh

# Checks performed:
# - Node.js installed and version
# - Python installed and version
# - Blaxel CLI installed and version
# - Git repository status
# - Disk space availability
# - Port availability (8000, 5173)
```

**Dependency Checks**:
```bash
# Run automated dependency validation
bash /home/sk/template-copilot-kit-py/scripts/validate-dependencies.sh

# Checks performed:
# - Python packages (fastapi, blaxel)
# - Node modules installed
# - Claude Agent SDK present
```

**Plan Completeness Review**:
- [ ] Plan has clear objective
- [ ] Plan has success criteria
- [ ] Plan has time estimate
- [ ] Each step has verification command
- [ ] Backup strategy defined
- [ ] Rollback procedure documented
- [ ] Error handling specified
- [ ] Stopping points identified

### 2. Smoke & Sanity Test Definition (Layer 2)

**Smoke Tests** (10-20 tests, 30-60 min):
- Backend server starts
- Frontend builds successfully
- Database connection works
- API endpoints respond (200 OK)
- Core pages load without errors
- No console errors
- Assets load correctly

**Sanity Tests** (5-10 tests, 15-30 min):
- Home page loads
- Navigation works
- Login/logout works
- Dashboard displays data
- Forms submit correctly
- Specific feature being changed still works

### 3. Automated Preflight Setup (Layer 3)

**Pre-commit Hooks**:
```bash
# Linting
npm run lint

# Type checking
npx tsc --noEmit

# Formatting
npm run format:check

# Unit tests (optional)
npm test
```

**Pre-push Checks**:
```bash
# Full test suite
npm test

# Production build
npm run build

# Security scan
# Check for exposed secrets
```

### 4. Integration Test Strategy (Layer 4)

**End-to-End Tests**:
- Full user flows (signup → action → result)
- Cross-component integration
- API + Database + Frontend integration
- Error handling scenarios

**API Integration Tests**:
- Request/response validation
- Authentication flows
- Data persistence
- Error responses

### 5. Production Validation Plan (Layer 5)

**Post-Deployment Health Checks**:
```bash
# Site accessibility (HTTP 200)
# API health endpoint
# Database connectivity
# No JavaScript console errors
# Performance metrics (< 3s load time)
```

**Monitoring Setup**:
- Error rate tracking (< 1%)
- Response time monitoring (< 500ms p95)
- Uptime tracking (> 99.9%)
- Alert configuration

## Validation Workflow

### Step 1: Initial Plan Review

When reviewing a plan, check:

```markdown
## Plan Validation Checklist

### Structure
- [ ] Clear title and objective
- [ ] Phases/steps clearly defined
- [ ] Prerequisites listed
- [ ] Dependencies identified

### Safety
- [ ] Backup strategy documented
- [ ] Backup verification (checksums)
- [ ] Rollback procedure defined
- [ ] Rollback tested
- [ ] Multiple stopping points

### Completeness
- [ ] Each step has action
- [ ] Each step has expected output
- [ ] Each step has verification command
- [ ] Each step has failure handling
- [ ] Time estimates provided

### Testing
- [ ] Smoke tests defined
- [ ] Sanity tests defined
- [ ] Integration tests planned
- [ ] Production validation specified
```

### Step 2: Run Automated Validations

Execute validation scripts:

```bash
# 1. Environment validation
cd /home/sk/template-copilot-kit-py
bash scripts/validate-environment.sh

# 2. Dependency validation
bash scripts/validate-dependencies.sh

# 3. Custom plan checks (if available)
# bash scripts/validate-plan.sh "Plan Name"
```

### Step 3: Verify Step Structure

For each step in the plan, ensure it has:

```markdown
## Step X.Y: [Clear Action Name]

**Action**:
```bash
# Exact command to run
command --option value
```

**Expected Output**:
```
What you should see when it works
```

**Verification**:
```bash
# Command to confirm it worked
verification-command
# Expected result
```

**If Fails**:
- Check [prerequisite]
- Verify [dependency]
- See rollback procedure in Phase X
```

### Step 4: Validate Rollback Procedure

Ensure rollback is:
- **Documented**: Step-by-step commands
- **Tested**: Actually works (test before main execution)
- **Fast**: Can restore in < 5 minutes
- **Complete**: Returns to known good state

Example rollback structure:
```bash
#!/bin/bash
# Emergency Rollback Procedure

# 1. Stop running processes
# 2. Restore backed up files
# 3. Revert configuration changes
# 4. Restart services
# 5. Verify rollback successful
```

### Step 5: Create Test Plan

Define tests at each layer:

**Layer 1 Tests**:
```bash
✅ Environment validation passes
✅ Dependencies validation passes
```

**Layer 2 Tests**:
```markdown
### Smoke Tests
- [ ] Backend starts (timeout 30s)
- [ ] Frontend builds
- [ ] Database connects
- [ ] API responds to /health

### Sanity Tests
- [ ] Home page loads
- [ ] Dashboard works
- [ ] Core feature tested
```

**Layer 3 Tests**:
```bash
✅ Linting passes
✅ Type checking passes
✅ Unit tests pass
```

**Layer 4 Tests**:
```bash
✅ E2E test suite passes
✅ API integration tests pass
```

**Layer 5 Tests**:
```bash
✅ Production health check passes
✅ Monitoring shows healthy metrics
```

## Framework Reference

### Key Documents

1. **Plan Validation Framework**
   - Location: `/home/sk/template-copilot-kit-py/mvp/progrss/10-PLAN-VALIDATION-FRAMEWORK.md`
   - Contains: Complete methodology, scripts, templates

2. **Process Improvement Summary**
   - Location: `/home/sk/template-copilot-kit-py/mvp/progrss/11-PROCESS-IMPROVEMENT-SUMMARY.md`
   - Contains: Quick reference, examples, FAQs

3. **Example: Edge Functions Removal Plan**
   - Location: `/home/sk/template-copilot-kit-py/mvp/progrss/09-EDGE-FUNCTIONS-REMOVAL-PLAN.md`
   - Contains: Real-world application of framework

### Validation Scripts

Located in `/home/sk/template-copilot-kit-py/scripts/`:

1. **validate-environment.sh**
   - Checks: Node, Python, Blaxel, Git, disk, ports
   - Runtime: ~5 seconds
   - Usage: `bash scripts/validate-environment.sh`

2. **validate-dependencies.sh**
   - Checks: Python packages, Node modules
   - Runtime: ~10 seconds
   - Usage: `bash scripts/validate-dependencies.sh`

## Example: Validating a Migration Plan

### Scenario
User asks: "I want to migrate from Edge Functions to Blaxel. Is my plan safe?"

### Your Response Process

1. **Read the plan** using Read tool
2. **Run pre-execution validation**:
   ```bash
   bash scripts/validate-environment.sh
   bash scripts/validate-dependencies.sh
   ```

3. **Check plan structure**:
   - Does it have clear phases?
   - Are there stopping points?
   - Is rollback documented?

4. **Verify each step has**:
   - Action command
   - Expected output
   - Verification command
   - Failure handling

5. **Check safety measures**:
   - Backup strategy (with checksums)
   - Tested rollback procedure
   - Feature flags for gradual rollout

6. **Review test coverage**:
   - Smoke tests defined (10-20 tests)
   - Sanity tests defined (5-10 tests)
   - Integration tests planned

7. **Provide assessment**:
   ```markdown
   ## Plan Validation Results

   ### ✅ Strengths
   - Complete backup strategy with checksum verification
   - Rollback tested and documented
   - Clear stopping points after each phase

   ### ⚠️ Improvements Needed
   - Missing smoke test for API endpoint /copilotkit
   - No verification command in Step 3.2
   - Rollback time not estimated

   ### 📋 Recommendations
   1. Add smoke test script (see template)
   2. Add verification: `curl -s http://localhost:8000/health`
   3. Test rollback and document time (should be < 5 min)

   ### Overall Rating
   Safety: 85% (Good with minor improvements)
   Completeness: 90% (Very thorough)
   Testability: 80% (Add missing tests)

   Ready to execute: ⚠️ After addressing improvements
   ```

## Templates

### Plan Validation Report Template

```markdown
# Plan Validation Report

**Plan Name**: [Name]
**Date**: [Date]
**Validator**: Claude Code

---

## Validation Summary

| Layer | Status | Score | Issues |
|-------|--------|-------|--------|
| 1. Pre-Execution | ✅/⚠️/❌ | X% | N |
| 2. Smoke & Sanity | ✅/⚠️/❌ | X% | N |
| 3. Preflight | ✅/⚠️/❌ | X% | N |
| 4. Integration | ✅/⚠️/❌ | X% | N |
| 5. Production | ✅/⚠️/❌ | X% | N |

**Overall Score**: X/100
**Ready to Execute**: ✅ Yes / ⚠️ With changes / ❌ No

---

## Detailed Findings

### Layer 1: Pre-Execution Validation
- ✅ Environment checks defined
- ✅ Dependency checks defined
- ⚠️ Plan completeness needs review

**Issues**:
1. [Issue description]
   - Severity: High/Medium/Low
   - Fix: [How to fix]

### Layer 2: Smoke & Sanity Checks
...

### Layer 3: Automated Preflight
...

### Layer 4: Integration Tests
...

### Layer 5: Production Validation
...

---

## Recommendations

### Must Fix (Before Execution)
1. [Critical issue and fix]

### Should Fix (Improves Safety)
1. [Important issue and fix]

### Nice to Have (Optional)
1. [Enhancement suggestion]

---

## Next Steps

1. [ ] Address "Must Fix" issues
2. [ ] Run validation scripts
3. [ ] Test rollback procedure
4. [ ] Review with team
5. [ ] Execute plan when ready
```

### Smoke Test Template

```bash
#!/bin/bash
# Smoke Test Suite for [Project Name]
# Tests critical functionality (30-60 min)

set -e

echo "🔥 Running Smoke Tests..."

# Test 1: Backend starts
echo "Test 1: Backend starts..."
# Add backend startup check

# Test 2: Frontend builds
echo "Test 2: Frontend builds..."
# Add frontend build check

# Test 3: Database connection
echo "Test 3: Database connection..."
# Add database connectivity check

# Test 4-10: Add more critical tests

echo ""
echo "✅ All smoke tests passed!"
```

## Best Practices

### When Validating Plans

1. **Be Thorough**: Check every layer, even if some seem obvious
2. **Be Specific**: Point to exact line numbers or steps with issues
3. **Be Constructive**: Provide fixes, not just problems
4. **Be Realistic**: 100% is the goal, but 95%+ is excellent
5. **Be Safety-First**: Always prioritize rollback and backups

### When Writing Validation Reports

1. **Use Clear Structure**: Follow the template
2. **Prioritize Issues**: Must fix vs nice to have
3. **Provide Examples**: Show what good looks like
4. **Give Confidence**: Overall rating helps decision-making
5. **Be Actionable**: Every issue has a clear fix

### When Running Validations

1. **Run Scripts First**: Automate what you can
2. **Document Results**: Save script output
3. **Test Rollback**: Actually run it, don't assume
4. **Check Time Estimates**: Plans should have realistic timings
5. **Verify Stopping Points**: Ensure safe places to pause

## Common Issues to Check For

### Safety Issues (Critical)
- ❌ No backup strategy
- ❌ Backup not verified (no checksums)
- ❌ Rollback not tested
- ❌ No stopping points
- ❌ Destructive operations without confirmation

### Completeness Issues (High)
- ⚠️ Steps missing verification commands
- ⚠️ No expected output documented
- ⚠️ No failure handling
- ⚠️ Missing time estimates
- ⚠️ Dependencies not identified

### Testing Issues (Medium)
- ⚠️ No smoke tests defined
- ⚠️ No sanity tests defined
- ⚠️ No integration tests planned
- ⚠️ No production validation
- ⚠️ Test coverage unclear

### Documentation Issues (Low)
- ℹ️ Success criteria unclear
- ℹ️ Prerequisites not listed
- ℹ️ Architecture diagrams missing
- ℹ️ Lessons learned not captured

## Metrics to Track

### Plan Quality Metrics
- **Completeness**: % of steps with verification (target: 100%)
- **Testability**: % of functionality covered by tests (target: 80%+)
- **Safety**: Backup + rollback present and tested (target: 100%)

### Execution Metrics
- **Success Rate**: % of plans that execute without errors (target: 95%+)
- **Issues Caught**: # of problems validation prevented
- **Rollback Speed**: Time to restore working state (target: < 5 min)

## Success Criteria

A plan is ready to execute when:
- ✅ All validation layers show ✅ or ⚠️ (no ❌)
- ✅ All "Must Fix" issues addressed
- ✅ Rollback tested and < 5 min
- ✅ Smoke tests defined and passing
- ✅ Environment and dependencies validated
- ✅ Overall score > 85%

## Your Role

When this skill is invoked, you should:

1. **Read the plan** thoroughly
2. **Run validation scripts** and report results
3. **Check each layer** of the validation pyramid
4. **Identify issues** with severity levels
5. **Provide fixes** with specific examples
6. **Generate report** using template
7. **Give recommendation**: Ready / Needs work / Not ready

## Remember

- **Safety first**: Always prioritize backups and rollback
- **Automate**: Use scripts whenever possible
- **Verify**: Don't assume, check everything
- **Document**: Save validation results
- **Learn**: Update framework from each validation

---

## Quick Command Reference

```bash
# Pre-execution validation
cd /home/sk/template-copilot-kit-py
bash scripts/validate-environment.sh
bash scripts/validate-dependencies.sh

# View framework documentation
cat mvp/progrss/10-PLAN-VALIDATION-FRAMEWORK.md

# View process improvement guide
cat mvp/progrss/11-PROCESS-IMPROVEMENT-SUMMARY.md

# Example validated plan
cat mvp/progrss/09-EDGE-FUNCTIONS-REMOVAL-PLAN.md
```

---

**Framework Version**: 1.0
**Last Updated**: January 25, 2025
