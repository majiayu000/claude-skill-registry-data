---
name: review-history
description: Analyze how code changed over time. Use when investigating regressions, understanding why code was written a certain way, or finding when a behavior changed.
argument-hint: <file, function, or feature area>
effort: medium
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Review History

Investigate how code evolved over time to understand current behavior or find regressions.

## Usage

```
/review-history src/auth/login.ts
/review-history the authentication flow
/review-history UserProfile component
```

## Gotchas
- `git log -S` finds commits where the string was added OR removed. A commit that deleted a function surfaces as equally relevant to the one that added it — verify the direction of change.
- Squash merges erase commit-level traceability. `git reflog` only works locally and expires — if another contributor squashed and force-pushed, the original commits are unrecoverable.

## Workflow

### Step 1: Identify Target Files

From the provided topic, identify the relevant files:
- If a file path is given, use it directly
- If a feature/function name, locate relevant files using this strategy:
  1. Grep for the exact function/class name to find where it is defined and used
  2. Glob for files with the feature name in the path (e.g., `**/*payment*`)
  3. Prioritize source files over test files; include tests only if investigating test behavior
  4. Limit to the 5 most relevant files to keep the analysis focused

### Step 2: Git History Analysis

Run these in parallel:

**Recent commits touching the area:**
```bash
git log --oneline -20 -- <file_or_directory>
```

**Detailed blame for key sections:**
```bash
# For files > 200 lines: target the specific function or section under investigation.
# Use Grep to find the line range first, then:
git blame -L <start>,<end> <file>

# For files ≤ 200 lines: blame the entire file:
git blame <file>
```

**Find when specific code was introduced:**
```bash
git log -S "<search_term>" --oneline -- <file>
```

**Check for recent refactors:**
```bash
git log --oneline --since="3 months ago" -- <file_or_directory>
```

Adjust the time window based on context:
- Investigating a recent regression: use `--since="2 weeks ago"`
- Understanding a feature's evolution: use `--since="6 months ago"` or omit `--since` entirely
- If the initial window returns fewer than 3 commits, double the window and retry once

### Step 3: Search Past Issue Logs

Check if this problem occurred before:

1. List past issue logs:
   - Glob pattern: `docs/log/*.md`

2. Search logs for relevant keywords:
   - Grep pattern: `{keywords}` path: `docs/log/`

Look for:
- Similar error messages
- Same file/function names
- Related symptoms

### Step 4: Synthesize Findings

Populate the report using these methods:

- **Recent Changes**: List commits from `git log`, most recent first. Include only commits that touch the target code.
- **Key Code Introduction**: Use `git log -S` results to identify when the function/feature first appeared and its last substantive change (skip formatting-only commits).
- **Related Past Issues**: Direct matches from Step 3. If none found, state "None found in docs/log/".
- **Regression Risk**: Compare current behavior against commit history. If code worked before a specific commit and broke after, name that commit. If no clear regression point, state "No clear regression identified — behavior may be by design."

Report:

```markdown
## History Analysis: {target}

### Recent Changes
| Date | Commit | Author | Summary |
|------|--------|--------|---------|
| {date} | {hash} | {author} | {message} |

### Key Code Introduction
- `{function/feature}` introduced in {commit} on {date}
- Last modified: {commit} by {author}

### Related Past Issues
{any matching docs/log entries, or "None found"}

### Regression Risk
{assessment: was this working before? when did it break?}
```

## Examples

**Trace when a payment bug was introduced:**
> /review-history processPayment

Uses `git log -S` and `git blame` to trace the payment processing function, identifies the commit that changed the rounding logic three weeks ago, and cross-references with past issue logs to confirm this is when the billing discrepancy started.

**Understand why validation works a certain way:**
> /review-history src/validators/address.ts

Analyzes the git history of the address validator, surfaces the original commit that added the unusual postal code regex along with its commit message explaining a partner API requirement, and checks past issue logs for related context.

## Troubleshooting

### Relevant commit was squashed or rebased away
**Solution:** Use `git reflog` to find the original commit before the squash or rebase. If the reflog has expired, search for the change using `git log -S "<code_snippet>" --all` to locate it in any branch or dangling commit.

### History is too large to analyze effectively
**Solution:** Narrow the scope by passing a specific file path or function name instead of a broad directory. Use `--since` with `git log` to limit the time window, or focus on a single author's contributions with `--author`.

## Notes

- Focus on commits from the last 3-6 months unless investigating older issues
- Pay attention to refactors, dependency updates, and merge commits
- If a past issue log matches, read it fully - it may contain the solution
