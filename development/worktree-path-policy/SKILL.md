---
name: worktree-path-policy
description: Ensures all file operations occur in the correct worktree directory to prevent accidental changes to the wrong codebase. Use when implementing, reviewing, testing, or documenting code in worktree-based development workflows.
---

# Worktree Path Policy

## Instructions

### Verify working directory before ANY file operation

**If worktree path provided:**
1. Navigate: `cd {{worktree_path}}`
2. Verify: `pwd` and `git branch`
3. Confirm in output: "Working directory: {{path}}, Branch: {{name}}"
4. Work exclusively in that directory

**If NO path provided:**
1. STOP immediately
2. Ask conductor for confirmation
3. Wait for explicit answer
4. Do NOT assume or proceed

### Why this matters

Multiple features develop in parallel using separate worktrees. Wrong directory = contaminate another feature's code or main project.

**Parallel development scenario:**
```
Main Project: /project/
├─ Worktree A: /project/.worktree/feature-auth/
├─ Worktree B: /project/.worktree/feature-api/
└─ Worktree C: /project/.worktree/fix-bug/
```

Without path verification:
- Agent A edits main project → breaks production
- Agent B edits Worktree C → corrupts another feature

With path verification:
- ✅ Each agent isolated to their worktree
- ✅ Safe parallel development

## Example

```bash
# Conductor: "Implement Phase 1 in .worktree/feature-auth/"

# 1. Navigate and verify
cd .worktree/feature-auth/
pwd  # Output: /project/.worktree/feature-auth
git branch  # Output: * feature/auth

# 2. Confirm
Working directory: .worktree/feature-auth/
Current branch: feature/auth
✅ Path verification complete

# 3. Now safe to work
Read("{{src_directory}}/{{service_file}}")
Edit("{{src_directory}}/{{service_file}}", ...)
```

## Checklist

```markdown
Before EVERY task:
[ ] Worktree path received from conductor?
[ ] If NO: Asked conductor and STOPPED?
[ ] Navigated: cd {{worktree_path}}?
[ ] Verified: pwd + git branch?
[ ] Confirmed in output?

During task:
[ ] ALL operations within worktree?
[ ] NO cross-worktree access?
[ ] NO main project access?
```

## Detailed Scenarios

### Scenario 1: Starting New Phase

**Conductor assigns:**
```
📍 Working Context
- Worktree Path: .worktree/feature-payment/
- Branch: feature/payment
- Current Phase: Phase 2 - Payment Gateway Integration
- Current Step: Step 3 (Code Implementation)
```

**Agent response:**
```bash
# Step 1: Navigate
cd .worktree/feature-payment/

# Step 2: Verify
pwd
# Output: /Users/{{user}}/{{project}}/.worktree/feature-payment

git branch
# Output: * feature/payment

# Step 3: Confirm
✅ Working directory verified:
   Path: .worktree/feature-payment/
   Branch: feature/payment

# Step 4: Begin work
Starting Phase 2 implementation...
```

---

### Scenario 2: No Worktree Path Provided

**Conductor assigns (MISSING PATH):**
```
Implement payment validation logic
```

**Agent response:**
```
⚠️ STOPPED: Worktree path not provided

Before proceeding, I need:
1. Worktree path (e.g., .worktree/{{feature-name}}/)
2. Branch name (e.g., feature/{{feature-name}})
3. Current Phase and Step

Please provide the working context.
```

**DO NOT:**
- Assume main project directory
- Guess the worktree path
- Proceed without confirmation

---

### Scenario 3: Switching Between Phases

**Phase 1 complete, starting Phase 2:**

**Conductor:**
```
Phase 1 complete. Continue to Phase 2 in same worktree:
- Worktree Path: .worktree/feature-payment/
- Branch: feature/payment
- Current Phase: Phase 2
```

**Agent response:**
```bash
# Re-verify (even if same worktree)
pwd
# Output: /Users/{{user}}/{{project}}/.worktree/feature-payment

git branch
# Output: * feature/payment

✅ Path re-verified for Phase 2

Continuing in same worktree...
```

**Why re-verify?**
- Agent session may have reset
- Directory context may have changed
- Safety first

---

### Scenario 4: Cross-Worktree Reference (READ-ONLY)

**Sometimes need to reference another worktree:**

**Allowed:**
```bash
# Current: .worktree/feature-payment/
# Need to check how authentication works in feature-auth

# Read-only reference
Read("/project/.worktree/feature-auth/{{src}}/auth_service.py")

# But NEVER write to it
# ❌ Edit("/project/.worktree/feature-auth/...")  # FORBIDDEN
```

**Rule:**
- ✅ Read from other worktrees (reference only)
- ❌ Write to other worktrees (contamination)
- ✅ Write only to current worktree

---

## Common Mistakes

### ❌ Mistake 1: Working in Main Project

```bash
# Agent starts working without verification
Edit("{{src}}/payment_service.py", ...)

# But current directory is main project!
pwd
# Output: /Users/{{user}}/{{project}}/  # ❌ WRONG!
```

**Impact:** Main project contaminated, production broken

**Prevention:**
```bash
# Always verify FIRST
cd .worktree/feature-payment/
pwd  # Confirm worktree path
# THEN work
Edit("{{src}}/payment_service.py", ...)
```

---

### ❌ Mistake 2: Cross-Worktree Contamination

```bash
# Agent in .worktree/feature-auth/
cd .worktree/feature-auth/

# But accidentally edits feature-payment
Edit("../.worktree/feature-payment/{{src}}/payment.py", ...)  # ❌ WRONG!
```

**Impact:** feature-payment corrupted by feature-auth agent

**Prevention:**
```bash
# Only work within current worktree
Edit("{{src}}/auth_service.py", ...)  # ✅ Relative to current worktree
# Never use .. to access other worktrees
```

---

### ❌ Mistake 3: Assuming Path Without Verification

```bash
# Conductor says "work in feature-payment"
# Agent assumes path without verification

Edit("{{src}}/payment_service.py", ...)  # ❌ Where am I?
```

**Impact:** Unknown working directory, unpredictable results

**Prevention:**
```bash
# Always verify explicitly
cd .worktree/feature-payment/
pwd && git branch  # Verify both path and branch
# THEN work
```

---

## Verification Script Template

**Agents should use this pattern:**

```bash
# ===== WORKTREE PATH VERIFICATION =====
# Provided: {{worktree_path}}

# Navigate
cd {{worktree_path}}

# Verify path
CURRENT_PATH=$(pwd)
echo "Current path: $CURRENT_PATH"

# Verify branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

# Confirm
echo "✅ Verification complete:"
echo "   Path: {{worktree_path}}"
echo "   Absolute: $CURRENT_PATH"
echo "   Branch: $CURRENT_BRANCH"

# ===== BEGIN WORK =====
```

---

## Integration with 9-Step Workflow

**Step 2.5 (User Approval):**
- git-worktree-manager creates `.worktree/{{feature-name}}/`
- Conductor records worktree path

**Step 3-9 (All work in worktree):**
- Conductor provides path to every agent
- Agent verifies before starting
- Agent works exclusively in that path

**After Step 9 (All phases complete):**
- Merge to main
- 4-step cleanup (plan → services → worktree → branch)

---

## Conductor Responsibility

**Always provide this information to Step 3-9 agents:**

```markdown
📍 Working Context
- Worktree Path: .worktree/{{feature-name}}/
- Branch: feature/{{feature-name}}
- Current Phase: Phase X - {{description}}
- Current Step: Step Y ({{step_name}})
- Work Scope: {{files/directories}}
```

**Never assume agents know the path**
**Never skip path verification**

---

**For detailed guidelines, see [reference.md](reference.md)**
**For more examples, see [examples.md](examples.md)**
