---
name: pulumi-neo
description: Manages cloud infrastructure through natural language conversations with Pulumi Neo, an AI agent for platform engineers. Enables infrastructure analysis, resource provisioning, stack deployment, and configuration management via conversational AI. Use when creating Neo tasks, requesting infrastructure analysis, automating cloud deployments, managing infrastructure as code (IaC), provisioning AWS/Azure/GCP resources, managing infrastructure through natural language prompts, reviewing PRs with Neo, handling Neo approval workflows, or checking Neo task status and events. Also use when the user mentions "Pulumi Neo", "Neo task", "Neo agent", or wants AI-assisted infrastructure management.
---

# Pulumi Neo Skill

## Prerequisites

- **Pulumi Cloud account** with Neo access
- **PULUMI_ACCESS_TOKEN** environment variable set with your Personal Access Token
- **Organization**: Required for all Neo API calls

## Detecting Organization

```bash
# Get current Pulumi organization from CLI
pulumi org get-default

# If no default org or using self-managed backend, ask user for organization name
```

If `pulumi org get-default` returns an error or shows a non-cloud backend, prompt the user for their Pulumi Cloud organization name.

## Quick Start

**IMPORTANT:** Always use `--no-poll` in Claude Code to prevent blocking.

**Preferred: Python Script**
```bash
python <skill-base-directory>/scripts/neo_task.py --org <org> --message "Your message" --no-poll
```

**Alternative: Direct API**
```bash
export PULUMI_ACCESS_TOKEN=<your-token>
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
curl -s -X POST "https://api.pulumi.com/api/preview/agents/<org>/tasks" \
  -H "Authorization: token $PULUMI_ACCESS_TOKEN" \
  -H "Accept: application/vnd.pulumi+8" \
  -H "Content-Type: application/json" \
  -d "{\"message\":{\"type\":\"user_message\",\"content\":\"How many stacks do I have?\",\"timestamp\":\"$TIMESTAMP\",\"entity_diff\":{\"add\":[],\"remove\":[]}}}"
```

Fetch events: `curl -s "https://api.pulumi.com/api/preview/agents/<org>/tasks/<task-id>/events" -H "Authorization: token $PULUMI_ACCESS_TOKEN" -H "Accept: application/vnd.pulumi+8" | jq '.events[-1].eventBody.content'`

**MCP Tools** (if Pulumi MCP server is installed): `mcp__pulumi__neo-bridge`, `mcp__pulumi__neo-get-tasks`, `mcp__pulumi__neo-continue-task`

## Using the Python Script

The script handles Neo task creation, polling, and management:

```bash
# Create a task and poll for updates (interactive/terminal use)
python scripts/neo_task.py --org <org-name> --message "Help me optimize my Pulumi stack"

# Create task without polling (CI/CD or programmatic use)
python scripts/neo_task.py --org <org-name> --message "Analyze this" --no-poll

# Create task with stack context
python scripts/neo_task.py --org <org-name> \
  --message "Analyze this stack" \
  --stack-name prod --stack-project my-infra --no-poll

# Create task with repository context
python scripts/neo_task.py --org <org-name> \
  --message "Review this infrastructure code" \
  --repo-name my-repo --repo-org my-github-org --no-poll

# List existing tasks
python scripts/neo_task.py --org <org-name> --list

# Fetch current events (single request, no polling)
python scripts/neo_task.py --org <org-name> --task-id <task-id> --get-events

# Poll an existing task for updates (interactive)
python scripts/neo_task.py --org <org-name> --task-id <task-id>

# Send approval for a pending request
python scripts/neo_task.py --org <org-name> --task-id <task-id> --approve

# Cancel a pending request
python scripts/neo_task.py --org <org-name> --task-id <task-id> --cancel
```

## Neo Task Workflow

### Creating Tasks

Tasks are created with a natural language message describing what you want Neo to do:

- **Infrastructure analysis**: "Analyze my production stack for security issues"
- **Maintenance operations**: "Help me upgrade my Kubernetes cluster"
- **Configuration changes**: "Add monitoring to my Lambda functions"
- **Multi-step workflows**: "Set up a complete CI/CD pipeline for this project"

### Entity Context

Attach entities for context: `stack` (name + project), `repository` (name + org + forge), `pull_request` (number + merged + repository), `policy_issue` (id).

### Task Status

| Status | Description |
|--------|-------------|
| `running` | Neo is actively processing the task |
| `idle` | Task is waiting for input or has finished processing |

**Note:** Task completion and approval requests are determined by examining events, not task status.

### Approval Flow

When Neo requires confirmation for an operation (this is a key concept — Neo never makes destructive changes without asking):

1. Task status remains `running` or transitions to `idle`
2. An `agentResponse` event contains `tool_calls` with an `approval_request` tool — this is the specific event structure to look for
3. The `approval_request_id` is found in the tool call parameters
4. User reviews the proposed changes
5. Send approval via `--approve` or cancellation via `--cancel`

**Detecting approvals:** Check events for `eventBody.tool_calls` containing `approval_request` entries rather than relying on task status. The approval_request_id from the tool call parameters is needed to respond.

```bash
# Approve a pending request
python scripts/neo_task.py --org <org> --task-id <task-id> --approve

# Cancel/reject a pending request
python scripts/neo_task.py --org <org> --task-id <task-id> --cancel
```

## Common Workflows

### Analyze Infrastructure

```bash
python scripts/neo_task.py --org myorg \
  --message "What security improvements can I make to my AWS infrastructure?" \
  --stack-name prod --stack-project aws-infra --no-poll
```

### Fix Policy Violations

```bash
python scripts/neo_task.py --org myorg \
  --message "Help me fix the policy violations in my production stack" --no-poll
```

### Generate Pulumi Code

```bash
python scripts/neo_task.py --org myorg \
  --message "Create a new Pulumi TypeScript project for a containerized web app on AWS ECS" --no-poll
```

### Review Pull Request

```bash
python scripts/neo_task.py --org myorg \
  --message "Review the infrastructure changes in this PR" \
  --repo-name infra --repo-org myorg --repo-forge github --no-poll
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| 401 | Invalid/missing token | Verify with `curl -s -H "Authorization: token $PULUMI_ACCESS_TOKEN" https://api.pulumi.com/api/user` |
| 404 | Wrong org or endpoint | Verify org with `pulumi org get-default` |
| 409 | Task busy | Wait for current operation to complete |
| Script hangs | Missing `--no-poll` | Kill with Ctrl+C, add `--no-poll` flag |
| Token not found | Not exported | Run `export PULUMI_ACCESS_TOKEN="$PULUMI_ACCESS_TOKEN"` |

## API Reference

Base URL: `https://api.pulumi.com/api/preview/agents`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/{org}/tasks` | POST | Create task |
| `/{org}/tasks` | GET | List tasks |
| `/{org}/tasks/{id}` | GET | Get task |
| `/{org}/tasks/{id}/events` | GET | Get events |
| `/{org}/tasks/{id}` | POST | Send message/approval |

Required headers:
- `Authorization: token $PULUMI_ACCESS_TOKEN`
- `Accept: application/vnd.pulumi+8`
- `Content-Type: application/json`

See [references/pulumi-neo-api.md](references/pulumi-neo-api.md) for full details.