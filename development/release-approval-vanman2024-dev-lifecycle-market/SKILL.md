---
name: Release Approval
description: Approval workflow templates with GitHub Actions and Slack integration for multi-stakeholder release gating. Use when setting up approval workflows, configuring stakeholder gates, automating approval notifications, integrating Slack webhooks, requesting release approvals, tracking approval status, or when user mentions release approval, stakeholder sign-off, approval gates, multi-stage approvals, or release gating.
---

# Release Approval

**CRITICAL: The description field above controls when Claude auto-loads this skill.**

## Overview

Provides comprehensive patterns, templates, and scripts for multi-stakeholder release approval workflows including GitHub Actions integration, Slack notifications, approval gate configuration, and status tracking automation.

## Instructions

### 1. Approval Workflow Architecture

**Understand Approval Gate Patterns:**
- **Sequential Approvals**: Stakeholders approve in order (dev → QA → security → release)
- **Parallel Approvals**: All stakeholders review simultaneously, release when all approve
- **Conditional Approvals**: Requirements change based on change scope (breaking vs patch)
- **Hybrid Approvals**: Some gates parallel, others sequential

**Design Workflow:**
1. Identify required stakeholder groups (technical lead, product owner, QA, security, compliance)
2. Define approval thresholds (required vs optional approvals)
3. Set timeout and escalation policies
4. Document veto power and override conditions

### 2. GitHub Actions Workflow Setup

**Configure Approval Workflows:**
1. Use `templates/github-actions-approval.yml` for basic approval workflow
2. Use `templates/github-actions-approval-slack.yml` for Slack-integrated workflow
3. Configure environment protection rules for production
4. Set required reviewers in repository settings

**Workflow Triggers:**
- Manual workflow dispatch for on-demand approvals
- Tag push events for automatic approval requests
- Pull request reviews for pre-merge approvals
- Issue comments for approval tracking

### 3. Approval Gate Configuration

**Setup Approval Gates:**
1. Use `templates/approval-gates.yml` to define stakeholder groups and requirements
2. Use `scripts/setup-approval-gates.sh` to initialize gate configuration
3. Configure approval thresholds per gate (required count, optional count)
4. Define approval dependencies (QA requires dev approval first)

**Configuration Structure:**
```yaml
approval_gates:
  - stage: development
    approvers: ["@dev-team-lead", "@tech-lead"]
    required: 2
    timeout_hours: 24
  - stage: qa
    approvers: ["@qa-lead"]
    required: 1
    depends_on: ["development"]
  - stage: security
    approvers: ["@security-team"]
    required: 1
    veto_power: true
  - stage: release
    approvers: ["@release-manager"]
    required: 1
    depends_on: ["development", "qa", "security"]
```

### 4. Slack Notification Integration

**Setup Slack Webhooks:**
1. Use `scripts/setup-slack-webhook.sh` to configure Slack integration
2. Use `templates/slack-webhook-config.json` for webhook configuration template
3. Store webhook URLs in GitHub Secrets (never hardcode)
4. Use `scripts/notify-slack.sh` for sending approval notifications

**Notification Types:**
- **Approval Requested**: Notify stakeholders when approval needed
- **Approval Granted**: Confirm when stakeholder approves
- **Approval Denied**: Alert when stakeholder rejects with reason
- **Approval Timeout**: Escalate when approval times out
- **Approval Complete**: Celebrate when all approvals obtained

### 5. Requesting and Tracking Approvals

**Request Approvals:**
1. Use `scripts/request-approval.sh` to send approval requests
2. Create GitHub issue for approval tracking
3. Request PR reviews from stakeholders
4. Send Slack notifications to stakeholder channels

**Track Approval Status:**
1. Use `scripts/check-approval-status.sh` to monitor approval progress
2. Update approval tracking issue as approvals come in
3. Generate approval audit trail
4. Store approval records in `.github/releases/approvals/`

### 6. Approval Automation Patterns

**Automate Common Scenarios:**

**Auto-Approve for Non-Breaking Changes:**
- Patch releases with docs-only changes
- Dependency updates with passing tests
- Automated security patches

**Escalation on Timeout:**
- Send reminder notifications after grace period
- Escalate to backup approvers
- Alert release manager for intervention

**Conditional Approval Requirements:**
- Breaking changes require additional security review
- Feature releases require product owner approval
- Hotfix releases have expedited approval process

### 7. Approval Audit Trail

**Document Approvals:**
1. Use `scripts/generate-approval-audit.sh` to create audit records
2. Store approval records in `.github/releases/approvals/v{version}.json`
3. Include: approver name, timestamp, decision, comments, justification
4. Commit approval records to git for permanent audit trail

**Audit Record Structure:**
```json
{
  "version": "1.2.3",
  "requested_at": "2025-01-15T10:00:00Z",
  "completed_at": "2025-01-15T14:30:00Z",
  "approvals": [
    {
      "stage": "development",
      "approver": "tech-lead",
      "decision": "approved",
      "timestamp": "2025-01-15T11:00:00Z",
      "comments": "All tests passing, ready for QA"
    },
    {
      "stage": "qa",
      "approver": "qa-lead",
      "decision": "approved_with_conditions",
      "timestamp": "2025-01-15T13:00:00Z",
      "comments": "Minor UI issue logged, non-blocking"
    }
  ],
  "final_decision": "approved",
  "conditions": ["Monitor UI issue #1234 post-release"]
}
```

## Available Scripts

1. **setup-approval-gates.sh**: Initialize approval gate configuration with stakeholder groups
2. **request-approval.sh**: Send approval requests to stakeholders via GitHub and Slack
3. **check-approval-status.sh**: Monitor approval progress and generate status reports
4. **notify-slack.sh**: Send Slack notifications for approval events
5. **setup-slack-webhook.sh**: Configure Slack webhook integration with GitHub Actions
6. **generate-approval-audit.sh**: Create comprehensive approval audit records
7. **escalate-approval.sh**: Handle approval timeouts with escalation logic

## Available Templates

1. **github-actions-approval.yml**: GitHub Actions workflow for approval orchestration
2. **github-actions-approval-slack.yml**: GitHub Actions workflow with Slack integration
3. **approval-gates.yml**: Approval gate configuration with stakeholder groups
4. **slack-webhook-config.json**: Slack webhook configuration template (placeholders only)
5. **approval-issue-template.md**: GitHub issue template for approval tracking
6. **approval-audit-template.json**: JSON template for approval audit records
7. **environment-protection-rules.md**: GitHub environment protection rules guide

## Available Examples

1. **basic-approval-workflow.md**: Simple sequential approval workflow example
2. **parallel-approval-gates.md**: Multi-stakeholder parallel approval pattern
3. **conditional-approval.md**: Change-scope-based conditional approval requirements
4. **slack-integration-complete.md**: Full Slack webhook integration example
5. **automated-gating.md**: Auto-approval and escalation patterns
6. **approval-audit-trail.md**: Complete audit trail generation example

## Requirements

- GitHub CLI (`gh`) installed and authenticated
- GitHub repository with write access
- GitHub Actions enabled
- Slack workspace with webhook permissions (optional)
- Repository secrets configured for sensitive data
- Stakeholder GitHub usernames documented
- Clear approval policies defined

## Security Considerations

**CRITICAL: Always use placeholders for sensitive data**

- ❌ Never hardcode Slack webhook URLs in code or configs
- ✅ Store webhook URLs in GitHub Secrets: `SLACK_WEBHOOK_URL`
- ✅ Use placeholders in templates: `https://hooks.slack.com/services/YOUR_WEBHOOK_HERE`
- ❌ Never commit `.env` files with real credentials
- ✅ Create `.env.example` with placeholder values
- ✅ Document how to obtain webhooks in README

**Environment Variable Pattern:**
```bash
# .env.example
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR_WEBHOOK_HERE
GITHUB_TOKEN=ghp_your_github_token_here
APPROVAL_TIMEOUT_HOURS=24
```

## Progressive Disclosure

For additional reference material:
- Read `examples/basic-approval-workflow.md` for quick start
- Read `examples/parallel-approval-gates.md` for multi-stakeholder patterns
- Read `examples/slack-integration-complete.md` for webhook setup
- Read `examples/automated-gating.md` for automation patterns
- Read `templates/github-actions-approval.yml` for workflow implementation

## Integration with Commands and Agents

**Commands that use this skill:**
- `/versioning:approve-release` - Orchestrates approval workflow using these patterns

**Agents that use this skill:**
- `approval-workflow-manager` - Uses templates and scripts for approval orchestration

**Workflow:**
1. User runs `/versioning:approve-release <version>`
2. Command invokes `approval-workflow-manager` agent
3. Agent loads this skill for templates and scripts
4. Agent uses `request-approval.sh` to notify stakeholders
5. Agent uses `check-approval-status.sh` to monitor progress
6. Agent uses `generate-approval-audit.sh` to document approvals

---

**Skill Location**: plugins/versioning/skills/release-approval/SKILL.md
**Version**: 1.0.0
