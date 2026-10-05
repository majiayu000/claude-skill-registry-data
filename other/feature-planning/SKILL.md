---
name: feature-planning
description: Plan before implementing - understand scope and approach with detailed guidance
languages: [all]
subagents: [all]
tools_needed: [read, glob]
---

## Instructions

### Step 1: Restate the Goal

**Purpose:** Ensure alignment before writing code.

**How:**
- Summarize the feature in 1-2 sentences
- State the problem it solves
- Clarify expected behavior

**Example:**
> "We're adding a password reset feature because users can't recover locked accounts.
> When a user clicks 'Forgot Password', they should receive an email with a time-limited
> reset link."

---

### Step 2: Read Relevant Source Files

**Purpose:** Understand existing patterns before proposing changes.

**How:**
- Use `read` tool to examine related files
- Identify patterns (naming, error handling, tests)
- Note dependencies and integrations

**Common Mistake:** ❌ Assuming file structure without reading
**Correct Approach:** ✅ Read first, then propose

---

### Step 3: Identify All Files to Change

**Purpose:** Scope the work and catch integration points.

**How:**
- List all files that need modification
- Include tests, docs, config
- Note new files to create

**Example:**
```
Files to modify:
- src/auth/password_service.py (add reset logic)
- src/api/auth_routes.py (add /reset endpoint)
- tests/test_password_reset.py (new file)
- docs/API.md (document endpoint)
```

---

### Step 4: Propose Implementation Approach

**Purpose:** Get feedback on design before coding.

**Include:**
- High-level approach
- Alternative options considered
- Tradeoffs and risks
- Why you chose this approach

**Template:**
```
Approach: [Your chosen approach]

Alternatives considered:
1. [Alternative 1] - Pros: X, Cons: Y
2. [Alternative 2] - Pros: X, Cons: Y

Chosen because: [Reasoning]

Risks: [What could go wrong]
```

---

### Step 5: Flag Assumptions

**Purpose:** Surface uncertainties early.

**Examples of assumptions to flag:**
- "Assuming we use JWT tokens (not sessions)"
- "Assuming email service is already configured"
- "Assuming password reset links expire after 1 hour"

---

### Step 6: Wait for Confirmation

**Purpose:** Don't waste effort on wrong approach.

**What to do:**
- Present your plan
- Ask: "Does this approach sound right?"
- Wait for explicit approval
- Don't start coding until confirmed

**Why this matters:** Prevents rework when assumptions are wrong.

---

## Common Mistakes

**❌ Starting to code immediately**
- Leads to rework when approach is wrong
- Misses integration points
- Creates tech debt

**✅ Plan first, then implement**
- Catches issues early
- Gets alignment on approach
- Results in cleaner code

**❌ Proposing solution without reading code**
- Misses existing patterns
- Violates conventions
- Creates inconsistent codebase

**✅ Read similar code first**
- Matches existing patterns
- Maintains consistency
- Learns from established approaches
