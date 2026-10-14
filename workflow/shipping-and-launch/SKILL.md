---
name: shipping-and-launch
description: Pre-launch checklists, staged rollouts (canary -> 10% -> 50% -> 100%), rollback plans, feature flag verification. Complements release-changelog (version bump + changelog) by covering the actual deployment and launch process.
---

# Shipping & Launch

## Problem it solves

Shipping is risky without a structured process:
- Deploying with unverified changes and hoping for the best
- No rollback plan — when something goes wrong, panic mode
- Rushed launches without smoke tests
- Feature flags that are enabled but nobody verified the off-state
- Staged rollouts done manually or skipped entirely
- No way to measure if the launch was successful

## Protocol

### 1. Pre-launch checklist

Before any deployment, verify:

- [ ] All tests pass (unit, integration, e2e)
- [ ] Code review completed and all findings resolved
- [ ] CI pipeline is green
- [ ] Database migrations are backward-compatible
- [ ] Feature flags are in place (if needed)
- [ ] Rollback plan is documented
- [ ] Monitoring and alerting are configured
- [ ] Performance benchmarks are within budget
- [ ] Dependencies are up to date (no known vulnerabilities)
- [ ] Documentation is updated
- [ ] Changelog is updated (see release-changelog)

### 2. Staged rollout

Do NOT deploy to 100% of users at once. Use progressive delivery:

1. **Canary (1-2%)** — Deploy to internal users or a small percentage. Verify core functionality.
2. **Ring 1 (10%)** — Expand. Watch monitoring closely for errors, latency, and usage patterns.
3. **Ring 2 (25-50%)** — Broader rollout. Verify all features work at scale.
4. **Production (100%)** — Full rollout only after all previous rings pass.

Between each stage, wait at least:
- Canary: 10-30 minutes
- Ring 1: 1-4 hours
- Ring 2: 4-24 hours
- Production: Monitor for 24-48 hours before declaring success

### 3. Rollback plan

Every deployment must have a documented rollback plan:

```markdown
## Rollback Plan
- **What triggers rollback**: Error rate >1%, P95 latency increase >50%, any P0 alert
- **Rollback command**: `kubectl rollout undo deployment/X` or `git revert HEAD && deploy`
- **Rollback verification**: Monitor dashboards for return to baseline
- **Data migration reversal**: Run `./scripts/rollback-db.sh` (if applicable)
- **Communication**: Notify #team channel, tag oncall
```

Test the rollback plan before the launch. If you can't roll back, you can't ship.

### 4. Feature flags

Before shipping a feature behind a flag:
- **Off-state verification**: Verify the system works normally with the flag OFF
- **On-state verification**: Verify the feature works with the flag ON
- **Flag cleanup**: Schedule a task to remove the flag after the rollout is complete
- **Kill switch**: Ensure the flag can be toggled off quickly without a deploy

### 5. Post-launch monitoring

After full rollout:
- Monitor dashboards for 24-48 hours
- Watch for: error rate, latency, traffic patterns, resource usage
- Compare against baseline metrics from before the launch
- Document any incidents or issues found
- Declare launch complete only after monitoring period passes

## Detection triggers

Activate when:
- Preparing for a deployment or release
- User says "ship", "deploy", "launch", "roll out"
- A release branch is created
- Feature flags are being enabled
- After a release (post-launch monitoring)

## When NOT to use

- Development deployments to local/staging
- Trivial hotfixes that need immediate deployment (use minimal checklist only)
- User explicitly says "just ship it, skip the process"

## Cross-references

- **release-changelog** — Run release-changelog first (version bump, changelog, tag), then shipping-and-launch (deploy, rollout, monitor).

- **ci-cd-automation** — CI/CD pipelines automate the deployment process. This skill defines the human process around the automation.

- **incremental-implementation** — Feature flags from incremental implementation are used in staged rollouts. Each slice ships independently.

- **git-workflow-conventional-commits** — The release commit should follow conventional commit format. Use `chore(release):` for release commits.

- **code-review** — Pre-launch checklist includes code review completion.

- **test-driven-development** — Pre-launch checklist includes test suite passing.

- **anti-premature-termination** — Do not declare the launch complete until the monitoring period passes and everything is verified.

- **project-backup-status** — Backup before launch to safeguard against destructive deployment mistakes.
