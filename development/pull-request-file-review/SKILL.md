---
name: Pull Request File Review
description: Identify and flag unnecessary test artifacts and temporary files in pull requests. Use when reviewing pull requests to ensure only production-relevant files are committed.
---

# Pull Request File Review

## Overview

Review pull request files to identify unnecessary test artifacts, temporary files, and non-production code based on naming patterns, locations, and usage.

## When to Use

- Reviewing pull requests before approval
- Files with test-related names (testresults.md, test_output.csv)
- Temporary scripts or data files in the changeset
- Before merging to ensure only production-relevant files are included

## Process

### 1. Identify Suspicious Files

Look for files matching these patterns:
- `test*.md`, `*results.md`, `*output.md` - Test result documentation
- `test_*.csv`, `*_test_data.csv` - Test data files
- `scratch.py`, `temp.py`, `debug.py` - Temporary scripts
- `output.txt`, `results.json`, `debug.log` - Output/log files
- Files in root directory that don't match project conventions

### 2. Evaluate File Necessity

For each suspicious file, ask:

**Location Analysis:**
- Is it in a test directory? (If yes, likely legitimate)
- Is it in a documentation directory with other docs? (If yes, likely legitimate)
- Is it in the project root or random location? (Red flag)

**Usage Analysis:**
- Is the file imported/referenced in production code?
- Is it required by tests that are committed?
- Is it part of CI/CD configuration?
- Does it have a clear purpose in the project structure?

**Naming Convention:**
- Does the name match the project's file naming conventions?
- Is it clearly temporary? (scratch, temp, test, output, debug)

### 3. Flag or Approve

**Flag for removal if:**
- File appears to be a one-off test artifact
- Name suggests temporary/debug purpose
- Not referenced anywhere in the codebase
- Located in an unusual place for its type

**Approve if:**
- File is referenced in production code
- Part of the test suite infrastructure
- Documented purpose in project structure
- Follows project conventions

### 4. Provide Feedback

When flagging files:
```
🚫 Unnecessary: `path/to/file.ext`
Reason: [Test artifact/temporary script/etc.]
Evidence: [Not referenced/unusual location/temporary naming]
Recommendation: Remove from PR or relocate
```

## Examples

### Example 1: Test Results File

**Context**: PR includes `testresults.md` in project root

**Application**:
1. Location: Root directory (suspicious)
2. Naming: "testresults" indicates test artifact
3. Search: `grep -r "testresults.md"` finds no references
4. Decision: Flag for removal

**Outcome**:
```
🚫 Unnecessary: `testresults.md`
Reason: Test artifact in root directory
Recommendation: Remove from PR
```

### Example 2: Test Data Referenced in Tests

**Context**: PR includes `tests/fixtures/sample_data.csv`

**Application**:
1. Location: `tests/fixtures/` (appropriate)
2. Naming: Follows fixture convention
3. Search: Referenced in `tests/test_parser.py`
4. Decision: Approve

**Outcome**: ✅ Necessary test fixture

### Example 3: Temporary Debug Script

**Context**: PR includes `debug_api.py` in root

**Application**:
1. Location: Root directory (suspicious)
2. Naming: "debug" indicates temporary purpose
3. Search: No imports found
4. Decision: Flag for removal

**Outcome**:
```
🚫 Unnecessary: `debug_api.py`
Reason: Temporary debug script in root
Recommendation: Remove from PR or add to .gitignore if needed locally
```

### Example 4: Configuration File

**Context**: PR includes `test_config.yaml`

**Application**:
1. Location: Root directory
2. Naming: Contains "test" but may be configuration
3. Search: Referenced in `tests/conftest.py`
4. Documentation: Mentioned in testing README
5. Decision: Approve

**Outcome**: ✅ Legitimate test configuration

## Anti-patterns

- ❌ **Don't**: Flag every file with "test" in the name
  - ✅ **Do**: Analyze context, location, and usage

- ❌ **Don't**: Approve files just because they're small
  - ✅ **Do**: Apply consistent criteria regardless of file size

- ❌ **Don't**: Require deep code analysis for obvious artifacts
  - ✅ **Do**: Use file name and location as primary signals

- ❌ **Don't**: Flag files without checking references first
  - ✅ **Do**: Search the codebase for imports/references before flagging

## Testing This Skill

To validate this skill:

1. **Create test PR with mixed files:**
   - `testresults.md` in root (should flag)
   - `tests/fixtures/data.csv` referenced in tests (should pass)
   - `scratch.py` in root (should flag)
   - Legitimate config with test-like name (should pass after analysis)

2. **Apply skill systematically:**
   - Follow the 4-step process for each file
   - Document reasoning for each decision

3. **Verify accuracy:**
   - All flagged files should be unnecessary
   - No legitimate files should be flagged
   - Feedback should be clear and actionable

## Quick Reference Commands

```bash
# List all files in PR
git diff --name-only main...HEAD

# Check if file is referenced in codebase
grep -r "filename.ext" --exclude-dir=.git

# Search for imports (Python example)
grep -r "from.*filename import\|import.*filename" .

# Find test-like files
find . -name "*test*" -o -name "*debug*" -o -name "*temp*" -o -name "*scratch*"
```

---

**Remember**: Catch obvious artifacts without creating friction. When uncertain, ask the author.
