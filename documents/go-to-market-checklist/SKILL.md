---
name: go-to-market-checklist
description: |
  Generate a pre-launch readiness checklist for feature releases. Use this skill when:
  - A feature is nearing completion and you need a launch readiness checklist
  - You want to ensure all pre-launch items are covered (docs, training, support, rollback)
  - You are planning a phased rollout and need a structured go-to-market plan
---

# Go-to-Market Checklist

Generate a comprehensive pre-launch readiness checklist covering documentation, training, support, communication, metrics, and rollback planning.

## Workflow

1. **Read feature spec** from your spec directory
2. **Identify GTM dimensions** from spec (users, channels, metrics, risks)
3. **Generate checklist** with status tracking
4. **Output** — Print to conversation or write file

## Checklist

### Documentation
- [ ] Release notes written
- [ ] User-facing help/FAQ updated
- [ ] Internal knowledge base updated
- [ ] API documentation updated (if applicable)
- [ ] Migration guide written (if breaking changes)

### Training
- [ ] Customer success team briefed
- [ ] Support team trained on new feature
- [ ] Demo video/walkthrough created
- [ ] Sales enablement materials ready (if B2B)

### Support Readiness
- [ ] Known issues documented
- [ ] Escalation path defined
- [ ] FAQ for common questions prepared
- [ ] Support ticket categories created

### Communication
- [ ] Internal announcement drafted
- [ ] Customer communication drafted (if applicable)
- [ ] Stakeholder notification sent
- [ ] Changelog updated

### Metrics & Monitoring
- [ ] Analytics events instrumented
- [ ] Dashboard configured
- [ ] Alerting rules set for error thresholds
- [ ] Baseline metrics captured pre-launch

### Rollback Plan
- [ ] Feature flag configured
- [ ] Rollback procedure documented
- [ ] Data migration rollback tested (if applicable)
- [ ] Go/No-go criteria defined

### Compliance
- [ ] PII audit completed
- [ ] Regulatory review signed off
- [ ] Privacy policy updated (if needed)

## Output Format

```markdown
# Go-to-Market Checklist — {Feature Name}

**Target Launch:** {date}
**Feature Spec:** {path}
**Status:** {Ready / Not Ready — N of M items complete}

{checklist sections above}

## Go/No-Go Summary

| Dimension | Status | Blocker? | Notes |
|-----------|--------|----------|-------|
| Documentation | Ready/Not Ready | Y/N | {detail} |
| Training | Ready/Not Ready | Y/N | |
| Support | Ready/Not Ready | Y/N | |
| Communication | Ready/Not Ready | Y/N | |
| Metrics | Ready/Not Ready | Y/N | |
| Rollback | Ready/Not Ready | Y/N | |
| Compliance | Ready/Not Ready | Y/N | |

**Decision:** GO / NO-GO
**Blockers to resolve:** {list if NO-GO}
```

## Anti-Patterns

- Don't skip the rollback plan — every launch needs a reversal path
- Don't launch without baseline metrics — you can't measure impact without a before
- Don't treat compliance as optional — data privacy is non-negotiable

## Quality Checklist

- [ ] All 7 dimensions covered
- [ ] Go/No-Go summary table present
- [ ] Blockers identified if status is NO-GO
- [ ] Rollback plan is specific, not just "we'll revert"
