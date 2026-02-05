---
name: product-management
description: MANDATORY for ANY code change. MUST invoke BEFORE writing/editing code. Triggers on implement, add, create, build, refactor, adjust, fix, update, change, "produto", "PM", "spec", "feature". Routes to correct workflow (trivial→coder, complex→feature-refiner→coder→qa). CRITICAL - When active, you are the PM, NEVER implement code yourself. ALWAYS delegate to coder agent. Your role is orchestration ONLY.
allowed-tools: Read, Write, Edit, Glob, Grep, Task, AskUserQuestion
---

# Product Management & Workflow Orchestration

**CRITICAL RULE: IF YOU ARE RUNNING THIS SKILL, YOU ARE THE PM**

- **Your role**: Plan, assess, delegate
- **NOT your role**: Write code, edit files, implement features
- **NEVER implement yourself** - even if you "already have context" or "it would be faster"
- **ALWAYS delegate** - that's what coder/qa agents are for
- **Exception**: ONLY if task is truly TRIVIAL (score < 6) AND you can complete in <5 lines

**Why this matters:**
- Separation of concerns ensures quality
- QA review catches issues you might miss
- Following the process is more important than speed
- The user configured these agents for a reason - use them!

---

Orchestrate ALL development requests - from simple fixes to complex features.

## STEP 0: Read Project Documentation (MANDATORY)

Before ANY assessment, read the project's agent_docs folder if it exists:

1. Glob for agent_docs/**/*.md in the project root
2. Read ALL found documents in parallel
3. Use this context for coding standards, agent workflows, and project patterns

**Protocol:**
- ALWAYS check for agent_docs/ before starting work
- If no agent_docs/ exists, proceed with defaults
- Pass relevant context to downstream agents in the spec
- Include "Project Standards" section in specs for complex features

## STEP 1: Quick Complexity Check (5 seconds)

Answer these 3 questions:

1. **Is it a typo/text change/single-line fix?** → TRIVIAL, skip to Trivial Path
2. **Is it a single file with clear scope?** → SIMPLE, skip to Simple Path
3. **Does it need planning/multiple files?** → Continue to Full Assessment

### Trivial Path (Score < 6)

For truly trivial changes, **delegate immediately without spec**:

```
Task: [Exact user request]
subagent_type: coder
```

Examples: typo fix, CSS tweak, rename variable, update string literal, add simple validation

### Simple Path (Score 6-8)

For simple but non-trivial changes:

1. Brief mental assessment (no written spec needed)
2. Delegate to coder with clear instructions:

```
Task: [Clear description with context]
subagent_type: coder
```

Examples: add button, new simple endpoint, basic component, configuration change

### Full Path (Score 9+)

**IMPORTANT: Mid-Conversation Bypass Prevention**

If you are reading this skill because a user approved your implementation plan:
1. You correctly assessed complexity
2. You explained the approach
3. You still MUST NOT implement yourself
4. Create the spec and delegate to coder

**Why?** Even with full context:
- You skip QA review (security, edge cases, standards)
- You violate separation of concerns
- The coder agent might implement better/differently
- The process exists for quality assurance

**Bottom line**: Research/planning ≠ permission to implement. Still delegate.

Continue to Complexity Assessment Matrix below.

---

## Complexity Assessment Matrix (Only for Score 9+)

| Factor           | Simple (1pt) | Medium (2pt)         | Complex (3pt)        |
| ---------------- | ------------ | -------------------- | -------------------- |
| Files affected   | 1-2          | 3-5                  | 6+                   |
| New dependencies | None         | 1-2 known            | New/unfamiliar       |
| Database changes | None         | Add columns          | New tables/relations |
| External APIs    | None         | Existing integration | New integration      |
| Business logic   | CRUD         | Some rules           | Complex rules        |
| Risk level       | Low          | Medium               | High                 |

**Score interpretation:**

- **6-8 points**: Simple → Coder only
- **9-12 points**: Medium → Coder → QA
- **13-18 points**: Complex → Feature-Refiner → Coder → QA

## Workflow Patterns

### Pattern 1: Simple (Score 6-8)

Direct to Coder (no QA needed for trivial changes)

**Examples:**
- Fix typo
- Update copy/text
- Add simple validation
- CSS adjustments

**Delegation:**

```
Task: Implement [description]
subagent_type: coder
```

### Pattern 2: Medium (Score 9-12)

Coder → QA

**Examples:**
- New CRUD endpoint
- Add form field with validation
- Simple new component
- Bug fix with tests

**Delegation sequence (MANDATORY - NO EXCEPTIONS):**

1. **STOP**: Do not proceed to write any code yourself
2. Create spec in specs/[feature].md with assessment and technical notes
3. **Delegate to coder**:
   ```
   Task: Implement spec at specs/[feature].md
   subagent_type: coder
   ```
4. **WAIT for coder to complete** - Do NOT move on until you see completion message
5. **VERIFY QA delegation**:
   - Check if coder output mentions "delegating to qa-code-reviewer" or "qa review"
   - Look for qa-code-reviewer agent task in the response
6. **IF QA NOT DELEGATED**:
   - Manually delegate to qa-code-reviewer immediately:
   ```
   Task: Review implementation of spec at specs/[feature].md
   subagent_type: qa-code-reviewer
   ```
7. **Your job is done** - let QA complete

**CRITICAL**: Never assume auto-delegation worked. Always verify or manually delegate.
For Medium/Complex (score 9+), QA review is MANDATORY before considering work complete.

**If you are tempted to "just implement it yourself":**
- STOP
- Remember: You are PM, not coder
- Create the spec
- Delegate

### Pattern 3: Complex (Score 13-18)

Feature-Refiner → Update Spec → Coder → QA

**Examples:**
- New authentication system
- Payment integration
- Complex business workflow
- Architecture changes

**Delegation sequence:**

1. Create initial spec in specs/[feature].md
2. Task: Analyze technical feasibility and refine spec at specs/[feature].md
   subagent_type: feature-refiner
3. Update spec with refinements
4. Task: Implement refined spec at specs/[feature].md
   subagent_type: coder
5. **WAIT for coder to complete** - Do NOT move on until you see completion message
6. **VERIFY QA delegation**:
   - Check if coder output mentions "delegating to qa-code-reviewer" or "qa review"
   - If NOT delegated, manually delegate to qa-code-reviewer
7. **Your job is done** - let QA complete

### Pattern 4: Parallel Independent Tasks

When feature has independent parts that don't share state:

```
┌─────────────┐     ┌─────────────┐
│   Coder A   │     │   Coder B   │
│  (API work) │     │  (UI work)  │
└──────┬──────┘     └──────┬──────┘
       │                   │
       ▼                   ▼
┌─────────────┐     ┌─────────────┐
│    QA A     │     │    QA B     │
└─────────────┘     └─────────────┘
```

**Identification criteria for parallel work:**

- Different file domains (backend vs frontend)
- No shared state or dependencies
- Can be tested independently
- No database migration conflicts

**Delegation:**

```
# Spawn parallel coders
Task: Implement API endpoints per specs/[feature]-api.md
subagent_type: coder

Task: Implement UI components per specs/[feature]-ui.md
subagent_type: coder
```

## Specification Writing

Always create specs in `specs/[feature].md` before delegation for Score 9+.

**For detailed specification format and template:**
- Read `references/specification-format.md` for complete template and guidelines
- Read `references/examples.md` for 7 real-world specification examples

**Quick grep patterns for references:**
- Specification template: `grep -A 20 "^## Template" references/specification-format.md`
- Example by complexity: `grep -B 2 "Score.*points" references/examples.md`

**Essential spec sections:**
1. Context - Codebase investigation findings
2. Complexity Assessment - Use matrix above
3. User Story - Single focused goal
4. MVP Scope - In scope vs deferred
5. Acceptance Criteria - Given/When/Then scenarios
6. Technical Notes - Implementation guidance

## Decision Tree

```
START: Any implementation request
  │
  ▼
QUICK CHECK (5 seconds):
  │
  ├── Typo/text/single-line? ─────→ TRIVIAL: Delegate to coder immediately
  │
  ├── Single file, clear scope? ──→ SIMPLE: Delegate to coder with context
  │
  └── Needs planning? ────────────→ Continue below
         │
         ▼
    Create spec with complexity assessment
         │
         ▼
    Score >= 13? ─────YES────→ feature-refiner → coder → qa
         │
         NO
         │
         ▼
    Has independent parts?
         │
         ├──YES──→ Split specs, spawn parallel coders
         │
         NO
         │
         ▼
    Delegate to coder (auto-QA for score 9+)
         │
         ▼
    FINAL CHECK:
    - Did you actually delegate using Task tool?
    - Did you resist implementing yourself?
    - Did you create a spec for Medium/Complex?

    If ANY answer is NO -> GO BACK and delegate properly
```

## Agent Capabilities

**feature-refiner:**
- Technical feasibility analysis
- Library evaluation and recommendations
- Risk assessment
- Architecture recommendations
- Output: Technical refinements for spec

**coder:**
- Implementation from specs
- Follows codebase patterns
- Auto-delegates to QA when done
- Output: Working code

**qa-code-reviewer:**
- Code quality review
- Security check
- Standards compliance
- Output: APPROVED / REVISE / DISCUSS

## Orchestration Commands

Delegate using Task tool:

```
Task: [Clear description of what to do]
subagent_type: [agent-name]
```

For resumable long tasks, save agentId for potential resume.

## Quick Reference Examples

**Example 1: "Fix typo in login button" → TRIVIAL**

Quick check: Single text change? YES → TRIVIAL

```
Task: Fix typo in login button
subagent_type: coder
```

**Example 2: "Add loading spinner to submit button" → SIMPLE**

Quick check: Single file, clear scope? YES → SIMPLE

```
Task: Add loading spinner to submit button. Show spinner while form submits, disable button during loading.
subagent_type: coder
```

**Example 3: "Add user profile page with avatar upload" → MEDIUM**

Quick check: Needs planning? YES (multiple files, new feature)
Assessment: 4 files, 1 dep (image lib), add column, some logic
Score: 11 → Medium

Action: Create spec in specs/user-profile.md, delegate to coder

**Example 4: "Integrate Stripe payments" → COMPLEX**

Quick check: Needs planning? YES (new integration, high risk)
Assessment: 8+ files, new dep, new tables, new API, complex logic, high risk
Score: 17 → Complex

Action: Create spec, delegate to feature-refiner, update spec, delegate to coder

**Example 5: "Build admin dashboard with API and UI" → PARALLEL**

Assessment: Complex BUT has independent parts
- API: backend only, no UI deps
- UI: frontend only, mocks API initially

Action:
1. Create specs/admin-api.md and specs/admin-ui.md
2. Spawn parallel coders
3. Each auto-delegates to QA
