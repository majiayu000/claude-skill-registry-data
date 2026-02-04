---
name: btb-workflow
description: BackToBack/ByTheBooks (BTB) - An in-repo collaboration pattern for Human-AI engineering teams. Use this skill when working in repositories with a SPECS/ directory containing README.md, PROGRESS.md, and design documents. BTB emphasizes documentation-driven development, mandatory progress tracking before commits, and a feedback loop between design → MVP → implementation.
---

# BTB Workflow (BackToBack/ByTheBooks)

## Overview

BTB (BackToBack/ByTheBooks) is a structured collaboration pattern for repositories where humans and AI work together on software projects. The pattern emphasizes:

- **Documentation as the foundation** - All work flows from SPECS/ documents
- **Progress accountability** - PROGRESS.md must be updated before every commit
- **Design refinement loop** - DESIGN → MVP → Implementation → Progress feedback
- **Clear role separation** - Humans provide vision (HUMAN: commits), AI implements (Claude commits)
- **Psychological safety** - Lean yet comprehensive documentation supports all participants

## When to Use BTB

Use this skill when:

- The repository contains a `SPECS/` directory with `README.md` as the entrypoint
- Working on projects with iterative design and implementation phases
- Collaborating between human designers/PMs and AI implementers
- The user mentions BTB, BackToBack, or ByTheBooks workflow
- The repository shows patterns of "HUMAN:" prefixed commits followed by implementation commits
- PROGRESS.md exists and needs updating before commits

## BTB Document Structure

### Core Documents (Required)

#### 1. SPECS/README.md - Navigation Entrypoint

**Purpose**: Help all participants quickly find what they need to read.

**Key sections**:
- **Quick Start guides by role** (Engineers, PMs, QA, etc.)
- **Document purposes table** - What each doc is for and who should read it
- **Architecture at-a-glance** - Technology stack, key decisions
- **Development workflow** - How to run, test, deploy
- **Troubleshooting** - Common issues and solutions
- **Learning path** - Day 1, Week 1, Expert level guides

**Psychological state**: Reduce overwhelm by providing clear reading order. New team members should know exactly where to start.

#### 2. SPECS/PROGRESS.md - Living Status Report

**Purpose**: Track current state, test results, and next actions.

**Required fields** (validated by `validate_progress.py`):
```markdown
**Report Date**: October 28, 2025  # Must be today's date
**Session**: claude/session-XXX     # If on claude/ branch
**Branch**: `current-branch-name`   # Must match actual branch
**Current Phase**: Phase 2 Complete ✅
```

**Key sections**:
- **Executive Summary** - 2-3 sentence current state
- **Timeline & Phases** - What's been completed with commits, test comprehensiveness, deliverables
- **Current Capabilities** - What users/system can do RIGHT NOW
- **Next Steps** - Tasks with acceptance criteria (checkboxes)
- **Known Issues & Technical Debt** - Transparency about problems
- **Success Criteria** - What "done" looks like

**BTB Rule**: PROGRESS.md MUST be updated before every commit. Use `scripts/validate_progress.py` to enforce this.

**Psychological state**: Maintain shared reality. All participants must know current status before making changes.

### Optional Documents (Design Phase)

#### 3. DESIGN Document (e.g., Architecture_Design.md)

**Purpose**: Comprehensive vision of the full system.

**Characteristics**:
- Describes the complete, ideal architecture
- May include features beyond initial implementation
- Serves as north star for long-term direction
- Contains domain requirements, user workflows, technical details
- Always phrased as long-lived document: NEVER contains incremental or current-progress-related details

**When to create**: At project inception when human has full vision to communicate.

**Commit pattern**: HUMAN commits with "HUMAN: added design document"

#### 4. MVP Document (e.g., MVP.md)

**Purpose**: "Refraction" of DESIGN into minimum viable scope.

**Characteristics**:
- Describes what to build to most quickly validate / de-risk design decisions by reducing scope
- Resolves conflicts between design and project reality
- Provides implementation roadmap for mid-level engineers
- Includes file structure, integration notes, testing strategy
- NEVER contains vague information -- the purpose of writing this document is to surface and force resolution on ambiguity
- Always phrased as long-lived document: NEVER contains incremental or current-progress-related details

**When to create**: After DESIGN exists but before implementation, to reduce scope and risk.

**Relationship to DESIGN**: MVP is a subset/adaptation of DESIGN, not a replacement. It answers "What can we build in 2-4 weeks that validates the core idea?"

## BTB Workflow Stages

### Stage 1: Human Provides Vision (DESIGN)

**Who**: Human (Product owner, architect, domain expert)

**Action**: Create comprehensive design document in SPECS/

**Commit pattern**:
```
HUMAN: added design document
```

**Content**: Full vision including:
- Domain requirements and user needs
- Architecture decisions
- Technology choices
- User workflows and use cases
- Success criteria

**Psychological state**: Human brain-dumps complete vision without worrying about implementation complexity.

### Stage 2: Scope Refinement (MVP)

**Who**: AI (Claude) in collaboration with human

**Action**: Create MVP document that refracts DESIGN into implementable scope

**Purpose**:
- Identify conflicts between design and current codebase
- Reduce scope to 2-4 week MVP
- Make critical decisions (framework choices, auth approach, etc.)
- Define implementation phases

**Commit pattern**:
```
docs: Add comprehensive MVP implementation plan
```

**Psychological state**: Reduce anxiety about "how do we build all of this?" by creating a realistic, phased plan.

### Stage 3: Implementation (Phases)

**Who**: AI (Claude) following TDD and phase roadmap

**Action**: Implement features in phases, updating PROGRESS.md before each commit

**Commit patterns**:
```
feat: Set up Vitest and implement vizStore with TDD
feat: Complete Phase 1 - Layout components and CORS with TDD
feat: Complete Phase 2 - MCP integration and model selection
docs: Add comprehensive progress report and documentation guide
```

**Process per phase**:
1. Read PROGRESS.md to understand current state
2. Implement next phase using TDD (test-first development)
3. Update PROGRESS.md with:
   - Test results
   - What was delivered
   - Current capabilities
   - Next tasks
4. Update README.md if workflow changes
5. Commit with descriptive message

**BTB Rule**: PROGRESS.md must be updated before commit. Validate with `scripts/validate_progress.py`.

**Psychological state**: Maintain confidence through incremental progress. Each phase has clear deliverables and test results.

### Stage 4: Continuous Feedback Loop

**Who**: All participants

**Action**: Review PROGRESS.md, adjust course, refine scope

**Triggers for feedback**:
- Blocker discovered during implementation
- Test failures requiring design change
- New requirements from stakeholders
- Technical debt accumulation

**Response options**:
1. **Adjust implementation** - If solution exists within current design
2. **Update MVP** - If scope needs refinement
3. **Consult DESIGN** - If fundamental architecture question
4. **Request human input** - If decision requires domain expertise

**Psychological state**: Safe to discover problems and adjust. Documentation supports course correction.

## BTB Psychological Principles

### 1. Reduce Cognitive Load

**Problem**: Large projects overwhelm participants who don't know where to start.

**BTB Solution**:
- README.md provides reading order by role
- Quick start sections (Day 1, Week 1 guides)
- Document purpose table

### 2. Maintain Shared Reality

**Problem**: Distributed teams lose sync on what's actually implemented vs planned.

**BTB Solution**:
- PROGRESS.md must be updated before every commit
- Test results included in progress reports
- "Current Capabilities" section describes what works TODAY

### 3. Support Safe Exploration

**Problem**: Fear of breaking things or going off-track paralyzes decision-making.

**BTB Solution**:
- DESIGN provides north star (never wrong to reference)
- MVP provides guardrails (scope boundaries)
- PROGRESS provides current state (always know where you are)
- Git history shows HUMAN vs AI commits (clear accountability)

### 4. Enable Incremental Progress

**Problem**: Large tasks feel insurmountable, causing procrastination or rushed work.

**BTB Solution**:
- Phase-based implementation with acceptance criteria
- Test-first development (TDD) provides confidence
- Each commit advances measurable progress
- Success criteria defined upfront

### 5. Facilitate Onboarding

**Problem**: New team members don't know how to contribute.

**BTB Solution**:
- README.md learning path (Day 1 → Day 2 → Week 2+)
- Role-specific reading guides (Engineer, PM, QA)
- File structure reference
- Troubleshooting section

## Using BTB Scripts

Three Python scripts support the BTB workflow:

### 1. Initialize BTB Structure

Use when starting a new BTB project or adding BTB to existing repo:

```bash
uv run scripts/init_btb.py
```

Creates:
- `SPECS/` directory
- `SPECS/README.md` (navigation template)
- `SPECS/PROGRESS.md` (status tracking template)

Options:
- `--force` - Overwrite existing files

### 2. Validate Before Commit

Use before every commit to ensure PROGRESS.md is updated:

```bash
uv run scripts/validate_progress.py
```

Checks:
- PROGRESS.md has been modified in working tree
- Report date matches today's date
- Branch name matches current git branch
- Session ID matches branch (if on claude/ branch)

**BTB Best Practice**: Add as git pre-commit hook or CI check.

### 3. Check BTB Status

Use to understand current project state:

```bash
uv run scripts/btb_status.py
```

Displays:
- Current phase/status from PROGRESS.md
- Document coverage (which BTB documents exist)
- Recent commits by author (HUMAN vs Claude vs Other)
- Recommendations for next actions

## BTB Commit Patterns

### HUMAN Commits (Design/Requirements)

Pattern: `HUMAN: <action>`

Examples:
```
HUMAN: added design document
HUMAN: updated MVP scope based on feedback
HUMAN: clarified authentication requirements
```

**Psychological marker**: These commits represent human decision-making and vision.

### AI Implementation Commits

Patterns:
- `feat: <what was built>`
- `docs: <what was documented>`
- `test: <what was tested>`
- `fix: <what was fixed>`

Examples:
```
feat: Set up Vitest and implement vizStore with TDD
feat: Complete Phase 2 - MCP integration and model selection
docs: Add comprehensive progress report and documentation guide
```

**BTB Convention**: Include "with TDD" when test-driven development was used.

**Commit bodies**: Include detailed bullets of what changed, test results, and references to PROGRESS.md updates.

### Commit Co-Authoring

AI commits should include co-author attribution:

```
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## BTB in Practice: Workflow Examples

### Example 1: Starting a New Feature

**Context**: PROGRESS.md shows Phase 2 complete, Phase 3 is next.

**Procedure**:

1. **Read current state**:
   ```bash
   uv run scripts/btb_status.py
   ```

2. **Review PROGRESS.md** to understand:
   - What was completed in Phase 2
   - What Phase 3 requires (acceptance criteria)
   - Current test coverage and capabilities

3. **Review MVP.md** for Phase 3 implementation details:
   - File structure
   - Integration notes
   - Testing strategy

4. **Implement Phase 3** using TDD:
   - Write tests first
   - Implement features
   - Run test suite
   - Verify acceptance criteria

5. **Update PROGRESS.md** before committing:
   - Update "Report Date" to today
   - Move Phase 3 from "Next Steps" to "Timeline & Phases"
   - Add test results, deliverables, key files
   - Update "Current Capabilities"
   - Add Phase 4 to "Next Steps"

6. **Validate and commit**:
   ```bash
   uv run scripts/validate_progress.py
   git add .
   git commit -m "feat: Complete Phase 3 - Chart visualization"
   ```

### Example 2: Discovering a Blocker

**Context**: During implementation, discover that a DESIGN assumption is invalid.

**Procedure**:

1. **Document in PROGRESS.md**:
   - Add to "Known Issues" section
   - Describe the blocker
   - Mark current task as "in_progress" (not completed)

2. **Consult hierarchy**:
   - Check MVP.md - Can we adjust MVP scope?
   - Check DESIGN - Is this a fundamental conflict?
   - Determine if human input needed

3. **If human input needed**:
   - Commit PROGRESS.md update describing blocker
   - Flag for human review
   - Wait for human to provide HUMAN: commit with decision

4. **If adjustable within scope**:
   - Update MVP.md with revised approach
   - Update PROGRESS.md with new plan
   - Commit docs changes
   - Continue implementation

### Example 3: Onboarding a New Team Member

**Context**: New engineer joins project mid-implementation.

**Procedure**:

1. **Direct to SPECS/README.md**:
   - Find their role (Engineer, PM, etc.)
   - Follow reading order

2. **Day 1 path** (for Engineers):
   - Read PROGRESS.md (15 min) - current status
   - Run the application (30 min)
   - Run tests (15 min)
   - Goal: See app working

3. **Day 2 path**:
   - Read MVP.md (60 min) - implementation guide
   - Explore codebase following file structure
   - Write a simple test (30 min)
   - Goal: Understand architecture

4. **Day 3+ path**:
   - Pick task from PROGRESS.md "Next Steps"
   - Follow BTB workflow (read → implement TDD → update PROGRESS → commit)
   - Goal: Contribute code

## BTB Anti-Patterns (What to Avoid)

### ❌ Committing Without Updating PROGRESS.md

**Problem**: Breaks shared reality. Team loses sync on current state.

**Solution**: Use `validate_progress.py` as pre-commit hook.

### ❌ Outdated README.md

**Problem**: New team members get lost or read wrong documents.

**Solution**: Update README.md when workflow changes. Review quarterly.

### ❌ MVP Scope Creep

**Problem**: MVP grows to match DESIGN, losing focus on de-risking.

**Solution**: MVP should be 2-4 weeks. If larger, create MVP v2 document.

### ❌ Missing Test Results in PROGRESS.md

**Problem**: Can't verify claims about what works. Confidence erodes.

**Solution**: Always include test output in progress reports. "50/50 tests passing (306ms)"

### ❌ Vague Next Steps

**Problem**: Participants don't know what to do next.

**Solution**: Use acceptance criteria checkboxes. Be specific about files, functions, features.

### ❌ Design/MVP Conflicts

**Problem**: DESIGN and MVP contradict each other.

**Solution**: MVP should reference DESIGN and explain deviations. "Design suggests X, MVP uses Y because..."

## BTB and Test-Driven Development (TDD)

BTB strongly encourages TDD as it aligns with the documentation-first philosophy:

**TDD Workflow**:
1. Read acceptance criteria from PROGRESS.md
2. Write tests for acceptance criteria (tests fail - red)
3. Implement minimum code to pass tests (tests pass - green)
4. Refactor if needed (tests still pass)
5. Update PROGRESS.md with test results
6. Commit

**Why TDD fits BTB**:
- Tests document behavior (living documentation)
- Test results in PROGRESS.md prove capabilities
- Incremental progress visible (N/M tests passing)
- Psychological safety (know when done)
- Regression prevention (existing features stay working)

**BTB Convention**: Include "with TDD" in commit messages when test-first approach used.

## BTB Document Templates

### Minimal PROGRESS.md Section

```markdown
## Next Steps: [Phase Name]

### Goals

[1-2 sentences: what are we building and why]

### Tasks ([Week/Sprint]: ~X days)

#### Task 1: [Component/Feature Name] (Days 1-2)

**Acceptance Criteria**:
- [ ] Specific testable requirement 1
- [ ] Specific testable requirement 2
- [ ] Specific testable requirement 3
- [ ] N+ tests covering all states

**Files to Create/Modify**:
- `path/to/Component.tsx`
- `path/to/Component.test.tsx`

**Implementation Notes**:
```typescript
// Pseudocode or key algorithm
function example() {
  // Show critical logic
}
```
```

### Commit Message Template

```
<type>: <short summary>

<detailed bullets>
- What changed behaviorally
- Integration notes
```

## Adapting BTB to Your Project

BTB is a pattern, not a rigid framework. Adapt as needed:

**Small projects**: May skip MVP, go straight from DESIGN to implementation
**Solo projects**: HUMAN commits might be notes-to-self
**Large teams**: Add more role-specific guides to README.md
**Non-software**: Adapt document types (e.g., "CONTENT_STRATEGY.md" instead of "DESIGN.md")

**Core principles to keep**:
1. Documentation-driven workflow
2. PROGRESS.md updated before commits
3. Clear reading order for new participants
4. Incremental, testable progress

## Summary: BTB in One Page

**What**: Documentation-driven collaboration pattern for Human-AI teams

**Documents**:
- README.md - Navigation entrypoint
- PROGRESS.md - Living status (MUST update before commits)
- DESIGN - Comprehensive vision (optional)
- MVP - Minimal scope refinement (optional)

**Workflow**:
1. Human provides vision (HUMAN: commits)
2. AI refracts to MVP if needed (docs: commits)
3. AI implements in phases with TDD (feat: commits)
4. PROGRESS.md updated before every commit
5. Feedback loop adjusts course

**Scripts**:
- `init_btb.py` - Initialize structure
- `validate_progress.py` - Enforce progress updates
- `btb_status.py` - Check current state

**Principles**:
- Reduce cognitive load (clear reading order)
- Maintain shared reality (mandatory progress tracking)
- Support safe exploration (DESIGN/MVP/PROGRESS hierarchy)
- Enable incremental progress (phases, TDD, acceptance criteria)
- Facilitate onboarding (role-specific guides)

**When to use**: Repositories with SPECS/, iterative projects, Human-AI collaboration
