---
name: review-comments
description: Review and clean up code comments for necessity, accuracy, non-duplication, clarity, and concise explanation of rationale. Use when comments may restate code, repeat a "why" already explained in the file, contain stale or vague claims, or need tightening before a PR.
argument-hint: '[targets...] [--all | --staged | --unpushed | --changed | --fix]'
effort: medium
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Review Comments

Review each comment in its full-file context, then offer actionable removals, rewrites, or code refactors.

## Flags

- `--staged` - git staged files
- `--unpushed` - files changed across all unpushed commits
- `--changed` - git unstaged changes
- `--all` - entire codebase (parallel agents)
- `--fix` - apply safe comment-only removals and rewrites without prompting
- `targets` - one or more source files or directories; overrides scope flags
- Default: `--staged --changed` combined

## Usage

```
/review-comments              # staged + changed (default)
/review-comments --all        # entire codebase
/review-comments --fix        # review and auto-fix
/review-comments src/auth     # review a file or directory
```

## Gotchas
- Framework directives (`// @ts-ignore`, `// eslint-disable`, `// noinspection`) look like "what" comments but are functional. Removing them silently breaks linting or type checking.
- `--staged` on a clean working tree (everything already committed) reviews nothing and reports "No files to review" — which looks like a passing review. Use `--all` after committing.
- Scope flags select files, not only changed lines. Read each selected file in full so repeated rationale and stale explanations can be detected.

## Workflow

### Step 1: Parse Flags

From `$ARGUMENTS`, determine scope:

| Flags Present | Scope |
|---------------|-------|
| (none) | `--staged --changed` |
| `--all` | Entire codebase |
| `--staged` | Staged files only |
| `--unpushed` | Files changed across unpushed commits |
| `--changed` | Unstaged files only |
| `--staged --changed` | Both |
| targets provided | Target files or directories; overrides scope flags |

Strip known flags from `$ARGUMENTS`. Treat any remaining non-flag arguments as targets.

### Step 2: Get File List

**For targets:**
Review each source file directly. For each directory, recursively find source files under it using the same exclusions as `--all`. Deduplicate the combined list. If no target exists or none contains source files, report "No files to review" and stop.

**For --staged:**
```bash
git diff --cached --name-only
```

**For --unpushed:**
```bash
# Range from oldest unpushed commit's parent to HEAD.
git diff --name-only "$(git rev-list HEAD --not --remotes | tail -1)^"..HEAD
```
If nothing is unpushed, or there is no remote/upstream (or the range walks back to the root commit) so it can't be determined reliably, stop and ask the user to pick another scope.

**For --changed:**
```bash
git diff --name-only
```

**For --all:**
```bash
# Use Glob to find all source files
**/*.{ts,tsx,js,jsx,py,go,java,kt,swift,rs,c,cpp,h,hpp,cs,rb,php}
```

Filter to only source code files (exclude node_modules, build dirs, etc.).

### Step 3: Review Comments

Apply any comment conventions from the repository's applicable agent instructions in addition to this rubric.

**For targets or --staged/--changed/--unpushed (small file lists):**
Read each file in full and analyze its comments against the surrounding declarations, control flow, and other comments in that file. Review comments outside the changed hunks too when they duplicate or contradict a comment in the changed code.

**For --all (large codebase):**
Split files into balanced batches that each worker can read in full:

1. Get all source files
2. Choose batch sizes that keep each assignment manageable; use the smallest useful set of workers.
3. Dispatch one worker per batch, queuing within the runtime concurrency limit. Each returns findings without editing files. Disable delegation tools where supported and tell workers to review their assigned files themselves:

```
Prompt per batch:
---
Review comments in these files for quality issues:
{file_list}

Read every assigned file in full. For each comment, determine whether it:
1. Repeats rationale already explained elsewhere in the same file, even with different wording
2. Explains a useful constraint or tradeoff less clearly or concisely than it could
3. Restates code or compensates for weak naming/structure
4. Makes an inaccurate, stale, vague, or unverifiable claim
5. Leaves old code commented out instead of relying on version control
6. Uses TODO/FIXME without naming the concrete action, blocker, or stable issue reference
7. Adds no information a maintainer needs

Do not flag a comment merely because it is long or uses a particular style. Report only actionable findings. Preserve functional directives, legal notices, generated markers, and comments whose repetition is necessary at separate hazardous call sites.
Apply any comment conventions in the repository's applicable agent instructions.

Return findings in this format:
## {filename}
- Line {n}: "{comment}" → {issue type}; {remove, exact rewrite, or refactor}. If duplicated, cite the earlier authoritative line.
---
```

4. Collect and merge results from all agents

### Step 4: Report Findings

```markdown
## Comment Review: {scope}

### Issues Found

#### {filename}
| Line | Current Comment | Issue | Suggestion |
|------|-----------------|-------|------------|
| {n} | "{comment}" | {Duplicate rationale / Verbose rationale / Unclear rationale / Stale claim / What not why / Commented-out code / Vague TODO / Noise} | {exact removal, rewrite, or refactor} |

### Summary
- Files reviewed: {count}
- Issues found: {count}
- Most common issue: {type}
```

### Step 5: Offer to Fix

**If `--fix` flag is present:** Skip the prompt and apply safe comment-only dispositions: remove duplicates, noise, and commented-out code; rewrite useful but unclear or verbose rationale. Do not rename symbols, extract functions, restructure executable code, or invent missing rationale. Leave refactor-only and unverifiable findings unchanged and list them as deferred in the cleanup summary.

**Otherwise**, if issues were found, ask the user:

```
Found {n} comments with actionable improvements. How would you like to proceed?

1. **Apply recommendations** - Remove, rewrite, or refactor each finding as reported
2. **Remove only** - Delete only comments classified as duplicate or noise
3. **Cherry-pick** - Show me each one and I'll decide
4. **Skip** - Keep the report, don't change anything
```

Based on user choice:

**Option 1 (Apply recommendations):**
- Apply the exact suggested disposition for each finding
- Preserve the underlying rationale when rewriting or consolidating comments
- Report removals, rewrites, and refactors separately

**Option 2 (Remove only):**
- Remove only findings classified as duplicate rationale or noise
- Leave rewrite and refactor findings unchanged
- Report the comments removed

**Option 3 (Cherry-pick):**
- Present each issue one at a time: "Line 42: `// increment counter` - Remove? (y/n/stop)"
- Apply user's choices

**Option 4 (Skip):**
- End without changes

## Comment Review Method

Judge comments by meaning, not by whether they superficially fit the "why" pattern.

For every non-functional comment:

1. **Identify the claimed rationale.** State the constraint, tradeoff, invariant, workaround, or business rule the comment is trying to preserve. If it has none, it is probably narrating the code.
2. **Verify the content.** Check that the surrounding code still behaves as claimed and that references, names, units, and edge cases are accurate. Do not invent intent to rescue a stale comment.
3. **Search the full file for the same idea.** Compare semantics, not exact wording. A second comment is duplicate if a maintainer learns no new constraint from it.
4. **Choose the authoritative location.** Keep the clearest explanation nearest the code whose maintenance depends on it. Consolidate nearby duplicates. Repetition is justified only when each location is independently hazardous or the comment documents a separate consequence.
5. **Compress without losing the reason.** Prefer one direct sentence naming the reason and its consequence. Remove scene-setting, history, code narration, hedging, and repeated details. A paragraph is acceptable only when multiple independent constraints are necessary and code or a focused reference cannot express them more clearly.
6. **Check maintenance markers.** Remove commented-out code unless it is an intentional example or test fixture. Require TODO/FIXME comments to name a concrete action plus either the blocking condition or a stable issue reference.
7. **Choose the right fix.** Remove comments with no durable information; rewrite useful but verbose or vague rationale; improve names or structure when the code can carry the meaning; retain comments that are already necessary, accurate, and concise.

Report only findings with a concrete improvement. For a rewrite, provide replacement text rather than saying only "make concise." For duplicate rationale, cite both locations and say which one should remain.

## Comment Quality Guidelines

### Good Comments (WHY)
- Explain business logic decisions
- Document performance considerations
- Clarify non-obvious algorithms
- Explain workarounds or edge cases
- Document assumptions or constraints
- Add rationale not already available in the same file
- State that rationale directly and at the narrowest useful scope

### Bad Comments (WHAT)
- Describe what the code is doing syntactically
- Restate variable names or method calls
- Explain obvious operations
- Add noise without value
- Repeat a rationale already documented nearby
- Preserve obsolete history instead of a current constraint
- Bury the useful reason inside a paragraph of setup or implementation detail
- Use vague claims such as "for performance" without naming the relevant cost or constraint
- Leave dead code commented out when version control already preserves it
- Say only `TODO: fix this` without a concrete action or traceable blocker

### Better Alternatives
Instead of "what" comments, prefer:
- Extracting functions with descriptive names
- Using meaningful variable names
- Writing self-documenting code
- One authoritative comment for a shared invariant or workaround
- A focused issue or design document when the full history matters

## Examples

### Bad Comment
```python
# Loop through users and check if active
for user in users:
    if user.is_active:
        active_users.append(user)
```

### Good Refactor
```python
active_users = [u for u in users if u.is_active]
```

### Good Comment (when needed)
```python
# Use binary search here because users list is sorted and can exceed 100k items
index = bisect.bisect_left(sorted_users, target_user)
```

### Duplicate Rationale
```python
# Preserve insertion order because the export format is user-visible.
ordered_fields = collect_fields(schema)

# Keep these fields ordered so exports remain stable for users.
return serialize(ordered_fields)
```

Keep the first comment if it establishes the invariant for the whole operation; remove the second because it adds no new constraint. Keep both only if the locations can be changed independently and each is unsafe without the local warning.

### Verbose but Useful Rationale
```python
# We need to make a copy of this list here. The reason is that callers often retain
# the original list and later compare it with the result, and sorting the same list
# in place would therefore create surprising behavior for them.
items = list(items)
```

Rewrite as:

```python
# Copy before sorting so callers' lists remain unchanged.
items = list(items)
```

## Troubleshooting

### False positives on license headers or necessary comments
**Solution:** Skip license headers, legal notices, generated markers, and regulatory annotations. Assess API documentation (JSDoc, docstrings) against its public contract rather than forcing it into the "why" rubric; flag it only when it is inaccurate, duplicated, or needlessly unclear.

### Comments in unfamiliar language or framework
**Solution:** Focus on structural patterns (e.g., comments restating the next line of code are low-quality in any language). For framework-specific annotations or directives you do not recognize, leave them in place and flag them for manual review rather than removing them.

## Notes

- For `--all` on large codebases, parallel agents significantly speed up review
- Focus on actionable suggestions, not nitpicks
- If no files match the scope, report "No files to review"
