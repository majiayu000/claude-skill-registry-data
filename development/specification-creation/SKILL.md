---
name: Specification Creation
description: Create technology-agnostic feature specifications using intelligence-first queries. Use when user describes what they want to build, mentions requirements, discusses user needs, or says "I want to create/build/implement" something. This skill enforces Article IV Specification-First Development.
degree-of-freedom: low
allowed-tools: Bash(fd:*), Bash(git:*), Bash(mkdir:*), Bash(project-intel.mjs:*), Read, Write, Edit, Grep
---

@.claude/shared-imports/constitution.md
@.claude/shared-imports/CoD_Σ.md
@.claude/templates/feature-spec.md

# Specification Creation

**Purpose**: Generate technology-agnostic feature specifications (WHAT/WHY only, no HOW) with intelligence-backed evidence and structured user stories.

**Constitutional Authority**: Article IV (Specification-First Development), Article I (Intelligence-First Principle), Article II (Evidence-Based Reasoning)

---

## Phase 1: Intelligence-First Context Gathering

**MANDATORY**: Execute intelligence queries BEFORE any file operations.

### Step 1.1: Auto-Number Next Feature

```bash
!`fd --type d --max-depth 1 '^[0-9]{3}-' specs/ 2>/dev/null | sort | tail -1`
```

Extract highest existing feature number, increment by 1 for next feature.

**Example**:
- Last feature: `specs/003-auth-system`
- Next number: `004`

### Step 1.2: Query Existing Patterns

```bash
!`project-intel.mjs --search "<user-keywords>" --type md --json > /tmp/spec_intel_patterns.json`
```

Search for related features, similar requirements, existing patterns.

**Save evidence** to `/tmp/spec_intel_patterns.json` for CoD^Σ tracing.

### Step 1.3: Understand Project Architecture

```bash
!`project-intel.mjs --overview --json > /tmp/spec_intel_overview.json`
```

Get project structure, tech stack, existing components to inform requirements.

---

## Phase 2: Extract User Requirements (WHAT/WHY Only)

**Article IV Mandate**: Specifications MUST be technology-agnostic.

### Step 2.1: Problem Statement

Extract from user description:
- What problem are they trying to solve?
- Why is this needed?
- Who will use this?
- What value does it provide?

**NO IMPLEMENTATION DETAILS**: No tech stack, no architecture, no "how to build it".

### Step 2.2: User Stories with Priorities

Organize requirements as user stories:

**Format**:
```
## User Story 1 - [Title] (Priority: P1)

**As a** [user type]
**I want to** [capability]
**So that** [value/benefit]

**Why P1**: [Rationale for priority]

**Independent Test**: [How to validate this story works standalone]

**Acceptance Scenarios**:
1. **Given** [state], **When** [action], **Then** [outcome]
2. **Given** [state], **When** [action], **Then** [outcome]
```

**Priority Levels**:
- **P1**: Must-have for MVP (core value)
- **P2**: Important but not blocking (enhances P1)
- **P3**: Nice-to-have (can be deferred)

**Requirement**: Each story MUST be independently testable (Article VII).

### Step 2.3: Functional Requirements (Technology-Agnostic)

Document as testable requirements:

```
- **FR-001**: System MUST [specific capability]
- **FR-002**: Users MUST be able to [interaction]
- **FR-003**: System MUST [behavior]
```

**Mark Unknowns**:
```
- **FR-004**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified]
```

**Maximum 3 [NEEDS CLARIFICATION] markers** - use sparingly, clarify rest through user dialogue.

---

## Phase 3: Generate Specification with CoD^Σ Evidence

### Step 3.1: Create Feature Directory Structure

```bash
NEXT_NUM=$(printf "%03d" $(($(fd --type d --max-depth 1 '^[0-9]{3}-' specs/ 2>/dev/null | wc -l) + 1)))
FEATURE_NAME="<derived-from-user-description>"  # Lowercase, hyphenated, 2-4 words
mkdir -p specs/$NEXT_NUM-$FEATURE_NAME
```

### Step 3.2: Create Git Branch (if git repo)

```bash
if git rev-parse --git-dir >/dev/null 2>&1; then
    git checkout -b "$NEXT_NUM-$FEATURE_NAME"
fi
```

### Step 3.3: Write Specification

Use `@.claude/templates/feature-spec.md` structure with:

1. **YAML Frontmatter**:
   ```yaml
   ---
   feature: <number>-<name>
   created: <YYYY-MM-DD>
   status: Draft
   priority: P1
   ---
   ```

2. **Problem Statement**: What problem are we solving and why?

3. **User Stories**: From Step 2.2 (prioritized, independently testable)

4. **Functional Requirements**: From Step 2.3 (technology-agnostic)

5. **Success Criteria**: Measurable outcomes (not technical metrics)

6. **CoD^Σ Evidence Trace**:
   ```
   Intelligence Queries:
   - project-intel.mjs --search "<keywords>" → /tmp/spec_intel_patterns.json
     Findings: [file:line references to similar features]
   - project-intel.mjs --overview → /tmp/spec_intel_overview.json
     Context: [existing architecture patterns]

   Assumptions:
   - [ASSUMPTION: rationale based on intelligence findings]

   Clarifications Needed:
   - [NEEDS CLARIFICATION: specific question]
   ```

7. **Edge Cases**: Boundary conditions, error scenarios

### Step 3.4: Save Specification

```bash
Write specs/$NEXT_NUM-$FEATURE_NAME/spec.md
```

---

## Phase 4: Report to User

**Output Format**:
```
✓ Feature specification created: specs/<number>-<name>/spec.md

Intelligence Evidence:
- Queries executed: project-intel.mjs --search, --overview
- Patterns found: <file:line references>
- Related features: <existing feature numbers>

User Stories:
- P1 stories: <count> (MVP scope)
- P2 stories: <count> (enhancements)
- P3 stories: <count> (future)

Clarifications Needed:
- [NEEDS CLARIFICATION markers if any, max 3]

**Automatic Next Steps**:
1. If clarifications needed: Use clarify-specification skill
2. Otherwise: **Automatically create implementation plan**

Invoking /plan command now...

[Plan creation, task generation, and audit will proceed automatically]
```

---

## Phase 5: Automatic Implementation Planning

**DO NOT ask user to trigger planning** - this is automatic workflow progression (unless clarifications needed).

### Step 5.1: Check for Clarifications

**If [NEEDS CLARIFICATION] markers exist**:
- Do NOT proceed to planning
- Report clarifications needed to user
- User must run clarify-specification skill or provide answers
- After clarifications, re-run specify-feature skill

**If NO clarifications** (or max 0-1 minor ones):
- Proceed automatically to implementation planning

### Step 5.2: Invoke /plan Command

**Instruct Claude**:

"Specification is complete. **Automatically create the implementation plan**:

Run: `/plan specs/$FEATURE/spec.md`

This will:
1. Create implementation plan with tech stack selection
2. Generate research.md, data-model.md, contracts/, quickstart.md
3. Define ≥2 acceptance criteria per user story
4. **Automatically invoke generate-tasks skill**
5. **Automatically invoke /audit quality gate**

The entire workflow from planning → tasks → audit happens automatically. No manual intervention needed."

### Step 5.3: Workflow Automation

After `/plan` is invoked, the automated workflow proceeds:

```
/plan specs/$FEATURE/spec.md
  ↓ (automatic)
create-implementation-plan skill
  ↓ (automatic)
generate-tasks skill
  ↓ (automatic)
/audit $FEATURE
  ↓
Quality Gate Result: PASS/FAIL
```

**User sees**:
- spec.md created ✓
- plan.md created ✓
- tasks.md created ✓
- audit report generated ✓
- Implementation readiness status

**User only needs to**:
- Review audit results
- Fix any CRITICAL issues (if audit fails)
- Or proceed with `/implement plan.md` (if audit passes)

---

**Note**: This completes specification creation. Next steps happen automatically unless clarifications are needed.
```

**Constitutional Compliance**:
- ✓ Article I: Intelligence queries executed before file operations
- ✓ Article II: CoD^Σ trace with evidence saved to /tmp/*.json
- ✓ Article IV: Specification is technology-agnostic (WHAT/WHY only)
- ✓ Article VII: User stories are independently testable

---

## Anti-Patterns to Avoid

**DO NOT**:
- Include tech stack choices in specification
- Design architecture or data models
- Specify implementation details ("use React hooks", "create API endpoint")
- Create more than 3 [NEEDS CLARIFICATION] markers (clarify through dialogue first)
- Write vague requirements ("system should be fast" → specify "p95 latency < 200ms")

**DO**:
- Focus on user value and business requirements
- Make requirements testable and measurable
- Prioritize user stories (P1, P2, P3)
- Document evidence from intelligence queries
- Limit unknowns (max 3 [NEEDS CLARIFICATION])

---

## Example Execution

**User Input**: "I want to build a user authentication system with social login options"

**Execution**:

1. **Intelligence Queries**:
   ```bash
   fd --type d --max-depth 1 '^[0-9]{3}-' specs/
   # Output: specs/001-dashboard, specs/002-api, specs/003-reporting
   # Next: 004

   project-intel.mjs --search "auth login" --type tsx --json
   # Findings: src/components/Login.tsx:12-45 (existing login form)
   #           src/utils/auth.ts:23 (auth helper functions)
   ```

2. **Extract Requirements**:
   ```
   Problem: Users need to securely access their accounts
   Why: Enable personalized experiences and data security
   Who: End users, administrators
   Value: Secure access, convenience

   User Stories:
   - P1: Basic email/password authentication
   - P2: Social login (Google, GitHub)
   - P3: Two-factor authentication
   ```

3. **Create Feature**:
   ```bash
   mkdir -p specs/004-user-authentication
   git checkout -b 004-user-authentication
   ```

4. **Write Spec** with CoD^Σ evidence, user stories, requirements

5. **Report**:
   ```
   ✓ Feature specification created: specs/004-user-authentication/spec.md

   Intelligence Evidence:
   - Found existing: src/components/Login.tsx:12-45, src/utils/auth.ts:23
   - Pattern: Email/password already partially implemented

   User Stories: 3 total (1 P1, 1 P2, 1 P3)

   Next: Run clarify-specification skill or create-implementation-plan skill
   ```

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-10-19
