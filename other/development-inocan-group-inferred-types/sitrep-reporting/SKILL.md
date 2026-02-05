---
name: sitrep-reporting
description: |
  Military-style SITuation REPort protocol for multi-agent coordination. Enforces structured status
  reporting with 🟢🟡🔴 codes, quantitative progress (0-100%), blockers, dependencies, ETAs, and
  authorization codes for secure handoffs. Prevents communication failures, lost context, and delayed
  blocker reporting. Use when: coordinating multiple agents, wave execution, reporting progress,
  requesting status updates, handing off deliverables.

skill-type: PROTOCOL
shannon-version: ">=4.0.0"

mcp-requirements:
  required:
    - name: serena
      version: ">=2.0.0"
      purpose: Save SITREPs for cross-session audit trail
      fallback: local-storage
      degradation: low

required-sub-skills: []
optional-sub-skills:
  - wave-orchestration
  - context-preservation

allowed-tools: Read, Write, Serena
---

# SITREP Reporting Protocol

## Overview

**Purpose**: Military-style situation reporting protocol that transforms vague, unstructured status updates into precise, actionable, auditable communication between agents. Prevents coordination failures, lost context, and delayed blocker reporting.

**Origin**: Adapted from Hummbl framework's sitrep-coordinator pattern. Enhanced with Shannon's anti-rationalization enforcement and quantitative metrics.

---

## When to Use

Use this skill when:
- Coordinating multiple agents in wave execution
- Agent needs to report progress during long-running tasks
- Wave coordinator requests status update
- Agent encounters blocker requiring immediate escalation
- Agent completes deliverable and needs to hand off work
- Executive/stakeholder requests project status

DO NOT use when:
- Casual conversation without status request
- Single-agent work with no coordination needed
- User asks for explanation (not status)

## Inputs

**Required:**
- `agent_name` (string): Name of reporting agent (e.g., "frontend-dev")
- `status` (string): Status code - "ON TRACK" (🟢), "AT RISK" (🟡), or "BLOCKED" (🔴)
- `progress` (integer): Progress percentage 0-100
- `current_task` (string): Description of current task

**Optional:**
- `completed_items` (list): List of completed work items
- `blockers` (string): Blocker description or "NONE"
- `dependencies` (list): List of dependencies (waiting or ready)
- `eta_hours` (float): Estimated time to completion in hours
- `handoff_ready` (boolean): Whether deliverable is ready for handoff (default: false)
- `format` (string): "full" or "brief" SITREP format (default: "full")

## Outputs

Formatted SITREP message (string):

**Full Format:**
```markdown
═══════════════════════════════════════════════════════════
🎯 SITREP: {AGENT_NAME}
═══════════════════════════════════════════════════════════

**STATUS**: 🟢 ON TRACK
**PROGRESS**: 75% complete
**CURRENT TASK**: {task_description}

**COMPLETED**:
- ✅ {item_1}
- ✅ {item_2}

**IN PROGRESS**:
- 🔄 {task_1} (60% complete)

**BLOCKERS**: NONE

**DEPENDENCIES**:
- ✅ Ready: {dependency}

**ETA TO COMPLETION**: {time_estimate}
**NEXT CHECKPOINT**: {checkpoint}
**HANDOFF**: {HANDOFF-CODE | N/A}
═══════════════════════════════════════════════════════════
```

**Brief Format:**
```markdown
🎯 **{AGENT}** | 🟢 | 75% | ETA: 2h
Blockers: NONE
```

---

## Anti-Rationalization (From Baseline Testing)

**CRITICAL**: Agents systematically rationalize skipping SITREP structure or providing informal updates. Below are the 5 most common rationalizations detected in baseline testing, with mandatory counters.

### Rationalization 1: "User knows what I mean"
**Example**: Agent says "Making progress on auth system" instead of structured SITREP

**COUNTER**:
- ❌ **NEVER** provide informal status updates
- ✅ "User knows" fails when coordinating 3-25 agents
- ✅ WAVE_COORDINATOR needs parseable status codes, not narratives
- ✅ Use SITREP format EVERY TIME status is requested
- ✅ Takes 15 seconds to format; saves hours of coordination failures

**Rule**: Format ALL status updates as SITREPs. No informal narratives.

### Rationalization 2: "Status is obvious from my messages"
**Example**: Agent says "Just finished the login form, now working on validation"

**COUNTER**:
- ❌ **NEVER** assume status is obvious without explicit codes
- ✅ Narratives require interpretation; status codes don't
- ✅ 🟢 ON TRACK vs 🟡 AT RISK is objective, not inferrable
- ✅ Cannot track metrics without structured progress %
- ✅ Use **STATUS**: 🟢/🟡/🔴 and **PROGRESS**: XX% ALWAYS

**Rule**: Explicit status codes. Narratives are supplementary, not primary.

### Rationalization 3: "I'll report when done"
**Example**: Agent waits until task completion to report, coordinator has no visibility

**COUNTER**:
- ❌ **NEVER** wait until completion to report
- ✅ 30-minute SITREP intervals are MANDATORY
- ✅ Blockers reported immediately (trigger-based SITREP)
- ✅ Coordinator needs real-time visibility, not retrospective updates
- ✅ "When done" reporting hides at-risk tasks until too late

**Rule**: Report every 30 minutes OR when blocked. Not "when done".

### Rationalization 4: "Coordinator can see my work"
**Example**: Agent assumes coordinator knows work is ready for handoff

**COUNTER**:
- ❌ **NEVER** assume coordinator knows deliverable status
- ✅ Without HANDOFF authorization code, work is NOT confirmed ready
- ✅ "Can see my work" creates ambiguity in multi-agent coordination
- ✅ Authorization codes provide audit trail and explicit confirmation
- ✅ Format: `HANDOFF-{AGENT}-{TIMESTAMP}-{HASH}` when ready

**Rule**: No handoff without authorization code. Seeing ≠ confirming.

### Rationalization 5: "This is urgent, skip the format"
**Example**: Agent reports blocker informally because "it's blocking everyone"

**COUNTER**:
- ❌ **NEVER** skip SITREP format for urgent issues
- ✅ Urgent issues NEED structure MORE, not less
- ✅ 🔴 BLOCKED status ensures coordinator triages correctly
- ✅ Structured format takes 15 seconds, even under pressure
- ✅ Informal "urgent" reports create confusion and slow resolution

**Rule**: Urgent = use SITREP format immediately. Structure enables speed.

### Rationalization 6: "Executives need narrative, not structure"
**Example**: During production outage, agent thinks "CEO needs story, not formatted SITREP"

**COUNTER**:
- ❌ **NEVER** assume executives prefer narrative over structure
- ✅ Executives need CLARITY, which structure provides instantly
- ✅ 🔴 BLOCKED is clearer than "we're having some issues"
- ✅ "25% complete" is clearer than "making progress on diagnosis"
- ✅ Structure enables instant understanding without reading comprehension
- ✅ Under pressure, clarity is MORE critical, not less

**Rule**: High-stakes reporting needs MAXIMUM clarity. Use structure.

### Detection Signal
**If you're tempted to**:
- Provide informal status ("making progress")
- Skip status codes ("seems to be going well")
- Wait to report ("I'll update when done")
- Assume visibility ("you can see my commits")
- Skip format for urgency ("this is blocking everyone!")
- Use narrative for executives ("CEO won't understand codes")

**STOP. You're rationalizing. Use SITREP format.**

---

## Workflow

### Phase 1: Determine SITREP Trigger

1. **Check Trigger Type**
   - Action: Identify why SITREP is needed
   - Triggers: 30-minute interval, blocker encountered, deliverable ready, coordinator request
   - Output: Trigger type and urgency level

2. **Select Format**
   - Action: Choose full or brief format
   - Decision: Full for detailed reports, brief for coordinator scanning
   - Output: Format selection

### Phase 2: Collect Status Data

1. **Determine Status Code**
   - Action: Evaluate current work state
   - Tool: Check blockers, dependencies, timeline
   - Output: 🟢 ON TRACK, 🟡 AT RISK, or 🔴 BLOCKED

2. **Calculate Progress**
   - Action: Quantify completion percentage
   - Validation: Must be 0-100, not qualitative
   - Output: Integer percentage

3. **Identify Blockers**
   - Action: List any blocking issues
   - Validation: Explicit statement (NONE or description)
   - Output: Blocker list

### Phase 3: Generate SITREP Message

1. **Format Message**
   - Action: Apply SITREP template
   - Tool: Use full or brief format
   - Output: Structured SITREP message

2. **Generate Authorization Code** (if deliverable ready)
   - Action: Create HANDOFF code
   - Tool: SHA-256 hash generation
   - Output: HANDOFF-{AGENT}-{TIMESTAMP}-{HASH}

### Phase 4: Save and Report

1. **Save to Serena**
   - Action: Store SITREP in memory
   - Tool: Serena write_memory()
   - Output: SITREP saved with timestamp

2. **Present to Coordinator**
   - Action: Report formatted SITREP
   - Output: SITREP message delivered

---

## SITREP Message Structure

### Full SITREP Format

Use this format for detailed status reports (every 30 minutes, or when coordinator requests):

```markdown
═══════════════════════════════════════════════════════════
🎯 SITREP: {AGENT_NAME}
═══════════════════════════════════════════════════════════

**STATUS**: {🟢 ON TRACK | 🟡 AT RISK | 🔴 BLOCKED}
**PROGRESS**: {0-100}% complete
**CURRENT TASK**: {task_description}

**COMPLETED**:
- ✅ {completed_item_1}
- ✅ {completed_item_2}

**IN PROGRESS**:
- 🔄 {active_task_1} ({percentage}% complete)
- 🔄 {active_task_2} ({percentage}% complete)

**BLOCKERS**: {blocker_description | NONE}

**DEPENDENCIES**:
- ⏸️ Waiting: {dependency} from {agent}
- ✅ Ready: {dependency} available

**ETA TO COMPLETION**: {time_estimate}
**NEXT CHECKPOINT**: {checkpoint_description}
**HANDOFF**: {HANDOFF-AGENT-TIMESTAMP-HASH | N/A}

═══════════════════════════════════════════════════════════
```

### Brief SITREP Format

Use this format for quick updates (coordinator scanning multiple agents):

```markdown
🎯 **{AGENT}** | {🟢🟡🔴} | {XX}% | ETA: {time}
Blockers: {NONE | description}
```

---

## Status Codes

### 🟢 ON TRACK
**Criteria**:
- All tasks progressing as planned
- No blockers or dependencies waiting
- ETA unchanged or ahead of schedule
- Deliverables on pace for checkpoint

**Example**:
```markdown
**STATUS**: 🟢 ON TRACK
**PROGRESS**: 65% complete
**CURRENT TASK**: Implementing user authentication API endpoints
**BLOCKERS**: NONE
**ETA TO COMPLETION**: 2 hours
```

### 🟡 AT RISK
**Criteria**:
- Minor blockers or delays present
- Dependencies not yet confirmed
- ETA slipping but recoverable
- May miss checkpoint without intervention

**Example**:
```markdown
**STATUS**: 🟡 AT RISK
**PROGRESS**: 40% complete
**CURRENT TASK**: Database schema migration
**BLOCKERS**: Schema validation taking longer than expected
**ETA TO COMPLETION**: 4 hours (originally 3 hours)
```

### 🔴 BLOCKED
**Criteria**:
- Cannot proceed without external action
- Critical dependency missing
- Blocker requires coordinator intervention
- Work stopped until resolved

**TRIGGER**: Report immediately (don't wait for 30-minute interval)

**Example**:
```markdown
**STATUS**: 🔴 BLOCKED
**PROGRESS**: 35% complete (paused)
**CURRENT TASK**: Frontend API integration
**BLOCKERS**: Backend API endpoints not available
**DEPENDENCIES**:
- ⏸️ Waiting: API specification from backend-dev agent
**ETA TO COMPLETION**: Unknown until blocker resolved
```

---

## Authorization Code Generation

### Purpose
Authorization codes ensure secure, traceable handoffs between agents:
- Prevent lost work
- Enable audit trail
- Confirm receipt
- Track lineage

### Code Format

```
HANDOFF-{AGENT_NAME}-{TIMESTAMP}-{HASH}
```

**Components**:
- `AGENT_NAME`: Reporting agent (e.g., frontend-dev)
- `TIMESTAMP`: Unix timestamp or ISO 8601
- `HASH`: First 8 chars of SHA-256 hash of deliverable

**Example**:
```
HANDOFF-frontend-dev-1699032450-a3f2c8b1
```

### Generation Algorithm

```python
import hashlib
import time

def generate_handoff_code(agent_name: str, deliverable: str) -> str:
    """Generate SITREP authorization code"""
    timestamp = int(time.time())
    hash_input = f"{agent_name}-{timestamp}-{deliverable}"
    hash_digest = hashlib.sha256(hash_input.encode()).hexdigest()[:8]
    return f"HANDOFF-{agent_name}-{timestamp}-{hash_digest}"
```

### Usage in SITREP

Only include HANDOFF code when deliverable is READY:

```markdown
**HANDOFF**: HANDOFF-frontend-dev-1699032450-a3f2c8b1

Deliverable: User authentication components (Login, Register, ResetPassword)
Location: /src/components/auth/
Status: Tested, documented, ready for integration
```

When NOT ready:
```markdown
**HANDOFF**: N/A
```

---

## Timing and Frequency Rules

### Regular Intervals
**Rule**: Report SITREP every 30 minutes during active work

**Rationale**:
- Coordinator needs real-time visibility
- 30 minutes allows course correction before issues escalate
- Too frequent (every 5 min) = overhead
- Too infrequent (every 2 hours) = lost visibility

**Implementation**:
```
T+0:00  - Start task, initial SITREP
T+0:30  - First interval SITREP
T+1:00  - Second interval SITREP
T+1:30  - Third interval SITREP
T+2:00  - Completion SITREP with HANDOFF code
```

### Trigger-Based Reporting

**IMMEDIATE SITREP Required** (don't wait for 30-minute interval):

1. **Status Change**: 🟢 → 🟡 or 🟡 → 🔴
2. **Blocker Encountered**: Any blocking issue
3. **Dependency Available**: Waited-for dependency now ready
4. **Deliverable Ready**: Work complete, ready for handoff
5. **Coordinator Request**: Explicit SITREP request

**Example**:
```markdown
🔴 IMMEDIATE SITREP (Blocker Encountered - T+0:42)

**STATUS**: 🔴 BLOCKED
**PROGRESS**: 55% complete (paused)
**BLOCKER**: API authentication endpoint returning 500 errors
**TRIGGER**: Blocker encountered at T+0:42, reporting immediately
```

### Silent Period Exception

**Rule**: If no work is being performed (waiting on dependency), silent period allowed with final SITREP before pause:

```markdown
**STATUS**: 🟡 AT RISK
**PROGRESS**: 30% complete (paused)
**DEPENDENCIES**:
- ⏸️ Waiting: Database schema from backend-dev agent
**NEXT SITREP**: When dependency available or T+2:00 (whichever first)
```

---

## Multi-Agent Coordination

### Wave Coordinator Pattern

When WAVE_COORDINATOR manages multiple sub-agents:

**Coordinator Request**:
```markdown
SITREP REQUEST to all Wave 2 agents:
- frontend-dev
- backend-dev
- database-dev

Format: Brief SITREP
Deadline: T+0:05
```

**Agent Responses**:
```markdown
🎯 **frontend-dev** | 🟢 | 70% | ETA: 1h
Blockers: NONE

🎯 **backend-dev** | 🟡 | 55% | ETA: 2h
Blockers: Performance optimization taking longer than expected

🎯 **database-dev** | 🔴 | 40% | ETA: Unknown
Blockers: Migration script failing on production schema
```

**Coordinator Analysis**:
- frontend-dev: ON TRACK, proceed
- backend-dev: AT RISK, monitor next SITREP
- database-dev: BLOCKED, escalate immediately

### Handoff Protocol

**Sender Agent**:
```markdown
**HANDOFF**: HANDOFF-backend-dev-1699032450-7f8a2c19

Deliverable: REST API endpoints for user management
Files:
- /api/users/create.ts
- /api/users/update.ts
- /api/users/delete.ts
- /api/users/list.ts
Tests: 47 passing
Documentation: /docs/api/users.md
Status: Ready for frontend integration
```

**Receiver Agent** (Acknowledgment):
```markdown
HANDOFF ACKNOWLEDGMENT

Received: HANDOFF-backend-dev-1699032450-7f8a2c19
Verified:
- ✅ All 4 endpoints present
- ✅ Tests passing
- ✅ Documentation complete
Status: Acknowledged, beginning integration
```

---

## Examples

### Example 1: On-Track Development

```markdown
═══════════════════════════════════════════════════════════
🎯 SITREP: frontend-dev
═══════════════════════════════════════════════════════════

**STATUS**: 🟢 ON TRACK
**PROGRESS**: 75% complete
**CURRENT TASK**: Implementing user profile component

**COMPLETED**:
- ✅ Login component with form validation
- ✅ Registration component with email verification
- ✅ Password reset flow
- ✅ Navigation routing

**IN PROGRESS**:
- 🔄 User profile component (60% complete)
- 🔄 Profile edit functionality (40% complete)

**BLOCKERS**: NONE

**DEPENDENCIES**:
- ✅ Ready: Backend user API (HANDOFF-backend-dev-1699030123-9a2f3c5e)
- ✅ Ready: Design system components

**ETA TO COMPLETION**: 1.5 hours
**NEXT CHECKPOINT**: User profile completion, ready for testing
**HANDOFF**: N/A (in progress)

═══════════════════════════════════════════════════════════
```

### Example 2: At-Risk Scenario

```markdown
═══════════════════════════════════════════════════════════
🎯 SITREP: database-dev
═══════════════════════════════════════════════════════════

**STATUS**: 🟡 AT RISK
**PROGRESS**: 60% complete
**CURRENT TASK**: Production database migration

**COMPLETED**:
- ✅ Schema design and review
- ✅ Migration scripts written
- ✅ Staging environment testing

**IN PROGRESS**:
- 🔄 Production migration execution (60% complete)
- 🔄 Data validation checks (30% complete)

**BLOCKERS**: Migration running slower than expected due to data volume

**DEPENDENCIES**:
- ✅ Ready: Backup completed
- ⏸️ Waiting: DBA review for performance optimization

**ETA TO COMPLETION**: 3 hours (originally 2 hours)
**NEXT CHECKPOINT**: Migration completion + validation
**HANDOFF**: N/A (at risk, may need coordinator intervention)

**NOTES**: Considering partitioning strategy to speed up remaining migration. Will report 🔴 BLOCKED if performance doesn't improve in next 30 minutes.

═══════════════════════════════════════════════════════════
```

### Example 3: Blocked Scenario (Immediate Report)

```markdown
═══════════════════════════════════════════════════════════
🎯 SITREP: backend-dev (IMMEDIATE - Blocker Encountered)
═══════════════════════════════════════════════════════════

**STATUS**: 🔴 BLOCKED
**PROGRESS**: 45% complete (PAUSED)
**CURRENT TASK**: Payment processing integration

**COMPLETED**:
- ✅ Payment gateway research
- ✅ API credential setup
- ✅ Test environment configuration

**IN PROGRESS**:
- 🔄 Payment endpoint implementation (PAUSED at 45%)

**BLOCKERS**:
Production API keys not available. Sandbox keys are working but cannot proceed to production integration without credentials. Payment gateway support team response time: 24-48 hours.

**DEPENDENCIES**:
- 🔴 BLOCKED: Production API keys from DevOps team
- ✅ Ready: Test environment

**ETA TO COMPLETION**: Unknown until blocker resolved
**NEXT CHECKPOINT**: Cannot proceed to next checkpoint
**HANDOFF**: N/A (blocked)

**COORDINATOR ACTION NEEDED**:
1. Escalate to DevOps lead for priority API key provisioning
2. OR: Switch to alternative payment gateway with available keys
3. OR: Proceed with mock integration, replace later (NOT RECOMMENDED)

**TRIGGER**: Blocker encountered at T+1:15, reporting immediately per protocol

═══════════════════════════════════════════════════════════
```

### Example 4: Handoff Ready

```markdown
═══════════════════════════════════════════════════════════
🎯 SITREP: frontend-dev
═══════════════════════════════════════════════════════════

**STATUS**: 🟢 ON TRACK (DELIVERABLE READY)
**PROGRESS**: 100% complete
**CURRENT TASK**: User authentication components (COMPLETED)

**COMPLETED**:
- ✅ Login component with form validation
- ✅ Registration component with email verification
- ✅ Password reset flow
- ✅ Session management
- ✅ Protected route handling
- ✅ Component unit tests (28 passing)
- ✅ Integration tests (12 passing)
- ✅ Documentation

**IN PROGRESS**: None

**BLOCKERS**: NONE

**DEPENDENCIES**: None required

**ETA TO COMPLETION**: COMPLETE
**NEXT CHECKPOINT**: Integration testing with backend
**HANDOFF**: HANDOFF-frontend-dev-1699034567-b8c4f2a9

**DELIVERABLE DETAILS**:
- **Location**: /src/components/auth/
- **Files**: Login.tsx, Register.tsx, PasswordReset.tsx, AuthContext.tsx
- **Tests**: /src/components/auth/__tests__/ (40 tests passing)
- **Documentation**: /docs/components/authentication.md
- **Status**: Code reviewed, tested, documented
- **Ready For**: Backend integration, E2E testing

**INTEGRATION NOTES**:
- Uses backend API endpoints: /api/auth/login, /api/auth/register, /api/auth/reset
- JWT tokens stored in httpOnly cookies
- Session refresh handled automatically
- Error handling follows design system patterns

═══════════════════════════════════════════════════════════
```

### Example 5: Brief SITREP for Coordinator Scan

```markdown
🎯 **frontend-dev** | 🟢 | 85% | ETA: 45min
Blockers: NONE

🎯 **backend-dev** | 🟢 | 90% | ETA: 30min
Blockers: NONE

🎯 **database-dev** | 🟡 | 70% | ETA: 1.5h
Blockers: Performance optimization needed

🎯 **test-dev** | 🟢 | 60% | ETA: 2h
Blockers: NONE

**Wave Status**: 4/4 agents reporting, 3 on track, 1 at risk
**Coordinator Decision**: Continue wave, monitor database-dev
```

---

## Success Criteria

A SITREP is compliant when it includes:

✅ **Status Code**: One of 🟢🟡🔴
✅ **Progress Percentage**: 0-100%
✅ **Current Task**: Specific task description
✅ **Completed Items**: List of finished work
✅ **Blockers**: Explicit statement (NONE or description)
✅ **ETA**: Time estimate to completion
✅ **Next Checkpoint**: Description of next milestone
✅ **Handoff Code**: When deliverable ready (or N/A)

Validation:
```python
def validate_sitrep(sitrep):
    assert sitrep["status"] in ["ON TRACK", "AT RISK", "BLOCKED"]
    assert 0 <= sitrep["progress"] <= 100
    assert "blockers" in sitrep
    assert sitrep["eta_hours"] > 0 or sitrep["status"] == "BLOCKED"
    if sitrep.get("handoff_ready"):
        assert sitrep["handoff_code"].startswith("HANDOFF-")
```

**Failure Modes to Avoid**:
- ❌ Informal narrative without structure
- ❌ Missing status code
- ❌ Qualitative progress ("almost done")
- ❌ No ETA or vague ETA ("soon")
- ❌ Unreported blockers
- ❌ Handoff without authorization code

---

## Advanced Situations (From Pressure Testing)

### Complex Situations Need MORE Structure

**Rule**: The more complex the situation, the MORE critical SITREP structure becomes.

**Multiple Blockers**: Use blocker priority levels
- **CRITICAL**: Blocks entire wave or system
- **HIGH**: Blocks dependent agents
- **MEDIUM**: Delays but doesn't block
- **LOW**: Can be deferred

**Multiple Agents**: Use wave summary format
- List each agent with status code
- Prioritize by critical path
- Identify blockers first
- Group by status (🔴 → 🟡 → 🟢)

**Example** (3 simultaneous blockers):
```markdown
**BLOCKERS** (3 active):

**BLOCKER 1** - Frontend Integration (Priority: CRITICAL)
- Agent: frontend-agent | Status: 🔴 BLOCKED at 85%
- Issue: API integration broken after deployment
- Action: Escalated to backend-agent

**BLOCKER 2** - Database Migration (Priority: HIGH)
- Agent: backend-agent | Status: 🔴 BLOCKED at 70%
- Issue: Production migration failing
- Action: Escalated to DBA team

**BLOCKER 3** - E2E Tests (Priority: MEDIUM)
- Agent: testing-agent | Status: 🟡 AT RISK at 40%
- Issue: Test timeouts, investigating infrastructure
```

### Communication Channel Independence

**Rule**: SITREP format is channel-independent. ANY medium gets structured reporting.

**Channel Guidelines**:
- **Email**: Use full SITREP format
- **Slack/Chat**: Use brief SITREP format
- **Project Tracker**: Use full SITREP format
- **Verbal/Voice**: "Status is 🟢 ON TRACK, 75% complete, ETA 1.5 hours, no blockers"
- **Any Channel**: Always include status code, progress, blockers, ETA

**Why**: Structured reporting ensures clarity regardless of medium. You can be FRIENDLY and STRUCTURED simultaneously.

**Example** (Slack):
```
[Informal Slack message - Still uses structure]

🎯 **backend-agent** | 🟢 | 75% | ETA: 1.5h
Blockers: NONE

Going great! Working on password reset endpoint.
Completed: Login, register, JWT refresh

Full SITREP in tracker: [link]
```

### Informal Requests Still Get Structured Responses

**Rule**: ANY status request gets SITREP format (full or brief), even casual check-ins.

**Informal requests that STILL get structure**:
- "How's it going?" → Brief SITREP
- "Quick check-in?" → Brief SITREP
- "Everything okay?" → Brief SITREP
- "Status?" → Brief SITREP
- "Just checking in..." → Brief SITREP

**Format**:
```markdown
Friendly + Structure = "Going great! 🎯 **agent** | 🟢 | 70% | ETA: 1.5h"
```

**Why**: Consistency enables coordination. Casual tone doesn't mean unstructured data.

### External Team Handoffs

**Rule**: Keep SITREP structure, provide translation if needed for non-Shannon teams.

**When handing off to external teams** (QA, DevOps, clients):
1. Use full SITREP format (maintains YOUR audit trail)
2. Include authorization code (provides traceability)
3. Add "FOR EXTERNAL TEAM" section with:
   - Status code translation
   - Authorization code explanation
   - Next steps in their workflow
   - Contact information

**Example**:
```markdown
**HANDOFF**: HANDOFF-frontend-agent-1699034567-b8c4f2a9

**FOR EXTERNAL QA TEAM**:
This deliverable is ready for quality assurance testing.

**Status Codes Translation**:
- 🟢 ON TRACK = Ready for testing
- 🟡 AT RISK = Issues found, in rework
- 🔴 BLOCKED = Cannot test until dependency available

**Authorization Code** (HANDOFF-frontend-agent-1699034567-b8c4f2a9):
This code confirms work is 100% complete and ready. Use it to track handoff in your system.

**Next Steps for QA**:
1. Review deliverable in /src/components/auth/
2. Run test suite: npm test
3. Execute manual testing (see /docs/qa-scenarios.md)
4. Report findings using your standard QA format
```

**Why**: Your SITREP is YOUR record. Provide context for them without abandoning structure.

### Velocity Honesty

**Rule**: Report actual status, not aspirational status. Coordinator needs REALITY to plan effectively.

**Behind Schedule**:
- ❌ Don't report 🟢 hoping to catch up
- ✅ Report 🟡 AT RISK with honest revised ETA
- ✅ Explain reason (complexity underestimated, unexpected blocker, etc.)
- ✅ Provide velocity data (expected vs actual progress rate)

**Velocity Analysis Template**:
```markdown
**ETA TO COMPLETION**: 2 hours (originally 2 hours, now T+3:00)
**ORIGINAL ESTIMATE**: 2 hours
**ACTUAL TIME SO FAR**: 3 hours
**REVISED ETA**: 2 additional hours (5 hours total)

**VELOCITY ANALYSIS**:
- Estimated: 2 hours total
- Actual: 60% complete at T+3:00
- Rate: 20% per hour (expected 50% per hour)
- Reason: Complexity underestimated by ~2.5x
```

**Why**:
- Hiding delays prevents proactive intervention
- Honest 🟡 enables resource reallocation
- "I'll catch up" often doesn't happen
- Transparent reporting builds trust
- Coordinator can plan ONLY with accurate data

**Example** (Behind schedule):
```markdown
**STATUS**: 🟡 AT RISK
**PROGRESS**: 60% complete

**NOTES**: I underestimated complexity. Reporting 🟡 AT RISK honestly
so coordinator can plan. Working to complete ASAP, but being transparent
about revised timeline.
```

---

## Common Pitfalls

### Pitfall 1: "Progress" Without Metrics
**Wrong**:
```
**PROGRESS**: Making good progress
```

**Right**:
```
**PROGRESS**: 65% complete
```

### Pitfall 2: Hidden Blockers
**Wrong**:
```
**BLOCKERS**: NONE
(but agent is actually waiting on dependency)
```

**Right**:
```
**BLOCKERS**: Waiting on API specification from backend team
**DEPENDENCIES**:
- ⏸️ Waiting: API spec from backend-dev agent
```

### Pitfall 3: Informal Handoff
**Wrong**:
```
**HANDOFF**: Yeah, the API is ready for you to use
```

**Right**:
```
**HANDOFF**: HANDOFF-backend-dev-1699034567-c9a2f4b8

Deliverable: REST API v1.0
Status: Tested, documented, ready
```

### Pitfall 4: Late Blocker Reporting
**Wrong**:
```
T+0:00 - Start task, STATUS: 🟢
T+0:30 - (blocker encountered, but don't report yet)
T+1:00 - Report STATUS: 🔴 (30 minutes too late)
```

**Right**:
```
T+0:00 - Start task, STATUS: 🟢
T+0:35 - IMMEDIATE SITREP: STATUS: 🔴 BLOCKED
T+1:00 - Regular SITREP: STATUS: still 🔴, update on resolution
```

### Pitfall 5: Assuming Visibility
**Wrong**:
```
(Agent completes work, commits to git, assumes coordinator knows)
```

**Right**:
```
**STATUS**: 🟢 ON TRACK (DELIVERABLE READY)
**HANDOFF**: HANDOFF-frontend-dev-1699034567-b8c4f2a9
(Explicit authorization code confirms readiness)
```

---

## Integration with Shannon

### With wave-orchestration
When WAVE_COORDINATOR orchestrates sub-agents, SITREP protocol enables:
- Real-time wave progress tracking
- Early blocker detection (🔴 status)
- Velocity calculations (progress over time)
- Checkpoint coordination (HANDOFF codes)

### With context-preservation
Save SITREPs as part of checkpoint for cross-session audit trail:

```markdown
shannon/waves/wave-2/sitreps/
├── frontend-dev-sitrep-1699034567.md
├── backend-dev-sitrep-1699034890.md
└── database-dev-sitrep-1699035123.md
```

### With functional-testing
Use SITREP structure to report test execution progress:

```markdown
**STATUS**: 🟢 ON TRACK
**PROGRESS**: 80% complete
**CURRENT TASK**: Running E2E test suite
**COMPLETED**:
- ✅ Unit tests (127 passing)
- ✅ Integration tests (45 passing)
**IN PROGRESS**:
- 🔄 E2E tests (12/15 passing)
```

---

## Testing This Skill

### Compliance Testing
After implementing this skill, verify agent behavior:

1. **Request informal status** → Agent MUST use SITREP format
2. **Request status without codes** → Agent MUST include 🟢🟡🔴
3. **Introduce blocker** → Agent MUST report immediately (trigger-based)
4. **Complete deliverable** → Agent MUST include HANDOFF authorization code
5. **Wait 35 minutes** → Agent MUST have reported at 30-minute mark

### Expected Compliance
- ✅ 100% of status updates use SITREP structure
- ✅ 100% include status code and progress %
- ✅ Blockers reported within 2 minutes (trigger-based)
- ✅ Authorization codes generated for all handoffs
- ✅ 30-minute intervals maintained during active work

### Failure Scenarios (Should Not Occur)
- ❌ Informal "making progress" updates
- ❌ Missing status codes
- ❌ Blockers reported 30+ minutes after occurring
- ❌ Handoffs without authorization codes
- ❌ Skipping format for "urgent" issues

---

## References

- **Origin**: Hummbl framework sitrep-coordinator pattern
- **Architecture**: Shannon V4 Architecture Design Doc, Section 8
- **Wave Coordination**: wave-orchestration skill
- **Context Preservation**: context-preservation skill

---

## Version History

- **v4.0.0**: Initial SITREP protocol implementation
  - Full + brief SITREP formats
  - Status codes (🟢🟡🔴)
  - Authorization code generation
  - 30-minute interval + trigger-based reporting
  - Anti-rationalization enforcement from baseline testing
