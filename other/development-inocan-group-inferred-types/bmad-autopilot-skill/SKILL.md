---
name: bmad-autopilot-skill
description: Autonomous development orchestrator for processing epics. Use when the user wants to run the autopilot, process epics, or automate the development workflow with BMAD method.
allowed-tools: Bash, Read
---

# BMAD Autopilot - Autonomous Development Orchestrator

This skill runs the BMAD Autopilot bash orchestrator to automatically process epics through the full development cycle.

## When to Use

Activate this skill when the user:
- Wants to run the autopilot or orchestrator
- Asks to process epics automatically
- Mentions BMAD development workflow
- Wants to automate PR creation and review cycles

## Execution

Run the orchestrator from the repository root:

```bash
# Process ALL epics automatically
./.autopilot/bmad-autopilot.sh

# Process specific epics
./.autopilot/bmad-autopilot.sh "7A 8A"

# With verbose output
./.autopilot/bmad-autopilot.sh --verbose

# Resume after interruption
./.autopilot/bmad-autopilot.sh --continue
```

## Workflow States

The orchestrator runs through these phases:
1. CHECK_PENDING_PR - Find unfinished PRs
2. FIND_EPIC - Select next epic to process
3. CREATE_BRANCH - Create feature branch
4. DEVELOP_STORIES - Claude develops the epic (interactive)
5. CODE_REVIEW - Run local checks and review (interactive)
6. CREATE_PR - Create pull request
7. → Auto-continue to next epic (PR added to pending list)
8. Background: Pending PRs monitored, auto-merged when ready
9. FIX_ISSUES - If Copilot has comments, fix and resolve threads
10. MERGE_PR - Merge when CI passes and approved
11. Loop until all epics DONE

## Auto-Approve Integration

The `auto-approve.yml` GitHub workflow handles PR approval with strict conditions:

**Approval conditions (ALL must be met):**
1. At least 10 minutes since last push
2. Copilot review exists
3. All review threads resolved
4. All CI checks passed

**Flow:**
1. **After PR creation** - Autopilot continues to next epic immediately
2. **Copilot reviews** - Triggers auto-approve workflow
3. **Workflow waits for CI** - Polls until all checks pass
4. **Workflow checks conditions** - 10 min wait, threads resolved
5. **Dismisses stale approvals** - If unresolved threads exist
6. **Approves only when ready** - All conditions met
7. **PR becomes mergeable** - Autopilot's background check merges it

**If Copilot has comments (FIX_ISSUES phase):**
1. Autopilot detects unresolved threads during periodic check
2. Fetches thread content (file, line, comment) via GraphQL
3. Claude fixes the issues
4. Posts reply to PR acknowledging feedback
5. Resolves all threads via GraphQL mutation
6. Pushes fixes → Copilot re-reviews → auto-approve triggers again
7. 10 min wait ensures Copilot has time to re-review

**Manual workflow trigger:**
```bash
gh workflow run auto-approve.yml -f pr_number=123
```

**Critical requirements:**
- Never approve with unresolved threads
- Always reply to review comments
- Always resolve threads after fixing
- Wait 10 min after push before approval

## Logs and State

- Log: `.autopilot/autopilot.log`
- State: `.autopilot/state.json`
- Debug: `.autopilot/tmp/debug.log` (when --debug)

## Prerequisites

The script requires: `claude`, `gh`, `jq`, `rg`, `git`
