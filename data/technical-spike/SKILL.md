---
name: technical-spike
description: Conduct objective-driven investigation to reduce uncertainty. Use when there's an unknown blocking estimation or implementation, when technical-pm identifies uncertainty, or when someone says "we need to investigate first".
allowed-tools: Read, Write, Glob, Grep, Bash, Task, WebSearch, WebFetch
---

# Technical Spike Skill

**Purpose:** Conduct objective-driven technical investigations to reduce uncertainty before committing to implementation.

**Philosophy:** A spike is finished when the objective is reached, NOT when a time limit expires. Spikes produce knowledge artifacts, not production code.

**When to use:**
- Technical feasibility is unknown ("Can this library handle 50MB files in under 200ms?")
- Behavioral requirements are unclear ("Should refunds work for partial orders?")
- Architecture needs validation ("Can we scale this pattern to 10k users?")
- Root cause of complex bug is unknown
- Before making architectural decisions (uncertainty reduction)

---

## Core Principles (Objective-Driven Framework)

### 1. The Completion Trigger
**A spike is finished the moment the specific objective is reached, not when a clock runs out.**

- If objective reached in 20 minutes → spike complete in 20 minutes
- If objective reached in 4 hours → spike complete in 4 hours
- If objective cannot be reached → document why, close spike

**Anti-pattern:** "We have 2 hours for this spike" (time-boxed approach)
**Correct pattern:** "We'll know we're done when we can successfully..." (objective-driven)

### 2. The "One-Question" Rule
**A spike must answer ONE high-level question.**

- If second question emerges → create second spike
- Prevents scope creep
- Ensures clear success criteria

**Example good question:** "Can WebSockets handle our real-time collaboration needs?"
**Example bad question:** "How should we build the entire real-time system?" (too broad, multiple questions)

### 3. The "Burn After Reading" Mandate
**Spike code must NEVER be merged into main branch.**

- Spike code is written to be read, learned from, and deleted
- Disposability enables speed
- Knowledge artifact (document) is the deliverable, not code

**Enforcement:**
- Create spike branches: `spike/topic-name`
- Never merge spike branches
- Delete branch after knowledge artifact created
- Or work in isolated directory and delete after

### 4. Zero Polishing
**No production quality needed.**

- No unit tests (unless testing IS the spike objective)
- No error handling for edge cases (unless that's what you're investigating)
- No styling (unless UI behavior is being spiked)
- Hardcode credentials, use fake data, skip validation

**Rationale:** Speed over quality. We're learning, not shipping.

---

## Spike Types

### Technical Spike (The "How")
**Focus:** Feasibility, architecture, performance

**Trigger phrases:**
- "I don't know if the technology CAN do this"
- "Will this approach scale?"
- "Can we integrate X with Y?"
- "Is this library fast enough?"

**Example questions:**
- "Can the XYZ library process a 50MB JSON file in under 200ms?"
- "Can we run Claude API calls in parallel without hitting rate limits?"
- "Will Qdrant handle 100k vectors with acceptable query time?"

### Functional Spike (The "What")
**Focus:** User flow, logic, requirement clarity

**Trigger phrases:**
- "I don't know how the system SHOULD behave"
- "What's the right user experience?"
- "How should this edge case work?"

**Example questions:**
- "Should multi-step vs single-page form feel more intuitive for our users?"
- "How should refund flow behave for partial orders?"
- "What happens when user tries to delete account with active subscription?"

---

## Expected Outcomes (Knowledge Artifacts)

Every spike must produce ONE of these:

### 1. The Verdict
**Format:** Definitive "Yes, this works" or "No, this is a dead end"

**Example:**
> "✅ YES - Qdrant can handle 100k vectors with <50ms query time on our VPS specs"

> "❌ NO - WebSockets disconnect every 30 seconds behind AWS ALB (need sticky sessions or different approach)"

### 2. The Proof of Concept (PoC)
**Format:** Screen recording, demo, or code snippet showing "it works"

**Example:**
> "✅ Working prototype: Users can drag-drop files, see upload progress, get confirmation. See recording: spike-file-upload.mov. Key insight: Need to chunk large files (>10MB) or upload times out."

### 3. The Architecture Draft
**Format:** Simple diagram or list of required components

**Example:**
> "✅ Architecture sketch: Need 3 components: (1) Upload service with chunking, (2) Background processor queue, (3) Notification system. Draft in spike-architecture.png"

### 4. The Bug Root-Cause
**Format:** Clear explanation of WHY complex error happens

**Example:**
> "✅ Root cause identified: Race condition between React state update and WebSocket message. Happens when user sends message during reconnection. Need mutex or message queue."

---

## Non-Goals (Explicitly Forbidden)

Spikes must NOT attempt to:

1. **Refine estimates** - Spikes remove "I don't know", but don't size work (that's planning)
2. **Produce production code** - If code is good enough to merge, it was a Feature Task in disguise
3. **Create user documentation** - Spikes produce internal knowledge only
4. **Make final decisions** - Spike provides data; team/architect makes decision

**Test:** If someone asks "Can we ship this?" and answer is yes → it's not a spike, it's a feature.

---

## Spike Protocol Template

**Fill in before starting spike (30 seconds):**

```markdown
## Spike: [One-sentence question]

**Question:** [e.g., Can we use WebSockets for real-time updates?]
**Type:** Technical | Functional
**Success Criteria:** [e.g., I have a local script that successfully echoes a message back from the server.]
**Code Strategy:** [e.g., Hardcoding all credentials; no error handling; single file script.]
**Next Step:** [e.g., Share snippet in spike doc and delete throwaway code.]
```

**Example:**
```markdown
## Spike: Can Qdrant handle 100k vectors efficiently?

**Question:** Will Qdrant perform well with 100k atomic notes on our VPS specs?
**Type:** Technical
**Success Criteria:** Query time <50ms for semantic search with 100k points loaded
**Code Strategy:** Load fake data, skip authentication, hardcode config, single Python script
**Next Step:** Document query times in spike doc, delete test data, close spike
```

---

## Spike Output Format

**Location:** `00 Inbox/spikes/spike-YYYY-MM-DD-topic.md`

**Template:**

```markdown
# Technical Spike: [Question]

**Type:** Technical | Functional
**Started:** [timestamp]
**Completed:** [timestamp]
**Duration:** [actual time spent]
**Objective reached:** Yes | No (with explanation)

## Question

[The one question we were trying to answer]

## Success Criteria

[What would prove the answer]

## Findings

[What we discovered - be specific, include numbers/metrics where relevant]

## Knowledge Artifact

**Type:** Verdict | PoC | Architecture Draft | Root Cause

[The concrete output from this spike]

## Recommendation

**Category:** Simple change | Moderate effort | Complex/Architectural | Dead end

[Simple next-step recommendation - NOT a detailed plan]

**If pursuing:** [Suggest creating ADR or development plan]
**If abandoning:** [Explain why, suggest alternative]

## What We Still Don't Know

[Any remaining unknowns - may trigger follow-up spike]

[If empty: "All unknowns resolved for this question."]

## Throwaway Code Location

[One of these:]
- "Deleted"
- "Branch: spike/topic-name (DO NOT MERGE)"
- "Directory: /tmp/spike-name (deleted)"
- "No code (research-only spike)"
```

---

## Workflow

### 1. Define Spike Objective
- State as ONE question
- Classify as Technical or Functional
- Define clear success criteria (what proves the answer)

### 2. Plan Throwaway Code Strategy
- Where will code live? (branch, /tmp, isolated directory)
- What can be hardcoded? (credentials, config, fake data)
- What can be skipped? (tests, error handling, edge cases)

### 3. Execute Spike
- Build minimum code to answer question
- Take notes as you learn
- Stop immediately when objective reached (or determined unreachable)

### 4. Document Knowledge Artifact
- Write spike document using template
- Include verdict, metrics, or architecture draft
- State what we now know vs still don't know

### 5. Clean Up Throwaway Code
- Delete spike branch or temporary files
- Preserve only the knowledge artifact (markdown doc)
- Update spike doc with "Code deleted" confirmation

### 6. Make Recommendation
- Simple change → implement directly
- Moderate effort → create development plan
- Complex/Architectural → create ADR, then plan
- Dead end → document why, suggest alternatives

---

## Integration with Decision-Making

**Typical flow:**

```
Uncertainty Identified
    ↓
Technical Spike (this skill)
    ↓
Knowledge Artifact Created
    ↓
Decision Point
    ├─→ Simple change? → Implement directly
    ├─→ Architectural? → Create ADR (write-adr skill)
    ├─→ Requires plan? → Create plan (create-plan skill)
    └─→ Dead end? → Document and move on
```

**Example:**
1. Technical PM identifies: "We don't know if Qdrant can scale to 100k vectors"
2. Spike conducted: Load test with fake data
3. Knowledge artifact: "Yes, <50ms query time confirmed"
4. Solutions Architect: Create ADR-003 documenting Qdrant choice
5. Development: Create PLAN-2025-XXX to implement Qdrant integration

---

## Quality Checklist

Before closing spike, verify:

- [ ] **One question answered** - Not multiple questions
- [ ] **Success criteria met** - Or documented why unreachable
- [ ] **Knowledge artifact created** - Verdict, PoC, draft, or root cause
- [ ] **Recommendation provided** - Clear next step
- [ ] **Throwaway code deleted** - Or clearly marked as disposable
- [ ] **Unknowns documented** - What we still don't know (if anything)
- [ ] **Spike doc complete** - All template sections filled

---

## Examples

### Example 1: Performance Spike

**Question:** Can Qdrant handle 100k atomic notes with <50ms query time?

**Type:** Technical

**Findings:**
- Loaded 100k fake notes (3072-dim embeddings)
- Average query time: 23ms (p95: 41ms)
- Memory usage: 2.1GB
- CPU: <5% during queries

**Verdict:** ✅ YES - Qdrant performs well beyond our needs

**Recommendation:** Simple - proceed with Qdrant integration. Create ADR-003 to document choice.

**Code:** Deleted after knowledge artifact created

---

### Example 2: UX Functional Spike

**Question:** Should account deletion be one-click or require confirmation flow?

**Type:** Functional

**Findings:**
- Built both flows in local branch
- One-click: Fast but risky (accidental deletion concern)
- Confirmation flow: Safer, shows what will be deleted
- Tested with 2 users: Both preferred confirmation (clarity on consequences)

**Verdict:** ✅ Confirmation flow preferred

**Recommendation:** Moderate - create PLAN-2025-XXX for account deletion flow with confirmation modal showing:
- What data will be deleted
- Irreversibility warning
- Final confirmation button

**Code:** Branch spike/account-deletion (DO NOT MERGE)

---

### Example 3: Technical Feasibility (Dead End)

**Question:** Can we use SQLite with async Python for concurrent writes?

**Type:** Technical

**Findings:**
- SQLite locks entire database for writes
- Concurrent write attempts fail with "database is locked" error
- Read-heavy workloads OK, write-heavy fails
- Our use case: 50+ concurrent users writing data

**Verdict:** ❌ NO - SQLite won't work for our multi-user write pattern

**Recommendation:** Dead end - switch to PostgreSQL (supports concurrent writes). Create ADR-005 to document database choice.

**Alternative considered:** Use SQLite with write-ahead logging (WAL), but testing showed still not sufficient for 50+ writers.

**Code:** Deleted

---

## Anti-Patterns to Avoid

1. **Time-Boxing Instead of Objective-Driven**
   - ❌ "We have 2 hours for this spike"
   - ✅ "We'll know we're done when we can successfully..."

2. **Polishing Spike Code**
   - ❌ Adding unit tests, error handling, documentation to throwaway code
   - ✅ Minimal code to prove the concept

3. **Merging Spike Code**
   - ❌ "This spike code is pretty good, let's just merge it"
   - ✅ "Spike proves it works. Now delete and implement properly with tests."

4. **Multi-Question Spikes**
   - ❌ "Let's spike authentication, authorization, and session management"
   - ✅ "Let's spike authentication approach" (separate spikes for auth and sessions)

5. **Decision-Making in Spike**
   - ❌ "Spike showed both work, so I chose Option A"
   - ✅ "Spike showed both work. Here's data. Solutions Architect will decide."

---

## Integration Points

**This skill is used by:**
- `technical-pm` agent - Identifies uncertainties blocking estimation
- `solutions-architect` agent - Reduces uncertainty before architectural decisions
- Manual `/spike` command - User-initiated investigation

**This skill spawns:**
- `artificial-shadow-dev` - For implementation spikes
- `hybrid-db-architect` - For database spikes
- No agents for research-only spikes

**This skill outputs to:**
- `write-adr` skill - When spike leads to architectural decision
- `create-plan` skill - When spike shows moderate/complex work needed

---

## Continuous Improvement

Update this skill when:
- New spike patterns emerge
- Quality issues identified in spike outputs
- Framework principles need refinement
- Integration patterns change

Document significant changes in repository CLAUDE.md.
