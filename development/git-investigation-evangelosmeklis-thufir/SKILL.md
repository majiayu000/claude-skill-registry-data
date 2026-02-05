---
name: Git Investigation
description: This skill should be used when the user asks to "use git blame", "check git history", "find git commits", "use git log", "use git diff", "use git bisect", "trace code changes", "find who changed this code", or mentions using git commands for investigating code history and changes during root cause analysis.
version: 0.1.0
---

# Git Investigation

## Overview

Git is a distributed version control system that tracks code changes over time. This skill provides guidance for using git commands to investigate code history, identify when bugs were introduced, and track down specific changes during root cause analysis.

## When to Use This Skill

Apply this skill when:
- Tracing when specific code was changed
- Finding who authored problematic code
- Identifying commits that introduced bugs
- Comparing code versions before/after incidents
- Searching commit messages for clues
- Binary searching for breaking commits (bisect)

## Essential Git Commands for RCA

### git log - View Commit History

**Basic usage**:
```bash
git log
```

**Useful flags for RCA**:

**Show commits with diffs**:
```bash
git log -p
```

**Show commits for specific file**:
```bash
git log -- path/to/file.js
```

**Show commits in time range**:
```bash
git log --since="2025-12-19 00:00" --until="2025-12-19 23:59"
```

**Show one-line summaries**:
```bash
git log --oneline
```

**Show commits by author**:
```bash
git log --author="Developer Name"
```

**Show commit graph**:
```bash
git log --graph --oneline --all
```

**Search commit messages**:
```bash
git log --grep="database" --grep="pool" --all-match
```

**Format output**:
```bash
git log --format="%h %an %ad %s" --date=short
```

### git blame - Find Line Authors

**Basic usage**:
```bash
git blame path/to/file.js
```

**Show line ranges**:
```bash
git blame -L 40,50 path/to/file.js
```

**Show email addresses**:
```bash
git blame -e path/to/file.js
```

**Follow line history through renames**:
```bash
git blame -C -C -C path/to/file.js
```

**Show commit details**:
```bash
git blame -s path/to/file.js
```

**Blame output format**:
```
abc123de (Developer Name 2025-12-19 10:15:00 +0000 45)   max: 10,
```
- `abc123de`: Commit SHA
- `Developer Name`: Author
- `2025-12-19 10:15:00`: Timestamp
- `45`: Line number
- `max: 10,`: Code content

### git diff - Compare Versions

**Compare working directory with last commit**:
```bash
git diff
```

**Compare specific commits**:
```bash
git diff commit1 commit2
```

**Compare file across commits**:
```bash
git diff commit1 commit2 -- path/to/file.js
```

**Compare with previous commit**:
```bash
git diff HEAD~1 HEAD
```

**Show diff for specific commit**:
```bash
git show commit_sha
```

**Unified diff with context**:
```bash
git diff -U5  # Show 5 lines of context
```

**Word-level diff**:
```bash
git diff --word-diff
```

### git show - View Commit Details

**Show complete commit**:
```bash
git show commit_sha
```

**Show specific file in commit**:
```bash
git show commit_sha:path/to/file.js
```

**Show commit metadata only**:
```bash
git show --stat commit_sha
```

### git bisect - Binary Search for Breaking Commit

**Use when**: You know code worked at one point and is broken now, but don't know which commit broke it.

**Workflow**:

1. **Start bisect**:
```bash
git bisect start
```

2. **Mark current as bad**:
```bash
git bisect bad
```

3. **Mark known good commit**:
```bash
git bisect good commit_sha  # or tag, or HEAD~20
```

4. **Test current code** (git checks out midpoint)
   - Run tests or reproduce bug
   - If broken: `git bisect bad`
   - If working: `git bisect good`

5. **Repeat** until git identifies first bad commit

6. **End bisect**:
```bash
git bisect reset
```

**Automated bisect**:
```bash
git bisect start HEAD v1.0
git bisect run ./test-script.sh
```

Test script should exit 0 for good, non-zero for bad.

## Git Investigation Workflows

### Workflow 1: Find When Line Changed

**Goal**: Identify when specific line was last modified

**Steps**:

1. Use blame to find commit:
```bash
git blame path/to/file.js | grep "suspicious code"
```

2. Extract commit SHA from blame output

3. View commit details:
```bash
git show commit_sha
```

4. Review commit message, author, timestamp, and changes

### Workflow 2: Track File History

**Goal**: See all changes to a file over time

**Steps**:

1. View commit history for file:
```bash
git log -p -- path/to/file.js
```

2. Focus on time range around incident:
```bash
git log --since="2025-12-18" --until="2025-12-19" -- path/to/file.js
```

3. Review each commit's diff to identify suspicious changes

### Workflow 3: Find Recent Changes to Multiple Files

**Goal**: Identify recent commits affecting several related files

**Steps**:

1. List recent commits with file stats:
```bash
git log --since="2025-12-19" --stat
```

2. Filter commits touching specific directory:
```bash
git log --since="2025-12-19" -- src/config/
```

3. Look for commits near incident time that modified relevant files

### Workflow 4: Search Commit Messages

**Goal**: Find commits related to specific feature or bug

**Steps**:

1. Search commit messages:
```bash
git log --grep="database" --grep="connection" --all-match
```

2. Or search for any of multiple terms:
```bash
git log --grep="database\|connection\|pool"
```

3. Review matching commits for relevance

### Workflow 5: Compare Working vs Deployed Version

**Goal**: Identify differences between deployed and current code

**Steps**:

1. Find deployed commit SHA (from deployment logs or tags):
```bash
deployed_sha="abc123"
```

2. Compare with current code:
```bash
git diff $deployed_sha HEAD
```

3. Or compare specific file:
```bash
git diff $deployed_sha HEAD -- path/to/file.js
```

4. Review differences for potential issues

### Workflow 6: Binary Search for Breaking Commit

**Goal**: Find exact commit that introduced bug

**Steps**:

1. Identify known-good commit (e.g., last working version):
```bash
git log --oneline
# Find commit SHA before issue appeared
```

2. Start bisect:
```bash
git bisect start
git bisect bad  # Current is broken
git bisect good good_commit_sha
```

3. Test each checkout:
   - Reproduce issue or run tests
   - Mark as `git bisect good` or `git bisect bad`

4. Git identifies first bad commit

5. Review that commit to find root cause

## Advanced Git Techniques

### Finding Deleted Code

**Search for deleted lines**:
```bash
git log -S "deleted code pattern" --all
```

**Example** - Find when "max: 100" was removed:
```bash
git log -S "max: 100" -- src/config/database.js
```

### Following Renames

**Track file across renames**:
```bash
git log --follow -- path/to/file.js
```

**Blame with rename detection**:
```bash
git blame -C -C -C path/to/file.js
```

### Finding Large Changes

**Show commits by diff size**:
```bash
git log --stat --format="%h %s" | head -20
```

**Find commits with many changes**:
```bash
git log --shortstat | grep -E "file.*change"
```

### Checking Specific Commit

**View commit details**:
```bash
git show commit_sha
```

**View files changed in commit**:
```bash
git show --name-only commit_sha
```

**View commit as patch**:
```bash
git format-patch -1 commit_sha
```

## Interpreting Git Output

### Git Blame Output

```
abc123de src/config/database.js (Developer Name 2025-12-19 10:15:00 +0000 45)   max: 10,
```

**Extract**:
- Commit: `abc123de`
- File: `src/config/database.js`
- Author: `Developer Name`
- Date: `2025-12-19 10:15:00`
- Line: `45`
- Code: `max: 10,`

**Action**: Check if timestamp correlates with incident start.

### Git Log Output

```
commit abc123def456789
Author: Developer Name <dev@example.com>
Date:   Thu Dec 19 10:15:00 2025 +0000

    Refactor database configuration

    Align pool size with staging environment
```

**Extract**:
- Full SHA: `abc123def456789`
- Author: `Developer Name <dev@example.com>`
- Date: `Thu Dec 19 10:15:00 2025`
- Message: Multi-line commit message

**Red flags**:
- Vague messages: "fix bug", "update code"
- Large refactors near incident time
- Config changes without explanation

### Git Diff Output

```diff
diff --git a/src/config/database.js b/src/config/database.js
index abc123d..def456e 100644
--- a/src/config/database.js
+++ b/src/config/database.js
@@ -42,7 +42,7 @@ function createConnectionPool() {
   return new Pool({
     host: process.env.DB_HOST,
     port: process.env.DB_PORT,
-    max: 100,
+    max: 10,  // Align with staging
     min: 10,
     idleTimeoutMillis: 30000
   });
```

**Interpret**:
- `-` line: Old code (removed)
- `+` line: New code (added)
- `@@ -42,7 +42,7 @@`: Line numbers (start at line 42, 7 lines shown)

**Identify issue**: `max: 100` → `max: 10` is likely problematic reduction.

## Best Practices

### Do:

- **Use time ranges** to focus on relevant commits
```bash
git log --since="2025-12-19 00:00" --until="2025-12-19 23:59"
```

- **Filter by file/directory** to reduce noise
```bash
git log -- src/config/
```

- **Combine flags** for precise queries
```bash
git log --author="Developer" --since="1 week ago" -- src/
```

- **Use grep** to search commit messages
```bash
git log --grep="database"
```

- **Follow renames** when tracking file history
```bash
git log --follow -- file.js
```

- **Use bisect** for efficient debugging
```bash
git bisect start HEAD v1.0.0
```

### Don't:

- Run `git log` without filters (too much output)
- Ignore commit messages (valuable clues)
- Forget time context (correlate with incident time)
- Skip reading full diffs (may miss subtle bugs)
- Blame individuals (focus on system improvements)

## Integration with Thufir

This skill integrates with:
- **root-cause-analysis skill**: Git provides evidence for RCA
- **platform-integration skill**: Complements GitHub/GitLab API data
- **RCA agent**: Agent uses git commands via Bash tool

### Using Git in RCA Agent

Agent can execute git commands:

```bash
# Find recent commits to file
git log --since="24 hours ago" --oneline -- src/config/database.js

# Blame specific line
git blame -L 45,45 src/config/database.js

# Show commit details
git show abc123

# Compare versions
git diff HEAD~1 HEAD -- src/config/database.js
```

Agent parses output to extract commit SHAs, authors, timestamps, and changes.

## Common Patterns

### Pattern 1: Stack Trace Points to File

1. Extract file and line from stack trace
2. Use `git blame` on that file/line
3. Identify commit that last touched it
4. Use `git show` to review commit
5. Correlate commit time with incident

### Pattern 2: Config Change Suspected

1. List recent commits to config files:
```bash
git log --since="1 week ago" -- config/ src/config/
```

2. Review each commit's diff:
```bash
git show commit_sha
```

3. Identify config value changes
4. Correlate changes with incident symptoms

### Pattern 3: Recent Deployment Broke Code

1. Find deployed commit (from deployment logs)
2. Compare with previous deployment:
```bash
git diff previous_commit deployed_commit
```

3. Review all changes in that diff
4. Identify suspicious changes
5. Test hypothesis by reverting specific changes

### Pattern 4: Bug Introduced Sometime Ago

1. Identify known-good version
2. Use git bisect:
```bash
git bisect start HEAD good_commit
git bisect run ./test-reproduction.sh
```

3. Git identifies first bad commit
4. Review that commit for root cause

## Additional Resources

### Reference Files

For advanced git techniques:
- **`references/git-aliases.md`** - Useful git aliases for RCA
- **`references/git-workflows.md`** - Complete RCA investigation workflows

### Example Files

Working examples:
- **`examples/bisect-script.sh`** - Sample automated bisect script

## Quick Reference

**Recent commits**: `git log --since="1 day ago" --oneline`
**Blame line**: `git blame -L 45,45 file.js`
**Show commit**: `git show abc123`
**Diff commits**: `git diff commit1 commit2`
**Search messages**: `git log --grep="pattern"`
**File history**: `git log -p -- file.js`
**Binary search**: `git bisect start HEAD good_commit`

**Correlate timestamps**: Always compare git timestamps with incident timeline
**Follow renames**: Use `--follow` flag for moved files
**Read full diffs**: Don't just trust commit messages

---

Master git investigation techniques to efficiently trace code history and identify exact commits that introduced production issues.
