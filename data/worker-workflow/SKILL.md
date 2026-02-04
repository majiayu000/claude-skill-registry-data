---
name: worker-workflow
description: Use for workflow guidance on HOW to work effectively. Covers task execution, decision escalation, and team coordination.
---

# Worker Workflow - HOW TO Work Effectively

## ⚠️ CRITICAL: Git Branch Hygiene

**Refer to `git-workflow` skill for detailed instructions.**

**BEFORE starting ANY new ticket, ALWAYS:**

1. **Check if ticket already has a PR** → Use `get_ticket()` to check `pull_request_url`
2. **If PR exists** → Checkout PR's branch (see "Starting Work on a Ticket" below)
3. **If NO PR** → Then follow these steps:

   ```bash
   # Check current branch
   git branch --show-current
   # If NOT on `main`, switch back:
   git checkout main
   git pull origin main
   # Then create new branch for your ticket
   ```

**NEVER start a new ticket on another ticket's branch!**

❌ **WRONG:**
- Finish Ticket A on `feature/ticket-A`
- Start Ticket B on same branch → commits mix together!

✅ **CORRECT:**
- Finish Ticket A on `feature/ticket-A`
- Return to main: `git checkout main && git pull`
- Create new branch for Ticket B: `git checkout -b feature/ticket-B`

🔄 **REWORKING A REJECTED TICKET:**
- Ticket #190 was rejected → has existing PR
- Checkout PR's branch: `gh pr view 117 --json headRefName`
- Fix, commit, push to SAME branch
- NO new PR created!

## Your Core Workflow

You receive assigned tickets and implement them. When uncertain, escalate rather than decide.

### Work Cycle

1. **Receive ticket** → Check git branch (ticket should already be assigned)
2. **Implement** → Use **git-workflow** skill (detailed below)
3. **Create PR** → Update ticket with PR URL
4. **Submit for review** → `transition_ticket(event: "submit_review")`

## What YOU Do (Your Actions)

### Implementation Tasks
- ✅ Write, modify, and refactor code
- ✅ Run and write tests
- ✅ Create and fix pull requests
- ✅ Investigate bugs and issues
- ✅ Read code to understand context
- ✅ Explore the codebase to find ALL affected files

### Git Workflow tasks
Follow instructions in `git-workflow` skill.
- ✅ Create branch
- ✅ Commit changes
- ✅ Create Pull Request
- ...

### Coordination Tasks
- ✅ Check git branch BEFORE starting new ticket
- ✅ Update tickets with PR URLs
- ✅ Add comments for blockers/questions
- ✅ Store decisions in memory for reference

### Escalation (When Uncertain)
| Situation | Action |
|-----------|--------|
| Need a task created | Add comment: "Please create ticket for..." |
| Need architectural decision | Add comment: "Decision needed on..." |
| Found dependency issue | Add comment: "Ticket #X blocks #Y" |
| Unclear requirement | Add comment: "Clarification needed on..." |

## HOW TO Handle Common Scenarios

### Starting Work on a Ticket

**IMPORTANT:** Check if the ticket already has a PR before choosing your workflow.

```bash
# Step 1: Get ticket details to check for existing PR
ticket_info = get_ticket(ticket_id: X)
existing_pr_url = ticket_info["pull_request_url"]

# Step 2: Choose workflow based on existing PR
if existing_pr_url
  # EXISTING PR: Follow "Fix existing PR" workflow
  # Extract PR number from URL (e.g., https://github.com/user/repo/pull/123)
  pr_number = extract_pr_number(existing_pr_url)

  # Checkout the existing PR's branch
  gh pr view #{pr_number} --json headRefName --jq '.headRefName'
  git checkout <branch_name>
  git pull origin <branch_name>

  # Rebase on main to get latest fixes (e.g. spec fixes from other branches)
  git pull --rebase origin main

  # Make your fixes, commit, push to SAME branch
  # NO new PR needed - existing PR will be updated
else
  # NEW TICKET: Follow "New feature" workflow
  # ⚠️ CRITICAL: Check current branch FIRST
  git branch --show-current    # If not 'main', go back to main!
  git checkout main
  git pull origin main

  # Create new branch for this ticket
  git checkout -b feature/<id>-description
end

# Read ticket details, understand requirements
# Follow git-workflow for commits
```

### Scenario: Fixing a Rejected PR

When you pick up a ticket that was rejected (status returned to `todo`):

1. **Ticket will have `pull_request_url` set** from the previous attempt
2. **Checkout the existing PR's branch** (don't create a new one!)
3. **Make fixes** on the existing branch
4. **Push updates** to the same branch
5. **No new PR created** - the existing PR is updated automatically

```bash
# Example workflow for rejected ticket
pr_number = extract_pr_number(ticket["pull_request_url"])  # e.g., 117
branch_name = gh pr view #{pr_number} --json headRefName --jq '.headRefName'
git checkout #{branch_name}
git pull origin #{branch_name}

# Rebase on main to get latest fixes
git pull --rebase origin main

# Make your fixes...
git add <files>
git commit -m "fix(scope): address reviewer feedback"
git push origin #{branch_name}

# PR is automatically updated, no gh pr create needed!
```

### Completing Work

Before submitting your work for review, ensure you:
- Have complete test suite passing
- Added specific tests for your changes
- Followed git-workflow for commits and PR creation

```bash
# Create PR, get URL
update_ticket(ticket_id: X, pull_request_url: "...")

# Set your worker confidence (0-100) before submitting
update_ticket(
  ticket_id: X,
  working_memory: { "worker_confidence" => 75 }  # Your confidence in the implementation
)

transition_ticket(ticket_id: X, event: "submit_review")
```

#### Setting Worker Confidence

Before submitting for review, set your confidence level (0-100):

| Range | Label | Use Case |
|-------|-------|----------|
| 0-33 | Low | Uncertain about implementation, may have issues |
| 34-66 | Medium | Reasonably confident, standard implementation |
| 67-100 | High | Very confident, well-tested, straightforward |

Examples:
- **75**: Standard feature implementation, tests pass
- **50**: Some uncertainty, edge cases may exist
- **25**: Experimental approach, not fully tested

### Asking for Input

```bash
add_comment(ticket_id: X, content: "Question: ...", comment_type: "question")
# Continue with best interpretation or wait if blocked
```

### Reporting Decisions Made

```bash
store_memory(content: "Chose X approach because...", memory_type: "decision", ticket_id: X)
```

