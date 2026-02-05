---
name: Phase Documenter
description: Document completed development phases in IMPROVEMENTS.md with comprehensive summaries, lessons learned, patterns discovered, and Follow-up status. Ensures session work is captured for future reference and self-improvement tracking.
tags: [documentation, phase-completion, improvements, session-tracking]
version: 1.0.0
framework_version: 0.5.0+
---

# Phase Documenter Skill

**Purpose:** Structured documentation of completed development phases in IMPROVEMENTS.md.

**When to invoke:**
- End of development phase (Phase A complete, Phase B complete, etc.)
- Before committing major work
- User requests: "Document Phase X"
- Part of SESSION_END workflow for significant sessions

---

## Phase Documentation Template

### Required Information

**Gather before documenting:**
1. **Phase identifier** (e.g., "Phase 14a", "Phase A", "Session 7 Improvements")
2. **Phase goal/theme** (what was this phase about?)
3. **Tasks completed** (list of specific deliverables)
4. **Commits made** (git log for this phase)
5. **Lessons learned** (what did we discover?)
6. **Patterns emerged** (repeating behaviors or insights)
7. **Follow-ups** (unresolved items or future work)
8. **Self-improvement** (how did framework/process improve?)

---

## Documentation Workflow

### Step 1: Identify Phase Scope

**Ask:**
> "I'm documenting **[Phase X]**. Let me gather the details.
>
> **Phase goal:** [from roadmap or session plan]
> **Tasks completed:** [list from commit messages and todo]
> **Date range:** [start] to [end]
>
> Does this capture the scope accurately?"

### Step 2: Review Commits

**Command:**
```bash
git log --oneline --since="[start-date]" --until="[end-date]"
```

**Extract:**
- Commit messages and hashes
- Files changed
- Issues closed (#N references)

**Summarize:**
```
Commits for Phase [X]:
- [hash]: [message] (#N if present)
- [hash]: [message]
Total: [N] commits
```

### Step 3: Identify Lessons Learned

**Reflect on:**
- What worked well? (patterns to reinforce)
- What didn't work? (patterns to avoid)
- What was surprising? (unexpected discoveries)
- What would we do differently? (process improvements)

**Example lessons:**
- "Forceful language in prompts > passive suggestions"
- "Creating roadmap before implementation prevented scope creep"
- "Parallel phases (E+F) more efficient than sequential"
- "Real-world testing revealed assumption in theory"

### Step 4: Document Patterns

**Pattern types:**
- **Architectural:** Design decisions that proved valuable
- **Process:** Workflow improvements discovered
- **Communication:** Effective collaboration approaches
- **Technical:** Implementation techniques that worked

**Pattern format:**
```
Pattern: [Name]
Context: [When this applies]
Insight: [What we learned]
Application: [How to use this going forward]
```

**Example:**
```
Pattern: Intra-session Documentation Monitoring
Context: Writing substantial documentation (>200 lines)
Insight: Monitoring growth WHILE writing prevents bloat better than post-hoc compression
Application: Every ~200 lines, ask: "Should this be split? Is this essential?"
```

### Step 5: Track Follow-ups

**Follow-up categories:**
1. **Unresolved** - Known issues not yet addressed
2. **Deferred** - Intentionally postponed to later phase/version
3. **Monitoring** - Needs real-world validation or ongoing observation
4. **Resolved** - Completed in this phase (update previous Follow-ups)

**Follow-up format:**
```
Follow-up: [Description]
Status: [Unresolved / Deferred / Monitoring / Resolved]
Context: [Why this matters]
Next action: [What needs to happen]
Target: [Session N / v X.Y.Z / Ongoing]
```

**Example:**
```
Follow-up: Test MCP installation in real repository
Status: Monitoring
Context: Phase C designed MCP installation workflow, but only theoretical validation done
Next action: Phase G integration testing or first v0.5.0 user adoption
Target: Phase G (Session 9+)
```

### Step 6: Assess Self-Improvement

**Questions:**
1. Did this phase improve the framework? How?
2. Did this phase improve the process? How?
3. Did this phase improve collaboration? How?
4. What framework docs were updated based on phase learnings?
5. What meta-prompts changed due to this phase?

**Capture:**
- Documentation updates (which files changed to reflect learnings)
- Process refinements (what we'll do differently next time)
- Framework enhancements (new capabilities or patterns added)

---

## Output Format for IMPROVEMENTS.md

**Section to add:**

```markdown
### Phase [X]: [Theme] (Session [N], [Date])

**Goal:** [What this phase aimed to accomplish]

**Tasks Completed:**
1. [Task 1] - [Brief description]
2. [Task 2] - [Brief description]
3. [Task 3] - [Brief description]

**Commits:**
- [hash]: [message] (#issue if present)
- [hash]: [message]
- [hash]: [message]

**Key Deliverables:**
- [File/feature 1] - [Purpose]
- [File/feature 2] - [Purpose]

**Lessons Learned:**
1. **[Lesson 1 title]**
   - **Insight:** [What we discovered]
   - **Application:** [How to use going forward]

2. **[Lesson 2 title]**
   - **Insight:** [What we discovered]
   - **Application:** [How to use going forward]

**Patterns Discovered:**
1. **Pattern: [Name]**
   - **Context:** [When this applies]
   - **Insight:** [Core learning]
   - **Application:** [How to implement]

**Follow-ups:**
1. **[Follow-up 1]**
   - **Status:** [Unresolved / Deferred / Monitoring / Resolved]
   - **Context:** [Why this matters]
   - **Next action:** [What needs to happen]
   - **Target:** [When/where to address]

2. **[Follow-up 2]**
   - [Same format]

**Self-Improvement:**
- **Framework:** [How framework improved]
- **Process:** [How development process improved]
- **Collaboration:** [How human-AI collaboration improved]

**Updated Documentation:**
- [File 1] - [What changed and why]
- [File 2] - [What changed and why]

**Success Metrics:**
- [Metric 1]: [Achieved / Not achieved] - [Evidence]
- [Metric 2]: [Achieved / Not achieved] - [Evidence]

**Estimated Effort:** [X sessions/hours] | **Actual Effort:** [Y sessions/hours]

**Status:** ✅ **COMPLETE**

---
```

---

## Integration with Session Workflow

### Part of SESSION_END

**When phase completes, include in EOS:**

```
End of Session Checklist:
1. ✅ Work verified and tested
2. ✅ Changes committed and pushed
3. 📝 **Document Phase [X] in IMPROVEMENTS.md** [THIS SKILL]
4. ✅ Update session count
5. ✅ Self-improvement introspection
```

**Invoke skill:**
> "Document Phase [X] completion"

**Or use directly:**
> "I'm completing Phase [X]. Let me document this in IMPROVEMENTS.md using the Phase Documenter skill."

### Version Release Integration

**Pre-release documentation:**

When releasing version X.Y.Z, synthesize all phases for that version:

```markdown
## Version X.Y.Z: [Release Theme] (Released [Date])

**Theme:** [Overarching theme across all phases]

**Development Period:** Session [N] to Session [M] ([X] sessions)

**Phases Completed:**
- Phase A: [Theme] (Session [N])
- Phase B: [Theme] (Session [N+1])
- Phase C: [Theme] (Session [N+2])
...

**Major Deliverables:**
1. [Feature 1] - [Description]
2. [Feature 2] - [Description]

**Total Commits:** [N]

**Key Learnings:** [Top 3-5 learnings from all phases]

**Outstanding Follow-ups:** [List any unresolved items]

**See:** Individual phase documentation below for detailed breakdown.

---

[Individual phase sections follow]
```

---

## Quality Checks

**Before marking phase documentation complete, verify:**

- [ ] Phase goal clearly stated
- [ ] All tasks listed with brief descriptions
- [ ] All commits captured with messages
- [ ] At least 1-2 lessons learned documented
- [ ] Patterns identified (if any emerged)
- [ ] Follow-ups tracked with status and target
- [ ] Self-improvement assessment included
- [ ] Updated documentation listed
- [ ] Success metrics evaluated
- [ ] Effort estimate vs actual noted

**If any checklist item missing:**
- Ask user for clarification
- Review git log and task list again
- Reflect on what was learned (don't leave "None")

---

## Common Scenarios

### Scenario 1: Simple Phase (1-2 tasks)

**Lighter documentation acceptable:**
```markdown
### Phase [X]: [Task] (Session [N], [Date])

**Task:** [What was accomplished]

**Commit:** [hash]: [message]

**Lesson:** [Key insight if any]

**Status:** ✅ **COMPLETE**
```

### Scenario 2: Complex Phase (5+ tasks)

**Use full template with:**
- Detailed task breakdown
- Multiple commits grouped logically
- Several lessons and patterns
- Multiple Follow-ups
- Comprehensive self-improvement section

### Scenario 3: Failed/Abandoned Phase

**Document failures too:**
```markdown
### Phase [X]: [Attempted Goal] (Session [N], [Date])

**Goal:** [What we tried to accomplish]

**Why abandoned:** [Reasons for stopping]

**Lessons learned:** [What failure taught us]

**Pivot:** [What we're doing instead]

**Status:** ❌ **ABANDONED** (See Phase [Y] for alternative approach)
```

### Scenario 4: Multi-Session Phase

**Track progress across sessions:**
```markdown
### Phase [X]: [Theme] (Sessions [N]-[M], [Date range])

**Sessions:**
- Session [N]: [Subtasks]
- Session [N+1]: [Subtasks]
- Session [M]: [Subtasks]

[Rest of template as normal]

**Notes:** Multi-session phases should track cumulative progress and synthesize learnings across all sessions.
```

---

## Follow-up Management

**When documenting phase, check previous Follow-ups:**

```bash
grep -A 5 "Follow-up:" IMPROVEMENTS.md | grep "Status: Unresolved"
```

**Update resolved Follow-ups:**
```markdown
Follow-up: [Original description]
Status: ~~Unresolved~~ → **RESOLVED** in Phase [X]
Resolution: [How it was addressed]
```

**Create new Follow-ups:**
- Issues discovered during phase
- Real-world validation needed
- Future enhancements identified
- Technical debt accumulated

---

## Metrics & Tracking

**Track over time:**
1. **Velocity:** Tasks completed per session
2. **Accuracy:** Estimated vs actual effort
3. **Learning rate:** Lessons documented per phase
4. **Follow-up resolution:** How many resolved vs created
5. **Self-improvement:** Framework docs updated per phase

**Use for:**
- Estimating future phase effort
- Identifying bottlenecks
- Celebrating progress
- Planning releases

---

## Success Criteria

**Phase documentation is successful when:**
1. Future self can understand what was built and why
2. Lessons captured prevent repeating mistakes
3. Patterns documented enable reuse
4. Follow-ups tracked prevent items from being forgotten
5. Self-improvement progress visible over time

**Documentation failed if:**
- Future self confused about phase scope
- Lessons too generic ("worked hard")
- No patterns identified when patterns clearly existed
- Follow-ups vague or unmeasurable
- Self-improvement section empty or boilerplate

---

**Skill version:** 1.0.0
**Framework version:** 0.5.0+
**Last updated:** 2025-10-31
