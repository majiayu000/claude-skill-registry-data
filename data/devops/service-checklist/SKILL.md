---
name: service-checklist
description: Shared validation and monitoring checklists for service deployment and upgrades. Referenced by deploy-service and service-upgrade skills.
---

# Service Checklist

Shared checklists for service deployment and upgrades.

## Deployment Validation

After deploying or upgrading a service:

- [ ] Pods running (no CrashLoopBackOff)
- [ ] No errors in logs (`kubectl logs -n <namespace> <pod> --tail=100`)
- [ ] Argo CD shows Synced/Healthy
- [ ] Ingress accessible (if applicable)
- [ ] Dependent services still operational

## Monitoring Requirements

After initial deployment or major upgrade:

### Metrics Collection
- [ ] Service exposes metrics endpoint (usually `/metrics`)
- [ ] Prometheus ServiceMonitor or PodMonitor configured
- [ ] Metrics appearing in Prometheus (`up{job="<service>"}`)

### Alerting
- [ ] Alert rules for error conditions
- [ ] Alert rules for service availability
- [ ] Severity levels appropriate (critical/warning)

### Dashboards
- [ ] Grafana dashboard exists for service
- [ ] Key metrics visualized
- [ ] Dashboard accessible and working

### Health Indicators
- [ ] Clear definition of "healthy" state
- [ ] Operators can verify service is working

## Human-in-the-Loop Workflow

### AI Assistant MUST
- ✅ Make file changes
- ✅ Show changes with `git diff`
- ✅ Stage and commit changes
- ✅ Review Argo CD diff (use `argocd-cli` skill)
- ✅ Sync after user approval
- ✅ Mark tasks complete in real-time

### AI Assistant MUST NOT
- ❌ Push commits (user must `git push`)
- ❌ Use `git commit --amend`
- ❌ Rewrite git history
- ❌ Sync without user approval

## Anti-Patterns

- ❌ Parallel deployments/upgrades (too many variables)
- ❌ Pushing without user approval
- ❌ Syncing without user approval
- ❌ Rushing validation
- ❌ Skipping monitoring setup
