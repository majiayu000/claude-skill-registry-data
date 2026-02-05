---
name: de-slop
description: This skill should be used to remove AI-generated artifacts and unnecessary code before committing. It scans changed files for redundant comments, AI TODOs, excessive docstrings, and unnecessary markdown files. Git-only, no GitHub required.
---

# De-Slop Skill

Remove AI-generated artifacts before committing or creating PRs. Always dry-run first with numbered selection.

## When to Use

This skill should be invoked when the user:
- Says "de-slop", "clean up slop", "remove AI artifacts", or "clean before commit"
- Is about to commit changes and mentions cleaning/reviewing code
- Asks to check for unnecessary comments, TODOs, or files
- Wants to prepare code for PR by removing AI-generated artifacts

## Workflow

### 1. Determine Comparison Base

**Ask user** what to compare against (or use sensible default):
- No args: Compare against main/master branch
- Branch name provided: Compare against that branch

```bash
# Get default branch
git remote show origin | grep "HEAD branch" | cut -d ":" -f 2 | xargs

# Get changed files
git diff --name-only {BASE}...HEAD

# Get change summary
git diff --stat {BASE}...HEAD
```

If no remote, fall back to:
```bash
git diff --name-only main...HEAD
# or
git diff --name-only master...HEAD
```

### 2. Scan for Slop Patterns (Dry Run Only)

Scan all changed files for these patterns. **DO NOT modify anything yet.**

#### A. Unnecessary Markdown Files

**Flag for deletion:**
- Filenames matching: `NOTES.md`, `PLAN.md`, `ARCHITECTURE.md`, `THOUGHTS.md`, `IDEAS.md`, `SCRATCH.md`, `TEMP.md`, `TODO.md`
- Case-insensitive match
- Only if they appear in changed files

**Never touch:**
- `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`
- Anything in `docs/**` directory
- Any markdown with specific project purpose

#### B. Redundant Comments

Comments that just restate what the next line obviously does:

**Python example:**
```python
# Create user  ← Redundant
user = User()

# Save to database  ← Redundant
db.save(user)
```

**TypeScript example:**
```typescript
// Initialize the counter  ← Redundant
const counter = 0;

// Return the result  ← Redundant
return result;
```

**Detection:**
- Single-line comment immediately before code
- Comment essentially restates the code
- Adds no context, reasoning, or "why"

#### C. AI TODO Comments

Pattern: `# TODO: (Add|Consider|Might|Should|Could|May|Probably)`

**Examples to flag:**
```python
# TODO: Add error handling
# TODO: Consider edge cases
# TODO: Might need optimization
# TODO: Should validate input
```

**Keep these (specific/actionable):**
```python
# TODO: Handle timezone conversion for EU users (ticket #123)
# TODO: Replace with new API endpoint after v2 launch
```

#### D. Excessive Docstrings

Flag docstrings that are excessively long for trivial functions.

**Check for:**
- Function has ≤5 lines of actual code
- Docstring has >3 lines
- Docstring just restates what code obviously does

**Bad example:**
```python
def get_name(self) -> str:
    """Get the name property.

    This method returns the name property of the object.
    It retrieves the stored name value and returns it to the caller.
    The name is a string representing the object's name.

    Returns:
        str: The name of the object
    """
    return self.name
```

**Good docstring (keep):**
```python
def parse_date(s: str, tz: str = "UTC") -> datetime:
    """Parse date string with timezone handling.

    Supports ISO 8601 and common formats. Falls back to UTC
    if timezone parsing fails.
    """
```

#### E. Mock-Heavy Tests

Flag tests with excessive mocking that test nothing real.

**Pattern:**
- Count `@patch` decorators per test function
- Flag if >3 patches
- Note: CLAUDE.md says "no mocking in tests"

**Example to flag:**
```python
@patch('module.thing1')
@patch('module.thing2')
@patch('module.thing3')
@patch('module.thing4')  # 4 patches = flag
def test_something(m1, m2, m3, m4):
    # Tests nothing real
    assert True
```

#### F. Fake Data in Comments/Docs

Flag suspiciously specific claims without citation:

**Patterns:**
- "according to studies" (no link)
- "research indicates" (no source)
- "X% of users" (no citation)
- Specific performance metrics without benchmark
- Made-up case studies

**Examples:**
```python
# This improves performance by 47%  ← Flag (no source)
# According to research, users prefer this  ← Flag (no citation)
```

### 3. Present Findings with Numbered Selection

Display all findings with clear numbering and actions:

```
🔍 Scanned X files, found Y slop patterns

[1] NOTES.md (45 lines)
    → DELETE: Unnecessary markdown file

[2] src/user.py:23-28 (6 lines)
    → REMOVE redundant comments:

    22: def create_user(name: str):
    23:     # Create user
    24:     user = User(name)
    25:     # Save to database
    26:     db.save(user)
    27:     # Return user
    28:     return user

[3] src/api.py:15-25 (11 lines)
    → SIMPLIFY excessive docstring on get_name()

    Current: 8 lines for 1-line getter
    Suggest: """Return the object's name."""

[4] src/utils.py:42
    → REMOVE AI TODO:
    # TODO: Add error handling

[5] tests/test_user.py:50-70 (test_create_with_mocks)
    → ⚠️  FLAG: Mock-heavy (5 @patch decorators)
    Review manually - may not test real behavior

[6] docs/performance.md:12
    → ⚠️  FLAG: "improves performance by 47%" (no source)
    Review manually - add citation or remove claim

---
Select items to clean:
  • Enter numbers: 1 2 4
  • Range: 1-4
  • 'all' - clean items 1-4 (skips flags)
  • 'none' - cancel

Selection: _
```

**Important:**
- Show ±3 lines of context for code issues
- Group by file when multiple issues in same file
- Separate "actions" (delete/remove/simplify) from "flags" (review needed)
- "all" only applies to action items, never flags

### 4. Execute User Selection

Parse user input (numbers, ranges, 'all', 'none').

#### For File Deletions
```bash
git rm {FILE}
```

If file has unstaged changes, show error and skip.

#### For Code Cleanup

Use Edit tool to:
- Remove redundant comments (preserve indentation)
- Simplify excessive docstrings (keep concise version)
- Remove AI TODO comments

**Show before/after for each edit:**
```
Editing src/user.py...

Before (lines 23-28):
    # Create user
    user = User(name)
    # Save to database
    db.save(user)

After:
    user = User(name)
    db.save(user)

✓ Removed 2 redundant comments
```

#### For Flagged Items

Do NOT auto-fix. Instead:
- Display file path and line numbers
- Show issue description
- Ask: "Open {file} for manual review? (y/n)"

### 5. Summary Report

```
✅ Cleaned:
  • 2 files deleted
    - NOTES.md
    - TODO.md
  • 12 redundant comments removed
  • 3 docstrings simplified
  • 8 AI TODOs removed
  • 67 total lines removed

⚠️  Flagged for manual review:
  • tests/test_user.py:50-70 (mock-heavy, 5 patches)
  • docs/performance.md:12 (uncited metric)

Next steps:
  1. Review flagged items (if any)
  2. Run tests: bun test
  3. Verify changes: git diff
  4. Commit: /commit
```

## Safety Rules

**Always follow these:**

1. **Dry run first**: Never modify anything until user selects items
2. **Never delete:**
   - README.md, CONTRIBUTING.md, CHANGELOG.md
   - Anything in docs/** directory
   - Test files (only flag them)
3. **When unsure**: Flag for review, don't auto-fix
4. **Confirm before:**
   - Deleting >5 files
   - Removing >50 lines total
   - User says "all" with >10 items
5. **Preserve formatting**: Keep indentation when removing comments
6. **Show context**: Always show ±3 lines for code issues

## Detection Details

### Redundant Comment Detection

A comment is redundant if:
1. It's a single-line comment immediately before code
2. It restates what the code obviously does
3. It adds no "why", no context, no reasoning

**Use Read tool** to scan files line by line, looking for:
```
{comment line}
{code line}
```

Compare comment text to code - if essentially the same meaning, flag it.

### Excessive Docstring Detection

Calculate ratio: `docstring_lines / function_code_lines`

Flag if:
- Ratio > 2.0
- Function is simple (getter, setter, obvious logic)
- Docstring restates obvious behavior

### AI TODO Detection

Use Grep tool with pattern:
```bash
grep -n "TODO:.*\(Add\|Consider\|Might\|Should\|Could\|May\|Probably\)" {files}
```

Only flag generic TODOs, keep specific ones with tickets/dates/details.

## Example Invocation

**User:** "de-slop before committing"

**Workflow:**
1. Ask: "Compare against main or different branch?"
2. Run git diff to get changed files
3. Scan all changed files for patterns
4. Present numbered findings
5. Wait for user selection
6. Execute cleanup
7. Show summary

## Edge Cases

**No changes found:**
```
✓ No slop detected in changed files!
Code looks clean.
```

**Git errors:**
- If `git remote show origin` fails (no remote), fall back to main/master
- If branch doesn't exist, show error and ask for valid branch
- If `git rm` fails, show error and skip that file

**File read errors:**
- If can't read file (permissions, binary, etc.), skip with warning
- Continue scanning other files

**User enters invalid selection:**
- Show error: "Invalid selection. Enter numbers (1 2 4), range (1-4), 'all', or 'none'"
- Re-prompt

## Good vs. Bad Examples

### Good Comments (Keep)
```python
# Use exponential backoff to avoid rate limiting
retry_with_backoff(api_call)

# HACK: API returns null for empty arrays, normalize to []
data = response.data or []
```

### Bad Comments (Remove)
```python
# Retry the API call
retry_with_backoff(api_call)

# Set data to response data
data = response.data
```

### Good Docstrings (Keep)
```typescript
/**
 * Debounce function calls to prevent excessive API requests.
 * Uses leading edge trigger for immediate first call.
 */
function debounce(fn: Function, ms: number) { ... }
```

### Bad Docstrings (Simplify)
```typescript
/**
 * Get the user's name.
 *
 * This function returns the name property from the user object.
 * It accesses the name field and returns its value to the caller.
 *
 * @returns The user's name as a string
 */
function getName(): string {
  return this.name;
}
```
→ Simplify to: `/** Return the user's name. */`

## Implementation Tips

1. **Use Grep for patterns**: Fast searching across files
2. **Use Read for context**: Get surrounding lines for code issues
3. **Use Edit for cleanup**: Precise removals preserving formatting
4. **Batch by file**: Group multiple issues in same file
5. **Track line numbers**: May shift after edits, re-scan if needed
6. **Test detection first**: Verify patterns work before showing user

## Final Notes

This skill is conservative by design:
- **When unsure, flag instead of delete**
- **Show before/after for all changes**
- **Never touch test files automatically** (only flag)
- **Always suggest running tests after cleanup**

The goal is to remove obvious AI artifacts while preserving intentional code, docs, and tests.
