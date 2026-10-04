---
name: code-review
description: Use when reviewing a branch, PR, or work-in-progress changes against standards and spec
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [review, code-quality, pr, standards, spec]
---

# Code Review

Two-axis review of the diff between HEAD and a fixed point the user supplies:
- **Standards** - does the code conform to this repo's documented coding standards?
- **Spec** - does the code faithfully implement the originating issue / PRD / spec?

## Process

### 1. Pin the fixed point
Whatever the user said as the fixed point - a commit SHA, branch name, tag, main, HEAD~5, etc. Capture the diff command: `git diff <fixed-point>...HEAD`. Also note the list of commits.

### 2. Identify the spec source
Look for the originating spec: issue references in commit messages, a spec file under docs/ or specs/, or a PRD.

### 3. Run parallel reviews
Spawn sub-agents for the Standards review and Spec review simultaneously. Aggregate findings side by side.

## Common Pitfalls

- **Fixed point not resolving**: Always verify the fixed point resolves with git rev-parse before spawning sub-agents. A bad ref wastes both agents' contexts.
- **Empty diff not caught early**: Check diff is non-empty before starting reviews. An empty diff should fail here, not inside two parallel sub-agents.
- **Spec source not found**: If no spec/issue can be found for the changes, the spec review axis has nothing to compare against. Report this clearly.

## Code Examples

```bash
# Step 1: Pin the fixed point
git rev-parse main
git diff main...HEAD --stat
git log main..HEAD --oneline

# Step 2: Find spec source
# Look in commit messages for issue references (#123)
# Check docs/, specs/, .scratch/ for matching spec files

# Step 3: Run parallel reviews
# Standards review: does code follow this repo's conventions?
# Spec review: does code implement the originating issue?
```

## Verification Checklist

- [ ] Fixed point confirmed (git rev-parse succeeds)
- [ ] Diff is non-empty
- [ ] Spec source identified or reported missing
- [ ] Standards review completed
- [ ] Spec review completed
- [ ] Findings aggregated and reported side by side
