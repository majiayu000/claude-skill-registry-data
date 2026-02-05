---
name: longplan
description: Autonomous multi-step work with dual-reviewer supervision (1A2A workflow) and compound engineering principles
---

# Longplan (Port)

Use this when the user requests `/longplan`.

Follow `.claude/commands/longplan.md`. If a step requires tools not
available, note the adaptation and proceed with the closest equivalent.

## When to Use This vs Alternatives

| Your Situation | Use This | Not These |
|----------------|----------|-----------|
| Complex multi-step feature, 30+ min work | `/longplan` | `/ralph` (asset gen only) |
| Plan exists, stay in session, 5-10+ subagents | `/longplan` | `executing-plans` (new session) |
| Need plan + autonomous execution | `/longplan` | `subagent-driven-development` (plan required) |
| Debug/investigate first | Use `systematic-debugging` | Any execution skill |

**Relationship to other skills:**
- vs `ralph`: `ralph` is for batch asset generation (tiles, sprites). `/longplan` is for complex features.
- vs `executing-plans`: Use that for parallel session (separate window). `/longplan` stays in this session.
- vs `subagent-driven-development`: That skill executes existing plans with fresh subagent per task + 2 reviewers.

## Autonomous Work Mode (2A Phase)

**When working without human interaction during 2A phase:**

### Self-Checkpoints (Every 30 min or 5 file operations)
- [ ] Re-verify alignment with plan file
- [ ] Run quick tests if available
- [ ] Update progress tracking (checkpoint in plan file)
- [ ] Clear context if approaching token limit

### Blocker Response (Without Asking User)
1. **Try 2-3 alternative approaches** (5 min)
2. **Spawn MiniMax subagent** for research/sanity check (5 min)
3. **Try subagent suggestions** (5 min)
4. **Document and skip to next task** - circle back later
5. **ONLY after 30+ min of real attempts** → consider user escalation

### Quality Gates (Self-Enforced Before Declaring Done)
- [ ] All explicit success criteria from plan are met
- [ ] Time commitment fulfilled (check `.session_manifest.json`)
- [ ] Visual proof captured (screenshots for visual work)
- [ ] Narrative consistency verified (for story/dialogue work)
- [ ] Tests pass (if applicable)

**Remember:** Checkpointing (clearing context) is NOT stopping. It's managing token budget to continue working.

## Compound Engineering: Multi-Agent Delegation

**Core Philosophy:** Each unit of work should make future work easier.

This means every task should:
1. Solve the immediate problem
2. Make similar future problems easier to solve
3. Leave behind documentation, patterns, or tools that accelerate subsequent work

**Reference:** See `docs/agent-instructions/COMPOUND_ENGINEERING.md` for detailed compound engineering principles.

### Massive Parallel Delegation (5-15+ Subagents)

The key to velocity is parallelizing work across multiple subagents rather than doing everything sequentially. **The main agent's job is orchestration, not execution.**

**Launch 5-15+ parallel agents in a single message** by delegating independent subtasks:

```
Main Agent (Orchestrator):
  → Delegate to Agent 1: Research task A
  → Delegate to Agent 2: Research task B
  → Delegate to Agent 3: Implement feature X
  → Delegate to Agent 4: Implement feature Y
  → Delegate to Agent 5: Test integration
  → Delegate to Agent 6: Update documentation
  → Delegate to Agent 7: Generate assets
  → [Continue launching parallel agents...]
  → Aggregate results as they complete
  → Implement all changes in batch
```

### Context Management (2A Phase)

**CRITICAL for GLM-4.7:** Checkpoint based on FILE OPERATIONS, not time or todo count.

**Checkpoint triggers:**
1. **After 3 Write operations** (each returns ~1,500-2,000 tokens to context)
2. **After 5 total Read/Write operations** combined
3. **Before starting large batch operations** (reading/writing many files)

**Checkpoint procedure:**

1. **Update plan file with checkpoint:**
   - What's been completed (file list with line numbers)
   - Current blockers / pending items
   - Next 3-5 todos to work on
   - Critical state (quest flags, positions, etc.)

2. **Clear API context properly:**
   ```bash
   # Option 1: Proper context clear sequence
   /context clear
   /context status  # Verify it's actually cleared

   # Option 2: Start completely fresh (most reliable)
   - Close Kimi Code CLI completely
   - Reopen and start new session
   - Reference plan: @temp/autonomous-work-[task].md
   ```

3. **Resume 2A phase:**
   - Reference the plan file: @temp/autonomous-work-[task].md
   - Continue with 2A phase from where you left off

**Why this doesn't violate "keep working":**
- You're not stopping to ask questions
- You're not providing a summary to the user
- You're just clearing token bloat and resuming
- Work continues uninterrupted across sessions

**GLM-4.7 Specific Notes:**
- GLM-4.7 has ~200K context (vs Claude's 1M)
- File operations are the primary context consumers
- `/clear` command is BUGGY - use `/context clear` or restart session entirely
- Consider using native Claude model for very long file-heavy sessions (as an alternative with larger context)

**Example checkpoint format:**
```markdown
## Context Checkpoint [operation count]

### Operations Since Last Checkpoint
- Read: hermes_idle.tres, quest2_start.tres, daedalus_idle.tres (3)
- Write: act1_transformation_cutscene.tres, exile_cutscene.tres (2)
- Total: 5 operations → Checkpoint triggered

### Completed
- game/shared/resources/dialogues/act1_transformation_cutscene.tres - 64 lines
- game/shared/resources/dialogues/exile_cutscene.tres - 100 lines

### Current Todo
- Adding Daedalus mercy discussion dialogue

### Next 3 Todos
- Fix Aeetes character dialogue
- Add missing quest completion dialogues
- Implement missing choice branches

### Blockers
- None

### Critical State
- Quest 4 complete, met_daedalus flag set
- Next: act2_daedalus_mercy_discussion.tres
```

**Quick Reference Card:**

| Operation | Token Cost | Checkpoint After |
|-----------|------------|------------------|
| Read file | ~1,000-2,000 | Count toward 5 total |
| Write file | ~1,500-2,000 | **3 writes = checkpoint** |
| Edit file | ~500-1,000 | Count toward 5 total |
| Grep/Glob | ~100-500 | Negligible |
| TodoWrite | ~50-100 | Negligible |
| Bash (short) | ~100-500 | Negligible |

**When in doubt:** After creating 3 new dialogue files, ALWAYS checkpoint before continuing.

**When to delegate:**
- Research tasks (codebase exploration, pattern finding, web search)
- Implementation of independent features
- Testing and validation
- Documentation updates
- Asset generation (images, sprites, etc.)
- Any task that can run independently

**Delegation tools:**
- **MiniMax MCP** - Research, image analysis, web search, best practices
- **MCP godot-mcp** - Runtime game state inspection, scene tree analysis
- **Parallel execution** - Launch multiple agents simultaneously, don't wait for each to complete

**Delegation strategy (Wave approach):**
1. **Wave 1 (Parallel Research):** Launch 5-10 agents to explore different aspects of the problem
2. **Wave 2 (Parallel Implementation):** While research completes, launch 5-10 agents for independent implementations
3. **Wave 3 (Validation & Integration):** As implementations complete, launch agents to test and integrate
4. **Continuous aggregation:** Review results as they complete, don't wait for all to finish

**Real-world example (Seed Phase 8):**
- **22 placeholder assets** needed regeneration
- Launched **10+ parallel agents** via MiniMax MCP
- Each agent handled 2-3 related assets
- All completed in ~15 minutes vs. 2+ hours sequential
- Main agent orchestrated and integrated results

### Skip-Around Pattern for Stuck Tasks

**When stuck on a task:**

1. Document the challenge (1-2 lines in plan file)
2. Move to next todo item immediately
3. Circle back to stuck items after progress elsewhere
4. Try 2-3 alternatives before documenting as pending

**What counts as "stuck":**
- One approach failing (try alternatives)
- Slow operations (time ≠ stop)
- Uncertain about next step (make reasonable assumption, continue)
- Sequential advancement taking time (skip to next, circle back)

**What does NOT count as "stuck":**
- HARD STOPS (creating .md files, git push, editing CONSTITUTION.md)

### Autonomous Work (2A Phase) - Keep Working

**Core Rule:** Work continuously without stopping for summaries.

**DO:**
- Work through todos systematically
- Update plan file with quick notes
- Skip around stuck tasks
- Try 2-3 alternatives before documenting blockers
- Delegate to multiple subagents in parallel
- Continue working until blocked or complete

**DO NOT:**
- Stop to provide progress summaries
- Stop to "check in" with user
- Stop when one approach fails (try alternatives)
- Stop when work is slow or challenging
- Ask "should I continue?" (unless HARD STOP)

**Only stop for HARD STOPS:**
- Creating NEW .md files (not edits)
- Editing `.cursor/` directory
- Git push, force push, or branch operations
- Editing CONSTITUTION.md
- Actions outside approved scope
- Explicit user request to stop/pause

**EXCEPTION:** If blocked, MUST follow troubleshoot-and-continue protocol first:
1. Try 3 different approaches
2. Spawn MiniMax subagent for help
3. Try subagent suggestions
4. Document in plan file
5. THEN consider if still truly blocked

**CRITICAL: Completion Criteria Enforcement**

NEVER declare a task "complete" until ALL completion criteria are met:

```
BEFORE declaring done, verify:
□ All explicit success criteria from plan are satisfied
□ Visual quality gates passed (if applicable)
□ Narrative consistency verified (if applicable)
□ Time commitment fulfilled (if user specified duration)
□ No premature "good enough" declarations
```

**Visual Quality Gates (for game/assets):**
- Screenshots of actual rendered game MUST be captured
- Quality MUST surpass reference images (e.g., Harvest Moon comparison)
- NO declaring visual work done without visual proof

**Narrative Consistency Gates (for dialogue/story):**
- Dialogue MUST be checked against Storyline.md
- All choices and branches MUST align with narrative doc
- NO declaring narrative work done without cross-reference

**Time Commitment Enforcement:**
- If user says "work for 1 hour" → Work the FULL hour unless HARD STOP
- Track start time, do not stop early
- Set timer/alarm if needed to ensure full duration
- Early completion does NOT equal early stopping

**Compound Engineering Prevention:**
Document these anti-patterns to prevent recurrence:
- ❌ "I think this is good enough" → ✅ Criteria met + evidence
- ❌ "I'll stop early and summarize" → ✅ Continue until time/criteria complete
- ❌ "No blockers so I'll finish" → ✅ Finish criteria check first

**Todo Quote for Reinforcement:**
Append to each autonomous todo task:
"Remember: Skip around stuck tasks. Try 2-3 alternatives. Move to next todo. Circle back. Keep working. Do not make major repo changes unless approved. DO NOT STOP EARLY - complete all criteria first."

**MiniMax Subagent Quote (REQUIRED when blocked):**
"BLOCKED? Spawn MiniMax subagent BEFORE stopping: Task(subagent_name='minimax-mcp', prompt='Help with: [problem]. Return specific solutions.'). Try all suggestions before considering user interruption."

**Todo Quote for Reinforcement:**
Append to each autonomous todo task:
"Remember: Skip around stuck tasks. Try 2-3 alternatives. Move to next todo. Circle back. Keep working. Do not make major repo changes unless approved."
