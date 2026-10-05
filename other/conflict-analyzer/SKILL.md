---
name: conflict-analyzer
description: Analyze and resolve merge conflicts systematically using three-way merge analysis, conflict classification, resolution strategies, and prevention.
---

# Conflict Analyzer

Systematically analyze merge conflicts to understand their root cause, classify their type (textual, semantic, or structural), and apply the correct resolution strategy. This skill covers three-way merge analysis, automated resolution techniques, manual resolution guidance, conflict prevention practices, and rebase-vs-merge decision making.

## When to Use This Skill

Use this skill when you need to:

- Resolve merge conflicts in a feature branch or pull request
- Understand why a conflict occurred and which changes to keep
- Decide between rebase and merge for branch integration
- Resolve conflicts in configuration files, lockfiles, or generated code
- Handle complex conflicts involving renamed or moved files
- Establish team conventions for conflict prevention
- Automate conflict resolution for predictable patterns (changelog, version files)
- Analyze a conflict-heavy repository to reduce future conflict frequency
- Resolve conflicts during a cherry-pick or rebase operation

**Trigger phrases**: "merge conflict", "resolve conflict", "conflict resolution", "rebase conflict", "three-way merge", "merge strategy", "conflict prevention", "rebase vs merge"

## What This Skill Does

### Core Capabilities

- **Conflict Classification**: Categorize conflicts as textual, semantic, or structural to determine the appropriate resolution approach
- **Three-Way Merge Analysis**: Examine the base, ours, and theirs versions to understand exactly what changed on each side
- **Resolution Strategy Selection**: Match conflict types to proven resolution strategies
- **Automated Resolution**: Generate resolution scripts for predictable conflict patterns
- **Prevention Guidance**: Identify practices and repository structures that minimize conflicts
- **Rebase vs Merge Analysis**: Evaluate which integration strategy is appropriate for the situation

### Conflict Types

| Type | Description | Resolution Complexity |
|------|-------------|----------------------|
| Textual | Same lines modified on both branches | Low to Medium |
| Semantic | Different lines changed but logic conflicts | Medium to High |
| Structural | File moved, renamed, or deleted on one side | Medium |
| Content-Model | Changes to data formats, schemas, or APIs | High |
| Lockfile | Package manager lockfile divergence | Low (regenerate) |
| Generated Code | Auto-generated files modified on both sides | Low (regenerate) |

### Three-Way Merge Model

```
          Base (common ancestor)
         /                      \
        v                        v
    Ours (current branch)    Theirs (incoming branch)
        \                        /
         v                      v
          Merged Result
```

## Instructions

### Phase 1: Analyze the Conflict

**Step 1.1: Identify all conflicting files**

```bash
# List all files with merge conflicts
git diff --name-only --diff-filter=U

# Show the conflict markers in each file
git diff --check

# Get a summary of the merge state
git status
```

**Step 1.2: Examine the three-way merge for each conflicting file**

```bash
# View the base version (common ancestor)
git show :1:path/to/file.ts    # Stage 1 = base

# View "ours" version (current branch)
git show :2:path/to/file.ts    # Stage 2 = ours

# View "theirs" version (incoming branch)
git show :3:path/to/file.ts    # Stage 3 = theirs

# Compare ours vs base (what we changed)
git diff :1:path/to/file.ts :2:path/to/file.ts

# Compare theirs vs base (what they changed)
git diff :1:path/to/file.ts :3:path/to/file.ts
```

**Step 1.3: Classify each conflict**

```python
from enum import Enum

class ConflictType(Enum):
    TEXTUAL_SAME_BLOCK = "textual_same_block"
    TEXTUAL_ADJACENT = "textual_adjacent"
    SEMANTIC_LOGIC = "semantic_logic"
    SEMANTIC_ORDERING = "semantic_ordering"
    STRUCTURAL_RENAME = "structural_rename"
    STRUCTURAL_DELETE = "structural_delete"
    LOCKFILE = "lockfile"
    GENERATED = "generated"

def classify_conflict(file_path: str, conflict_region: dict) -> ConflictType:
    """Classify a merge conflict based on the changes involved."""
    # Lockfiles are always regenerated
    if file_path.endswith(("package-lock.json", "yarn.lock", "Pipfile.lock", "go.sum")):
        return ConflictType.LOCKFILE

    # Generated files should be regenerated
    if file_path.endswith((".generated.ts", ".g.dart", ".pb.go")):
        return ConflictType.GENERATED

    # Check if both sides modified the exact same lines
    ours_changed_lines = set(conflict_region["ours_lines"])
    theirs_changed_lines = set(conflict_region["theirs_lines"])

    if ours_changed_lines & theirs_changed_lines:
        return ConflictType.TEXTUAL_SAME_BLOCK
    elif abs(min(ours_changed_lines) - max(theirs_changed_lines)) <= 3:
        return ConflictType.TEXTUAL_ADJACENT
    else:
        return ConflictType.SEMANTIC_LOGIC
```

### Phase 2: Understand What Changed

**Step 2.1: Read the conflict markers**

A standard conflict block looks like this:

```
<<<<<<< HEAD (ours)
  const timeout = 5000;
  const retries = 3;
=======
  const timeout = 10000;
  const retries = 5;
  const backoff = "exponential";
>>>>>>> feature/retry-config (theirs)
```

With `diff3` style (recommended), Git also shows the base:

```
<<<<<<< HEAD (ours)
  const timeout = 5000;
  const retries = 3;
||||||| merged common ancestors (base)
  const timeout = 5000;
  const retries = 3;
=======
  const timeout = 10000;
  const retries = 5;
  const backoff = "exponential";
>>>>>>> feature/retry-config (theirs)
```

**Step 2.2: Enable diff3 conflict style (highly recommended)**

```bash
# Enable globally for all repositories
git config --global merge.conflictstyle diff3

# Or for this repository only
git config merge.conflictstyle diff3
```

With `diff3`, the base version is visible, making it clear what each side changed relative to the original.

**Step 2.3: Understand the intent of each change**

```bash
# Find the commits that introduced each side of the conflict
git log --oneline --left-right HEAD...MERGE_HEAD -- path/to/file.ts

# View the full commit message for context
git log -1 --format="%B" <commit-hash>

# Show the PR or branch name for additional context
git log --oneline --decorate HEAD...MERGE_HEAD -- path/to/file.ts
```

### Phase 3: Apply Resolution Strategies

**Strategy 3.1: Accept one side entirely**

When one side's change is clearly correct or supersedes the other:

```bash
# Accept ours (keep current branch version)
git checkout --ours path/to/file.ts
git add path/to/file.ts

# Accept theirs (keep incoming branch version)
git checkout --theirs path/to/file.ts
git add path/to/file.ts
```

**Strategy 3.2: Combine both changes**

When both sides made non-overlapping improvements:

```
# Base:
def process(data):
    validate(data)
    return transform(data)

# Ours: Added logging
def process(data):
    logger.info("Processing started")
    validate(data)
    return transform(data)

# Theirs: Added error handling
def process(data):
    validate(data)
    try:
        return transform(data)
    except TransformError as e:
        raise ProcessingError(str(e))

# Resolution: Combine both improvements
def process(data):
    logger.info("Processing started")
    validate(data)
    try:
        return transform(data)
    except TransformError as e:
        raise ProcessingError(str(e))
```

**Strategy 3.3: Regenerate for lockfiles and generated code**

```bash
# Package lockfiles: delete and regenerate
git checkout --theirs package.json  # Accept the combined dependency list
rm package-lock.json
npm install

# Or for yarn
git checkout --theirs package.json
rm yarn.lock
yarn install

# For generated code
git checkout --theirs schema.graphql  # Accept the updated schema
npm run codegen  # Regenerate TypeScript types

# Stage the regenerated files
git add package-lock.json  # or yarn.lock, generated files
```

**Strategy 3.4: Resolve import/require conflicts**

Import conflicts are common when both branches add imports to the same region:

```typescript
// Conflict:
<<<<<<< HEAD
import { UserService } from "./services/user";
import { AuthMiddleware } from "./middleware/auth";
=======
import { UserService } from "./services/user";
import { RateLimiter } from "./middleware/rate-limiter";
>>>>>>> feature/rate-limiting

// Resolution: Keep all unique imports, maintain consistent ordering
import { AuthMiddleware } from "./middleware/auth";
import { RateLimiter } from "./middleware/rate-limiter";
import { UserService } from "./services/user";
```

**Strategy 3.5: Resolve changelog and version file conflicts**

```bash
# For CHANGELOG.md: both branches added entries at the top
# Resolution: include both entries, order by date (newest first)

# For version files: choose the higher version or merge version bumps
# If ours = 1.3.0 and theirs = 1.2.1, choose 1.3.0
# If both bump the same segment, bump further: 1.3.0 + 1.3.0 -> decide based on semver
```

**Automated changelog conflict resolution script**:

```bash
#!/bin/bash
# resolve-changelog.sh - Automatically resolve CHANGELOG.md conflicts

FILE="CHANGELOG.md"

if ! grep -q "<<<<<<" "$FILE"; then
    echo "No conflicts in $FILE"
    exit 0
fi

# Extract ours and theirs sections
git show :2:"$FILE" > /tmp/changelog-ours.md
git show :3:"$FILE" > /tmp/changelog-theirs.md
git show :1:"$FILE" > /tmp/changelog-base.md

# Find lines unique to ours (relative to base)
diff /tmp/changelog-base.md /tmp/changelog-ours.md | grep "^>" | sed 's/^> //' > /tmp/ours-additions.txt

# Find lines unique to theirs (relative to base)
diff /tmp/changelog-base.md /tmp/changelog-theirs.md | grep "^>" | sed 's/^> //' > /tmp/theirs-additions.txt

# Combine: use theirs as base, insert our additions after the header
# (customize this logic for your changelog format)
echo "Manual review recommended. Unique additions from each branch:"
echo "--- Ours ---"
cat /tmp/ours-additions.txt
echo "--- Theirs ---"
cat /tmp/theirs-additions.txt
```

### Phase 4: Validate the Resolution

**Step 4.1: Verify the resolution compiles and passes tests**

```bash
# Check for any remaining conflict markers
grep -rn "<<<<<<\|======\|>>>>>>" path/to/file.ts

# Compile/lint the resolved file
npx tsc --noEmit path/to/file.ts
npx eslint path/to/file.ts

# Run tests related to the changed code
npm test -- --filter="path/to/file"

# Run the full test suite to catch semantic conflicts
npm test
```

**Step 4.2: Review the merge result**

```bash
# Show the combined diff of the resolution
git diff --cached path/to/file.ts

# Compare the resolution against each branch
git diff HEAD -- path/to/file.ts       # Compare to ours
git diff MERGE_HEAD -- path/to/file.ts  # Compare to theirs
```

**Step 4.3: Complete the merge**

```bash
# Stage resolved files
git add path/to/file.ts

# Check that all conflicts are resolved
git status

# Complete the merge commit
git commit
# Git will open the editor with a pre-filled merge commit message
```

### Phase 5: Rebase vs Merge Decision Framework

**When to use merge (no-ff)**:

```bash
# Merge preserves the branch topology and is safer for shared branches
git merge --no-ff feature/my-feature
```

Use merge when:
- The branch has been pushed and shared with others
- You want to preserve the feature branch history as a unit
- The branch has many commits and you want them grouped under a merge commit
- Company policy requires merge commits for traceability

**When to use rebase**:

```bash
# Rebase creates a linear history by replaying commits on top of the target
git rebase main
```

Use rebase when:
- The branch is local and has not been shared
- You want a clean, linear history
- The branch has few commits that benefit from being replayed
- You are updating a feature branch to incorporate latest main changes

**Decision matrix**:

```
                    Branch shared?
                   YES          NO
              +----------+----------+
  Many        | Merge    | Rebase   |
  conflicts?  |          | or Merge |
  YES         |          |          |
              +----------+----------+
  Many        | Merge    | Rebase   |
  conflicts?  |          |          |
  NO          |          |          |
              +----------+----------+
```

### Phase 6: Conflict Prevention

**Step 6.1: Repository structure practices**

```yaml
prevention_strategies:
  - name: "Small, focused branches"
    description: "Keep branches short-lived (1-3 days) and focused on a single concern"
    impact: "Reduces the window for conflicting changes"

  - name: "Modular code organization"
    description: "Separate concerns into distinct files and modules"
    impact: "Different features modify different files"

  - name: "Consistent formatting"
    description: "Use automated formatters (Prettier, Black, gofmt) with pre-commit hooks"
    impact: "Eliminates whitespace and formatting conflicts"

  - name: "Lockfile regeneration"
    description: "Always regenerate lockfiles rather than manually resolving conflicts"
    impact: "Lockfile conflicts become trivial"

  - name: "Feature flags over long-lived branches"
    description: "Use feature flags to merge incomplete features into main safely"
    impact: "Eliminates long-lived branches, the primary source of complex conflicts"
```

**Step 6.2: Git configuration for conflict reduction**

```bash
# Use diff3 conflict style for better context
git config --global merge.conflictstyle diff3

# Enable rerere (reuse recorded resolution) to auto-resolve repeated conflicts
git config --global rerere.enabled true

# Set a merge strategy for specific file types
echo "package-lock.json merge=ours" >> .gitattributes
echo "yarn.lock merge=ours" >> .gitattributes

# Use union merge for changelog-style files (append both sides)
echo "CHANGELOG.md merge=union" >> .gitattributes
```

**Step 6.3: Pre-merge conflict detection**

```bash
# Check for conflicts before starting the merge
git merge --no-commit --no-ff feature/branch
if [ $? -ne 0 ]; then
    echo "Conflicts detected. Review before proceeding."
    git diff --name-only --diff-filter=U
    git merge --abort
fi
```

**Step 6.4: Use rerere for recurring conflicts**

```bash
# Enable rerere globally
git config --global rerere.enabled true

# After resolving a conflict, rerere records the resolution
git add resolved-file.ts
git commit

# Next time the same conflict occurs, Git applies the recorded resolution
# automatically. Check with:
git rerere status
git rerere diff
```

## Best Practices

- Always enable `diff3` conflict style to see the base version in conflict markers; without it, you are guessing what the original code looked like
- Enable `rerere` to automatically resolve recurring conflicts, especially useful during long-running rebase operations
- Resolve conflicts file by file, running the linter or compiler after each resolution to catch errors early
- For lockfiles, never manually edit the conflict markers; delete the lockfile and regenerate it
- Use `.gitattributes` to configure merge strategies for files that have predictable conflict patterns (changelogs, version files)
- Keep branches short-lived and rebase frequently against the target branch to minimize conflict surface area
- When resolving semantic conflicts, read the full context of both changes (not just the conflicting lines) to understand the intent
- After resolving all conflicts, run the full test suite before committing; textual resolution correctness does not guarantee semantic correctness
- Document non-obvious resolution decisions in the merge commit message so future reviewers understand why a particular resolution was chosen
- When in doubt, ask the author of the other branch to review the conflict resolution

## Common Pitfalls

- **Blindly accepting one side**: Using `--ours` or `--theirs` without understanding both changes risks losing important work. Always analyze both sides before deciding.
- **Manually editing lockfiles**: Lockfile conflicts should never be resolved by hand-editing JSON. The result is almost always an invalid or inconsistent lockfile. Regenerate instead.
- **Forgetting to check for remaining conflict markers**: A file can have multiple conflict regions. Resolving one and committing without checking for others leaves broken markers in the code.
- **Not running tests after resolution**: A textually correct resolution may be semantically wrong. Two functions that independently work may conflict in behavior (duplicate variable names, incompatible type changes, race conditions).
- **Resolving conflicts during a rebase without understanding the replay order**: During rebase, conflicts are resolved one commit at a time, and the "ours" and "theirs" semantics are reversed from what you might expect. In a rebase, "ours" is the branch you are rebasing onto (main), and "theirs" is your commit being replayed.
- **Force-pushing after rebase without communicating**: If you rebase a shared branch and force-push, everyone else working on that branch will have divergent history. Coordinate before rebasing shared branches.
- **Ignoring whitespace-only conflicts**: While whitespace conflicts seem trivial, resolving them inconsistently introduces formatting drift. Use a formatter to normalize after resolution.
- **Not using merge commits for traceability**: Squash-merging everything makes it impossible to trace which feature branch introduced a specific change. Use merge commits (with `--no-ff`) when branch history matters.
- **Resolving the same conflict repeatedly**: If you keep encountering the same conflict (e.g., during a rebase across many commits), enable `rerere` to record and replay the resolution automatically.
- **Not considering the broader impact**: A conflict in one file may indicate that related (non-conflicting) changes in other files also need to be reconciled. Review the full diff on both branches, not just the conflicting files.
