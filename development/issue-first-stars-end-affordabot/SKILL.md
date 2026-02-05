---
name: issue-first
description: |
  Enforce Issue-First pattern by creating Beads tracking issue BEFORE implementation. MUST BE USED for all implementation work.
  Classifies work type (epic/feature/task/bug/chore), determines priority (0-4), finds parent in hierarchy, creates issue, then passes control to implementation.
  Use when starting implementation work,
  or when user mentions "no tracking issue", "missing Feature-Key", work classification,
  creating features, building new systems, beginning development, or implementing new functionality.
tags: [workflow, beads, issue-tracking, implementation]
allowed-tools:
  - mcp__plugin_beads_beads__*
  - Bash(git:*)
  - Bash(bd:*)
---

# Issue-First Enforcement

Create Beads tracking issue BEFORE implementation (<30 seconds).

## Purpose

Ensures **Issue-First** pattern: All implementation work tracked in Beads BEFORE coding starts.

**Philosophy:** Fast classification + Hierarchical tracking + No lost work

## When to Use This Skill

**Auto-activated when:**
- User says "create X", "implement Y", "build Z"
- User says "fix bug", "refactor X", "update Y"
- User starts ANY implementation work without Beads issue

**Trigger phrases:**
- "create the X skill"
- "implement authentication"
- "fix the bug in X"
- "refactor Y component"
- "update Z service"

## Workflow

### 1. Set Beads Context

```typescript
mcp__plugin_beads_beads__set_context(
  workspace_root="/Users/fengning/prime-radiant-ai"
)
```

### 2. Check if Issue Already Exists

```typescript
// Check current branch
currentBranch = git branch --show-current
// Extract Feature-Key if exists

if (currentBranch.startsWith("feature-")) {
  featureKey = extract_key(currentBranch)

  try {
    issue = mcp__plugin_beads_beads__show(issue_id=featureKey)
    // Issue exists, use it
    echo "✓ Using existing issue: ${issue.id}"
    return issue
  } catch {
    // No issue, continue to create
  }
}
```

### 3. Classify Work Type

**Ask user to classify:**

```
What type of work is this?

1. **epic** - Large feature with multiple phases (weeks)
   Examples: Authentication system, analytics dashboard

2. **feature** - New functionality (days)
   Examples: Add OAuth login, create export feature

3. **task** - Work item (hours to days)
   Examples: Write tests, update docs, refactor code

4. **bug** - Something broken (varies)
   Examples: Fix session timeout, resolve API error

5. **chore** - Maintenance (hours)
   Examples: Update dependencies, improve tooling
```

**User provides:** Type

### 4. Determine Priority

**Ask user to confirm priority:**

```
What priority? (Based on Beads convention)

0. **Critical** - Security, data loss, broken builds
1. **High** - Major features, important bugs
2. **Medium** - Default, nice-to-have (RECOMMENDED)
3. **Low** - Polish, optimization
4. **Backlog** - Future ideas
```

**User provides:** Priority number (default: 2)

### 5. Find Parent in Hierarchy

**Analyze Beads context:**

```typescript
// Get current context
currentContext = bash: scripts/bd-context

// Parse for current epic/feature
if (currentContext contains epic or feature in_progress) {
  parentIssue = current epic/feature
} else {
  // Ask user
  readyWork = mcp__plugin_beads_beads__ready()

  echo "Current work context:"
  for issue in readyWork:
    echo "  ${issue.id}: ${issue.title} (${issue.type})"

  echo "\nIs this work under one of these? (or standalone?)"
}
```

**Determine:**
- Parent issue ID (if applicable)
- Hierarchical ID pattern (bd-xyz.N if child)

### 6. Create Tracking Issue

**Generate title:**
```
Format: [TYPE_PREFIX]: [DESCRIPTION]

Prefixes:
- epic: No prefix, just description
- feature: No prefix, just description
- task: "Task: " or phase-specific (Research/Spec/Implementation/Testing)
- bug: "Bug: "
- chore: "Chore: "
```

**Create issue:**
```typescript
issue = mcp__plugin_beads_beads__create({
  title: generated_title,
  issue_type: work_type,  // epic/feature/task/bug/chore
  priority: priority_num,  // 0-4
  description: user_description,
  assignee: "claude-code",
  deps: parent_id ? [parent_id] : undefined,
  id: hierarchical_id  // e.g., bd-xpi.7 if child
})
```

**Start work immediately:**
```typescript
mcp__plugin_beads_beads__update(
  issue.id,
  status="in_progress"
)
```

### 7. Optional: Setup Documentation

**For epics and features only:**

```typescript
if (issue.type === "epic" || issue.type === "feature") {
  echo "\n📄 Setup documentation?"
  echo "   [y] Yes - Create docs/${issue.id}/ with templates"
  echo "   [n] No - Just track in Beads"
  echo "   (Recommended for epics/features)"

  read choice

  if (choice === "y") {
    // Call helper script
    bash: scripts/setup-feature-docs ${issue.id} "${issue.title}" ${issue.type}

    // Commit doc setup
    bash: git commit -m "docs: initialize ${issue.id} documentation

Feature-Key: ${issue.id}
Agent: claude-code
Role: doc-setup"

    echo "\n✅ Documentation created: docs/${issue.id}/"
  }
}
```

**Why optional:**
- Tasks/bugs don't need docs (update parent docs)
- User controls (can say no)
- Epics/features benefit most from templates

### 8. Confirm and Pass Control

**Confirm to user:**
```
✅ Created tracking issue: ${issue.id}
📋 Type: ${issue.type} | Priority: P${issue.priority}
🔗 Parent: ${parent_id || 'standalone'}
📍 Status: in_progress
📄 Docs: ${docs_created ? `docs/${issue.id}/` : 'None (Beads only)'}

Proceed with implementation using Feature-Key: ${issue.id}
```

**Optional: External Documentation**

If this epic/feature requires external reference docs (API docs, guides, tool documentation):

```
💡 Tip: Create epic-specific doc skill with:
   /docs-create ${issue.id} <url1> <url2> <url3> ...

This caches docs and creates auto-activating skill for this epic.
```

Only mention if user hasn't already set up docs. Keep it brief - just a pointer, not required.

### 9. Auto-Create Feature Branch (When on Master)

**For epics, features, and P0-P1 work only:**

After creating the Beads issue, automatically create a matching git branch if currently on master.

**Decision Logic:**
```typescript
const currentBranch = git branch --show-current
const shouldCreateBranch = (
  currentBranch === "master" &&
  (issue.type === "epic" ||
   issue.type === "feature" ||
   issue.priority <= 1)
)

if (!shouldCreateBranch) {
  // Skip if:
  // - Already on a feature branch (resume work)
  // - Working on tasks/bugs/chores (P2+, trunk workflow OK)
  return
}
```

**Branch Creation Flow:**
```bash
# Auto-create branch (no prompt when on master)
echo "\n🌿 Creating feature branch for ${issue.id}..."
echo "   Branch name: feature-${issue.id}"
echo "   (Auto-created for ${issue.type}, P${issue.priority} on master)"
echo ""
# Call helper script (handles all edge cases)
bash scripts/git-create-feature-branch "${issue.id}" "${issue.type}" ${issue.priority}

exit_code=$?

case $exit_code in
  0)
    # Success
    echo "✅ Branch created: feature-${issue.id}"
    echo "   Ready to code!"
    ;;

  3)
    # Needs commit first
    echo "⚠️  Uncommitted changes detected on master."
    echo "   Auto-committing current work before branch creation..."
    echo ""

    # Invoke sync-feature-branch skill automatically
    # (User would say: "commit my work")
    # After commit completes, retry branch creation
    bash scripts/git-create-feature-branch "${issue.id}" "${issue.type}" ${issue.priority}
    ;;

  *)
    # Error
    echo "❌ Failed to create branch"
    echo "   Falling back to master branch workflow."
    echo "   You can manually create branch later: git checkout -b feature-${issue.id}"
    ;;
esac
```

**Why Automatic (No Prompt):**
- Prevents accidental commits to master for large/important work
- Small tasks/bugs (P2+) still use trunk workflow (not auto-created)
- Auto-detects uncommitted changes and commits them first
- Guarantees clean git state before branch creation
- User requested: "wouldn't that have made the process way easier?" (bd-axb)

**Clean State Guarantees:**

The `git-create-feature-branch` script ensures:

1. ✅ **Pre-flight checks:**
   - Uncommitted changes → Offer auto-commit via sync-feature-branch
   - Staged changes → Offer auto-commit
   - Untracked files → Warn (won't carry over)
   - Branch exists → Error
   - Not in repo → Error

2. ✅ **Creation:**
   - Always create from master/main (latest)
   - Never carry uncommitted changes
   - Checkout new branch automatically

3. ✅ **Post-verification:**
   - Verify on correct branch
   - Verify clean working tree
   - Verify no staged changes

**Next Step: Check for Matching Skill**

Before implementing directly, check if a specialized subagent or skill exists:

1. **For complex work, use specialized subagents** (`.claude/agents/`):
   - "backend/api/service/endpoint" → Task(subagent_type="backend-engineer")
   - "frontend/component/ui/page" → Task(subagent_type="frontend-engineer")
   - "security/auth/encryption" → Task(subagent_type="security-engineer")
   - "devops/ci/deployment" → Task(subagent_type="devops-engineer")
   - "testing/e2e/integration" → Task(subagent_type="quality-assurance-tester")

2. **For workflow automation, use skills** (`.claude/skills/`):
   - "create skill" → skill-creator
   - "commit work" → sync-feature-branch
   - "open PR" → create-pull-request

3. **If using subagent:**
   ```
   Task(
     subagent_type="subagent-name",
     prompt="Implement ${issue.title} for ${issue.id}"
   )
   ```

4. **If no specialized tool:**
   Implement directly using Feature-Key: ${issue.id}

**Implementation continues with:**
- Feature-Key: ${issue.id}
- All commits include Feature-Key trailer
- Close issue when complete

## Classification Rules

### Epic vs Feature

| Indicator | Epic | Feature |
|-----------|------|---------|
| Time | Weeks | Days |
| Scope | Multiple phases | Single capability |
| Deliverables | Multiple PRs | Single PR |
| Complexity | Requires breaking down | Focused implementation |

**Examples:**
- "Authentication system" → Epic (OAuth + JWT + sessions + 2FA)
- "Add OAuth login button" → Feature (single component)

### Task vs Bug vs Chore

| Type | When | Examples |
|------|------|----------|
| **task** | Work item, not broken | Tests, docs, refactor, research |
| **bug** | Something broken | Timeout not handled, API 500 error |
| **chore** | Maintenance | Update deps, improve tooling, cleanup |

### Priority Guidelines

| Priority | Use When | Examples |
|----------|----------|----------|
| **P0 (Critical)** | Production broken, security, data loss | SQL injection, broken build, data corruption |
| **P1 (High)** | Blocking work, major features | Auth broken, key feature needed for launch |
| **P2 (Medium)** | Default, most work | New features, improvements, most bugs |
| **P3 (Low)** | Nice-to-have | Polish, minor optimizations |
| **P4 (Backlog)** | Future consideration | Ideas, maybe someday |

## Hierarchical ID Assignment

**Pattern:**
```
bd-xyz (Parent)
├── bd-xyz.1 (Child 1)
├── bd-xyz.2 (Child 2)
│   ├── bd-xyz.2.1 (Grandchild 1)
│   └── bd-xyz.2.2 (Grandchild 2)
└── bd-xyz.3 (Child 3)
```

**How to determine ID:**

```typescript
if (parentIssue exists) {
  // Get existing children
  parent = mcp__plugin_beads_beads__show(parent_id)

  // Count children (dependents with discovered-from or blocks)
  childCount = parent.dependents.filter(d =>
    d.type === "discovered-from" || d.type === "blocks"
  ).length

  // Next child ID
  hierarchical_id = `${parent_id}.${childCount + 1}`
} else {
  // Standalone issue, Beads auto-generates ID
  hierarchical_id = undefined  // Let Beads assign bd-xxx
}
```

## Integration Points

### With Beads

**Core operations:**
- `set_context()` - Required first step
- `show()` - Check if issue exists
- `ready()` - Find parent context
- `create()` - Create tracking issue
- `update()` - Set status to in_progress

**Hierarchy:**
- Use `deps` parameter for parent-child
- Hierarchical IDs track structure
- discovered-from for work found during implementation

### With Implementation

**After issue-first completes:**
1. User proceeds with implementation
2. All commits include: `Feature-Key: ${issue.id}`
3. When done: Close issue via sync-feature-branch or manually
4. PR links to issue automatically

### With Other Skills

**Relationship:**
- **issue-first** → Creates tracking issue
- **beads-workflow** → Creates epics with phases (uses issue-first internally)
- **sync-feature-branch** → Commits with Feature-Key
- **create-pull-request** → Links PR to issue

## Best Practices

### Do

✅ Always create issue BEFORE coding
✅ Classify accurately (epic/feature/task/bug/chore)
✅ Use correct priority (P2 default)
✅ Link to parent when applicable
✅ Set status to in_progress immediately
✅ Use hierarchical IDs for children
✅ Commit with Feature-Key: ${issue.id}

### Don't

❌ Skip for "quick fixes" (>10 lines = not quick)
❌ Create issue after implementation starts
❌ Guess at classification (ask user)
❌ Default everything to feature
❌ Forget to link to parent
❌ Leave status as open (start work immediately)

## What This Skill Does

✅ Detects implementation work without tracking issue
✅ Classifies work type (epic/feature/task/bug/chore)
✅ Determines priority (0-4)
✅ Finds parent in Beads hierarchy
✅ Generates hierarchical ID if child
✅ Creates Beads tracking issue
✅ Sets status to in_progress
✅ **Offers to create feature branch (epics/features/P0-P1)**
✅ **Ensures clean git state before branch creation**
✅ **Auto-recovers from uncommitted changes**
✅ Passes control to implementation with Feature-Key

## What This Skill DOESN'T Do

❌ Implement the actual work (just creates tracking)
❌ Force creation for tiny edits (<10 lines)
❌ Create issue if one already exists
❌ Block workflow (fast classification only)
❌ Make decisions without user input

## Examples

### Example 1: Create Skill (Task)

```
Hook detects: "create the skill-creator skill"

issue-first activates:

1. Set Beads context ✓
2. Check existing: No issue found
3. Classify:
   User: "This is a task"
   AI: ✓ task

4. Priority:
   AI: "Default P2 for normal work?"
   User: "Yes, P2"

5. Parent:
   AI detects: bd-xpi (DX_V3_BEADS_INTEGRATION) in progress
   AI: "This work is under bd-xpi?"
   User: "Yes"

   Children of bd-xpi: bd-xpi.1 through bd-xpi.6 exist
   Next ID: bd-xpi.7

6. Create:
   mcp__plugin_beads_beads__create({
     title: "Implementation: skill-creator meta-skill",
     issue_type: "task",
     priority: 2,
     id: "bd-xpi.7",
     deps: ["bd-xpi"],
     assignee: "claude-code"
   })

7. Confirm:
   ✅ Created: bd-xpi.7
   📋 Type: task | Priority: P2
   🔗 Parent: bd-xpi
   📍 Status: in_progress

   Feature-Key: bd-xpi.7

User proceeds with skill-creator implementation.
```

### Example 2: Fix Bug (Bug)

```
User: "fix the session timeout bug"

issue-first:

1. Classify: bug (something broken)
2. Priority: P1 (high - security/ux issue)
3. Parent: bd-auth (current authentication work)
   Next ID: bd-auth.3

4. Create:
   mcp__plugin_beads_beads__create({
     title: "Bug: Session timeout not handled",
     issue_type: "bug",
     priority: 1,
     id: "bd-auth.3",
     deps: ["bd-auth"]
   })

5. Status: in_progress

Feature-Key: bd-auth.3

User proceeds with bug fix.
```

### Example 3: Standalone Feature

```
User: "add export to CSV feature"

issue-first:

1. Classify: feature
2. Priority: P2
3. Parent: None (standalone)

4. Create:
   mcp__plugin_beads_beads__create({
     title: "CSV_EXPORT_FEATURE",
     issue_type: "feature",
     priority: 2,
     assignee: "claude-code"
   })
   # Returns: bd-new (Beads auto-generates)

5. Status: in_progress

Feature-Key: bd-new

User proceeds with CSV export implementation.
```

## Troubleshooting

### Issue Already Exists

**Symptom:** Beads says "issue ID already exists"

**Solution:** Check current branch/context, use existing issue instead of creating new one

### Can't Determine Parent

**Symptom:** Unclear what parent should be

**Solution:**
```typescript
// Show all in-progress work
mcp__plugin_beads_beads__list(status="in_progress")

// Ask user to choose or create standalone
```

### Classification Unclear

**Symptom:** User unsure if epic vs feature, or task vs bug

**Solution:**
- Epic vs Feature: Ask about timeline and phases
- Task vs Bug: Ask "is something broken?" (bug) or "is this new work?" (task)

## Related Skills

- **beads-workflow**: Creates epics with phase tasks (uses issue-first pattern)
- **sync-feature-branch**: Commits with Feature-Key from this skill
- **create-pull-request**: Links PR to issue created by this skill
- **fix-pr-feedback**: Creates child issues using same pattern

## Resources

**Beads reference:**
- Official AGENTS.md: https://github.com/steveyegge/beads/blob/main/AGENTS.md
- Issue types: bug, feature, task, epic, chore
- Priorities: 0 (critical) → 4 (backlog)
- Hierarchical IDs: bd-xyz.N pattern

---

**Last Updated:** 2025-01-17
**Skill Type:** Workflow
**Average Duration:** <30 seconds (+ branch creation if opted)
**Related Docs:**
- https://github.com/steveyegge/beads/blob/main/AGENTS.md
- .claude/skills/beads-workflow/SKILL.md
- AGENTS.md (Issue-First core principle)
**Related Scripts:**
- scripts/git-create-feature-branch
- scripts/lib/git-state-checks.sh
