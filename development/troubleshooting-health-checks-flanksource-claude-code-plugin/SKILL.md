---
name: troubleshooting-health-checks
description: Debugs and troubleshoots Mission Control health checks by analyzing check configurations, reviewing failure patterns, and identifying root causes. Use when users ask about failing health checks, mention specific health check names or IDs, inquire why a health check is failing or unhealthy, or need help understanding health check errors and timeouts.
allowed-tools: search_health_checks, get_check_status, run_health_check, list_all_checks, search_catalog, describe_config, search_catalog_changes
---

# Health Check Troubleshooting Skill

## Core Purpose

This skill enables Claude to troubleshoot Mission Control health checks by analyzing check configurations, diagnosing failure patterns, identifying timeout and error root causes, and recommending configuration adjustments to improve reliability.

Note: Read @skills/troubleshooting-health-checks/reference/query-syntax.md to for query syntax

## Health check troubleshooting workflow

Copy this checklist and track your progress:

```
Troubleshooting Progress:
- [ ] Step 1: Gather health check information
- [ ] Step 2: Analyze failure patterns
- [ ] Step 3: Cross-reference configuration issues
- [ ] Step 4: Create diagnostic summary
- [ ] Step 5: Verify remediation steps
```

## Gather health check information

To begin with, get the id of the check in question.
Use `search_health_checks` with query syntax to find checks. Read @skills/troubleshooting-health-checks/reference/query-syntax.md to for query syntax
Else, if you could not get the health check Id from the user provided name, use `list_all_checks` to get complete metadata for all health checks .

Then, follow this procedure:

- **Historical Context**: Use `get_check_status` to retrieve execution history
- **Investigate the check specification**: Understand the intention of the check.
- **Investiagte the chagnes to the canray**: Use `search_catalog_changes(<canary_uuid>)` to get the changes on the canary.
  Look for the change details to see any new changes on the specification.

## Analyze failure patterns

Examine the historical data to identify patterns. Look for:

- **Intermittent failures**: Passes sometimes, fails others
  - Suggests: Network instability, load-related issues, race conditions
- **Consistent failures**: Always failing
  - Suggests: Configuration error, endpoint down, authentication issue
- **Recent pattern changes**: Was passing, now failing
  - Suggests: Recent deployment, config change, infrastructure change
- **Timeout patterns**: Fails with timeout errors
  - Suggests: Performance degradation, insufficient timeout value
- **Time-based patterns**: Fails at specific times
  - Suggests: Scheduled jobs, traffic patterns, resource contention

Duration analysis:

- Increasing duration → Performance degrading (may lead to timeouts)
- Spiky duration → Intermittent load or resource contention
- Consistent slow duration → Timeout threshold too aggressive

## Create diagnostic summary

Organize findings systematically. Include:

- **Primary diagnosis**

  - Root cause identification with supporting evidence
  - Quote specific error messages from last_result
  - Reference historical pattern statistics
  - Cite configuration values that contribute to the issue

- **Contributing factors**

  - Secondary issues that may worsen the problem
  - Environmental factors (network, infrastructure)
  - Configuration mismatches

- **Impact assessment**
  - How long has the issue persisted
  - Frequency and severity of failures
  - Potential downstream effects

Example diagnostic format:

> The health check "api-status" (ID: check-123) is failing based on `get_check_status` history showing error "timeout exceeded" in recent executions. Historical data shows duration increasing from 3s to 5s over 6 hours. This indicates backend performance degradation requiring investigation and potential timeout adjustment.

## Verify remediation steps

Provide and validate specific fixes. For each recommendation:

- Use `run_health_check` to test fixes immediately
- Verify check passes after configuration changes
- Monitor execution duration and response

## Success criteria checklist

Before completing troubleshooting:

- [ ] Health check configuration fully analyzed
- [ ] Failure pattern clearly identified with evidence
- [ ] Root cause diagnosed with supporting data
- [ ] Specific remediation steps provided
- [ ] Configuration adjustments justified
- [ ] Validation approach included
