---
name: git-squash
description: Safely squash multiple commits into one with automatic backup and verification
allowed-tools: Bash, Read
---

# Git Squash Skill

**Purpose**: Safely squash multiple consecutive commits into a single commit with automatic backup, verification, and cleanup.

**When to Use**:
- Cleaning up commit history before merge
- Combining related commits into logical units
- Simplifying pull request history
- Preparing feature branch for main merge

## Squash vs Fixup: Choosing the Right Command

**CRITICAL**: When combining commits via interactive rebase, use the correct command:

| Command | Message Behavior | When to Use |
|---------|-----------------|-------------|
| `squash` | Opens editor with ALL commit messages combined | Different features/changes being combined |
| `fixup` | Discards secondary commit messages | Incremental fixes (typos, "oops forgot file") |

**⚠️ COMMON MISTAKE**: Using `fixup` when combining commits about different features.

```bash
# ❌ WRONG - Using fixup loses important context
pick abc123 Add FQN rule example
fixup def456 Add assert that() pattern      # Message discarded!
fixup ghi789 Add Instant/Duration patterns  # Message discarded!
# Result: Commit message only mentions FQN rule

# ✅ CORRECT - Using squash preserves all messages
pick abc123 Add FQN rule example
squash def456 Add assert that() pattern      # Message preserved
squash ghi789 Add Instant/Duration patterns  # Message preserved
# Result: Editor opens with all 3 messages for editing
```

**Decision Rule**:
- **Same logical change** (fix typo, add forgotten file, fix test) → Use `fixup`
- **Different logical changes** (different features, different rules) → Use `squash`

**When in doubt**: Use `squash` - you can always edit the combined message, but `fixup` irreversibly
discards messages.

## Default Behavior: Squash Into Earliest Commit

**When squashing multiple commits, the default is to squash into the EARLIEST (first) commit in the sequence.**

**Example**: Given commits in chronological order:
```
abc123 First commit   ← EARLIEST (squash target)
def456 Second commit  ← squashed into abc123
ghi789 Third commit   ← squashed into abc123
```

Running `squash abc123 def456 ghi789` produces:
```
xyz999 Combined commit (contains changes from all three)
```

**Why earliest?**:
- Preserves original authorship timestamp
- Maintains logical sequence (feature start → incremental changes)
- Matches git's native squash behavior in interactive rebase
- The "base commit" in this skill is the PARENT of the earliest commit

**To squash into a different commit**: Explicitly specify by reordering in interactive rebase, or use the cherry-pick approach documented in "Squashing Non-Adjacent Commits" section.

## Multiple Independent Squash Requests

**CRITICAL**: When multiple squash requests are received in sequence, treat each as an **independent operation** unless the user explicitly relates them.

**Example**:
```
User: Squash commits A, B, C into one
User: Squash commits X, Y into one
```

**Correct interpretation**: Two separate squash operations
1. First squash: Combine A, B, C
2. Second squash: Combine X, Y

**Wrong interpretation**: ~~Second request replaces or modifies first request~~

**When requests ARE related**: User will explicitly state the relationship:
- "Actually, squash A, B, C, X, Y all together" (combines both requests)
- "Instead of A, B, C, squash just A and B" (replaces first request)
- "In addition to the previous squash, also squash..." (adds to previous)

**Default assumption**: Each squash request is independent and should be executed separately.

## Archival Files in Multi-Commit Patterns {#archival-multi-commit}

**⚠️ CRITICAL**: When organizing commits into a multi-commit pattern (e.g., code/docs/config separation),
archival files (`todo.md` and `changelog.md`) MUST be included in the appropriate existing commit - NOT
added as a separate commit.

### Archival File Placement Rules

| Commit Pattern | Where Archival Goes | Rationale |
|----------------|---------------------|-----------|
| Single commit | Same commit | All changes together |
| code / docs | `[docs]` commit | Archival is documentation |
| code / docs / config | `[docs]` commit | Archival is documentation |
| implementation / config | Implementation commit | No separate docs commit |

### Common Mistake

```bash
# ❌ WRONG - Archival as separate 4th commit
[code] feat: Add feature implementation
[docs] docs: Update JavaDoc
[config] chore: Update CLAUDE.md
[archival] docs: Update todo.md and changelog.md  # UNNECESSARY 4TH COMMIT!

# ✅ CORRECT - Archival included in docs commit
[code] feat: Add feature implementation
[docs] docs: Update JavaDoc, todo.md, changelog.md  # ARCHIVAL INCLUDED HERE
[config] chore: Update CLAUDE.md
```

### When Hook Blocks Merge for Missing Archival

If merge is blocked because archival files are missing AFTER commits are already organized:

```bash
# Scenario: 3 commits already organized, hook blocks for missing archival

# ✅ CORRECT: Amend the docs commit to include archival
git log --oneline -3
# abc123 [config] chore: Update CLAUDE.md
# def456 [docs] docs: Update JavaDoc       ← AMEND THIS ONE
# ghi789 [code] feat: Add feature

# Step 1: Interactive rebase to edit the docs commit
git rebase -i ghi789^  # Parent of first commit

# Step 2: Mark docs commit for edit (change 'pick' to 'edit')
# pick ghi789 [code] feat: Add feature
# edit def456 [docs] docs: Update JavaDoc   ← Change to 'edit'
# pick abc123 [config] chore: Update CLAUDE.md

# Step 3: When rebase stops, add archival and amend
# (Edit todo.md and changelog.md)
git add todo.md changelog.md
git commit --amend --no-edit
git rebase --continue

# ❌ WRONG: Create new commit for archival
git add todo.md changelog.md
git commit -m "docs: Update archival"  # Creates unnecessary 4th commit!
```

### Pre-Squash Archival Checklist

Before finalizing a multi-commit pattern, verify:

- [ ] Archival files (todo.md, changelog.md) are updated
- [ ] Archival is included in an existing commit (not separate)
- [ ] If docs commit exists: archival is in docs commit
- [ ] If no docs commit: archival is in implementation commit
- [ ] `git show --stat <docs-commit>` shows both todo.md AND changelog.md

## Supports Both Tip and Mid-History Squashing

**This skill now handles both scenarios**:

### ✅ Tip Squashing (commits at branch HEAD)
```bash
# Current state:
# HEAD → 043a992 (commit 7) ← Last to squash
#        ...     (commits 1-6) ← Squash these
#        61edb5a (base)

# Simple case: No commits after squash range
# Workflow: Squash → Move branch pointer
```

### ✅ Mid-History Squashing (commits have others after them)
```bash
# Current state:
# HEAD → 39f3981 (commit 10)
#        a25506b (commit 9)
#        4a2e49a (commit 8)
#        043a992 (commit 7) ← Last to squash
#        ...     (commits 1-6) ← Squash these
#        61edb5a (base)

# Mid-history case: Commits exist after squash range
# Workflow: Squash → Rebase commits after → Move branch pointer
# Commits 8-10 are automatically rebased on top of squashed commit
```

**The skill automatically detects which scenario and handles it appropriately.**

**Alternative: Interactive Rebase**

You can also use interactive rebase for mid-history squashing:
```bash
git rebase -i <base-commit>
# Change "pick" to "squash" for commits to combine
```

Both approaches work. git-squash provides more safety checks and verification,
while interactive rebase is the traditional git approach.

## ⚡ Performance: Optimized Script Available

**RECOMMENDED**: Use the optimized batch script for 85% faster execution

**Performance Comparison**:
- Traditional workflow: 9-11 LLM round-trips, 45-90 seconds
- Optimized script: 2-3 LLM round-trips, 5-10 seconds
- Safety checks: All preserved (no reduction)

**When to use optimized script**:
- ✅ Squashing adjacent commits (common case)
- ✅ Simple squash without conflicts
- ✅ Want minimal LLM involvement

**When to use manual workflow**:
- Complex mid-history squashing with potential conflicts
- Need to understand each step in detail
- Learning the git squash process

**Optimized Script Reference**: See [Usage § Optimized Script](#optimized-script-recommended) section below

## ⚠️ Critical Safety Rules

**MANDATORY BACKUP**: Always create timestamped backup before squashing
**VERIFICATION REQUIRED**: Verify no changes lost or added beyond original commits
**NON-SQUASHED COMMITS**: Verify commits outside squash range remain completely unchanged
**FINAL STATE VERIFICATION**: Verify working tree state matches original HEAD
**AUTOMATIC CLEANUP**: Remove backup only after verification passes
**WORKING DIRECTORY**: Must be clean (no uncommitted changes)

## Prerequisites

Before using this skill, verify:
- [ ] Working directory is clean: `git status` shows no uncommitted changes
- [ ] Know base commit (where to squash back to - parent of first commit to squash)
- [ ] Know first and last commits to squash
- [ ] **HEAD is positioned at the LAST commit to squash** (not beyond it)
- [ ] Current branch is correct

**⚠️ CRITICAL**: If HEAD has commits beyond the last commit you want to squash,
you will squash MORE commits than intended. Ensure HEAD is exactly at the
last commit to include in the squash before running this skill.

## Skill Workflow

### Step 1: Position HEAD (MANDATORY - DO NOT SKIP)

**🚨 CRITICAL: This step is MANDATORY and must be done FIRST**

```bash
# YOU MUST checkout the last commit to squash BEFORE creating backup
git checkout <last-commit-to-squash>

# Example: If squashing commits abc123 and def456, checkout def456
git checkout def456
```

**Why this is mandatory**:
- If HEAD is beyond the last commit to squash, you'll squash MORE commits than intended
- Example: HEAD at main with commits after def456 → squashes everything from base to main
- This was the exact mistake that occurred and required adding this checkpoint

**Verification**:
```bash
# Verify you're at the right commit
git log --oneline -1
# Should show the LAST commit you want to include in the squash
```

**⚠️ DO NOT PROCEED to Step 2 until you've verified HEAD position**

### Step 2: Create Mandatory Backup

**⚠️ CRITICAL - Always Create Backup First**:
```bash
# Create timestamped backup branch
BACKUP_BRANCH="backup-before-squash-$(date +%Y%m%d-%H%M%S)"
git branch "$BACKUP_BRANCH"

# Verify backup created
if ! git rev-parse --verify "$BACKUP_BRANCH" >/dev/null 2>&1; then
  echo "❌ ERROR: Failed to create backup - STOP"
  exit 1
fi

echo "✅ Backup created: $BACKUP_BRANCH"
echo "   Restore command if needed: git reset --hard $BACKUP_BRANCH"
```

### Step 3: Verify Preconditions

**Check Working Directory**:
```bash
# Ensure no uncommitted changes
if [[ -n "$(git status --porcelain)" ]]; then
  echo "❌ ERROR: Working directory not clean"
  echo "   Commit or stash changes first"
  exit 1
fi

echo "✅ Working directory clean"
```

**Identify Commits to Squash**:
```bash
# Specify the range to squash
BASE_COMMIT="<commit-sha>"     # Parent of first commit to squash
EXPECTED_LAST_COMMIT="<commit-sha>"  # Last commit to include in squash (optional but recommended)

# Verify HEAD position if EXPECTED_LAST_COMMIT is specified
if [[ -n "$EXPECTED_LAST_COMMIT" ]]; then
  CURRENT_HEAD=$(git rev-parse HEAD)
  EXPECTED_HEAD=$(git rev-parse "$EXPECTED_LAST_COMMIT")

  if [[ "$CURRENT_HEAD" != "$EXPECTED_HEAD" ]]; then
    echo "❌ ERROR: HEAD is not at expected last commit!"
    echo "   Current HEAD:  $(git log --oneline -1 HEAD)"
    echo "   Expected HEAD: $(git log --oneline -1 "$EXPECTED_LAST_COMMIT")"
    echo ""
    echo "   You may be about to squash MORE commits than intended."
    echo "   Checkout the last commit before squashing:"
    echo "   git checkout $EXPECTED_LAST_COMMIT"
    exit 1
  fi
  echo "✅ HEAD positioned at expected last commit"

  # Check for commits AFTER the squash range (mid-history squashing)
  if git rev-parse --verify "$ORIGINAL_BRANCH" >/dev/null 2>&1; then
    COMMITS_AFTER_COUNT=$(git rev-list --count HEAD.."$ORIGINAL_BRANCH" 2>/dev/null || echo "0")
    if [[ "$COMMITS_AFTER_COUNT" -gt 0 ]]; then
      echo "⚠️  Mid-history squash detected: $COMMITS_AFTER_COUNT commits exist after squash range"
      echo "   Will automatically rebase them after squashing"
      echo ""

      # Record the original branch HEAD and commits after squash range
      ORIGINAL_BRANCH_HEAD=$(git rev-parse "$ORIGINAL_BRANCH")
      NEED_REBASE="true"
      echo "ORIGINAL_BRANCH_HEAD=$ORIGINAL_BRANCH_HEAD" >> /tmp/squash-vars.sh
      echo "NEED_REBASE=true" >> /tmp/squash-vars.sh
      echo "COMMITS_AFTER_COUNT=$COMMITS_AFTER_COUNT" >> /tmp/squash-vars.sh

      echo "   Commits to preserve after squash:"
      git log --oneline HEAD.."$ORIGINAL_BRANCH"
      echo ""
    else
      echo "✅ No commits after squash range (tip squashing)"
      echo "NEED_REBASE=false" >> /tmp/squash-vars.sh
    fi
  else
    echo "NEED_REBASE=false" >> /tmp/squash-vars.sh
  fi
fi

# Show commits to be squashed
echo "Commits to squash:"
git log --oneline "$BASE_COMMIT..HEAD"
echo ""

# Count commits
COMMIT_COUNT=$(git rev-list --count "$BASE_COMMIT..HEAD")
echo "Will squash $COMMIT_COUNT commits into 1"
```

### Step 4: Record Original State

**⚠️ CRITICAL - Record State for Verification**:
```bash
# Record original HEAD for final state verification
ORIGINAL_HEAD=$(git rev-parse HEAD)
echo "Original HEAD: $ORIGINAL_HEAD"

# Verify BASE_COMMIT exists
if ! git rev-parse --verify "$BASE_COMMIT" >/dev/null 2>&1; then
  echo "❌ ERROR: Base commit $BASE_COMMIT does not exist"
  exit 1
fi

# CRITICAL: Verify HEAD is at or within the squash range
# If HEAD is beyond the commits to squash, we'll squash too many commits
COMMITS_AFTER_ORIGINAL=$(git rev-list HEAD --not "$BACKUP_BRANCH" 2>/dev/null || true)
if [[ -n "$COMMITS_AFTER_ORIGINAL" ]]; then
  echo "❌ ERROR: HEAD has moved beyond backup branch!"
  echo "   This indicates commits exist after the squash range"
  echo "   Current HEAD: $(git rev-parse --short HEAD)"
  echo "   Backup HEAD: $(git rev-parse --short "$BACKUP_BRANCH")"
  exit 1
fi

# Display final confirmation of squash range
echo "═══════════════════════════════════════"
echo "Squash Summary:"
echo "  Base commit:   $(git log --oneline -1 "$BASE_COMMIT")"
echo "  Commits to squash: $COMMIT_COUNT"
echo "  Final result: 1 commit"
echo "═══════════════════════════════════════"

# Record commits before base (these must remain unchanged)
if git rev-parse "${BASE_COMMIT}~1" >/dev/null 2>&1; then
  COMMITS_BEFORE_BASE=$(git rev-list "${BASE_COMMIT}~1")
  echo "Commits before base recorded for verification"
else
  COMMITS_BEFORE_BASE=""
  echo "Base commit is first commit (no prior commits to verify)"
fi
```

### Step 5: Execute Squash

**Soft Reset to Base**:
```bash
# Reset to base commit, keeping all changes staged
git reset --soft "$BASE_COMMIT"

# Verify changes are staged
git status --short
```

### Step 6: Verify No Changes Lost or Added

**⚠️ MANDATORY VERIFICATION**:
```bash
# Compare staged changes with backup branch
# No output = no differences = verification passed
DIFF_OUTPUT=$(git diff --stat "$BACKUP_BRANCH")

if [[ -n "$DIFF_OUTPUT" ]]; then
  echo "❌ ERROR: Staged changes don't match original commits!"
  echo "$DIFF_OUTPUT"
  echo ""
  echo "ROLLBACK: git reset --hard $BACKUP_BRANCH"
  exit 1
fi

echo "✅ Verification passed: No changes lost or added"
```

### Step 7: Create Squashed Commit

**⚠️ CRITICAL: Write Meaningful Commit Message**

The commit message must describe WHAT the changes DO, not just say "squashed".

**⚠️ CRITICAL: Verify IMMEDIATELY After This Step**

DO NOT mark task as "completed" or move to another todo item before verifying the squashed commit contains all expected changes. Verification must be ATOMIC with commit creation.

**Step 7a: Review Commits Being Squashed**:
```bash
# Review all commits to understand their combined purpose
echo "Commits being squashed:"
git log --format="%h %s" "$BASE_COMMIT..HEAD"
```

**⚠️ CRITICAL: Commit Message Must Describe FINAL STATE**

<!-- ADDED: 2025-11-27 to clarify that squashed commit messages must describe
     the final result of all changes combined, not just list individual commits.
     PREVENTS: Commit messages that simply concatenate individual commit messages
     without synthesizing what the final code actually does. -->

The squashed commit message must describe what the **final code does** after all changes are
applied, not just list what each individual commit did.

**❌ WRONG - Lists individual commits**:
```
Fix typo in README
Update model name from Sonnet to Opus
Add missing import statement
Fix test that was broken by import change
```

**✅ CORRECT - Describes final state**:
```
Update model configuration to use Opus for analysis phase

Changes model selection from Sonnet to Opus in REQUIREMENTS phase to improve
analysis quality. Includes necessary import updates and test fixes to support
the model change.

Changes:
- Replace Sonnet 4.5 with Opus in model configuration
- Add Opus-specific imports and remove deprecated Sonnet references
- Fix test assertions to match Opus output format
- Update README to reflect current model usage

Final configuration uses Opus for analysis/decisions, Haiku for code generation.
```

**Key difference**: The second message tells you what the code **does now** (uses Opus for
analysis), not just a chronological list of fixes. When someone reads this commit in 6 months,
they understand the purpose, not just the implementation steps.

**Workflow for Crafting Final-State Messages**:
1. Review all commits being squashed
2. **Look at the actual code changes** (not just commit messages)
3. **Ask**: "What does this code do now that it didn't do before?"
4. Write subject line answering that question
5. Write body explaining why this matters and listing key changes
6. **Verify**: Does message describe final capability, not just implementation steps?

**⚠️ ANTI-PATTERN: Do NOT Include Commit Bodies in Bash Commands**

<!-- ADDED: 2025-11-24 after encountering bash parse error with git log format
     including commit bodies that contained parentheses. Original error:
     "(eval):1: parse error near '('" when using %b in format string.
     PREVENTS: Parse errors from special characters in commit messages. -->

**❌ WRONG - Causes parse errors**:
```bash
# Including %b or %B outputs commit bodies with special characters
git log --format="%h %s%n%b" "$BASE_COMMIT..HEAD"
# ERROR: Parse errors if commit messages contain parentheses, quotes, etc.
```

**✅ CORRECT - Safe alternatives**:
```bash
# Option 1: Subject only (shown above)
git log --format="%h %s" "$BASE_COMMIT..HEAD"

# Option 2: Redirect to file first (if bodies needed)
git log --format="%h %s%n%b" "$BASE_COMMIT..HEAD" > /tmp/commits.txt
cat /tmp/commits.txt

# Option 3: Use git show for individual commits
for commit in $(git rev-list "$BASE_COMMIT..HEAD"); do
  git show --stat "$commit"
done
```

**Why this matters**: Commit message bodies may contain special characters
(parentheses, quotes, backticks) that cause bash parse errors when output
directly in command pipelines.

**Step 7b: Craft Message Following git-commit Skill Guidelines**:

See `git-commit` skill for complete guidance on writing commit messages.

**Key principles for squashed commits**:
- **MOST IMPORTANT**: Describe what the final code DOES, not what commits were made
- Subject line: Summarize the final capability/change (imperative mood, 50-72 chars)
- Body: Explain the final result and why it matters
- Changes section: List key changes that achieve the final result (use bullet points)
- Rationale: Explain why these changes work together and what problem they solve

❌ **WRONG - Generic placeholder**:
```bash
git commit -m "Squashed: feature improvements"
```

✅ **CORRECT - Describes what the code does**:
```bash
# After reviewing commits, synthesize meaningful message
git commit -m "$(cat <<'EOF'
Enhance optimize-doc with iterative loop and session ID

Adds multi-pass optimization capability with proper session
management for agent continuity between optimization phases.

Changes:
- Add iterative optimization loop for multi-pass document refinement
- Integrate session ID capture from Phase 1 agent for Phase 2 resume
- Clarify that main agent optimizes directly (not via Task tool)
- Strengthen to use general-purpose agent only for both phases
- Fix Phase 2 to resume Phase 1 agent (not create new agent)
- Remove unnecessary agent ID file storage

These enhancements enable proper multi-pass optimization with agent
continuity between phases while maintaining session context.

EOF
)"

echo "✅ Squashed commit created"
```

**Reference**: See `git-commit` skill for detailed examples and anti-patterns

**Step 7c: Rewriting Squashed Commit Message (If Needed)**

<!-- ADDED: 2025-11-27 to document simpler reset-amend-cherry-pick approach and
     warn against exec command usage after mistake in session 79d387b4 where exec
     approach created duplicate commits and history divergence.
     PREVENTS: Using exec commands to amend commits (creates duplicates). -->

**⚠️ CRITICAL: Do NOT use `git commit --amend` after rebase completes**

If you need to rewrite the squashed commit message after the rebase has finished:

**❌ WRONG - Amends wrong commit**:
```bash
# Rebase completes, HEAD is at branch tip
git commit --amend -m "New message"  # ← Amends HEAD, NOT the squashed commit!
```

**Why this fails**:
- Interactive rebase with squashing creates the squashed commit
- Rebase continues, rebasing commits that came after the squash range
- When rebase completes, HEAD is at the branch tip (last commit)
- The squashed commit is back in history, NOT at HEAD
- `git commit --amend` modifies commit at HEAD, not a historical commit

**✅ CORRECT - Use interactive rebase with edit**:
```bash
# After rebase completes, identify the squashed commit
git log --oneline -10
# Example output:
# aa4f0c6 Latest commit (HEAD)
# ...
# 28b1631 Add bash-to-script skill  ← The squashed commit (back in history)
# af98b4f Base commit

# Create script to mark squashed commit for editing
cat > /tmp/edit-squash.sh << 'EOF'
#!/bin/bash
# Change pick to edit for the squashed commit
sed -i 's/^pick 28b1631/edit 28b1631/' "$1"
EOF
chmod +x /tmp/edit-squash.sh

# Start interactive rebase from base of squashed commit
BASE_COMMIT="af98b4f"  # Parent of squashed commit
GIT_SEQUENCE_EDITOR=/tmp/edit-squash.sh git rebase -i "$BASE_COMMIT"

# Rebase stops at squashed commit
# Now you can amend it
git commit --amend -m "$(cat <<'EOF'
New commit message
...
EOF
)"

# Continue rebase to reapply subsequent commits
git rebase --continue
```

**Alternative 1 - Use reword in original interactive rebase**:

Instead of fixing the message after rebase completes, you can specify "reword" during the initial rebase:

```bash
# During initial squash rebase, the todo list looks like:
# pick 2df90f4 First commit
# squash edbf606 Second commit
# squash e98d3b0 Third commit
# squash 625cc88 Fourth commit
#
# Git will prompt for combined message after squashing
# This is the BEST time to write the final message
```

**Alternative 2 - Reset-Amend-Cherry-pick (SIMPLER)**:

If the squashed commit is in history with other commits after it, the simplest approach is:

```bash
# Step 1: Identify commits
SQUASHED_COMMIT="07fe839"  # The squashed commit with wrong message
COMMITS_AFTER=("c3132c8" "70bd297" "2c536b6")  # Commits that come after

# Step 2: Create new message file
cat > /tmp/new-message.txt << 'EOF'
New unified commit message

Describes what the final code does...
EOF

# Step 3: Reset to squashed commit
git reset --hard "$SQUASHED_COMMIT"

# Step 4: Amend the message
git commit --amend -F /tmp/new-message.txt

# Step 5: Cherry-pick commits that came after
for commit in "${COMMITS_AFTER[@]}"; do
  git cherry-pick "$commit"
done

# Step 6: Verify
git log --oneline -5
```

**Why this is simpler**:
- No interactive rebase complications
- Clear, sequential steps
- Easy to verify at each stage
- No risk of rebase conflicts

**⚠️ NEVER use exec commands to amend commits**:

❌ **WRONG - Creates duplicate commits**:
```bash
# DON'T DO THIS - exec runs on wrong commit
cat > /tmp/bad-script.sh << 'EOF'
sed -i '/^pick 07fe839/c\exec git commit --amend -F /tmp/msg.txt\npick 07fe839' "$1"
EOF
GIT_SEQUENCE_EDITOR=/tmp/bad-script.sh git rebase -i BASE

# Result: Creates NEW commit, doesn't modify 07fe839
# You end up with 2 commits instead of 1!
```

**Why exec approach fails**:
- exec runs commands at current HEAD position
- When exec runs before pick, HEAD is at previous commit
- Amend creates new commit instead of modifying target
- Results in duplicate commits and history divergence

**✅ Verification after message change**:
```bash
# Always verify immediately after changing commit message
git log --oneline -5

# Check commit count didn't increase
EXPECTED_COUNT=4
ACTUAL_COUNT=$(git rev-list --count BASE..HEAD)
if [[ "$ACTUAL_COUNT" -ne "$EXPECTED_COUNT" ]]; then
  echo "❌ ERROR: Expected $EXPECTED_COUNT commits, got $ACTUAL_COUNT"
  echo "   Likely created duplicate - rollback and retry"
  git reset --hard BACKUP_BRANCH
  exit 1
fi

echo "✅ Commit message updated successfully"
```

**Best Practice**: Write the final commit message during the initial squash operation when Git prompts you. This avoids the need for any post-squash message changes.

### Step 7d: Immediate Post-Commit Verification (MANDATORY)

**⚠️ CRITICAL: Verify squashed commit content IMMEDIATELY after creation**

This verification MUST happen BEFORE marking the task as complete or moving to another todo item.

```bash
# Verify squashed commit exists
SQUASHED_COMMIT=$(git rev-parse HEAD)
echo "Squashed commit: $SQUASHED_COMMIT"

# Verify commit message is meaningful (not generic)
COMMIT_MSG=$(git log -1 --format=%B)
if echo "$COMMIT_MSG" | grep -qiE "^(squash|fixup|wip|tmp)"; then
  echo "⚠️  WARNING: Generic commit message detected"
  echo "   Consider revising with more specific description"
fi

# CRITICAL: Verify squashed commit contains changes from ALL original commits
# Method 1: Check file count matches
FILES_IN_ORIGINAL=$(git diff --name-only "$BASE_COMMIT" "$BACKUP_BRANCH" | wc -l)
FILES_IN_SQUASHED=$(git diff --name-only "$BASE_COMMIT" HEAD | wc -l)

if [[ "$FILES_IN_ORIGINAL" -ne "$FILES_IN_SQUASHED" ]]; then
  echo "❌ ERROR: File count mismatch!"
  echo "   Original commits affected $FILES_IN_ORIGINAL files"
  echo "   Squashed commit affects $FILES_IN_SQUASHED files"
  echo "   Changes may have been lost!"
  echo "ROLLBACK: git reset --hard $BACKUP_BRANCH"
  exit 1
fi

echo "✅ File count matches: $FILES_IN_SQUASHED files"

# Method 2: Compare actual content
CONTENT_DIFF=$(git diff "$BACKUP_BRANCH" HEAD)
if [[ -n "$CONTENT_DIFF" ]]; then
  echo "❌ ERROR: Content doesn't match backup!"
  echo "   Squashed commit has different changes than original commits"
  echo "$CONTENT_DIFF" | head -20
  echo "ROLLBACK: git reset --hard $BACKUP_BRANCH"
  exit 1
fi

echo "✅ Content verification passed: Squashed commit matches original commits"

# Method 3: Sample key changes (manual spot-check)
echo ""
echo "=== SPOT-CHECK: Review key changes in squashed commit ==="
echo "Files changed:"
git diff --name-status "$BASE_COMMIT" HEAD | head -10
echo ""
echo "Sample diff (first 30 lines):"
git diff "$BASE_COMMIT" HEAD | head -30
echo ""
echo "⚠️  MANUAL VERIFICATION REQUIRED:"
echo "   Review above output to confirm all expected changes present"
echo "   If anything looks wrong, ROLLBACK: git reset --hard $BACKUP_BRANCH"
echo ""
read -p "Does the squashed commit look correct? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Aborting due to user verification failure"
  echo "ROLLBACK: git reset --hard $BACKUP_BRANCH"
  exit 1
fi

echo "✅ Manual verification passed"
```

**Why Immediate Verification Matters**:
- Catches lost changes BEFORE proceeding to next steps
- Prevents marking task as "completed" with incomplete squash
- Allows quick rollback before additional operations
- Separating "squash" and "verify" into different todo items risks missing issues

**Lesson from 2025-11-11 Mistake**:
During non-adjacent commit squash, rebase completed successfully but changes from one commit were lost. Issue was discovered only after marking task complete and moving to separate "verification" phase, requiring full restoration from backup. **Always verify IMMEDIATELY after commit creation, not as separate todo item.**

### Step 8: Verify Non-Squashed Commits Unchanged

**⚠️ CRITICAL - Verify Commits Outside Squash Range**:
```bash
# Verify commits before base remain completely unchanged
if [[ -n "$COMMITS_BEFORE_BASE" ]]; then
  CURRENT_COMMITS_BEFORE_BASE=$(git rev-list "${BASE_COMMIT}~1")
  if [[ "$COMMITS_BEFORE_BASE" != "$CURRENT_COMMITS_BEFORE_BASE" ]]; then
    echo "❌ ERROR: Commits before base were modified!"
    echo "   This should never happen - non-squashed commits changed"
    echo "ROLLBACK: git reset --hard $BACKUP_BRANCH"
    exit 1
  fi
  echo "✅ Verification passed: Commits before base unchanged"
fi

# Verify final working tree state matches original HEAD
TREE_DIFF=$(git diff --stat "$ORIGINAL_HEAD")
if [[ -n "$TREE_DIFF" ]]; then
  echo "❌ ERROR: Working tree state doesn't match original HEAD!"
  echo "$TREE_DIFF"
  echo "   Final contents should be identical to original"
  echo "ROLLBACK: git reset --hard $BACKUP_BRANCH"
  exit 1
fi
echo "✅ Verification passed: Final working tree matches original HEAD"
```

### Step 9: Final Count Verification

**Verify Squash Success**:
```bash
# Check commit count
NEW_COMMIT_COUNT=$(git rev-list --count "$BASE_COMMIT..HEAD")
if [[ "$NEW_COMMIT_COUNT" -ne 1 ]]; then
  echo "❌ ERROR: Expected 1 commit after squash, got $NEW_COMMIT_COUNT"
  exit 1
fi

# Show result
git log --oneline -3
echo "✅ Squash successful: $COMMIT_COUNT commits → 1 commit"
```

### Step 10: Rebase Commits After Squash Range (Mid-History Only)

**If commits existed after the squash range, rebase them on top**:

```bash
source /tmp/squash-vars.sh

if [[ "$NEED_REBASE" == "true" ]]; then
  echo ""
  echo "═══════════════════════════════════════"
  echo "Mid-history squash: Rebasing $COMMITS_AFTER_COUNT commits on top"
  echo "═══════════════════════════════════════"

  # Current state: We're at the squashed commit
  SQUASHED_COMMIT=$(git rev-parse HEAD)

  # Rebase commits that came after the squash range onto the squashed commit
  # Uses --onto to replay commits from (last-to-squash) to (original-branch-head)
  # onto the squashed commit
  echo "Rebasing commits from $EXPECTED_LAST_COMMIT to $ORIGINAL_BRANCH_HEAD"
  echo "onto squashed commit $SQUASHED_COMMIT"
  echo ""

  if ! git rebase --onto "$SQUASHED_COMMIT" "$EXPECTED_LAST_COMMIT" "$ORIGINAL_BRANCH_HEAD"; then
    echo "" >&2
    echo "❌ ERROR: Rebase encountered conflicts!" >&2
    echo "" >&2
    echo "   Squashed commit created successfully: $SQUASHED_COMMIT" >&2
    echo "   But rebasing commits after squash range failed." >&2
    echo "" >&2
    echo "   MANUAL RESOLUTION REQUIRED:" >&2
    echo "   1. Resolve conflicts: git status" >&2
    echo "   2. Stage resolved files: git add <files>" >&2
    echo "   3. Continue rebase: git rebase --continue" >&2
    echo "   4. Or abort: git rebase --abort && git reset --hard $BACKUP_BRANCH" >&2
    echo "" >&2
    echo "   Backup available: $BACKUP_BRANCH" >&2
    exit 1
  fi

  echo "✅ Successfully rebased $COMMITS_AFTER_COUNT commits"
  echo ""

  # Update branch pointer to the final rebased state
  if [[ -n "$ORIGINAL_BRANCH" ]]; then
    git branch -f "$ORIGINAL_BRANCH" HEAD
    git checkout "$ORIGINAL_BRANCH"
    echo "✅ Updated $ORIGINAL_BRANCH to final state"
  fi

  # Verify final commit count
  FINAL_COUNT=$(git rev-list --count "$BASE_COMMIT..HEAD")
  EXPECTED_FINAL=$((COMMITS_AFTER_COUNT + 1))  # Squashed commit + commits after
  if [[ "$FINAL_COUNT" -ne "$EXPECTED_FINAL" ]]; then
    echo "⚠️  WARNING: Expected $EXPECTED_FINAL commits, got $FINAL_COUNT" >&2
    echo "   This may indicate an issue - verify history" >&2
  fi

  echo ""
  echo "Final history:"
  git log --oneline "$BASE_COMMIT..HEAD"
else
  # Tip squashing - just update branch pointer
  if [[ -n "$ORIGINAL_BRANCH" ]] && [[ "$(git rev-parse --abbrev-ref HEAD)" == "HEAD" ]]; then
    git branch -f "$ORIGINAL_BRANCH" HEAD
    git checkout "$ORIGINAL_BRANCH"
    echo "✅ Updated $ORIGINAL_BRANCH to squashed commit"
  fi
fi
```

### Step 11: Remove Backup

**⚠️ Only After Verification Passes**:
```bash
# Delete backup branch (verification passed)
source /tmp/squash-vars.sh
git branch -D "$BACKUP_BRANCH"
rm -f /tmp/squash-vars.sh
echo "✅ Backup removed after successful verification"
```

**⚠️ CRITICAL: Do NOT Run Immediate Reflog/GC Cleanup**

<!-- ADDED: 2026-01-05 after agent ran reflog expire immediately after filter-branch,
     permanently destroying the safety net for recovery. -->

**NEVER** run these commands immediately after squash:
```bash
# ❌ DANGEROUS - Destroys recovery safety net
git reflog expire --expire=now --all
git gc --prune=now
```

**Why this is dangerous:**
- The reflog keeps references to ALL previous HEAD positions (~90 days default)
- If the squash had issues (lost changes, wrong commits), reflog lets you recover
- Running `reflog expire --expire=now` PERMANENTLY destroys this safety net

**Safe approach:**
- Let git's natural gc handle cleanup (90-day default expiration)
- Only consider aggressive cleanup after verifying operation was 100% correct AND you have a remote backup

## Complete Example

### Example: Squash 2 Commits

```bash
#!/bin/bash
set -euo pipefail

# Configuration
BASE_COMMIT="4d3e19e"              # Parent of first commit to squash
EXPECTED_LAST_COMMIT="b732939"     # Last commit to include in squash
ORIGINAL_BRANCH="main"             # Branch to update after squash

echo "=== Git Squash: Multiple commits → 1 commit ==="
echo ""

# Step 1: Position HEAD at last commit to squash
git checkout "$EXPECTED_LAST_COMMIT"
echo "✅ Checked out last commit to squash"

# Step 2: Create backup
BACKUP_BRANCH="backup-before-squash-$(date +%Y%m%d-%H%M%S)"
git branch "$BACKUP_BRANCH"
echo "✅ Backup created: $BACKUP_BRANCH"

# Step 3: Verify preconditions
if [[ -n "$(git status --porcelain)" ]]; then
  echo "❌ ERROR: Working directory not clean"
  exit 1
fi
echo "✅ Working directory clean"

# Verify HEAD position
CURRENT_HEAD=$(git rev-parse HEAD)
EXPECTED_HEAD=$(git rev-parse "$EXPECTED_LAST_COMMIT")
if [[ "$CURRENT_HEAD" != "$EXPECTED_HEAD" ]]; then
  echo "❌ ERROR: HEAD is not at expected last commit"
  exit 1
fi
echo "✅ HEAD positioned at expected last commit"

COMMIT_COUNT=$(git rev-list --count "$BASE_COMMIT..HEAD")
echo "Will squash $COMMIT_COUNT commits into 1"

# Step 4: Record original state
ORIGINAL_HEAD=$(git rev-parse HEAD)
if git rev-parse "${BASE_COMMIT}~1" >/dev/null 2>&1; then
  COMMITS_BEFORE_BASE=$(git rev-list "${BASE_COMMIT}~1")
else
  COMMITS_BEFORE_BASE=""
fi

# Step 5: Execute squash
git reset --soft "$BASE_COMMIT"
echo "✅ Soft reset to base commit"

# Step 6: Verify no changes lost
DIFF_OUTPUT=$(git diff --stat "$BACKUP_BRANCH")
if [[ -n "$DIFF_OUTPUT" ]]; then
  echo "❌ ERROR: Changes don't match!"
  echo "ROLLBACK: git reset --hard $BACKUP_BRANCH"
  exit 1
fi
echo "✅ Verification passed: No changes lost or added"

# Step 7: Create squashed commit
git commit -m "$(cat <<'EOF'
Combined commit message

[Details from all squashed commits]

EOF
)"
echo "✅ Squashed commit created"

# Step 8: Verify non-squashed commits unchanged
if [[ -n "$COMMITS_BEFORE_BASE" ]]; then
  CURRENT_COMMITS_BEFORE_BASE=$(git rev-list "${BASE_COMMIT}~1")
  if [[ "$COMMITS_BEFORE_BASE" != "$CURRENT_COMMITS_BEFORE_BASE" ]]; then
    echo "❌ ERROR: Commits before base were modified!"
    echo "ROLLBACK: git reset --hard $BACKUP_BRANCH"
    exit 1
  fi
  echo "✅ Commits before base unchanged"
fi

TREE_DIFF=$(git diff --stat "$ORIGINAL_HEAD")
if [[ -n "$TREE_DIFF" ]]; then
  echo "❌ ERROR: Working tree doesn't match original!"
  echo "ROLLBACK: git reset --hard $BACKUP_BRANCH"
  exit 1
fi
echo "✅ Final working tree matches original HEAD"

# Step 9: Final verification
NEW_COUNT=$(git rev-list --count "$BASE_COMMIT..HEAD")
if [[ "$NEW_COUNT" -ne 1 ]]; then
  echo "❌ ERROR: Expected 1 commit, got $NEW_COUNT"
  exit 1
fi
echo "✅ Final verification passed"

# Step 10: Update original branch (if detached)
if [[ -n "$ORIGINAL_BRANCH" ]] && [[ "$(git rev-parse --abbrev-ref HEAD)" == "HEAD" ]]; then
  git branch -f "$ORIGINAL_BRANCH" HEAD
  git checkout "$ORIGINAL_BRANCH"
  echo "✅ Updated $ORIGINAL_BRANCH to squashed commit"
fi

# Step 11: Remove backup
git branch -D "$BACKUP_BRANCH"
echo "✅ Backup removed"

echo ""
echo "=== Squash complete ==="
git log --oneline -3
```

## Safety Guarantees

**This skill guarantees**:
- ✅ Backup always created before any destructive operation
- ✅ Verification that staged changes = original commits (no loss, no additions)
- ✅ Verification that commits before base remain completely unchanged
- ✅ Verification that final working tree matches original HEAD state
- ✅ Verification that only intended commits are squashed (not commits beyond)
- ✅ HEAD position validation to prevent squashing beyond intended range
- ✅ Backup removed only after all verifications pass
- ✅ Clear rollback instructions on any error
- ✅ Atomic operation (all or nothing)

**Error Recovery**:
```bash
# If anything goes wrong, restore from backup:
git reset --hard backup-before-squash-YYYYMMDD-HHMMSS
```

## Common Mistakes and How to Avoid Them

### Mistake #1: Target Commit Hash Unchanged After Squash (DATA LOSS)

**⚠️ CRITICAL: This is the most serious mistake - causes silent data loss**

**Problem**: When squashing commits INTO another commit, the target commit's hash MUST change because
its content changes. If the target hash remains the same, the squash DID NOT HAPPEN - commits were
dropped instead of squashed.

**Real Example from 2025-11-26**:
```bash
# Requested: Squash b325852, 3178bcb, 6a707bc INTO 778b26b
# Used custom sed script with GIT_SEQUENCE_EDITOR
# After rebase completed:
git log --oneline | grep 778b26b
# 778b26b [config] Comprehensive shrink-doc...  ← SAME HASH!

# ❌ FAILURE: Hash unchanged means content unchanged
# The commits were DROPPED, not squashed!
# ~4400 lines of changes silently lost
```

**Why Hash Must Change**:
- Squashing INTO a commit adds content to that commit
- Git commits are content-addressed (SHA-1 hash of content)
- Different content = different hash (always)
- Same hash = same content = squash didn't happen

**MANDATORY Validation After Squash**:
```bash
# Record target hash BEFORE squash
TARGET_BEFORE="778b26b"
TARGET_HASH_BEFORE=$(git rev-parse "$TARGET_BEFORE")

# After squash operation...

# Find the new commit at target's position
# (It should have a DIFFERENT hash)
TARGET_HASH_AFTER=$(git rev-parse HEAD~X)  # Position where target should be

if [[ "$TARGET_HASH_BEFORE" == "$TARGET_HASH_AFTER" ]]; then
  echo "❌ CRITICAL ERROR: Target commit hash unchanged!"
  echo "   Squash DID NOT HAPPEN - commits were dropped, not squashed"
  echo "   IMMEDIATE ROLLBACK REQUIRED"
  git reset --hard "$BACKUP_BRANCH"
  exit 1
fi

echo "✅ Target commit hash changed: squash successful"
echo "   Before: $TARGET_HASH_BEFORE"
echo "   After:  $TARGET_HASH_AFTER"
```

**Prevention**:
1. **NEVER use untested sed/awk scripts** for GIT_SEQUENCE_EDITOR
2. **ALWAYS verify target hash changed** immediately after squash
3. **Prefer git-squash skill** over custom rebase scripts - it has built-in safety checks
4. If using custom scripts, test on a throw-away branch first

**Root Cause of 2025-11-26 Mistake**:
- Custom sed script had flawed logic for moving and squashing commits
- Script deleted commit lines but didn't properly reinsert them as squash
- No immediate hash validation caught the silent failure
- User correctly identified: "How is it possible you squashed if hash hasn't changed?"

### Mistake #2: Squashing Beyond Intended Range (MOST COMMON)

**Problem**: Running squash while HEAD is beyond the last commit you want to squash will include ALL commits from base to current HEAD, not just the commits you intended.

**Real Example from 2025-11-05**:
```bash
# User wanted to squash: 3ebecc4 and b732939 (2 commits)
# But HEAD was at: 5879391 (main branch, 43 commits ahead)

git log --oneline
# 5879391 (HEAD -> main) Fix optimize-doc...  ← Current HEAD (WRONG)
# ...
# 5cc46a9 Optimize task-protocol-agents...
# ...
# b732939 Add AWAITING_USER_APPROVAL...     ← Last commit to squash
# 3ebecc4 Update project documentation...   ← First commit to squash
# 4d3e19e Implement TOML-based...           ← Base commit

# Running: git reset --soft 4d3e19e
# Result: Squashed ALL 43 commits from 4d3e19e to 5879391 (WRONG!)
# Expected: Only 2 commits (3ebecc4 and b732939)
```

**Solution**: ALWAYS checkout the LAST commit FIRST (Step 1):
```bash
# 🚨 MANDATORY Step 1: Position HEAD
git checkout b732939                # Position HEAD at LAST commit to squash
git log --oneline -1                # Verify: should show b732939

# Now create backup and squash
BACKUP_BRANCH="backup-before-squash-$(date +%Y%m%d-%H%M%S)"
git branch "$BACKUP_BRANCH"
git reset --soft 4d3e19e           # Now squashes ONLY 3ebecc4 and b732939
```

**Prevention Measures Added**:
1. **Step 1 added**: Mandatory HEAD positioning before backup
2. **Usage section updated**: Emphasizes Step 1 with warnings
3. **Verification checks**: HEAD position validated in Step 3
4. **This example added**: Documents real mistake for future reference

**Why This Works**:
- `git reset --soft` moves current branch pointer but keeps working tree
- If HEAD is at wrong position, wrong range gets squashed
- Checking out last commit FIRST ensures correct range

## Squashing Specific Non-Consecutive Commits

**⚠️ CRITICAL: When user provides SPECIFIC commit hashes to squash**

When the user provides a list of specific commit hashes (e.g., "Squash 76894f6 d9af66d 7ef72f1"),
these commits may NOT be consecutive in history. **NEVER use `git reset --soft`** for this case.

**Mistake Pattern (from 2025-12-04)**:
```bash
# User asked: "Squash 76894f6 d9af66d 7ef72f1 d2c5a6c ccecf0c"
# These 5 commits had 12 OTHER commits between them in history

# ❌ WRONG - Soft reset to oldest commit parent
git checkout ccecf0c  # Last commit to squash
git reset --soft 76894f6~1  # Stages ALL 17 commits from parent to HEAD!
# Result: Squashed 17 commits instead of 5

# ✅ CORRECT - Interactive rebase to reorder and squash ONLY specified commits
git rebase -i 76894f6~1
# In editor: Move the 5 commits to be adjacent, mark with "squash"
# All other commits remain unchanged
```

**Why Soft Reset Fails for Specific Commits**:
- `git reset --soft <base>` stages ALL commits from base to HEAD
- It cannot selectively include only specific commits
- Use interactive rebase instead to pick specific commits

**Procedure for Specific Commit Squashing**:
1. Identify which commits are specified
2. Find the earliest commit's parent as rebase base
3. Use interactive rebase to:
   - REORDER specified commits to be adjacent
   - Mark them for squashing
   - PRESERVE all other commits unchanged
4. Verify only the specified commits were combined

**See "Approach 2: Interactive Rebase with Reorder" below for detailed procedure.**

---

## Squashing Non-Adjacent Commits

**When commits to squash are NOT adjacent** (separated by other commits in between):

### Approach 1: Cherry-Pick Method (SAFER - RECOMMENDED)

**When to use**: Non-adjacent commits with many intermediate commits (5+), or when rebase automation is complex.

**Advantages**:
- More explicit control over what gets combined
- Easier to verify at each step
- Lower risk of losing changes from automated reorder scripts
- Better for complex histories

**Procedure**:
```bash
# 1. Create backup
BACKUP_BRANCH="backup-before-squash-$(date +%Y%m%d-%H%M%S)"
git branch "$BACKUP_BRANCH"

# 2. Identify commits to squash
TARGET_COMMIT="2871c93"          # Base commit (others squash into this)
COMMIT_TO_COMBINE="19bcf07"       # Commit to squash into target
BASE_PARENT="2871c93~1"          # Parent of target commit

# 3. Create working branch from parent of target
git checkout -b temp-squash "$BASE_PARENT"

# 4. Cherry-pick target commit
git cherry-pick "$TARGET_COMMIT"
# Resolves as normal commit

# 5. Cherry-pick commit to combine WITHOUT committing
git cherry-pick --no-commit "$COMMIT_TO_COMBINE"
# Changes staged but not committed

# 6. Resolve conflicts if any
git status  # Check for conflicts
# If conflicts: resolve, then git add <files>

# 7. Amend target commit with combined changes
git commit --amend --no-edit
# Now target commit contains changes from both commits

# 8. IMMEDIATE VERIFICATION (MANDATORY)
# Verify combined commit has ALL expected changes
git show --stat HEAD  # Review files changed
git diff "$TARGET_COMMIT" HEAD  # Should show additions from second commit
git diff "$COMMIT_TO_COMBINE" "$BASE_PARENT"  # Compare what was added

# Manual spot-check of key changes
git show HEAD | grep -A5 "key change pattern"

# 9. Cherry-pick remaining commits in order
git cherry-pick <commit-after-target>..HEAD  # Or specify individually

# 10. Final verification
git diff "$BACKUP_BRANCH" HEAD  # Should show NO differences in content
git rev-list --count "$BASE_PARENT..HEAD"  # Verify commit count is N-1

# 11. Update main branch
git checkout main
git reset --hard temp-squash
git branch -D temp-squash

# 12. Delete backup after verification
git branch -D "$BACKUP_BRANCH"
```

**Why This Worked (2025-11-11 Example)**:
- Interactive rebase with awk script LOST changes from 19bcf07
- Cherry-pick approach: explicitly combined both commits, immediate verification caught issues
- Result: All changes preserved correctly

### Approach 2: Interactive Rebase with Reorder

**When to use**: Few intermediate commits (1-3), simple history, comfortable with interactive rebase.

**Use Case**: You want to squash multiple commits together, but they're currently separated by other commits in the history.

**Two-Step Workflow**:
1. **Reorder**: Use interactive rebase to move commits adjacent to each other
2. **Squash**: Change "pick" to "squash" to combine them into one commit

**Example Command Interpretation**:

When you say: "Squash commits A, B, C into commit X"
- Means: Move commits A, B, C to be adjacent to commit X, then squash them together
- Workflow: Interactive rebase moves A, B, C next to X, marks them as "squash"
- Result: One combined commit at X's position

**Concrete Example**:
```bash
# Current history:
# 625cc88 - Commit C (separated)
# e98d3b0 - Commit B (separated)
# ...     - Many other commits
# 2df90f4 - Commit A (separated)
# edbf606 - Target commit X
# ...     - Earlier commits

# Goal: Squash A, B, C into X
# Result after rebase:
# edbf606 - Combined commit (X + A + B + C)
# ...     - Earlier commits
# (All other commits preserved in original positions)
```

### General Procedure: Multiple Separated Commits

**Procedure for squashing multiple non-adjacent commits**:

```bash
# 1. Create backup
BACKUP_BRANCH="backup-before-squash-$(date +%Y%m%d-%H%M%S)"
git branch "$BACKUP_BRANCH"

# 2. Identify commits to squash
TARGET_COMMIT="edbf606"          # Base commit (all others squash into this)
COMMITS_TO_SQUASH=(              # Commits currently separated in history
  "2df90f4"
  "e98d3b0"
  "625cc88"
)
BASE_COMMIT="${TARGET_COMMIT}^"  # Parent of target commit

# 3. Start interactive rebase from base
git rebase -i "$BASE_COMMIT"

# 4. In the interactive editor:
#    - FIND each commit in COMMITS_TO_SQUASH array
#    - MOVE them to be directly after TARGET_COMMIT
#    - CHANGE their "pick" to "squash"
#    - PRESERVE all other commits in original order
#    - Save and exit

# Example transformation for "Squash 2df90f4, e98d3b0, 625cc88 into edbf606":
# BEFORE:
#   pick edbf606 Target commit
#   pick abc1234 Other commit
#   pick 2df90f4 Commit A to squash
#   pick def5678 Other commit
#   pick e98d3b0 Commit B to squash
#   pick ghi9012 Other commit
#   pick 625cc88 Commit C to squash
#
# AFTER:
#   pick edbf606 Target commit
#   squash 2df90f4 Commit A to squash    ← MOVED & CHANGED
#   squash e98d3b0 Commit B to squash    ← MOVED & CHANGED
#   squash 625cc88 Commit C to squash    ← MOVED & CHANGED
#   pick abc1234 Other commit
#   pick def5678 Other commit
#   pick ghi9012 Other commit

# 5. Git prompts for combined commit message
#    - Edit to create unified message
#    - Save and exit

# 6. Verify result
git log --oneline -10
git diff "$BACKUP_BRANCH"  # Should show no differences

# 7. Remove backup after verification
git branch -D "$BACKUP_BRANCH"
```

### Specific Example: Fix Commit Into Original

**Use Case**: Squashing a fix commit into the commit that introduced the issue, while preserving all commits in between.

**Example**: Squash commit 285d9b9 (removes broken reference) into 977d7b9 (introduced broken reference), preserving 77 commits in between.

**Procedure**:
```bash
# 1. Create backup
BACKUP_BRANCH="backup-before-squash-$(date +%Y%m%d-%H%M%S)"
git branch "$BACKUP_BRANCH"

# 2. Identify the commits
TARGET_COMMIT="977d7b9"           # Commit that introduced issue
FIX_COMMIT="285d9b9"              # Commit that fixes issue
BASE_COMMIT="${TARGET_COMMIT}^"   # Parent of target commit

# 3. Start interactive rebase
git rebase -i "$BASE_COMMIT"

# 4. In the interactive editor:
#    - FIND the fix commit line
#    - MOVE it directly after the target commit line
#    - CHANGE "pick" to "squash" (or "fixup" ONLY if fix is trivial like typo)
#    - PRESERVE all other commits in their original order
#    - Save and exit

# Example transformation:
# BEFORE:
#   pick 977d7b9 Initial commit (TARGET)
#   pick abc1234 Some other commit
#   pick def5678 Another commit
#   ...
#   pick 285d9b9 Remove broken reference (FIX)
#
# AFTER:
#   pick 977d7b9 Initial commit (TARGET)
#   squash 285d9b9 Remove broken reference (FIX) ← MOVED & CHANGED
#   pick abc1234 Some other commit
#   pick def5678 Another commit
#   ...

# 5. Git will prompt for combined commit message
#    - Edit to create unified message
#    - Save and exit

# 6. Verify result
git log --oneline -10
git diff "$BACKUP_BRANCH"  # Should show no differences

# 7. Remove backup after verification
git branch -D "$BACKUP_BRANCH"
```

**Critical Rules for Reordering**:
- ✅ Only reorder the commits being squashed together
- ✅ Preserve all other commits in their exact original positions
- ❌ Never reorder commits that aren't being squashed
- ❌ Never drop commits accidentally

**Safety Verification**:
```bash
# After rebase, verify commit count
ORIGINAL_COUNT=$(git rev-list --count "$BACKUP_BRANCH")
NEW_COUNT=$(git rev-list --count HEAD)
EXPECTED_NEW=$((ORIGINAL_COUNT - 1))  # One less due to squash

if [[ "$NEW_COUNT" -ne "$EXPECTED_NEW" ]]; then
  echo "❌ ERROR: Expected $EXPECTED_NEW commits, got $NEW_COUNT"
  git rebase --abort
  git reset --hard "$BACKUP_BRANCH"
  exit 1
fi

echo "✅ Verification passed: $ORIGINAL_COUNT commits → $NEW_COUNT commits"
```

### Automating Reorder with GIT_SEQUENCE_EDITOR

**⚠️ CRITICAL: Commit Order Assumptions**

When automating rebase with `GIT_SEQUENCE_EDITOR`, git presents commits in **chronological order** (oldest first). Scripts MUST NOT assume they will encounter commits in any particular order.

**❌ WRONG Pattern - Assumes Order**:
```python
#!/usr/bin/env python3
# ❌ BUG: Assumes commit B comes BEFORE commit A
import sys

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

result = []
moved_commit = None

for line in lines:
    if 'commit-B' in line:  # Try to save this commit
        moved_commit = line.replace('pick', 'squash', 1)
    elif 'commit-A' in line:  # Try to insert saved commit here
        result.append(line)
        if moved_commit:  # ❌ Won't work if commit-A comes first!
            result.append(moved_commit)
            moved_commit = None
    else:
        result.append(line)

# ❌ BUG: If commit-A comes before commit-B chronologically,
# moved_commit will never be appended, silently dropping commit-B!
```

**✅ CORRECT Pattern - Process All, Then Reorder**:
```python
#!/usr/bin/env python3
# ✅ CORRECT: Process all lines first, then reorder
import sys

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

# Step 1: Extract commits (don't assume order)
commits = []
for line in lines:
    if line.startswith('#') or not line.strip():
        continue
    commits.append(line)

# Step 2: Find specific commits
commit_a = None
commit_b = None
other_commits = []

for commit in commits:
    if 'commit-A' in commit:
        commit_a = commit
    elif 'commit-B' in commit:
        commit_b = commit.replace('pick', 'squash', 1)
    else:
        other_commits.append(commit)

# Step 3: Verify both found
if not commit_a or not commit_b:
    print(f"ERROR: Commits not found", file=sys.stderr)
    sys.exit(1)

# Step 4: Build new order
result = []
if commit_a:
    result.append(commit_a)
if commit_b:
    result.append(commit_b)
result.extend(other_commits)

# Step 5: Verify count (defensive programming)
if len(result) != len(commits):
    print(f"ERROR: Commit count mismatch! {len(commits)} → {len(result)}", file=sys.stderr)
    sys.exit(1)

# Write result
with open(sys.argv[1], 'w') as f:
    f.writelines(result)
```

**Key Principles**:
1. **Never assume commit order** in git rebase todo list
2. **Process all lines first**, extract what you need
3. **Then reorder** based on requirements
4. **Verify count** before writing (defensive check)
5. **Exit with error** if commits not found or count mismatch

**See Also**: [git-workflow.md § Handling Non-Contiguous Commits](../../docs/project/git-workflow.md#handling-non-contiguous-commits) for complete documentation.

## Usage

### Optimized Script (Recommended)

**Best for**: Simple adjacent commit squashing (most common case)

**Workflow**:
```bash
# 1. Review commits to squash
git log --oneline <base-commit>..HEAD

# 2. Draft commit message
cat > /tmp/squash-msg.txt <<'EOF'
Combined feature improvements

- Add validation logic
- Fix edge cases
- Update documentation
EOF

# 3. Execute optimized script
/workspace/main/.claude/scripts/git-squash-optimized.sh \
  <base-commit> \
  <last-commit> \
  /tmp/squash-msg.txt \
  main

# Script executes ALL steps atomically:
# ✅ Position HEAD
# ✅ Create backup
# ✅ Verify preconditions
# ✅ Execute squash
# ✅ Verify no changes lost
# ✅ Verify non-squashed commits unchanged
# ✅ Create squashed commit
# ✅ Cleanup backup
# ✅ Output JSON result

# 4. Check result
git log --oneline -3
```

**Parameters**:
- `base_commit` - Parent of first commit to squash
- `last_commit` - Last commit to include in squash
- `message_file` - File containing commit message
- `branch` - Optional branch to update (default: current branch)

**Output**: JSON with status, duration, squashed commit SHA

**Error handling**: Script outputs clear rollback commands on any failure

### Interactive Mode (Manual Workflow)

**For Adjacent Commits** (when you want step-by-step control):
```bash
# 1. Identify commits to squash
git log --oneline -10
# Note:
# - Base commit (parent of first commit to squash)
# - Last commit to include in squash

# 2. 🚨 MANDATORY: Checkout the last commit to squash FIRST
git checkout <last-commit-sha>
# ⚠️ CRITICAL: This MUST be done before creating backup
# If skipped, you'll squash MORE commits than intended

# Verify HEAD position
git log --oneline -1
# Should show the LAST commit you want in the squash

# 3. Run skill (follows Step 1-10 from workflow)
Skill: git-squash

# 4. When prompted, provide:
#    - Base commit SHA (parent of first commit)
#    - Expected last commit SHA (for verification)
#    - Combined commit message

# 5. After squash, update original branch if needed
git branch -f main HEAD
git checkout main
```

**For Non-Adjacent Commits**:
```bash
# Use interactive rebase with reordering (see section above)
# This handles commits with other commits in between
```

### Direct Invocation

**For scripting/automation**:
```bash
# Set base commit
BASE_COMMIT="abc123"

# Execute skill workflow
# [Follow steps 1-7 from workflow section]
```

## Related Documentation

- git-workflow.md: Git workflows and commit management
- git-rebase/SKILL.md: For complex history editing
- git-merge-linear/SKILL.md: For linear merge workflows
- CLAUDE.md: Branch management rules

## Success Criteria

Squash is successful when:
1. ✅ Backup created before squash
2. ✅ HEAD was positioned at correct last commit to squash
3. ✅ Verification passed (no changes lost/added)
4. ✅ Commits before base remain unchanged
5. ✅ Final working tree matches original HEAD state
6. ✅ Single commit created with all changes
7. ✅ Commit count reduced by exactly (N-1) where N = commits squashed
8. ✅ Backup removed after all verifications pass
9. ✅ `git log` shows clean, linear history
10. ✅ No uncommitted changes remain
