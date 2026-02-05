---
name: create-pull-request
description: |
  Create GitHub pull request with atomic Beads issue closure. MUST BE USED for opening PRs.
  Asks if work is complete - if YES, closes Beads issue BEFORE creating PR (JSONL merges atomically with code).
  If NO, creates draft PR with issue still open. Automatically links Beads tracking and includes Feature-Key.
  Use when user wants to open a PR, submit work for review, merge into master, or prepare for deployment,
  or when user mentions "ready for review", "create PR", "open PR", "merge conflicts", "CI checks needed",
  "branch ahead of master", PR creation, opening pull requests, deployment preparation, or submitting for team review.
tags: [workflow, github, pr, beads, review]
allowed-tools:
  - mcp__plugin_beads_beads__*
  - Bash(git:*)
  - Bash(gh:*)
  - Bash(bd:*)
  - Bash(scripts/bd-link-pr:*)
---

# Create Pull Request

Open GitHub PR with Beads integration (<10 seconds total).

## Workflow

### 1. Extract and Validate Feature Key

```bash
CURRENT_BRANCH=$(git branch --show-current)

# Validate branch naming convention
# Allow dots for hierarchical IDs (e.g., feature-bd-xyz.1.2)
if [[ ! "$CURRENT_BRANCH" =~ ^feature-bd-[a-zA-Z0-9.-]+$ ]]; then
  echo "❌ Branch name doesn't follow convention"
  echo ""
  echo "Current branch: $CURRENT_BRANCH"
  echo "Expected format: feature-bd-<ID> (e.g., feature-bd-xyz or feature-bd-xyz.1.2)"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Recovery options:"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "Option 1: Rename branch to match Beads issue"
  echo "  1. Find your Beads issue:"
  echo "     bd list --status open"
  echo ""
  echo "  2. Rename branch:"
  echo "     git branch -m feature-bd-<ID>"
  echo ""
  echo "  3. If pushed to remote:"
  echo "     git push origin :$CURRENT_BRANCH  # Delete old"
  echo "     git push -u origin feature-bd-<ID>  # Push new"
  echo ""
  echo "Option 2: Create Beads issue for current work"
  echo "  1. Extract descriptive name:"
  DESCRIPTIVE_NAME=$(echo "$CURRENT_BRANCH" | sed 's/^feature-//')
  echo "     Title: $DESCRIPTIVE_NAME"
  echo ""
  echo "  2. Create issue:"
  echo "     bd create '$DESCRIPTIVE_NAME' --type feature --priority 2"
  echo "     # Returns: bd-xyz"
  echo ""
  echo "  3. Rename branch to match:"
  echo "     git branch -m feature-bd-xyz"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Why this matters:"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "- Enables automatic PR-to-Beads linking"
  echo "- Provides commit history tracking via Feature-Key"
  echo "- Supports multi-developer coordination"
  echo "- Enforces Issue-First workflow"
  echo ""
  exit 1
fi

# Extract FEATURE_KEY from feature-bd-<ID> pattern
FEATURE_KEY=$(echo "$CURRENT_BRANCH" | sed 's/^feature-//')
```

**Why validate:**
- Enforces convention (feature-bd-xyz)
- Prevents silent failures downstream
- Provides clear recovery steps
- Educates on Issue-First workflow

### 2. Get Beads Context
Use MCP tool:
```
mcp__plugin_beads_beads__set_context(workspace_root="/path/to/project")
issue = mcp__plugin_beads_beads__show(issue_id=<FEATURE_KEY>)
```

If not found, create proactively:
```
mcp__plugin_beads_beads__create(
  title=<FEATURE_KEY>,
  issue_type="feature",
  id=<FEATURE_KEY>,
  priority=2
)
```

**Detect epic vs feature:**
- If issue is epic → PR closes all child tasks, not epic itself
- If issue is feature → PR closes the feature directly
- Check: `issue.dependents` to find child tasks

### 2.3. Structural Verification (If Needed)
If `layout.tsx`, `middleware.ts`, or global config changed:
```bash
echo "ℹ️  Structural changes detected. Running build check..."
make build
if fails: exit 1
```

### 2.4. Sync with Master (Prevent JSONL Conflicts)

**Before creating PR, merge master to prevent conflicts:**

```bash
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔄 SYNCING WITH MASTER"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Fetch latest master
git fetch origin master

# Check if .beads/issues.jsonl exists and has diverged
if [ -f .beads/issues.jsonl ]; then
  JSONL_DIVERGED=$(git diff origin/master...HEAD -- .beads/issues.jsonl | wc -l)

  if [ "$JSONL_DIVERGED" -gt 0 ]; then
    echo "⚠️  Beads JSONL has diverged from master ($JSONL_DIVERGED lines)"
    echo "   Merging master now to prevent PR conflicts..."
    echo ""

    # Merge master (union merge auto-applies for JSONL)
    if git merge origin/master --no-edit; then
      echo "✅ Merged master successfully (clean merge)"
    else
      # Check if only JSONL has conflicts
      CONFLICT_FILES=$(git diff --name-only --diff-filter=U)

      if [ "$CONFLICT_FILES" = ".beads/issues.jsonl" ]; then
        echo "✅ Auto-resolving JSONL conflict with union merge..."

        # Union merge: keep all lines from both sides
        git checkout --union .beads/issues.jsonl
        git add .beads/issues.jsonl
        git commit --no-edit -m "chore: Auto-merge JSONL (union strategy)

Feature-Key: ${FEATURE_KEY}
Agent: claude-code
Role: create-pull-request-skill"

        echo "✅ JSONL conflict resolved automatically"
      else
        echo "❌ Multiple files have conflicts, aborting auto-merge"
        echo "   Conflict files:"
        echo "$CONFLICT_FILES"
        echo ""
        echo "Please resolve conflicts manually, then run this skill again"
        git merge --abort
        exit 1
      fi
    fi

    # Run bd sync to import merged JSONL
    if command -v bd >/dev/null 2>&1; then
      echo "Running bd sync to import merged JSONL..."
      bd sync --import-only
    fi

    # Push merged changes
    echo "Pushing merged changes..."
    git push

    echo ""
    echo "✅ Synced with master, JSONL conflicts prevented"
    echo ""
  else
    echo "✅ JSONL already in sync with master"
    echo ""
  fi
else
  echo "ℹ️  No Beads JSONL file, skipping sync check"
  echo ""
fi
```

**Why this is critical:**
- **Prevents PR conflicts:** Merges master BEFORE creating PR
- **Union merge strategy:** Auto-resolves JSONL conflicts (keeps all lines)
- **Multi-agent safety:** Works across VMs (each agent syncs independently)
- **Complements GitHub Action:** Proactive prevention (skill) + reactive fallback (action)

**What happens:**
1. Check if JSONL diverged from master
2. If yes: Merge master automatically
3. If conflict: Auto-resolve with union merge (JSONL only)
4. Run `bd sync --import-only` to update local database
5. Push merged changes
6. Continue with PR creation

### 2.5. Ask if Work is Complete (CRITICAL)

**Decision point:** Is work complete and ready to merge?

```bash
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 WORK COMPLETION CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Is this work complete and ready to merge?"
echo ""
echo "✅ YES → Close Beads issue, create PR for merge"
echo "⏸️  NO  → Leave open, create draft PR for feedback"
echo ""
read -p "Complete? (y/n): " COMPLETE
echo ""
```

**If YES (work complete):**
```bash
# Close Beads issue BEFORE creating PR
echo "Closing Beads issue ${FEATURE_KEY}..."
bd close ${FEATURE_KEY} --reason "Work complete, ready for review in PR"

# Export and commit JSONL to feature branch
echo "Syncing Beads state to feature branch..."
bd sync

# Push to include JSONL in PR
echo "Pushing branch with JSONL..."
git push

echo ""
echo "✅ Issue closed and JSONL committed to feature branch"
echo "   → JSONL will merge atomically with code"
echo ""
```

**If NO (work in progress):**
```bash
# Leave issue as in_progress
echo "ℹ️  Keeping ${FEATURE_KEY} as in_progress"
echo "   → PR will be marked as draft"
echo ""

DRAFT_FLAG="--draft"
```

**Why this is critical:**
- **Atomic merge:** JSONL closes issue on feature branch → merges with code
- **No post-merge mutations:** Never need to modify JSONL on master
- **Prevents hook conflicts:** All Beads state changes happen on feature branch
- **Clear workflow:** Close issue = "ready to ship", open issue = "work in progress"

### 2.6. Validate Docs (Epics/Features Only)

**Check if docs exist and are linked:**

```bash
DOC_DIR="docs/${FEATURE_KEY}"

if [ "$issue.type" = "epic" ] || [ "$issue.type" = "feature" ]; then
  # Check if docs directory exists
  if [ -d "$DOC_DIR" ]; then
    # Check if linked to Beads
    CURRENT_REF=$(bd show ${FEATURE_KEY} --json | jq -r '.external_ref // ""')

    if [ -z "$CURRENT_REF" ] || [ "$CURRENT_REF" = "null" ]; then
      echo "ℹ️  Docs exist but not linked to Beads"
      echo "   Auto-linking: ${FEATURE_KEY} ↔ ${DOC_DIR}/"
      bd update ${FEATURE_KEY} --external-ref "docs:${DOC_DIR}/"
    fi

    # Check if docs updated recently (within last 7 days)
    LAST_COMMIT=$(git log -1 --format=%at -- "$DOC_DIR")
    NOW=$(date +%s)
    DAYS_AGO=$(( ($NOW - $LAST_COMMIT) / 86400 ))

    if [ $DAYS_AGO -gt 7 ]; then
      echo ""
      echo "⚠️  Docs may be stale (last updated ${DAYS_AGO} days ago)"
      echo "   Consider reviewing: $DOC_DIR/"
      echo ""
    else
      echo "✅ Docs updated recently ($DAYS_AGO days ago)"
    fi
  else
    # No docs directory - informational only
    echo "ℹ️  No docs/ directory for ${FEATURE_KEY}"
    echo "   (OK for small features, recommended for epics)"
  fi
fi
```

**Why informational:**
- Non-blocking (doesn't prevent PR creation)
- Epics/features benefit from docs, but not required
- Tasks/bugs don't need separate docs
- User controls doc creation timing

**What this checks:**
- ✅ Docs exist? → Auto-link to Beads if not linked
- ✅ Docs recent? → Warn if stale (>7 days)
- ℹ️ No docs? → Informational (not error)

### 3. Push Branch
```bash
# Check if branch exists on remote
if ! git ls-remote --heads origin <branch>:
  git push -u origin <branch>
```

### 4. Create PR with gh CLI

**Prepare doc link:**
```bash
DOC_DIR="docs/${FEATURE_KEY}"
if [ -d "$DOC_DIR" ]; then
  DOC_LINK="📄 Design docs: [\`$DOC_DIR/\`]($DOC_DIR/)"
else
  DOC_LINK="📄 No docs/ directory (tracked in Beads only)"
fi
```

**For Features:**
```bash
gh pr create \
  ${DRAFT_FLAG} \
  --title "{FEATURE_KEY}: Feature implementation" \
  --body "
## Feature

{FEATURE_KEY}

## Beads Issue

$(if [ -z "$DRAFT_FLAG" ]; then echo "Closes: bd-{ID}"; else echo "Related: bd-{ID} (in progress)"; fi)

See: `.beads/issues.jsonl` (line with id: bd-{ID})

## Documentation

${DOC_LINK}

## Next Steps

- Dev environment: Auto-deploying
- CI checks: Running in background
- Review: $(if [ -z "$DRAFT_FLAG" ]; then echo "Ready once CI passes"; else echo "Ready when work complete"; fi)

---

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
  " \
  --base master
```

**For Epics (closes child tasks, not epic):**
```bash
gh pr create \
  --title "{FEATURE_KEY}: Epic implementation" \
  --body "
## Epic

{FEATURE_KEY}

## Beads Issues

**This PR completes the following tasks:**
- Closes: bd-{ID}.1 (Research)
- Closes: bd-{ID}.2 (Spec)
- Closes: bd-{ID}.3 (Implementation)
- Closes: bd-{ID}.4 (Testing)

**Epic:** bd-{ID} (remains open for future work)

See: `.beads/issues.jsonl`

## Documentation

${DOC_LINK}

## Next Steps

- Dev environment: Auto-deploying
- CI checks: Running in background
- Review: Ready once CI passes

---

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
  " \
  --base master
```

### 5. Link PR to Beads
```bash
PR_NUMBER=$(gh pr view --json number -q .number)

# Use helper script if available
scripts/bd-link-pr $PR_NUMBER

# Or update via MCP
mcp__plugin_beads_beads__update(
  issue_id=<FEATURE_KEY>,
  status="in_progress",
  external_ref="PR#{PR_NUMBER}"
)
```

### 6. Confirm to User
```
✅ PR#{PR_NUMBER} created
✅ CI running in background
✅ Dev environment deploying

Check status: gh pr view {PR_NUMBER}
Test in dev: dev.yourapp.com/pr-{PR_NUMBER}
```

## Best Practices

- **Create Beads issue if missing** - Never block on missing metadata
- **Use gh CLI** - More reliable than API calls
- **Link PR bidirectionally** - Beads → PR and PR → Beads
- **Trust async validation** - CI runs in background

## What Happens Next (Automatic)

- ✅ CI runs full test suite
- ✅ Dev environment auto-deploys PR
- ✅ GitHub posts check results
- ✅ Danger bot comments with guidance

**User can test immediately** in dev environment while CI runs.

## What This DOESN'T Do

- ❌ Wait for CI (runs async)
- ❌ Run tests locally (CI handles it)
- ❌ Validate deployment (environments handle it)

**Philosophy:** Fast PR creation + Trust the pipeline
