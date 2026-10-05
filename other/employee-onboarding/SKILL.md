---
name: employee-onboarding
displayName: Employee Onboarding
tagline: Automate new employee onboarding with checklists, account provisioning, and welcome workflows.
description: |
  Streamlines new employee onboarding by automating account creation,
  checklist management, and welcome workflows. Creates personalized
  onboarding plans with role-specific tasks, sends welcome messages,
  provisions tool access, and tracks completion across HR systems.
department:
  - HR
  - People Operations
use_cases:
  - Employee Onboarding
  - Account Provisioning
  - HR Automation
tools_required:
  - BambooHR MCP
  - Slack MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-05-08
version: 1.0.0
exampleInput: |
  Onboard new engineer starting Monday.
  Name: Alex Chen, Role: Senior Backend Engineer, Team: Platform.
exampleOutput: |
  Onboarding Plan — Alex Chen

  PRE-START (before Monday)
  ✅ BambooHR profile created
  ✅ Equipment ordered (MacBook Pro 16")
  ✅ Slack account invited to #platform, #engineering
  ✅ GitHub added to platform-team org
  ✅ Welcome email sent with Day 1 schedule

  WEEK 1 CHECKLIST
  □ Meet with manager (30 min)
  □ Team introductions
  □ Development environment setup
  □ Codebase walkthrough with buddy (@carol)
  □ HR orientation and benefits enrollment

  WEEK 2-4 CHECKLIST
  □ First PR submitted and reviewed
  □ Shadow on-call rotation
  □ Complete security training
  □ 30-day check-in with manager
---

# Employee Onboarding

Automate new employee onboarding with checklists, account provisioning, and welcome workflows.

**Integrations:** BambooHR, Slack

## When to Use

- A new employee is joining and needs onboarding setup
- HR wants to automate repetitive onboarding tasks
- The user mentions "onboarding", "new hire", or "employee setup"

## Steps

### Step 1: Create Employee Profile

Set up the employee record in BambooHR with role and team info.

### Step 2: Provision Accounts

Create accounts in required tools and add to appropriate groups.

### Step 3: Generate Onboarding Plan

Create a personalized checklist with role-specific tasks and milestones.

### Step 4: Send Welcome Communication

Post welcome messages in Slack and send Day 1 schedule.

## Output

Deliver:
- Employee profile in HR system
- Account provisioning confirmation
- Personalized onboarding checklist
- Welcome communication sent
