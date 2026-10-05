---
name: git-bisect-assistant
description: Guide efficient bug-finding with git bisect using binary search across commit history, automated test scripts, skip strategies, and complex history.
---

# Git Bisect Assistant

Use git bisect to efficiently find the exact commit that introduced a bug, regression, or unwanted behavioral change. This skill covers manual and automated bisect workflows, handling complex repository histories, writing bisect test scripts, skip strategies for untestable commits, and techniques for bisecting across merge-heavy histories.

## When to Use This Skill

Use this skill when you need to:

- Find the commit that introduced a bug or regression
- Identify when a performance degradation was introduced
- Determine which change broke a previously passing test
- Track down when a configuration change caused unexpected behavior
- Find when a visual regression was introduced
- Identify the commit that changed an API response format
- Locate the source of a memory leak or resource exhaustion
- Determine when a flaky test started failing

**Trigger phrases**: "git bisect", "find regression", "find the commit that broke", "binary search commits", "when did this break", "bisect bug", "track down regression", "find introducing commit"

## What This Skill Does

### Core Capabilities

- **Binary Search Guidance**: Structured approach to bisecting across any commit range
- **Automated Bisect Scripts**: Write test scripts that automate the good/bad classification
- **Skip Strategy**: Handle commits that cannot be tested (build failures, incomplete work)
- **Complex History Navigation**: Bisect across merge commits, rebased branches, and non-linear history
- **Bisect Visualization**: Understand the bisect state and remaining search space
- **Results Interpretation**: Analyze the identified commit and understand the root cause

### How Git Bisect Works

Git bisect performs a binary search through commit history. Given a known "good" commit and a known "bad" commit, it repeatedly selects the midpoint, asks you to test it, and narrows the range based on your answer.

```
Known Good                                              Known Bad
    |                                                       |
    v                                                       v
    G---G---G---?---?---?---?---?---?---?---B---B---B---B---B
                        ^
                    First test (midpoint)

    If midpoint is GOOD:
    G---G---G---G---G---G---G---G---?---?---B---B---B---B---B
                                        ^
                                    Next test

    If midpoint is BAD:
    G---G---G---?---?---B---B---B---B---B---B---B---B---B---B
                    ^
                Next test
```

For N commits, bisect finds the introducing commit in at most log2(N) steps. For 1000 commits, that is approximately 10 tests.

## Instructions

### Phase 1: Prepare for Bisect

**Step 1.1: Identify the good and bad commits**

Before starting bisect, you need two reference points:

```bash
# The bad commit: usually HEAD (current broken state)
BAD_COMMIT="HEAD"

# The good commit: the last known working state
# Option 1: Use a known release tag
GOOD_COMMIT="v2.3.0"

# Option 2: Find the last good commit by testing recent tags/releases
git tag --sort=-v:refname | head -10
# Test each until you find one where the bug does not exist

# Option 3: Use a date-based approach
git log --oneline --after="2025-01-01" --before="2025-02-01" | tail -1
# Test the oldest commit in the range where the bug might have been introduced

# Option 4: If you have no idea when it broke, start with a wide range
git log --oneline | tail -1  # First commit in the repo
```

**Step 1.2: Define the test condition**

Write a clear, repeatable test that determines whether a commit is "good" or "bad":

```markdown
## Test Condition
- **Bug description**: The /api/users endpoint returns 500 instead of 200
- **Test command**: `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/users`
- **Good result**: HTTP 200
- **Bad result**: HTTP 500
- **Prerequisites**: Application must be running (`npm start`)
```

**Step 1.3: Ensure the test is reliable**

```bash
# Verify the test identifies the bad commit correctly
git checkout $BAD_COMMIT
npm install && npm start &
sleep 5
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/users
# Should return 500
kill %1

# Verify the test identifies the good commit correctly
git checkout $GOOD_COMMIT
npm install && npm start &
sleep 5
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/users
# Should return 200
kill %1
```

### Phase 2: Manual Bisect

**Step 2.1: Start the bisect session**

```bash
# Start bisect
git bisect start

# Mark the current commit as bad
git bisect bad HEAD

# Mark the known good commit
git bisect good v2.3.0

# Git checks out the midpoint commit
# Output: Bisecting: 42 revisions left to test after this (roughly 6 steps)
```

**Step 2.2: Test each commit**

At each step, Git checks out a commit for you to test:

```bash
# Build and test the current commit
npm install
npm run build
npm test

# If the bug is present at this commit:
git bisect bad

# If the bug is NOT present at this commit:
git bisect good

# If you cannot test this commit (build failure, etc.):
git bisect skip
```

**Step 2.3: Interpret the result**

When bisect narrows down to a single commit:

```bash
# Git outputs the first bad commit:
# abc1234 is the first bad commit
# commit abc1234
# Author: Jane Developer <jane@example.com>
# Date:   Mon Jan 15 10:30:00 2025 +0000
#
#     Add user caching middleware
#
# path/to/file.ts | 45 ++++++++++++++++++++++++++-------------------

# Examine the commit in detail
git show abc1234
git diff abc1234^ abc1234

# End the bisect session and return to original branch
git bisect reset
```

### Phase 3: Automated Bisect

Automated bisect is the preferred approach for repeatable tests. You provide a script that exits with code 0 (good), 1-124/126-127 (bad), or 125 (skip).

**Step 3.1: Write a bisect test script**

```bash
#!/bin/bash
# bisect-test.sh - Automated bisect test script

set -e

# Clean state
npm ci 2>/dev/null || { echo "npm install failed"; exit 125; }
npm run build 2>/dev/null || { echo "build failed"; exit 125; }

# Run the specific test
npm test -- --filter="users endpoint" 2>/dev/null
TEST_RESULT=$?

# Exit code 0 = good (test passes), 1 = bad (test fails), 125 = skip
if [ $TEST_RESULT -eq 0 ]; then
    exit 0  # Good: bug not present
else
    exit 1  # Bad: bug present
fi
```

**Step 3.2: Run automated bisect**

```bash
# Start bisect with known range
git bisect start HEAD v2.3.0

# Run automated bisect with the test script
git bisect run bash bisect-test.sh

# Git will:
# 1. Check out a commit
# 2. Run your script
# 3. Mark as good/bad/skip based on exit code
# 4. Repeat until the first bad commit is found
# 5. Output the result

# When done, reset
git bisect reset
```

**Step 3.3: Advanced test script patterns**

Test script with server startup:

```bash
#!/bin/bash
# bisect-test-server.sh - Test that requires a running server

cleanup() {
    # Kill background processes
    if [ -n "$SERVER_PID" ]; then
        kill "$SERVER_PID" 2>/dev/null
        wait "$SERVER_PID" 2>/dev/null
    fi
}
trap cleanup EXIT

# Build
npm ci 2>/dev/null || exit 125
npm run build 2>/dev/null || exit 125

# Start server in background
npm start &
SERVER_PID=$!

# Wait for server to be ready
for i in $(seq 1 30); do
    if curl -s http://localhost:3000/health > /dev/null 2>&1; then
        break
    fi
    sleep 1
done

# Test
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/users)

if [ "$HTTP_CODE" = "200" ]; then
    exit 0  # Good
else
    exit 1  # Bad
fi
```

Test script for performance regression:

```bash
#!/bin/bash
# bisect-test-perf.sh - Find when performance regressed

npm ci 2>/dev/null || exit 125
npm run build 2>/dev/null || exit 125

# Run benchmark and capture the result
RESULT=$(npm run benchmark -- --json 2>/dev/null | jq '.results[0].mean')

if [ -z "$RESULT" ]; then
    exit 125  # Could not run benchmark, skip
fi

# Threshold: if mean response time exceeds 200ms, it's "bad"
THRESHOLD=200
EXCEEDED=$(echo "$RESULT > $THRESHOLD" | bc -l)

if [ "$EXCEEDED" = "1" ]; then
    exit 1  # Bad: performance regression present
else
    exit 0  # Good: performance acceptable
fi
```

Test script for Python projects:

```bash
#!/bin/bash
# bisect-test-python.sh

# Set up virtual environment
python3 -m venv .venv 2>/dev/null || exit 125
source .venv/bin/activate

pip install -e ".[dev]" 2>/dev/null || exit 125

# Run specific test
python -m pytest tests/test_users.py::test_list_users -x --tb=short 2>/dev/null
exit $?
```

### Phase 4: Handle Complex Scenarios

**Scenario 4.1: Bisecting across merge commits**

When the history contains many merge commits, bisect may check out merge commits that are difficult to test:

```bash
# Option 1: Use --first-parent to only bisect the mainline commits
git bisect start --first-parent HEAD v2.3.0

# Option 2: Skip merge commits in the test script
#!/bin/bash
# Check if the current commit is a merge commit
PARENT_COUNT=$(git cat-file -p HEAD | grep -c "^parent")
if [ "$PARENT_COUNT" -gt 1 ]; then
    exit 125  # Skip merge commits
fi

# ... rest of test
```

**Scenario 4.2: Bisecting when some commits do not build**

```bash
#!/bin/bash
# bisect-test-with-skip.sh

# Attempt to build; skip if it fails
make build 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Build failed at $(git rev-parse --short HEAD), skipping"
    exit 125
fi

# Run test
make test-specific 2>/dev/null
exit $?
```

When too many consecutive commits fail to build, bisect may report "unable to determine first bad commit" due to insufficient good/bad data points. In that case:

```bash
# Manually test commits around the skip range
git bisect visualize --oneline

# Manually mark specific commits
git bisect good abc1234
git bisect bad def5678
```

**Scenario 4.3: Bisecting a specific file or path**

When you know the bug is in a specific area:

```bash
# Start bisect, limiting to commits that touch specific paths
git bisect start HEAD v2.3.0 -- src/services/user.ts src/middleware/cache.ts

# This restricts bisect to only consider commits that modified these paths
```

**Scenario 4.4: Bisecting with submodules**

```bash
#!/bin/bash
# bisect-test-submodules.sh

# Update submodules for the current commit
git submodule update --init --recursive 2>/dev/null || exit 125

# Build and test
npm ci 2>/dev/null || exit 125
npm test -- --filter="integration" 2>/dev/null
exit $?
```

**Scenario 4.5: Narrowing the range before bisecting**

For very large commit ranges, pre-narrow before bisecting:

```bash
# Find the approximate range using a coarse search
# Test every 100th commit
git log --oneline HEAD...v2.0.0 | awk 'NR % 100 == 0 {print $1}' | while read commit; do
    echo "Testing $commit..."
    git checkout "$commit" 2>/dev/null
    npm ci --silent 2>/dev/null && npm test --silent 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "GOOD: $commit"
        break
    else
        echo "BAD: $commit"
    fi
done

# Once you have a narrower range, bisect within it
git bisect start BAD_COMMIT GOOD_COMMIT
```

### Phase 5: Analyze the Result

**Step 5.1: Examine the introducing commit**

```bash
# Show the full commit details
git show <first-bad-commit>

# Show only the files changed
git show --stat <first-bad-commit>

# Show the diff
git diff <first-bad-commit>^..<first-bad-commit>

# Check if this commit was part of a PR
git log --oneline --merges --ancestry-path <first-bad-commit>..HEAD | head -5
```

**Step 5.2: Verify the finding**

```bash
# Confirm: the parent of the first bad commit should be good
git checkout <first-bad-commit>^
# Run test... should pass (good)

git checkout <first-bad-commit>
# Run test... should fail (bad)
```

**Step 5.3: Document the finding**

```markdown
## Bisect Result

- **First bad commit**: abc1234 ("Add user caching middleware")
- **Author**: Jane Developer
- **Date**: 2025-01-15
- **Files changed**: src/middleware/cache.ts, src/routes/users.ts
- **Root cause**: The caching middleware returns stale data for the /api/users endpoint because it caches responses by URL without considering query parameters.
- **Verification**: Parent commit (abc1233) passes the test; the bad commit fails.
- **Fix**: Add query parameter awareness to the cache key generation in cache.ts.
```

### Bisect Log and Replay

You can save and replay a bisect session:

```bash
# Save the current bisect log
git bisect log > bisect-log.txt

# View the log
cat bisect-log.txt
# git bisect start
# # good: [abc1234] Initial release
# git bisect good abc1234
# # bad: [def5678] HEAD
# git bisect bad def5678
# # good: [111aaaa] Add logging
# git bisect good 111aaaa
# ...

# Replay a previous bisect session
git bisect replay bisect-log.txt
```

### Bisect Visualization

```bash
# Visualize the remaining bisect range
git bisect visualize --oneline

# Show the bisect state in a graph
git bisect visualize --graph --oneline

# Show how many steps remain
git bisect log | tail -1
# "Bisecting: 5 revisions left to test after this (roughly 3 steps)"
```

## Best Practices

- Always write a repeatable, automated test script for bisect rather than testing manually; manual testing is error-prone and slow across many commits
- Use exit code 125 (skip) generously in your test script; it is better to skip a commit than to incorrectly classify it
- Start with a narrow commit range when possible; bisecting across 10,000 commits is feasible but slow if each test takes minutes
- Clean the working directory between tests (use `git clean -fdx` in the test script if needed) to avoid artifacts from previous commits affecting results
- Use `--first-parent` when bisecting on a branch with many merges; it keeps the bisect on the mainline and avoids testing intermediate merge states
- Save the bisect log (`git bisect log`) before resetting, especially for long sessions that you might need to replay
- Verify the result by testing the first bad commit and its parent independently; false results can occur if the test is non-deterministic
- For flaky tests, run the test multiple times in the bisect script and only mark as "bad" if it fails consistently
- Document the bisect process and result in the bug fix commit message or PR description for future reference
- Consider using `git bisect run` with a CI-like script that handles dependency installation, environment setup, and teardown

## Common Pitfalls

- **Non-deterministic tests**: If the test is flaky (sometimes passes, sometimes fails), bisect will produce incorrect results. Run the test multiple times in your script and use majority voting.
- **Forgetting to reset**: If you forget `git bisect reset` after finishing, you remain in a detached HEAD state. Always reset before continuing other work.
- **Incorrect good/bad labels**: Swapping good and bad is easy to do, and bisect will silently search in the wrong direction. Double-check your initial labels.
- **State leaking between tests**: Build artifacts, caches, or database state from a previous commit can affect the test at the current commit. Clean thoroughly between tests.
- **Skipping too many commits**: If too many commits are skipped (exit 125), bisect may not have enough data points to converge. Investigate why commits are being skipped and fix the build issues.
- **Testing the wrong thing**: Ensure your test script is specific to the bug you are investigating. A test that fails for unrelated reasons will mislead the bisect.
- **Ignoring bisect with path limiting**: When you know the bug is in a specific area, using `git bisect start -- path/to/dir` dramatically reduces the number of commits to test.
- **Not handling dependency changes**: Commits that change `package.json`, `requirements.txt`, or build configuration need dependency reinstallation. Always include `npm ci` or equivalent in your test script.
- **Running bisect on uncommitted changes**: Bisect checks out different commits, which will fail or produce confusing results if you have uncommitted changes. Stash or commit before bisecting.
- **Giving up too early**: If bisect seems stuck or produces a suspicious result, check the bisect log, verify the test, and consider restarting with adjusted good/bad boundaries. Bisect is reliable when the test is reliable.
