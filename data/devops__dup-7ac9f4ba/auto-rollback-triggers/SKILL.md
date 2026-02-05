---
name: auto-rollback-triggers
description: Error rate monitoring, SLO detection, and notification webhooks for automated rollback triggers. Use when setting up automated deployment rollback, monitoring error rates, configuring SLO thresholds, implementing deployment safety nets, setting up alerting webhooks, or when user mentions automated rollback, error rate monitoring, SLO violations, deployment safety, or rollback automation.
allowed-tools: Bash, Read, Write, Edit
---

# Auto-Rollback Triggers

Automated rollback trigger patterns with error rate monitoring, SLO detection, and notification webhooks for deployment safety.

## Overview

This skill provides functional monitoring scripts, CI/CD workflow templates, and webhook integration examples for automated deployment rollback triggers. All scripts include proper error handling, threshold configuration, and notification patterns for production safety nets.

## Scripts

All scripts are located in `scripts/` and are fully functional (not placeholders).

### Core Monitoring Scripts

1. **monitor-error-rate.sh** - Real-time error rate monitoring with configurable thresholds and time windows
2. **check-slo.sh** - SLO (Service Level Objective) validation with success rate calculations
3. **trigger-rollback.sh** - Automated rollback orchestration with platform-specific implementations
4. **collect-metrics.sh** - Metrics collection from various sources (logs, APM, monitoring services)
5. **notify-webhook.sh** - Webhook notification delivery with retry logic and templating

### Usage Examples

```bash
# Monitor error rate (5% threshold over 5 minutes)
bash scripts/monitor-error-rate.sh https://api.example.com/metrics 5.0 300

# Check SLO compliance (99.9% uptime target)
bash scripts/check-slo.sh https://api.example.com/health 99.9

# Trigger rollback to previous version
bash scripts/trigger-rollback.sh vercel my-project previous-deployment-id

# Collect metrics from deployment
bash scripts/collect-metrics.sh https://api.example.com/metrics

# Send webhook notification
bash scripts/notify-webhook.sh "https://hooks.slack.com/services/your_webhook_url_here" "Deployment failed SLO check"
```

## Templates

All templates are located in `templates/` and provide configuration examples.

### GitHub Actions Workflows

1. **github-actions-error-monitoring.yml** - GitHub Actions workflow for continuous error rate monitoring
2. **github-actions-slo-check.yml** - GitHub Actions workflow for SLO validation post-deployment
3. **github-actions-auto-rollback.yml** - Complete auto-rollback workflow with monitoring and triggers
4. **gitlab-ci-auto-rollback.yml** - GitLab CI/CD equivalent for auto-rollback patterns

### Configuration Templates

5. **error-threshold-config.json** - Error rate threshold configuration with time windows
6. **error-threshold-config.yaml** - YAML version of error threshold configuration
7. **slo-config.json** - SLO definition and validation rules
8. **webhook-config.json** - Webhook endpoint configuration with retry policies
9. **rollback-policy.json** - Rollback decision policy configuration

### Platform-Specific Templates

10. **vercel-deployment-protection.json** - Vercel deployment protection rules
11. **digitalocean-app-rollback.json** - DigitalOcean App Platform rollback configuration
12. **railway-deployment-check.json** - Railway deployment health check configuration

### Template Usage

```bash
# Copy workflow to GitHub Actions
cp templates/github-actions-auto-rollback.yml .github/workflows/auto-rollback.yml

# Configure error thresholds
cp templates/error-threshold-config.json config/error-thresholds.json

# Set up SLO definitions
cp templates/slo-config.json config/slo.json
```

## Examples

All examples are located in `examples/` and demonstrate real-world usage patterns.

### Example Files

1. **basic-error-monitoring.md** - Simple error rate monitoring setup
2. **slo-based-rollback.md** - SLO violation detection and automated rollback
3. **slack-webhook-integration.md** - Slack notification webhook integration
4. **discord-webhook-integration.md** - Discord notification webhook integration
5. **multi-platform-rollback.md** - Multi-platform rollback orchestration (Vercel, DigitalOcean, Railway)
6. **advanced-monitoring.md** - Advanced monitoring with APM integration (Datadog, New Relic, Sentry)
7. **gradual-rollout-protection.md** - Canary deployment protection with auto-rollback

## Instructions

### Setting Up Error Rate Monitoring

1. **Configure Error Thresholds**
   ```bash
   # Copy and customize threshold configuration
   cp templates/error-threshold-config.json config/error-thresholds.json

   # Edit thresholds for your application
   # Example: 5% error rate over 5 minutes triggers rollback
   ```

2. **Deploy Monitoring Script**
   ```bash
   # Run monitoring in background or CI/CD pipeline
   bash scripts/monitor-error-rate.sh \
     https://api.myapp.com/metrics \
     5.0 \
     300 \
     config/error-thresholds.json
   ```

3. **Integrate with GitHub Actions**
   ```bash
   # Copy workflow template
   cp templates/github-actions-error-monitoring.yml .github/workflows/monitor-errors.yml

   # Configure secrets: DEPLOYMENT_URL, WEBHOOK_URL, ROLLBACK_TOKEN
   ```

### Setting Up SLO-Based Rollback

1. **Define SLO Targets**
   ```bash
   # Copy SLO configuration template
   cp templates/slo-config.json config/slo.json

   # Define targets: 99.9% uptime, <500ms p95 latency, <1% error rate
   ```

2. **Run SLO Validation**
   ```bash
   # Check SLO compliance after deployment
   bash scripts/check-slo.sh \
     https://api.myapp.com/health \
     99.9 \
     config/slo.json

   # Exit code 0 = SLO met, 1 = SLO violated (trigger rollback)
   ```

3. **Automate with CI/CD**
   ```bash
   # Copy complete auto-rollback workflow
   cp templates/github-actions-auto-rollback.yml .github/workflows/auto-rollback.yml

   # Workflow automatically monitors and rolls back on SLO violations
   ```

### Webhook Integration

**Slack Webhook Integration**
```bash
# Set webhook URL (use placeholder, replace with real URL)
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/your_webhook_url_here"

# Send notification
bash scripts/notify-webhook.sh \
  "$SLACK_WEBHOOK_URL" \
  "Deployment failed: Error rate 8.5% exceeds threshold 5.0%"
```

**Discord Webhook Integration**
```bash
# Set webhook URL (use placeholder, replace with real URL)
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/your_webhook_url_here"

# Send notification with custom formatting
bash scripts/notify-webhook.sh \
  "$DISCORD_WEBHOOK_URL" \
  "Auto-rollback triggered" \
  --discord
```

### Platform-Specific Rollback

**Vercel Rollback**
```bash
# Trigger Vercel deployment rollback
bash scripts/trigger-rollback.sh vercel \
  my-project \
  previous-deployment-id \
  "$VERCEL_TOKEN"
```

**DigitalOcean App Platform Rollback**
```bash
# Trigger DigitalOcean App rollback
bash scripts/trigger-rollback.sh digitalocean \
  app-id \
  previous-deployment-id \
  "$DIGITALOCEAN_TOKEN"
```

**Railway Rollback**
```bash
# Trigger Railway deployment rollback
bash scripts/trigger-rollback.sh railway \
  project-id \
  previous-deployment-id \
  "$RAILWAY_TOKEN"
```

## Integration Patterns

### GitHub Actions Integration

1. **Continuous Monitoring Workflow**
   - Runs every 5 minutes during deployment window
   - Monitors error rates and SLO metrics
   - Automatically triggers rollback on threshold violations
   - Sends notifications to Slack/Discord

2. **Post-Deployment Validation**
   - Runs immediately after deployment
   - Validates SLO compliance for 15 minutes
   - Rolls back if SLO violations detected
   - Reports results to deployment dashboard

3. **Canary Deployment Protection**
   - Monitors canary deployment metrics
   - Compares error rates: canary vs stable
   - Automatically promotes or rolls back
   - Gradual traffic shift with safety checks

### GitLab CI/CD Integration

Similar patterns available for GitLab CI/CD using `templates/gitlab-ci-auto-rollback.yml`

### Platform-Specific Integration

**Vercel Deployment Protection**
- Use `templates/vercel-deployment-protection.json` for native Vercel checks
- Configure automated checks in Vercel dashboard
- Integrate with GitHub Actions for advanced monitoring

**DigitalOcean App Platform**
- Use `templates/digitalocean-app-rollback.json` for health checks
- Configure App Platform health checks
- Use doctl CLI for automated rollback

**Railway**
- Use `templates/railway-deployment-check.json` for health checks
- Configure Railway health check endpoints
- Use Railway CLI for automated rollback

## Requirements

### Core Dependencies

- `curl` - For HTTP requests to metrics endpoints
- `jq` - For JSON parsing and metrics extraction
- `bc` - For threshold calculations
- `date` - For time window calculations (GNU coreutils)

### Optional Dependencies

- **Platform CLIs**:
  - `vercel` - Vercel CLI for deployment management
  - `doctl` - DigitalOcean CLI for App Platform management
  - `railway` - Railway CLI for project management

- **Monitoring Tools**:
  - `datadog-cli` - Datadog metrics collection
  - `newrelic-cli` - New Relic APM integration
  - `sentry-cli` - Sentry error tracking integration

### GitHub Actions Secrets

Configure these secrets in your GitHub repository:

- `DEPLOYMENT_URL` - Application metrics endpoint
- `WEBHOOK_URL` - Slack/Discord webhook URL (use placeholder: `https://hooks.example.com/your_webhook_url_here`)
- `ROLLBACK_TOKEN` - Platform API token for rollback operations
- `VERCEL_TOKEN` - Vercel API token (if using Vercel)
- `DIGITALOCEAN_TOKEN` - DigitalOcean API token (if using DigitalOcean)
- `RAILWAY_TOKEN` - Railway API token (if using Railway)

## Exit Codes

All scripts follow standard exit code conventions:

- `0` - Metrics within thresholds, SLO met, rollback successful
- `1` - Threshold exceeded, SLO violated, rollback required
- `2` - Invalid arguments or missing dependencies
- `3` - Timeout or network error accessing metrics
- `4` - Platform API error during rollback
- `5` - Webhook notification failed

## Best Practices

1. **Start with Conservative Thresholds** - Set thresholds that catch real issues without false positives
2. **Use Time Windows** - Monitor over time windows (5-15 minutes) to avoid reacting to transient spikes
3. **Test in Staging First** - Validate rollback triggers in staging environment before production
4. **Implement Gradual Rollout** - Use canary deployments with automated protection
5. **Monitor Rollback Success** - Verify rollback actually resolves the issue
6. **Alert Human Teams** - Always notify teams when auto-rollback triggers
7. **Document Thresholds** - Clearly document why specific thresholds were chosen
8. **Review Rollback History** - Regularly review triggered rollbacks to improve thresholds
9. **Use Placeholder Webhooks** - Never commit real webhook URLs, use placeholders
10. **Secure API Tokens** - Store platform tokens in CI/CD secrets, never in code

## Security Considerations

1. **Webhook URLs** - Always use placeholders like `https://hooks.example.com/your_webhook_url_here` in templates
2. **API Tokens** - Store in CI/CD secrets or environment variables, never hardcode
3. **Metrics Endpoints** - Ensure metrics endpoints are authenticated and secured
4. **Rollback Permissions** - Limit rollback permissions to CI/CD service accounts only
5. **Audit Logging** - Log all rollback triggers and actions for audit trail

## Troubleshooting

**False Positive Rollbacks**
- Increase time window for error rate monitoring
- Adjust thresholds based on normal application behavior
- Filter out expected errors (e.g., 404s from bots)

**Missed Rollback Triggers**
- Decrease monitoring interval (e.g., 1 minute instead of 5)
- Lower thresholds if issues aren't caught
- Add multiple SLO metrics (error rate, latency, availability)

**Webhook Notifications Not Delivered**
- Verify webhook URL is correct (not placeholder)
- Check webhook service status
- Implement retry logic with exponential backoff
- Add fallback notification channels

**Platform Rollback Failures**
- Verify API token permissions
- Check platform API rate limits
- Ensure previous deployment ID is valid
- Implement manual rollback fallback

---

**Location**: /home/gotime2022/.claude/plugins/marketplaces/dev-lifecycle-marketplace/plugins/deployment/skills/auto-rollback-triggers/
