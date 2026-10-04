---
name: launch-checklist
description: "Generate launch readiness checklists for product releases. Covers engineering, QA, design, legal, marketing, support, and rollback planning. Adapts to launch size (feature flag, beta, GA) and AI/ML-specific requirements."
argument-hint: "[feature or product being launched]"
---

# Launch Checklist Skill

Generate a comprehensive, customized launch readiness checklist for any product release.

## When to Use
- User is preparing to launch a feature or product
- User needs to ensure nothing is missed before go-live
- User says `/launch-checklist` followed by what they're launching
- Any pre-launch review or go/no-go decision

## Framework: Launch Readiness Checklist

### Step 1: Scope the Launch
- **What's launching?** Feature name and brief description
- **Launch type**: Feature flag → Internal → Beta → GA
- **Target date**: When is this going live?
- **Blast radius**: How many users are affected?
- **Reversibility**: Can we roll back easily?

### Step 2: Generate Checklist by Function

#### Engineering
- [ ] Code complete and merged to release branch
- [ ] Unit tests passing (coverage threshold met)
- [ ] Integration tests passing
- [ ] Load/performance testing complete (meets latency/throughput targets)
- [ ] Feature flag configured and tested (on/off/gradual rollout)
- [ ] Database migrations tested and reversible
- [ ] API versioning handled (no breaking changes for existing clients)
- [ ] Monitoring and alerting configured
- [ ] Logging sufficient for debugging
- [ ] Rollback procedure documented and tested

#### QA
- [ ] Test plan executed (happy path, edge cases, error states)
- [ ] Cross-browser/cross-platform testing complete
- [ ] Accessibility testing (screen reader, keyboard nav, contrast)
- [ ] Regression testing on adjacent features
- [ ] Security review complete (auth, input validation, data handling)

#### Design
- [ ] Final designs match implementation
- [ ] Empty states, loading states, error states all designed
- [ ] Mobile/responsive behavior verified
- [ ] Copy reviewed and finalized
- [ ] Animations/transitions smooth and performant

#### Legal & Compliance
- [ ] Privacy review complete (data collection, retention, deletion)
- [ ] Terms of service updated if needed
- [ ] GDPR/CCPA compliance verified
- [ ] Licensing for any third-party components cleared

#### Marketing & Communications
- [ ] Launch announcement drafted
- [ ] Help center / documentation updated
- [ ] In-app messaging configured (tooltips, onboarding)
- [ ] Social media / blog post scheduled (if applicable)
- [ ] Internal comms sent to stakeholders

#### Support
- [ ] Support team briefed on new feature
- [ ] FAQ and troubleshooting guide prepared
- [ ] Escalation path defined for launch-related issues
- [ ] Known limitations documented

#### AI/ML-Specific (if applicable)
- [ ] Model eval results meet quality bar
- [ ] Safety/red-team testing complete
- [ ] Content policy and guardrails configured
- [ ] Hallucination rate within acceptable threshold
- [ ] Cost per query within budget
- [ ] Fallback behavior for model errors/timeouts
- [ ] Data pipeline monitoring active
- [ ] Bias testing on key demographic segments

### Step 3: Go/No-Go Criteria

Define clear criteria for each launch stage:

**Internal Launch Go/No-Go:**
- All P0 bugs resolved
- Core user flow works end-to-end
- Monitoring active

**Beta Launch Go/No-Go:**
- All P0 and P1 bugs resolved
- Performance meets targets
- Support team briefed
- Rollback tested

**GA Launch Go/No-Go:**
- All P0-P2 bugs resolved
- Load testing passed at 2x expected traffic
- Documentation complete
- Legal review signed off
- Monitoring and alerting verified

### Step 4: Rollback Plan
- **Trigger criteria**: What signals would trigger a rollback?
- **Rollback steps**: Exact steps to revert (feature flag off, DB rollback, etc.)
- **Communication**: Who to notify and how
- **Timeline**: Maximum time from decision to rollback complete

## Output Format
Generate as a markdown checklist grouped by function. Mark items as applicable/not applicable based on the specific launch. Include a summary section with launch date, owner, and go/no-go criteria.
