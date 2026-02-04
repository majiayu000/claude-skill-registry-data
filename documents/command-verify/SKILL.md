---
name: command-verify
version: "0.2.0"
description: Intelligent command verification for documentation. Discovers all commands in markdown files, validates them using git diff-based cache invalidation, and ensures documentation accuracy with zero token cost after initial setup. Use when asked to verify commands, check documentation, or validate command references.
author: "Claude Code"
categories: ["documentation", "validation", "automation", "git"]
keywords: ["command", "verification", "documentation", "cache", "git-diff", "validation", "automation"]
allowed-tools: Read,Glob,Grep,Bash
---

# Command Verify

## Overview

This skill provides intelligent command verification for documentation with git-aware caching. It discovers commands in markdown files, validates them, and uses git diff to only revalidate affected commands.

## When to Use

Invoke this skill when the user asks to:
- "Verify all commands" or "verify commands"
- "Check documentation commands" or "validate docs"
- "Find all commands in markdown/docs"
- "What commands were affected by recent changes?"

## How It Works

### 1. Command Discovery

Discovers ALL commands across ALL markdown files in the codebase.

**Supported formats:**
- Code blocks: ```bash, ```shell, ```console, ```sh
- Inline code: `npm run build`
- Multiple command types: npm, python, cargo, docker, git, etc.

**Tracks:**
- Exact command text
- All file locations where command appears
- Line numbers for precise error reporting
- Command type (code-block vs inline)

**File patterns:**
- Include: `**/*.md`
- Exclude: `node_modules/**`, `.git/**`, `dist/**`, `build/**`

### 2. Cache Strategy

Git diff-based intelligent cache invalidation. **Zero LLM tokens after initial run.**

**Core principle:** Only revalidate commands when relevant files change.

**Process:**
1. On first run: Validate all commands, save current git commit
2. On subsequent runs:
   - Get git diff since last validation
   - Analyze which commands are affected
   - Revalidate only affected commands
   - Keep cached results for unchanged commands

**Invalidation rules:**
- `*.md` changed → Revalidate commands in that file
- `package.json` changed → Revalidate ALL npm commands
- `tsconfig.json` changed → Revalidate build/typecheck commands
- `src/**` changed → Revalidate test commands
- `Cargo.toml` changed → Revalidate cargo commands
- `requirements.txt` changed → Revalidate pip commands

**Expected cache hit rate:** 90%+ after first run

### 3. Command Validation

Smart command categorization and validation:

**Categories:**

1. **SAFE** - Auto-validate, no risk
   - `npm run build`, `test`, `lint`, `typecheck`
   - `git status`, `git log`
   - Read-only operations (`ls`, `cat`, `find`)

2. **CONDITIONAL** - Ask before running
   - `npm install` (modifies node_modules)
   - `npm run format` (modifies source)
   - Commands with side effects

3. **DANGEROUS** - Never auto-run
   - `rm -rf`
   - `git push --force`
   - `npm run clean/clear`
   - Database drops
   - Any `--force` or `--delete` flags

**For each command, track:**
- Validation status (success/fail/skipped)
- Execution time
- Error messages
- All locations in documentation

### 4. Cache Structure

**Location:** `.cache/command-validations`

**Files:**
- `last-validation-commit.txt` - Git commit hash of last validation
- `commands/*.json` - One file per unique command (hashed filename)

**Cache entry format:**
```json
{
  "command": "npm run build",
  "locations": [
    {"file": "README.md", "line": 45, "type": "code-block"},
    {"file": "docs/guide.md", "line": 23, "type": "inline"}
  ],
  "validation": {
    "validated": true,
    "category": "safe",
    "success": true,
    "duration": 2341,
    "message": "Build completed successfully"
  },
  "cachedAt": "2025-10-29T10:00:00Z",
  "commit": "a1b2c3d4e5f6"
}
```

## Self-Learning Memory System

This skill uses an auto-updating knowledge base at `.claude/knowledge.json` that learns from corrections and user feedback.

### When to Update Knowledge Base

**Implicit memory requests** - Auto-detect when user is correcting or teaching:
- "X is wrong, it should be Y"
- "The CLI is called X not Y"
- "That command doesn't exist, use Z instead"
- "Always check X before running Y"

**Update triggers:**
1. User provides a correction about command names
2. Validation discovers a new command pattern
3. User teaches a project-specific rule
4. Repeated validation errors suggest a pattern

### How to Update

When user provides a correction:

1. **Read** `.claude/knowledge.json`
2. **Update** the relevant section:
   - `corrections.cliNames` - For CLI name fixes
   - `patterns.commandPrefixes` - For new command types
   - `validationRules` - For safety categorization
   - `filePatterns.rules` - For invalidation rules
3. **Append** to `learningLog.entries` with timestamp and context
4. **Write** updated knowledge back to file
5. **Apply** the correction to affected files (README, docs, etc.)

### Knowledge Base Structure

```json
{
  "corrections": {
    "cliNames": {"wrong-name": {"correct": "right-name", "reason": "..."}}
  },
  "patterns": {
    "commandPrefixes": ["npm", "git", "claude"]
  },
  "validationRules": {
    "safe": [...], "conditional": [...], "dangerous": [...]
  },
  "learningLog": {
    "entries": [{"date": "...", "type": "correction", "from": "...", "to": "..."}]
  }
}
```

## Instructions for Claude

When this skill is invoked:

0. **Memory Check Phase** (ALWAYS RUN FIRST)
   - Read `.claude/knowledge.json` to load learned corrections
   - Apply any CLI name corrections from `corrections.cliNames`
   - Use custom patterns from `patterns.commandPrefixes`
   - If user provides correction (e.g., "X is wrong, use Y"):
     - Update knowledge.json immediately
     - Apply correction to all affected files
     - Log the learning in learningLog

1. **Discovery Phase**
   - Use the Glob tool to find all `**/*.md` files (excluding node_modules, .git, dist, build)
   - Use the Read tool to read each markdown file
   - Extract all commands from code blocks and inline code
   - Track command text, file locations, and line numbers
   - Check commands against learned corrections in knowledge.json

2. **Cache Analysis Phase**
   - Check if `.cache/command-validations/last-validation-commit.txt` exists
   - If it exists:
     - Read the cached commit hash
     - Run `git diff <cached-commit>..HEAD --name-only` to get changed files
     - Apply invalidation rules to determine which commands need revalidation
   - If it doesn't exist: treat as first run (validate all)

3. **Validation Phase**
   - For each command not in cache or invalidated:
     - Categorize as SAFE, CONDITIONAL, or DANGEROUS
     - If SAFE: Execute and capture result
     - If CONDITIONAL: Ask user for permission, then execute
     - If DANGEROUS: Skip execution, mark as skipped
   - For cached commands: Use cached results

4. **Reporting Phase**
   - Show summary:
     - Total commands discovered
     - Cache hit rate (% reused from cache)
     - Commands validated this run
     - Commands skipped (dangerous)
     - Commands failed (need fixing)
     - Token usage (always 0)
     - Time saved vs full validation
   - Provide detailed breakdown if any commands failed

5. **Cache Update Phase**
   - Save current git commit hash to `last-validation-commit.txt`
   - Save each command's validation result to `commands/<hash>.json`

## Performance Expectations

**First run:**
- Discovery: ~100ms for 10 .md files
- Validation: ~5-10s for 20 commands
- Total: ~10-15 seconds
- Tokens: 0 (deterministic)

**Subsequent runs (no changes):**
- Discovery: ~100ms
- Cache check: ~50ms (git diff)
- Validation: 0ms (all cached)
- Total: ~150ms
- Tokens: 0
- Cache hit rate: 100%

**Subsequent runs (with changes):**
- Discovery: ~100ms
- Cache check: ~50ms
- Validation: ~2s for 3 affected commands
- Total: ~2.5 seconds
- Tokens: 0
- Cache hit rate: 85%

## Error Handling

- **Not a git repo:** Warn and treat as first run (validate all)
- **Command execution fails:** Log failure, continue with other commands
- **Malformed cache:** Ignore corrupted entry, revalidate
- **Missing dependencies:** Provide clear error with installation instructions

## Safety First

- **NEVER** execute dangerous commands automatically
- **ALWAYS** ask before executing conditional commands
- **ALWAYS** provide clear feedback about what will be executed
- Use the AskUserQuestion tool when permission is needed

## Example Usage

**User:** "Verify all commands in the documentation"

**Claude's actions:**
1. Discover all markdown files using Glob
2. Extract commands from each file using Read
3. Check cache using Bash (git diff)
4. Validate affected commands using Bash
5. Report results to user

**Output format:**
```
Command Verification Report
===========================
✓ Total commands discovered: 25
✓ Commands from cache: 22 (88%)
✓ Commands validated: 3
✓ Commands skipped (dangerous): 2
✗ Commands failed: 1

Failed commands:
- `npm run nonexistent` in README.md:45
  Error: Script "nonexistent" not found in package.json

Cache hit rate: 88%
Token usage: 0
Time: 2.3 seconds (saved ~8s vs full validation)
```
