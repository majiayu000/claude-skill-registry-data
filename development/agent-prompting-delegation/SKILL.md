---
name: Agent Prompting & Delegation
description: Best practices for writing effective Task tool prompts that produce clear, structured outputs from sub-agents. Covers context engineering, instruction clarity, output format specification, and parallel delegation patterns. MUST BE USED PROACTIVELY when spawning sub-agents to ensure high-quality results.
allowed-tools:
  - Read
---

# Agent Prompting & Delegation Skill

**Purpose:** Write effective prompts that produce clear, structured, actionable outputs from sub-agents.

**When to use:** PROACTIVELY before every Task tool invocation. This skill improves all agent delegation.

---

## Core Prompting Principles (2025 Best Practices)

1. **Clear over clever** - Ambiguity is the enemy. Explicit instructions beat clever wording.
2. **Structure over prose** - Use XML tags, bullets, code blocks. Not paragraphs.
3. **Examples over explanations** - Show what you want (multishot prompting).
4. **Iteration over perfection** - Test prompts, analyze outputs, refine approach.
5. **Context engineering > prompt engineering** - Right context matters more than perfect wording.
6. **QUALITY OVER TOKENS** - Never shortcut work due to token concerns. See below.

**Golden rule:** If a human would be confused by your prompt, an AI definitely will be.

---

## TOKEN BUDGET DIRECTIVE (CRITICAL - INCLUDE IN ALL PROMPTS)

**MANDATORY for all agent prompts during orchestrations:**

```
TOKEN BUDGET DIRECTIVE:
- You have a 200K token budget - this is a CEILING, not a target
- NEVER shortcut work because you see token warnings
- NEVER skip validation, reviews, or fixes to "save tokens"
- NEVER use placeholders, TODOs, or "implement later" due to token concerns
- Better to hit 200K limit doing excellent work than finish early with half-assed work
- If you run out of tokens mid-task: THAT'S FINE - you'll be resumed
- Quality first, token count never
```

**Why this matters:**
Claude Code shows token usage notifications ("30K tokens remaining"). Agents see these and panic, thinking they need to rush and cut corners. THIS IS WRONG. The human prefers you run out of tokens doing thorough work than conserve tokens by skipping steps.

---

## Essential Prompt Components

Every effective Task prompt should include:

### 1. Clear Objective (REQUIRED)

**What success looks like in one sentence.**

```
GOOD: "Find the JWT token verification logic and return file:line where it happens."

BAD: "Investigate authentication."
```

### 2. Success Criteria (REQUIRED)

**How to know when done - specific, measurable outcomes.**

```
GOOD:
Success criteria:
- File path + line number of verification logic
- Library/function name used
- Code snippet (5-10 lines) showing verification

BAD:
Success criteria:
- Understand how auth works
```

### 3. Context (OPTIONAL - use judiciously)

**What you already know - only what's needed, not everything.**

```
GOOD:
Context: I know auth middleware exists in src/middleware/. Just need to find where token validation logic lives.

BAD:
Context: [dumps entire project README, architecture docs, and 50 files]
```

**Context pollution:** Too much context = agent gets lost. Provide only what's directly relevant.

### 4. Expected Output Format (CRITICAL)

**Structure, not just content. Tell the agent exactly how to format results.**

```
GOOD:
Expected output:
### Verification Logic
**Location:** path/to/file.py:45-52
**Library:** PyJWT
**Code:**
```python
[snippet]
```
**Dependencies:** Redis for token blacklist

BAD:
Expected output: Tell me what you find.
```

### 5. Error Handling (RECOMMENDED)

**What to do with missing data or failures.**

```
GOOD:
If verification logic not found:
1. Check for external auth service (Auth0, Cognito)
2. Look for JWT in dependencies (package.json, requirements.txt)
3. Report "No internal JWT verification found, likely external service"

BAD:
[No error handling guidance - agent makes assumptions]
```

### 6. Files Hint (OPTIONAL - when you know)

**Where to start looking - saves agent time.**

```
GOOD:
Start looking in:
- src/middleware/auth.js
- src/lib/jwt.js
- src/services/authentication/

BAD:
[No hints - agent searches entire codebase]
```

---

## Structured Output Patterns (Brief)

### Common Patterns

**XML tags** for unambiguous section delimiters:
```xml
<verification-logic>
Location: path/to/file.py:line
</verification-logic>
```

**Markdown structure** for hierarchy:
```markdown
## Files Modified
- path/to/file.py - [description]

## Implementation Summary
[2-3 sentences]
```

**Prefilling** to guide format from first line:
```
Begin your response with:
### Analysis Results
**Status:** [FOUND/NOT_FOUND]
```

**Chain-of-thought** for complex tasks:
```
Think through step-by-step:
1. First, identify all auth endpoints
2. Then, trace to verification logic
3. Finally, determine library used
```

**For detailed examples:** See reference.md

---

## Multi-Agent Delegation

### Parallel vs Sequential Execution

**Use PARALLEL when:**
- Tasks are independent
- No shared state
- Can run simultaneously
- Want 5-10x speedup

**Example - Parallel (GOOD):**
```python
# Single message, multiple Task calls
Task(query="Find JWT verification in auth module", role="investigator")
Task(query="Find JWT verification in API routes", role="investigator")
Task(query="Find JWT verification in middleware", role="investigator")
Task(query="Check dependencies for JWT libraries", role="investigator")
```

**Use SEQUENTIAL when:**
- Task B depends on Task A output
- Shared state (file modifications)
- Order matters

**Example - Sequential (GOOD):**
```python
# Message 1: Discovery
Task(query="Find all auth endpoints", role="investigator")

# Wait for response, then Message 2: Implementation
Task(query="Implement rate limiting on endpoints: [list from Task 1]", role="implementation-executor")
```

### Clear Task Boundaries

**Prevent overlap/gaps:**
```
GOOD:
- Agent A: User authentication (login, logout, sessions)
- Agent B: Authorization (permissions, roles, access control)
- Agent C: Token management (JWT creation, validation, refresh)

BAD:
- Agent A: Work on auth
- Agent B: Work on security
- Agent C: Work on users
```

**Why bad:** Overlapping responsibilities cause duplication and conflicts.

### Context Handoff Between Agents

**Explicit handoff:**
```
Agent 1 output:
JWT verification found at src/middleware/auth.js:45-67 using jsonwebtoken v9.0.0.

Agent 2 prompt:
Context: JWT verification at src/middleware/auth.js:45-67 using jsonwebtoken v9.0.0.
Your task: Add rate limiting, preserve existing token blacklist logic.
```

---

## Common Delegation Pitfalls

| Pitfall | Example (BAD) | Fix (GOOD) |
|---------|---------------|------------|
| **Vague objective** | "Investigate auth" | "Find JWT verification logic with file:line" |
| **Under-specification** | "Add tests" | "Add unit tests covering: happy path, invalid token, expired token. Use pytest. Target 95% coverage." |
| **Context overload** | [Dumps 50 files] | "Context: Auth uses JWT. Middleware in src/middleware/. Find verification logic." |
| **Resource conflicts** | 2 agents modifying same file simultaneously | "Agent A: auth.py lines 1-50. Agent B: auth.py lines 51-100" OR sequential |
| **Missing output format** | "Tell me what you find" | "Expected output: File path, line numbers, code snippet, library name" |
| **Too simple tasks** | Task("Read src/auth.py") | Use Read tool directly |
| **No error handling** | "Find config file" | "Find config file. If not found, check environment variables or report missing." |
| **Ambiguous success** | "Make auth better" | "Success: Auth has rate limiting (5 req/min), tested, no security audit failures" |

---

## When to Use Agents vs Direct Tools

### Decision Framework

| Can you specify exact path/pattern? | Tool to Use |
|-------------------------------------|-------------|
| **YES** - Know exact file to read | Read tool directly |
| **YES** - Know exact grep pattern | Grep tool directly |
| **YES** - Know exact bash command | Bash tool directly |
| **NO** - Need to explore/discover | Use Task (agent) |
| **NO** - Need to analyze/synthesize | Use Task (agent) |
| **NO** - Need to validate/review | Use Task (agent) |

### Examples: Tools vs Agents

**USE TOOLS DIRECTLY:**
```
# Specific file read
Read(file_path="src/auth.py")

# Known grep pattern
Grep(pattern="def verify_jwt", path="src/", output_mode="content")

# Simple bash command
Bash(command="pytest tests/unit/test_auth.py -v")
```

**USE AGENTS:**
```
# Exploration (don't know exact file)
Task(query="Find where JWT verification happens in codebase", role="investigator")

# Complex analysis
Task(query="Analyze auth flow and identify security vulnerabilities", role="security-auditor")

# Multiple operations
Task(query="Find JWT logic, analyze it, and suggest improvements", role="investigator")
```

### Threshold: >3 Files = Use Agent

**Rule of thumb:**
- 1-3 known files → Read tools in parallel
- >3 files OR unknown files → Use agent

---

## Practical Checklist: Before Every Task Call

**Before spawning any agent, verify:**

- [ ] Clear objective (one sentence: what success looks like)
- [ ] Success criteria (measurable outcomes: file paths, test pass, etc.)
- [ ] Expected output format (structure specified: sections, fields, format)
- [ ] Context provided (only what's needed, not everything)
- [ ] Error handling (what to do if not found / fails)
- [ ] Role appropriate (investigator for discovery, implementer for code, etc.)
- [ ] Parallel tasks grouped (independent tasks in single message)
- [ ] Sequential dependencies clear (Task B depends on Task A output)
- [ ] Task boundaries non-overlapping (no resource conflicts)

**Optional but recommended:**
- [ ] Files hint (where to start looking)
- [ ] Tool usage guidance (which tools, how many calls)
- [ ] Step-by-step process (prevent excessive exploration)

---

## Quick Reference: Prompt Template

```
[Clear objective in one sentence]

Success criteria:
- [Measurable outcome 1]
- [Measurable outcome 2]
- [Measurable outcome 3]

Context: [Only what's directly relevant]

Expected output format:
[Specific structure with sections, fields, format]

If [error condition]:
- [How to handle]

Start looking in: [Files hint if you know]
```

---

## Critical Inline Standards by Agent Type

**BELT + SUSPENDERS APPROACH:**

1. **Belt:** All agents have instructions to read CLAUDE.md first (in their agent definitions)
2. **Suspenders:** Include critical standards inline in Task prompts (below) to guarantee they're seen

**IMPORTANT:** When spawning sub-agents, include these critical inline standards in your prompts. Even though agents are instructed to read CLAUDE.md, inline standards provide redundancy and highlight the most critical rules.

### Implementation Agents (implementation-executor, general-builder, skeleton-builder)

```
TOKEN BUDGET DIRECTIVE:
- NEVER shortcut work due to token warnings
- NEVER skip implementation to "save tokens"
- NEVER use placeholders/TODOs due to token concerns
- Better to run out of tokens mid-excellence than finish with half-assed work

CRITICAL STANDARDS (inline in prompt):
- Logging: import logging; LOG = logging.getLogger(__name__)
- try/except ONLY for connection errors (network, database, cache, external APIs)
  - Network: requests.Timeout, requests.ConnectionError, requests.HTTPError
  - Database: pymongo errors, sqlalchemy errors, redis errors
  - NEVER wrap: dict.get(), file I/O, JSON parsing, type conversions
- Type hints required for all new code
- 80 char line limit (ruff enforced)
- snake_case functions/vars, PascalCase classes, UPPER_CASE constants
- No # noqa / # type: ignore without documented reason
- No single-line wrapper functions that add no value
- No commented code (delete it)
- DO NOT run tests unless explicitly instructed

OUTPUT REQUIREMENTS:

IF during orchestration (/conduct or /solo):
  If you discover gotchas or deviations from spec:
  1. Append to $WORK_DIR/.spec/DISCOVERIES.md with discovery
  2. Return brief summary (3-5 sentences): what implemented + gotchas found

OTHERWISE (ad-hoc work):
  Return normal detailed output

OPTIONAL SKILL LOAD:
- python-style (detailed patterns if needed)
```

### Test Agents (test-implementer, test-skeleton-builder)

```
TOKEN BUDGET DIRECTIVE:
- NEVER shortcut tests due to token warnings
- NEVER skip test cases to "save tokens"
- NEVER use incomplete mocks or assertions due to token concerns
- Better to run out of tokens mid-excellence than finish with half-assed tests

CRITICAL STANDARDS (inline in prompt):
- 1:1 file mapping: tests/unit/test_<module>.py for src/<module>.py
- 95% coverage minimum for unit tests
- AAA pattern (Arrange-Act-Assert)
- Mock EVERYTHING external to the function being tested:
  - Mock: database calls, API calls, file I/O, cache operations
  - Mock: OTHER INTERNAL FUNCTIONS called by the function under test
  - Test function in ISOLATION, not with its dependencies
  - Unit tests = pure isolation, integration tests = real dependencies
- Descriptive names: test_<function>_<scenario> or test_<function> (if single)
- Use parametrized tests: @pytest.mark.parametrize for multiple cases
- Integration tests: 2-4 files per module (ADD to existing, don't create new)
- DO NOT run tests unless explicitly instructed
- NO shortcuts or workarounds in test implementation

SKILL TO LOAD:
- testing-standards (fixture patterns, E2E structure)
```

### Spike Tester

```
CRITICAL STANDARDS (inline in prompt):
- All work in /tmp/spike_<name>/
- Write LEGITIMATE tests - NO half-assed tests, NO workarounds allowed
- If you can't test something properly, EXPLAIN WHY in detail
- Tests must use proper mocking, proper assertions, proper structure
- Same quality standards as production tests (just throwaway location)
- Document findings clearly with evidence from test results

SKILL TO LOAD:
- testing-standards (test structure, mocking patterns)
```

### Review Agents (security-auditor, performance-optimizer, code-reviewer, code-beautifier)

**IMPORTANT:** Review agents have Write tool access to save findings to files.

```
TOKEN BUDGET DIRECTIVE:
- NEVER shortcut reviews due to token warnings
- NEVER skip checking files to "save tokens"
- NEVER reduce thoroughness due to token concerns
- Better to run out of tokens mid-review than deliver incomplete findings

CRITICAL STANDARDS (inline in prompt):
- Check for improper try/except usage (wrapping safe operations)
- Check logging (should use logging.getLogger(__name__))
- Check type hints (required for new code)
- Check 80 char line limit, no # noqa without reason

OUTPUT REQUIREMENTS:

IF during orchestration (/conduct or /solo):
  1. Write detailed findings to: $WORK_DIR/.spec/review_findings/[phase]/[context]_[role]_[N].md
  2. Return ONLY 2-3 sentence summary

OTHERWISE (ad-hoc reviews):
  1. Write detailed findings to: /tmp/review_findings/[timestamp]_[context]_[role].md
  2. Return ONLY 2-3 sentence summary

Summary format:
- Critical issue count (if any)
- Important issue count (if any)
- Overall status (CLEAN / ISSUES_FOUND)

DO NOT return full JSON in response - it's in the file.

File format (JSON):
{
  "status": "COMPLETE",
  "critical": [{"file": "path/to/file.py", "line": 123, "issue": "...", "fix": "..."}],
  "important": [...],
  "minor": [...]
}

OPTIONAL SKILL LOADS:
- python-style (code-reviewer)
- vulnerability-triage (security-auditor)
- mongodb-aggregation-optimization (performance-optimizer if MongoDB)
```

### Fix Agents (fix-executor)

```
TOKEN BUDGET DIRECTIVE:
- NEVER shortcut fixes due to token warnings
- NEVER skip fixing issues to "save tokens"
- NEVER use workarounds instead of proper fixes due to token concerns
- Better to run out of tokens mid-fix than deliver partial fixes

CRITICAL STANDARDS (inline in prompt):
- Fix issues PROPERLY - no workarounds, no shortcuts, no half-measures
- Follow all code quality standards:
  - Logging: logging.getLogger(__name__)
  - try/except ONLY for connection errors
  - Type hints required, 80 char limit
- DO NOT use # noqa / # type: ignore as a "fix"
- DO NOT wrap safe operations in try/except to silence warnings
- If fix requires architectural changes, ESCALATE with:
  - What the issue is
  - Why proper fix needs architectural decision
  - Options available
  - Your recommendation
- Max 3 attempts, then ESCALATE with clear explanation

OUTPUT REQUIREMENTS:

IF during orchestration (/conduct or /solo):
  1. Return brief summary (3-5 sentences):
     - How many issues fixed
     - What files modified
     - Any remaining concerns
  DO NOT return full list of changes - reviewers will validate

OTHERWISE (ad-hoc fixes):
  Return detailed list of changes made

IMPORTANT: After fix-executor completes, 2 reviewers MUST review again to validate fixes.

OPTIONAL SKILL LOADS:
- python-style (if fixing naming/logging)
- code-refactoring (if fixing complexity)
```

### Documentation Agents (documentation-writer)

```
CRITICAL STANDARDS (inline in prompt):
MUST LOAD SKILL BEFORE STARTING:
- ai-documentation (hierarchical inheritance, line count targets, structure patterns)

Standards from skill:
- Concise over comprehensive (map not tutorial)
- Structure over prose (tables, bullets >>> paragraphs)
- Location references with file:line_number
- 100-200 line target for most docs (300-400 max for complex)
- Hierarchical inheritance (never duplicate parent content)
```

### Analysis Agents (general-investigator, Explore)

```
CRITICAL STANDARDS (inline in prompt):
- Start narrow, expand if needed (progressive disclosure)
- Use Grep (cheap) before Read (focused)
- Don't read >5 files without reporting findings first
- Include file:line references in all findings

No mandatory skill loads (read-only exploration)
```

---

## Prompt Template with Inline Standards

**Example implementation-executor prompt:**

```
Task(implementation-executor, """
Implement rate limiting for authentication endpoints.

Spec: $WORK_DIR/.spec/BUILD_rate_limit.md
Workflow: solo

TOKEN BUDGET DIRECTIVE:
- NEVER shortcut work due to token warnings
- NEVER skip implementation to "save tokens"
- NEVER use placeholders/TODOs due to token concerns
- Better to run out of tokens mid-excellence than finish with half-assed work

CRITICAL STANDARDS:
- Logging: import logging; LOG = logging.getLogger(__name__)
- try/except ONLY for connection errors (network, DB, cache)
- Type hints required, 80 char limit
- No # noqa without documented reason
- DO NOT run tests

OUTPUT:
- If gotchas found: Append to $WORK_DIR/.spec/DISCOVERIES.md
- Return brief summary (3-5 sentences): what implemented + gotchas

Load python-style skill if needed.

Context:
- Auth endpoints in src/auth/endpoints.py
- Existing Redis connection in src/db/redis.py
- Rate limit: 5 requests/minute per IP

Agent will read spec automatically.
""")
```

**Example test-implementer prompt:**

```
Task(test-implementer, """
Implement comprehensive tests for rate limiting.

Spec: $WORK_DIR/.spec/BUILD_rate_limit.md
Workflow: solo

CRITICAL STANDARDS:
- 1:1 file mapping: tests/unit/test_rate_limiter.py
- 95% coverage minimum
- Mock EVERYTHING external to function being tested:
  - Redis calls, time.time(), other internal functions
- DO NOT run tests
- NO shortcuts or workarounds

Load testing-standards skill.

Production code: src/auth/rate_limiter.py

Agent will read spec automatically.
""")
```

**Example fix-executor prompt:**

```
Task(fix-executor, """
Fix all validation issues.

Spec: $WORK_DIR/.spec/BUILD_rate_limit.md
Workflow: solo

Issues from: $WORK_DIR/.spec/review_findings/task_2/rate_limit_code-reviewer_*.md

TOKEN BUDGET DIRECTIVE:
- NEVER shortcut fixes due to token warnings
- NEVER skip fixing issues to "save tokens"
- NEVER use workarounds instead of proper fixes due to token concerns
- Better to run out of tokens mid-fix than deliver partial fixes

CRITICAL RULES:
- Fix PROPERLY - no workarounds
- DO NOT use # noqa as a "fix"
- DO NOT wrap safe operations in try/except
- If architectural issue, ESCALATE with options

OUTPUT:
- Return brief summary (3-5 sentences): issues fixed, files modified
- 2 reviewers will validate after you complete

Load python-style skill if needed.

Agent will read spec and review findings automatically.
""")
```

**Example code-reviewer prompt:**

```
Task(code-reviewer, """
Review rate limiting implementation.

Spec: $WORK_DIR/.spec/BUILD_rate_limit.md
Workflow: solo
Phase: task_2

Focus: Code quality, logic correctness, standards compliance

TOKEN BUDGET DIRECTIVE:
- NEVER shortcut reviews due to token warnings
- NEVER skip checking files to "save tokens"
- NEVER reduce thoroughness due to token concerns
- Better to run out of tokens mid-review than deliver incomplete findings

CRITICAL STANDARDS:
- Check for improper try/except usage (wrapping safe operations)
- Check logging (should use logging.getLogger(__name__))
- Check type hints (required for new code)
- Check 80 char line limit, no # noqa without reason

OUTPUT:
1. Write findings to: $WORK_DIR/.spec/review_findings/task_2/rate_limit_code-reviewer_1.md
   Format (JSON):
   {
     "status": "COMPLETE",
     "critical": [{"file": "...", "line": 123, "issue": "...", "fix": "..."}],
     "important": [...],
     "minor": [...]
   }

2. Return summary (2-3 sentences):
   - Critical: X, Important: Y, Minor: Z
   - Overall: CLEAN or ISSUES_FOUND

Load python-style skill.

Agent will read spec automatically.
""")
```

---

## Bottom Line

**Writing effective agent prompts is a skill - practice makes perfect.**

**Remember:**
1. Clear objective (what success looks like)
2. Success criteria (measurable outcomes)
3. Expected output format (structure specified)
4. Context (only what's needed)
5. Error handling (what to do if fails)

**Before every Task call, ask:**
- Is my objective clear?
- Will the agent know when it's done?
- Have I specified the output format?
- Can I run this in parallel with other tasks?

**The skill compounds:** Better prompts → better outputs → more effective delegation → faster iteration → better results.

Use this skill PROACTIVELY. Don't wait until you get bad results to improve your prompts.

---

**For detailed examples and advanced patterns:** See reference.md
