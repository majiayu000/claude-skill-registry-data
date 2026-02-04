---
name: vibe
description: 'Talos-class comprehensive code validation. Use for "validate code", "run vibe", "check quality", "security review", "architecture review", "accessibility audit", "complexity check", or any validation need. One skill to validate them all.'
---

# Vibe Skill

> **Quick Ref:** Validate code across 8 aspects (security, quality, architecture, etc). Output: `.agents/vibe/*.md` + grade A-F.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Comprehensive code validation across 8 quality aspects.

## Execution Steps

Given `/vibe [target]`:

### Step 1: Load Vibe-Coding Science

**Read the vibe-coding reference:**
```
Tool: Read
Parameters:
  file_path: skills/vibe/references/vibe-coding.md
```

This gives you:
- Vibe Levels (L0-L5 trust calibration)
- 5 Core Metrics and thresholds
- 12 Failure Patterns to detect
- Grade mapping

### Step 1a: Pre-flight Checks

**Before proceeding, verify we have work to validate:**

```bash
# Check if in git repo
git rev-parse --git-dir 2>/dev/null || echo "NOT_GIT"
```

If NOT_GIT and no explicit path provided, STOP with error:
> "Not in a git repository. Provide explicit file path: `/vibe path/to/files`"

### Step 2: Determine Target and Vibe Level

**If target provided:** Use it directly.

**Classify the vibe level based on task type:**
| Task Type | Vibe Level | Depth |
|-----------|:----------:|-------|
| Format, lint | L5 | Skip |
| Boilerplate | L4 | Quick |
| CRUD, tests | L3 | Quick |
| Features | L2 | Deep |
| Architecture, security | L1 | Deep |

**If no target:** Auto-detect from git state:
```bash
# Check staged changes
git diff --cached --name-only 2>/dev/null | head -10

# Check unstaged changes
git diff --name-only 2>/dev/null | head -10

# Check recent commits
git log --oneline -5 --since="24 hours ago" 2>/dev/null
```

Use the first non-empty result. If nothing found, ask user.

### Step 2a: Pre-flight Check - Files Exist

**If auto-detected 0 files to review:**
```
STOP and return:
  Grade: PASS
  Reason: "No changes detected to review"
  Action: None required
```

Do NOT proceed with empty file list - this wastes context.

### Step 3: Get Changed Files

```bash
# For "recent" target
git diff --name-only HEAD~3 2>/dev/null | head -20

# For specific path
ls -la <path>
```

### Step 4: Read the Files

Use the Read tool to read each changed file. Understand what the code does.

### Step 5: Validate 8 Aspects

For each file, check:

| Aspect | What to Look For |
|--------|------------------|
| **Semantic** | Does code match docstrings? Misleading names? |
| **Security** | SQL injection, XSS, hardcoded secrets, auth issues |
| **Quality** | Dead code, copy-paste, magic numbers, code smells |
| **Architecture** | Layer violations, circular deps, god classes |
| **Complexity** | Deep nesting, long functions, too many params |
| **Performance** | N+1 queries, unbounded loops, resource leaks |
| **Slop** | AI hallucinations, cargo cult code, over-engineering |
| **Accessibility** | Missing ARIA, keyboard nav issues, contrast |

### Step 6: Dispatch Expert Agents (for deep validation)

For comprehensive validation, dispatch 6 specialized agents **in parallel (single message, 6 Task tool calls)**:

```
Tool: Task (ALL 6 IN PARALLEL)
Parameters:
  subagent_type: "agentops:security-reviewer"
  model: "haiku"
  description: "Security review"
  prompt: "Review these files for security issues: <file-list>"

Tool: Task
Parameters:
  subagent_type: "agentops:code-reviewer"
  model: "haiku"
  description: "Code quality review"
  prompt: "Review these files for quality issues: <file-list>"

Tool: Task
Parameters:
  subagent_type: "agentops:architecture-expert"
  model: "haiku"
  description: "Architecture review"
  prompt: "Review architecture and patterns in: <file-list>"

Tool: Task
Parameters:
  subagent_type: "agentops:code-quality-expert"
  model: "haiku"
  description: "Complexity review"
  prompt: "Check complexity and maintainability of: <file-list>"

Tool: Task
Parameters:
  subagent_type: "agentops:security-expert"
  model: "haiku"
  description: "Security deep dive"
  prompt: "Deep security analysis of: <file-list>"

Tool: Task
Parameters:
  subagent_type: "agentops:ux-expert"
  model: "haiku"
  description: "UX/Accessibility review"
  prompt: "Review UX and accessibility of: <file-list>"
```

**Timeout handling:** Per-agent timeout of 3 minutes (180000ms). If agent times out, continue with remaining results if quorum (80%) met. See `.agents/specs/conflict-resolution-algorithm.md` for synthesis rules.

### Step 6a: Apply Conflict Resolution (for swarm results)

**If multiple agents dispatched:**
1. Check quorum (80% minimum must return)
2. Apply severity escalation (if ANY agent reports CRITICAL → final is CRITICAL)
3. Deduplicate findings by file:line (±5 lines tolerance)
4. Track agreement per finding (e.g., "3/6 agents found this")
5. Compute weighted grade

**If quorum not met:** Report as INCOMPLETE, do not publish grade.

See: `.agents/specs/conflict-resolution-algorithm.md`

### Step 7: Check for Failure Patterns

**Detect the 12 failure patterns from vibe-coding science:**

| Pattern | Detection Method |
|---------|------------------|
| #1 Tests Lie | Compare test output to actual behavior |
| #4 Debug Spiral | Count consecutive fix commits |
| #5 Eldritch Horror | Functions >500 lines |
| #6 Collision | Multiple recent editors on same file |

### Step 8: Categorize Findings

Group findings by severity:

| Severity | Definition | Gate |
|----------|------------|------|
| **CRITICAL** | Security vulnerability, data loss risk | BLOCKS |
| **HIGH** | Significant bug, performance issue | Should fix |
| **MEDIUM** | Code smell, maintainability issue | Worth noting |
| **LOW** | Style, minor improvement | Optional |

### Step 9: Compute Grade

Based on findings:
- **A**: 0 critical, 0-2 high
- **B**: 0 critical, 3-5 high
- **C**: 0 critical, 6+ high OR 1 critical (fixed)
- **D**: 1+ critical unfixed
- **F**: Multiple critical, systemic issues

### Step 10: Write Vibe Report

**Write to:** `.agents/vibe/YYYY-MM-DD-<target>.md`

```markdown
# Vibe Report: <Target>

**Date:** YYYY-MM-DD
**Files Reviewed:** <count>
**Grade:** <A-F>

## Summary
<Overall assessment in 2-3 sentences>

## Gate Decision
[ ] PASS - 0 critical findings
[ ] BLOCK - <count> critical findings must be fixed

## Findings

### CRITICAL
1. **<File:Line>** - <Issue>
   - **Risk:** <what could happen>
   - **Fix:** <how to fix>

### HIGH
1. **<File:Line>** - <Issue>
   - **Fix:** <how to fix>

### MEDIUM
- <File:Line>: <brief issue>

## Aspects Summary
| Aspect | Status |
|--------|--------|
| Semantic | <OK/Issues> |
| Security | <OK/Issues> |
| Quality | <OK/Issues> |
| Architecture | <OK/Issues> |
| Complexity | <OK/Issues> |
| Performance | <OK/Issues> |
| Slop | <OK/Issues> |
| Accessibility | <OK/N/A> |
```

### Step 11: Report to User

Tell the user:
1. Overall grade
2. Gate decision (PASS/BLOCK)
3. Critical and high findings (if any)
4. Location of full report

## Key Rules

- **0 CRITICAL = PASS** - the gate rule
- **Evidence for every finding** - cite file:line
- **Actionable fixes** - tell them HOW to fix, not just what's wrong
- **Grade reflects reality** - don't inflate or deflate
- **Write the report** - always produce `.agents/vibe/` artifact

## Quick vs Deep

- **Quick** (`/vibe`): Read files, check obvious issues
- **Deep** (`/vibe --deep`): Dispatch expert agents for thorough review

## Prescan Script

The vibe skill includes an automated prescan script at `scripts/prescan.sh`:

```bash
# Run prescan for secret detection
./scripts/prescan.sh <target-path>
```

**What it checks:**
- Hardcoded secrets (API keys, passwords, tokens)
- AWS/GCP/Azure credentials
- Private keys
- Connection strings

**Exit codes:**
- `0`: No secrets found
- `1`: Secrets detected (blocks gate)

**Integration:** Run prescan before full vibe validation to catch secrets early.
