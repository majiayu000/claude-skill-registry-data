---
name: temporal-cli
description: Master Temporal CLI workflow management with smart query building, payload decoding, and history filtering using temporal, base64, and jq
version: 1.0.0
---

# Temporal CLI Skill

Execute Temporal CLI commands with smart patterns for workflow management. This skill provides comprehensive knowledge for using Temporal CLI v1.5.1 effectively with base64 and jq.

## Prerequisites

- **Temporal CLI v1.5.1+** installed and available in PATH
- **Configured environments** in `~/.config/temporalio/temporal.yaml`
- **base64** command-line tool (standard on most systems)
- **jq** JSON processor for parsing and filtering

## Core Command Pattern

ALL Temporal CLI commands follow this base pattern:

```bash
temporal --env <environment> -o json --time-format iso workflow <operation> [args...]
```

**Global flags (ALWAYS used):**
- `--env <env>` - Temporal environment from config
- `-o json` - JSON output format
- `--time-format iso` - ISO 8601 timestamps

## Quick Reference

### Essential Operations

| Operation | Reference Guide | Use Case |
|-----------|----------------|----------|
| **list** workflows | [Command Patterns](references/01-command-patterns.md#list-workflows) | Find workflows by query |
| **count** workflows | [Command Patterns](references/01-command-patterns.md#count-workflows) | Get result scope before listing |
| **describe** workflow | [Command Patterns](references/01-command-patterns.md#describe-workflow) | Get current workflow state |
| **show** history | [Command Patterns](references/01-command-patterns.md#get-workflow-history) | View execution events |
| **start** workflow | [Command Patterns](references/01-command-patterns.md#start-workflow) | Create new execution |
| **signal** workflow | [Command Patterns](references/01-command-patterns.md#signal-workflow) | Send signal to running workflow |
| **query** workflow | [Command Patterns](references/01-command-patterns.md#query-workflow) | Query workflow state |
| **cancel** workflow | [Command Patterns](references/01-command-patterns.md#cancel-workflow) | Request cancellation |
| **terminate** workflow | [Command Patterns](references/01-command-patterns.md#terminate-workflow) | Force termination |
| **reset** workflow | [Command Patterns](references/01-command-patterns.md#reset-workflow) | Reset execution to previous point |
| **stack** trace | [Command Patterns](references/01-command-patterns.md#trace-workflow) | Get workflow stack trace |

### Knowledge Guides

| Guide | Purpose |
|-------|---------|
| [Query Construction](references/02-query-construction.md) | Complete query syntax with 50+ examples |
| [Custom Search Attributes](references/03-custom-search-attributes.md) | Using custom fields in queries |
| [Payload Decoding](references/04-payload-decoding.md) | Base64/jq recipes for history payloads |
| [History Filtering](references/05-history-filtering.md) | jq patterns for managing large histories |
| [Smart Patterns](references/06-smart-patterns.md) | Count-first, auto-retry, validation logic |
| [Error Handling](references/07-error-handling.md) | Common errors and recovery |
| [Safety Checks](references/08-safety-checks.md) | Validation for destructive operations |

## Progressive Disclosure Strategy

1. **Start here** - Read this SKILL.md for overview
2. **Need specific command?** - Check [Command Patterns](references/01-command-patterns.md)
3. **Building queries?** - See [Query Construction](references/02-query-construction.md)
4. **Large history?** - Use [History Filtering](references/05-history-filtering.md)
5. **Custom attributes?** - Review [Custom Search Attributes](references/03-custom-search-attributes.md)
6. **Hit errors?** - Consult [Error Handling](references/07-error-handling.md)
7. **Destructive ops?** - Verify [Safety Checks](references/08-safety-checks.md)

## Key Principles

### 1. Always Count Before Listing

```bash
# Get count first to understand scope
COUNT=$(temporal --env prod -o json --time-format iso workflow count \
  --query "ExecutionStatus = 'Failed'" | jq '.count')

# Then list with appropriate limit
temporal --env prod -o json --time-format iso workflow list \
  --query "ExecutionStatus = 'Failed'" \
  --limit ${COUNT}
```

### 2. Filter Large Histories

Histories with 100+ events should be filtered:

```bash
# Use jq to show only failures
temporal --env prod -o json --time-format iso workflow show \
  --workflow-id "my-workflow" | \
  jq '.events[] | select(.eventType | contains("Failed"))'
```

See [History Filtering](references/05-history-filtering.md) for more patterns.

### 3. Validate Queries First

Pre-validate queries before execution to avoid errors:

```bash
# Check for unsupported LIKE operator
if echo "$QUERY" | grep -qi 'LIKE'; then
  echo "ERROR: Use STARTS_WITH instead of LIKE"
  exit 1
fi
```

See [Smart Patterns](references/06-smart-patterns.md) for validation logic.

### 4. Decode Payloads Carefully

Workflow event payloads are base64-encoded:

```bash
# Decode workflow input
temporal --env prod -o json --time-format iso workflow show \
  --workflow-id "my-workflow" | \
  jq -r '.events[0].workflowExecutionStartedEventAttributes.input.payloads[0].data' | \
  base64 -d | \
  jq '.'
```

See [Payload Decoding](references/04-payload-decoding.md) for complete recipes.

## Common Workflows

### Find Failed Workflows
```bash
# Count failures
temporal --env prod -o json --time-format iso workflow count \
  --query "ExecutionStatus = 'Failed'"

# List failed workflows
temporal --env prod -o json --time-format iso workflow list \
  --query "ExecutionStatus = 'Failed'" \
  --limit 10
```

### Find Non-Deterministic / Problematic Workflows

**IMPORTANT**: Workflows with non-deterministic errors often remain in `Running` status, not `Failed`. Use `TemporalReportedProblems` to find them:

```bash
# Find running workflows with WorkflowTask failures (includes non-deterministic errors)
temporal --env prod -o json --time-format iso workflow list \
  --query "ExecutionStatus = 'Running' AND TemporalReportedProblems IN ('category=WorkflowTaskFailed', 'category=WorkflowTaskTimedOut')" \
  --limit 20

# Count problematic workflows
temporal --env prod -o json --time-format iso workflow count \
  --query "ExecutionStatus = 'Running' AND TemporalReportedProblems IN ('category=WorkflowTaskFailed')"
```

**TemporalReportedProblems values:**
- `category=WorkflowTaskFailed` - WorkflowTask failed (includes non-deterministic errors)
- `category=WorkflowTaskTimedOut` - WorkflowTask timed out
- `cause=WorkflowTaskFailedCauseNonDeterministicError` - Specifically non-deterministic errors

**Get failure details from history:**
```bash
# Get the last WorkflowTaskFailed event with full error message
temporal --env prod -o json --time-format iso workflow show \
  --workflow-id "my-workflow" | \
  jq '[.events[] | select(.eventType == "EVENT_TYPE_WORKFLOW_TASK_FAILED")] | .[-1]'
```

### Debug Stuck Workflow
```bash
# Get stack trace
temporal --env prod -o json --time-format iso workflow stack \
  --workflow-id "stuck-workflow-123"

# Check history for patterns
temporal --env prod -o json --time-format iso workflow show \
  --workflow-id "stuck-workflow-123" | \
  jq '[.events[] | .eventType] | group_by(.) | map({type: .[0], count: length})'
```

### Customer-Specific Workflows
```bash
# Using custom search attribute
temporal --env prod -o json --time-format iso workflow list \
  --query "CustomerId = 'customer-abc-123'" \
  --limit 20
```

## Safety First

**Before destructive operations (terminate, reset):**
1. Double-check workflow ID
2. ALWAYS provide `--reason`
3. For batch operations, count affected workflows first
4. Review [Safety Checks](references/08-safety-checks.md)

## Quick Examples

### List Workflows by Type
```bash
temporal --env staging -o json --time-format iso workflow list \
  --query "WorkflowType = 'OnboardingFlow'" \
  --limit 10
```

### Start New Workflow
```bash
temporal --env staging -o json --time-format iso workflow start \
  --type "OnboardingFlow" \
  --task-queue "patient-workflows" \
  --workflow-id "patient-onboard-$(date +%s)" \
  --input '{"customerId": "cust-123"}'
```

### Signal Workflow
```bash
temporal --env prod -o json --time-format iso workflow signal \
  --workflow-id "order-processing-456" \
  --name "approvalReceived" \
  --input '{"approved": true}'
```

## Asset Templates

Pre-built templates available in `assets/`:
- `query-templates.json` - Common query patterns
- `jq-filters.json` - Reusable jq filters
- `event-types.json` - Event type reference

## Getting Started

1. Verify Temporal CLI is installed: `temporal --version`
2. Check environment configuration: `cat ~/.config/temporalio/temporal.yaml`
3. Try counting workflows: `temporal --env staging -o json --time-format iso workflow count`
4. Explore [Command Patterns](references/01-command-patterns.md) for detailed examples

## When Things Go Wrong

1. **Query syntax error?** → Check [Query Construction](references/02-query-construction.md)
2. **Unknown operator?** → See [Error Handling](references/07-error-handling.md)
3. **Empty results?** → Try WorkflowId fallback in [Smart Patterns](references/06-smart-patterns.md)
4. **Large history overwhelming?** → Use [History Filtering](references/05-history-filtering.md)
5. **Non-deterministic errors?** → Use `TemporalReportedProblems` query (see above) or [Error Handling](references/07-error-handling.md#non-deterministic-workflow-errors)

## Next Steps

Start with [Command Patterns](references/01-command-patterns.md) for complete bash examples of all operations.
