---
name: wolf-context-management
description: Phase-aware context management for coder agents to prevent token bloat through checkpoint/restore pattern
version: 1.0.0
triggers:
  - context bloat
  - checkpoint progress
  - summarize exploration
  - clean context
  - compact context
  - too much context
category: development-workflow
integration: wolf-roles (coder-agent, research-agent, qa-agent)
---

# Wolf Context Management

**Purpose**: Prevent context bloat in agent workflows through phase-aware checkpointing and compaction.

**Problem Solved**: Coder agents accumulate 10,000-40,000 tokens of irrelevant context during exploration (Glob/Grep/Read operations). Once relevant files are found, non-useful search results persist, wasting context capacity.

**Solution**: Phase-aware checkpoint/restore pattern that creates durable artifacts (`.claude/context/*.md`) at workflow transitions, enabling clean context compaction while preserving essential information.

---

## When to Use This Skill

### Automatic Triggers (Agent Should Recognize)

✅ **After Exploration Phase**
- You've found the relevant files for your task
- Context contains many Read/Grep results from files you won't modify
- Ready to start implementation (TDD workflow)

✅ **After Implementation Phase**
- Tests are passing
- You have multiple test run outputs in context
- Ready to collect evidence for verification

✅ **Before Review Handoff**
- All evidence collected
- Context contains implementation details + exploration history
- Ready to hand off to code-reviewer-agent

### Manual Triggers (User Can Request)

✅ **Context Feels Bloated**
- Token budget warnings appearing
- Conversation history is long
- Agent performance degrading (slow responses)

✅ **Task Phase Transition**
- Switching from one archetype to another
- Moving from research to implementation
- Preparing for major milestone (demo, release)

---

## The 3-Step Workflow (MANDATORY)

### Step 1: Identify Compaction Type ⚠️

**REQUIRED**: Determine which phase transition you're at.

**Options**:

**A. Exploration → Implementation**
- **When**: Found relevant files, ready to code
- **Checkpoint Type**: Exploration
- **What to Keep**: Relevant file list, key findings, architecture understanding
- **What to Discard**: Irrelevant file contents, failed searches, full doc pages

**B. Implementation → Verification**
- **When**: Tests passing, ready for evidence collection
- **Checkpoint Type**: Implementation
- **What to Keep**: Changes summary, final test results, key decisions
- **What to Discard**: Failed test runs, debugging logs, intermediate attempts

**C. Verification → Handoff**
- **When**: All evidence collected, ready for review
- **Checkpoint Type**: Verification
- **What to Keep**: Evidence summary, quality metrics, PR checklist
- **What to Discard**: Raw test output, detailed logs, full CI dumps

**D. Reference Compaction** (anytime)
- **When**: Searched docs/web, found answer, don't need full content anymore
- **Checkpoint Type**: Reference
- **What to Keep**: Key findings, links, one-sentence summaries
- **What to Discard**: Full documentation pages, Stack Overflow threads, examples

---

### Step 2: Create Checkpoint File ⚠️ (BLOCKING)

**REQUIRED**: Write checkpoint to `.claude/context/` **BEFORE** requesting compaction.

#### Create Directory (First Time)

```bash
mkdir -p .claude/context
```

#### Choose Checkpoint Template

Use the appropriate template from `wolf-context-management/templates/`:

- **Exploration**: `exploration-checkpoint-template.md`
- **Implementation**: `implementation-checkpoint-template.md`
- **Verification**: `verification-checkpoint-template.md`
- **Reference**: Create simple markdown with key findings

#### Naming Convention

**Format**: `{phase}-{YYYY-MM-DD}-{feature-slug}.md`

**Examples**:
```
.claude/context/exploration-2025-01-14-jwt-refresh.md
.claude/context/implementation-2025-01-14-jwt-refresh.md
.claude/context/verification-2025-01-14-jwt-refresh.md
.claude/context/reference-2025-01-14-react-patterns.md
```

#### Write Checkpoint

1. **Read the template** for your phase (exploration/implementation/verification)
2. **Fill in all sections** with context-specific details
3. **Verify completeness**: Could you resume work from this checkpoint alone?
4. **Write file** using Write tool

**Critical**: Checkpoint must be self-contained. Assume you're reading it in a fresh session with zero prior context.

---

### Step 3: Verify Checkpoint and Request Compact ⚠️

**REQUIRED**: Do NOT compact without checkpoint artifact.

#### Verification Checklist

Before requesting compaction:

- [ ] Checkpoint file created in `.claude/context/`
- [ ] Checkpoint filename follows naming convention
- [ ] All template sections filled in (no placeholders like `{TODO}`)
- [ ] Checkpoint is self-contained (can resume work from it)
- [ ] Essential context preserved:
  - [ ] Relevant files identified with line ranges
  - [ ] Key decisions documented with rationale
  - [ ] Architecture/patterns understood and summarized
  - [ ] Acceptance criteria or requirements linked

#### Request User Approval

**MANDATORY**: Show checkpoint path and request review:

```markdown
Context checkpoint created: .claude/context/{phase}-{date}-{feature}.md

Ready to compact context. This will:
- ✅ Keep: Wolf framework context (principles, archetype, governance)
- ✅ Keep: Current task requirements and acceptance criteria
- ✅ Keep: Checkpoint file reference
- ❌ Discard: {X} file contents from exploration
- ❌ Discard: {Y} search results
- ❌ Discard: {Z} test run outputs

Review checkpoint at: .claude/context/{filename}
Approve compact? (User can review file first)
```

#### Execute Compaction

Once user approves:

```bash
# Use Claude Code's manual compact command
/compact preserve checkpoints in .claude/context/ and Wolf framework context
```

**Alternative** (if auto-compact at 95% is acceptable):
- Let auto-compact trigger naturally
- Checkpoint ensures essential context is preserved in artifact

---

## Checkpoint Templates

### Exploration Checkpoint Template

Use `wolf-context-management/templates/exploration-checkpoint-template.md`:

```markdown
# Exploration Summary - {FEATURE_NAME}

**Date**: {YYYY-MM-DD}
**Phase**: Exploration → Implementation
**Archetype**: {archetype-name}

## Relevant Files Identified

1. **`{file-path}`** (lines {start}-{end})
   - {What this file does}
   - {Why it's relevant}
   - {Key patterns or APIs}

2. **`{file-path}`** (lines {start}-{end})
   - {Description}

## Key Findings

- **Current State**: {How feature currently works}
- **Gap Identified**: {What's missing or broken}
- **Pattern to Follow**: {Existing patterns in codebase}
- **Testing Strategy**: {How to test this}

## Architecture Understanding

{Brief description of relevant architecture, can use diagrams}

## Ready for Implementation

**Files to Modify**:
- `{file}` - {what changes}

**Tests to Add**:
- Test: {description}

**Patterns to Follow**:
- {Pattern 1}

## Wolf Framework Context

**Archetype**: {archetype-name}
**Lenses**: {lenses if any}
**Acceptance Criteria**:
- [ ] {criterion 1}
- [ ] {criterion 2}

**Exploration Complete**: Ready for TDD implementation.
```

### Implementation Checkpoint Template

Use `wolf-context-management/templates/implementation-checkpoint-template.md`:

```markdown
# Implementation Summary - {FEATURE_NAME}

**Date**: {YYYY-MM-DD}
**Phase**: Implementation → Verification
**Archetype**: {archetype-name}

## Changes Implemented

### Modified Files

1. **`{file-path}`** (+{lines added}, -{lines removed})
   - {Summary of changes}
   - {Key decisions made}

## Test Results

**Final Test Run**:
```
{Paste final test output - summary only}
```

✅ {X} tests passing
❌ {Y} tests failing (if any)
✅ Coverage: {percentage}
✅ Linting: {result}

## Key Decisions

1. **{Decision topic}**: {What you decided}
   - Rationale: {Why}

2. **{Decision topic}**: {What you decided}
   - Rationale: {Why}

## Lenses Applied (if any)

- [x] {Lens name}: {How you applied it}

## Ready for Verification

**Tests passing**: Yes/No
**Documentation updated**: Yes/No
**Journal created**: Yes/No
**Evidence collected**: {Summary}

**Next**: Load wolf-verification, collect evidence.
```

### Verification Checkpoint Template

Use `wolf-context-management/templates/verification-checkpoint-template.md`:

```markdown
# Verification Summary - {FEATURE_NAME}

**Date**: {YYYY-MM-DD}
**Phase**: Verification → Handoff
**Archetype**: {archetype-name}

## Evidence Collected

**Tests**: {Summary}
**Coverage**: {percentage}
**Linting**: {result}
**CI Status**: {passing/failing}

## Quality Metrics

**Performance** (if applicable):
- Baseline: {metric}
- Post-change: {metric}
- Impact: {+/-X%}

**Security** (if applicable):
- Vulnerabilities: {count by severity}
- Threat model: {completed/not-required}

## Acceptance Criteria Status

- [x] {Criterion 1} - ✅ Met
- [x] {Criterion 2} - ✅ Met
- [ ] {Criterion 3} - ⏳ Pending

## Handoff Checklist

- [x] All tests passing
- [x] Documentation updated
- [x] Journal entry created
- [x] Evidence collected
- [ ] PR created
- [ ] Review requested from code-reviewer-agent

## PR Summary (Draft)

**Title**: {PR title following wolf-governance format}

**Changes**:
- {Change 1}
- {Change 2}

**Testing**:
- {Test summary}

**Evidence**:
- Tests: {link or summary}
- Journal: {path}

**Ready for Review**: Yes
```

---

## Red Flags - STOP 🛑

### ❌ **"I'll compact now and checkpoint later"**
**FORBIDDEN**. Checkpoint is the safety net. Create it BEFORE compacting.

**Why it fails**: Once context is compacted, you can't reconstruct what was important. Checkpoint ensures essential details aren't lost.

**Solution**: Always checkpoint first. If urgent, create a quick checkpoint (can refine later).

---

### ❌ **"Compacting before finding the solution"**
**NO**. Only compact completed phases, not active exploration.

**Why it fails**: You might need that "irrelevant" file later. Only compact when confident you've found what you need.

**Solution**: Finish the phase (find files, tests pass, evidence collected), THEN checkpoint and compact.

---

### ❌ **"Checkpoint is too much work, just compact"**
**STOP**. Checkpoint takes 5 minutes, saves hours if you need to recover context.

**Why it fails**: Without checkpoint, compaction is lossy. You might lose critical understanding that forces re-exploration.

**Solution**: Use templates (fill in blanks), don't write free-form. Time-box to 5 minutes.

---

### ❌ **"Checkpoint missing essential info"**
**FORBIDDEN**. Test: Could you resume work from this checkpoint alone in a fresh session?

**Why it fails**: Incomplete checkpoints defeat the purpose. You'll need to re-explore anyway.

**Solution**: Review checklist:
- [ ] Relevant files identified with line ranges?
- [ ] Key decisions documented with rationale?
- [ ] Architecture/patterns understood?
- [ ] Acceptance criteria linked?

---

### ❌ **"Checkpoint has placeholders like {TODO}"**
**NO**. Checkpoint must be complete and self-contained.

**Why it fails**: Future you won't know what to fill in. Placeholders render checkpoint useless.

**Solution**: If you don't know something, write "Unknown: {why unknown}" or "Not applicable: {why}".

---

## Integration with Wolf Framework

### Alignment with Wolf Principles

**Principle #1: Artifact-First Development** ✅
- Checkpoints are durable artifacts (`.claude/context/*.md`)
- Can commit to git, review, version
- Persistent across sessions

**Principle #5: Evidence-Based Decision Making** ✅
- Checkpoints capture evidence of exploration/implementation
- Compaction decisions based on observable phase transitions
- Auditable (can review checkpoint quality)

**Principle #6: Self-Improving Systems** ✅
- Agents learn to create better checkpoints over time
- Can measure token savings (before/after metrics)
- Feedback loop: better checkpoints → better compaction

**Principle #9: Incremental Value Delivery** ✅
- Checkpoints align with 2-8 hour work increments
- Each phase produces compacted summary
- Enables clean handoffs between agents

### Integration with Wolf Workflows

**Coder-Agent Workflow**:
```
wolf-archetypes → coder-agent → wolf-context-management → superpowers:test-driven-development
                                        ↓ (at phase transitions)
                                Create checkpoint, compact context
```

**When to Use in Coder Workflow**:
1. **After exploration** (found files) → Checkpoint before TDD
2. **After implementation** (tests pass) → Checkpoint before verification
3. **Before review** (evidence collected) → Checkpoint before handoff

**Multi-Agent Workflow**:
```
pm-agent → research-agent → architect-lens-agent → coder-agent → qa-agent → code-reviewer-agent
                 ↓               ↓                      ↓            ↓
            checkpoint      checkpoint           checkpoint   checkpoint
```

Each agent creates checkpoint at handoff, next agent has clean context.

---

## Usage Examples

### Example 1: Exploration → Implementation

**Scenario**: Coder agent searched for auth-related code, read 15 files, ready to implement JWT refresh.

**Before Compaction**:
- Context: 35,000 tokens
- Contents: 15 file reads, 50+ grep results, 3 doc pages, Wolf framework

**Agent Actions**:
1. ✅ Recognizes phase transition (found files, ready to code)
2. ✅ Creates `exploration-2025-01-14-jwt-refresh.md` checkpoint
3. ✅ Checkpoint contains: 3 relevant files with line ranges, key findings, architecture understanding
4. ✅ Requests user approval: "Review checkpoint, ready to compact"
5. ✅ User approves: `/compact preserve checkpoints in .claude/context/`

**After Compaction**:
- Context: 8,000 tokens (77% reduction)
- Contents: Checkpoint summary, Wolf framework, current task
- Lost: 12 irrelevant file contents, grep dumps, doc pages
- Preserved: Everything needed in checkpoint artifact

**Result**: Clean context for TDD implementation, token budget extended.

---

### Example 2: Implementation → Verification

**Scenario**: Tests passing after 8 test runs, ready for evidence collection.

**Before Compaction**:
- Context: 42,000 tokens
- Contents: 8 test runs (7 failures, 1 pass), debugging logs, implementation iterations

**Agent Actions**:
1. ✅ Recognizes phase transition (tests pass, ready for verification)
2. ✅ Creates `implementation-2025-01-14-jwt-refresh.md` checkpoint
3. ✅ Checkpoint contains: Final test results, changes summary, key decisions
4. ✅ Requests compact
5. ✅ Compaction removes: 7 failed test runs, debugging logs, intermediate code versions

**After Compaction**:
- Context: 12,000 tokens (71% reduction)
- Contents: Final implementation, checkpoint summary, Wolf framework
- Ready for verification phase with clean context

---

### Example 3: Reference Compaction

**Scenario**: Searched React documentation for useEffect patterns, found answer.

**Before Compaction**:
- Context: 18,000 tokens
- Contents: 3 doc pages, 2 Stack Overflow threads, 5 code examples

**Agent Actions**:
1. ✅ Recognizes reference bloat (found answer, don't need full docs)
2. ✅ Creates `reference-2025-01-14-react-useeffect.md` checkpoint
3. ✅ Checkpoint contains: Key finding (cleanup function pattern), link to docs, one example
4. ✅ Compacts context

**After Compaction**:
- Context: 5,000 tokens (72% reduction)
- Contents: Checkpoint with key finding, implementation continues

---

## Measuring Success

### Token Efficiency Metrics

**Baseline** (no context management):
- Average coder-agent session: 80,000-120,000 tokens
- Exploration phase: 30,000 tokens (files + searches)
- Implementation phase: 40,000 tokens (test runs + iterations)
- Verification phase: 20,000 tokens (evidence)

**Target** (with context management):
- Exploration checkpoint: -70% (30k → 9k tokens)
- Implementation checkpoint: -60% (40k → 16k tokens)
- Verification checkpoint: -50% (20k → 10k tokens)
- **Total savings: 30-50% per session**

### Quality Metrics

**Validate**:
- ✅ Code quality unchanged (test coverage, review feedback)
- ✅ No increase in rework (agent didn't lose critical context)
- ✅ Faster review cycles (cleaner context = clearer handoff)

**Red Flags**:
- ❌ Agent re-exploring already-explored files (checkpoint incomplete)
- ❌ Forgotten decisions causing rework (decisions not documented)
- ❌ Review delays due to missing context (verification checkpoint inadequate)

---

## After Using This Skill

### What Changed

- ✅ **Context compacted**: Removed irrelevant files, searches, old test runs
- ✅ **Checkpoint artifact created**: Essential context preserved in `.claude/context/`
- ✅ **Token budget extended**: 30-50% more capacity for current phase
- ✅ **Clean handoffs**: Next agent/phase starts with focused context

### What's Preserved

- ✅ **Essential context**: In checkpoint file (can read back if needed)
- ✅ **Wolf framework**: Principles, archetype, governance remain in context
- ✅ **Current task**: Requirements and acceptance criteria unchanged
- ✅ **Audit trail**: Checkpoint is artifact, can commit to git

### Next Steps

**After Exploration Checkpoint**:
- **RECOMMENDED NEXT SKILL**: superpowers:test-driven-development
- Start TDD workflow with clean context
- Reference checkpoint if need to recall exploration findings

**After Implementation Checkpoint**:
- **RECOMMENDED NEXT SKILL**: superpowers:verification-before-completion
- Collect evidence with focused context
- Reference checkpoint for changes summary

**After Verification Checkpoint**:
- **REQUIRED NEXT STEP**: Create PR, request code-reviewer-agent review
- Handoff to code-reviewer-agent with clean context
- Code-reviewer reads verification checkpoint for context

---

## Troubleshooting

### Issue: "I don't know which phase I'm in"

**Symptom**: Uncertain whether to create exploration, implementation, or verification checkpoint.

**Diagnosis**:
- Check coder-agent template: Which phase checklist are you on?
- Ask: "Have I found the files?" → If yes, past exploration
- Ask: "Are tests passing?" → If yes, past implementation
- Ask: "Is evidence collected?" → If yes, ready for handoff

**Solution**: When in doubt, create checkpoint anyway. Better to have extra checkpoints than bloated context.

---

### Issue: "Checkpoint feels incomplete"

**Symptom**: Reviewing checkpoint, feels like something is missing.

**Diagnosis**: Use the "fresh session" test: Could you resume work from this checkpoint alone, with zero prior context?

**Solution**:
- Add missing context to checkpoint (files, decisions, understanding)
- Use template sections as guide (all sections required)
- If still uncertain, ask user: "Does this checkpoint have enough context?"

---

### Issue: "Compaction removed something I needed"

**Symptom**: After compacting, realize you need context that was discarded.

**Diagnosis**: Checkpoint was incomplete or wrong phase was compacted.

**Solution**:
1. **Read checkpoint file**: Does it have what you need?
2. **If yes**: Use checkpoint context to continue
3. **If no**: Re-explore (this is why we checkpoint before compacting)
4. **Lesson**: Next time, be more conservative in checkpoint (include more)

---

### Issue: "Too many checkpoint files accumulating"

**Symptom**: `.claude/context/` directory has 20+ checkpoint files from past tasks.

**Diagnosis**: Checkpoints are persistent artifacts (not auto-deleted).

**Solution**:
- **Short term**: Ignore (checkpoints are small, <10kb each)
- **Long term**: Manual cleanup after PR merged
- **Future**: Automated cleanup (see PLAN.md Enhancement Ideas #5)
- **Git**: Add `.claude/context/` to `.gitignore` if temporary checkpoints

---

## Advanced Patterns

### Cross-Session Context

**Use Case**: Task spans multiple days/sessions.

**Pattern**:
1. At end of day: Create checkpoint, compact context
2. Next session: Read checkpoint to recover context
3. Continue work with fresh context + checkpoint knowledge

**Benefit**: Clean session start, no context bloat carryover.

---

### Multi-Agent Context Sharing

**Use Case**: Hand off task from coder-agent to qa-agent.

**Pattern**:
1. Coder creates verification checkpoint
2. Coder hands off to QA with checkpoint path
3. QA reads checkpoint for implementation context
4. QA starts with clean context + checkpoint knowledge

**Benefit**: No context bloat transferred between agents.

---

### Hierarchical Checkpoints

**Use Case**: Very long tasks (>40 hour efforts).

**Pattern**:
1. Create checkpoint per day (exploration-day1, exploration-day2)
2. At week end, create summary checkpoint (exploration-week1-summary)
3. Summary references daily checkpoints
4. Next week starts with summary + latest daily

**Benefit**: Scales to long-running tasks without bloat.

---

## Success Criteria

**You have succeeded when:**

- ✅ Checkpoint file created in `.claude/context/` before compaction
- ✅ Checkpoint is self-contained (can resume work from it alone)
- ✅ User reviewed and approved compaction
- ✅ Context compacted successfully (30-50% token reduction)
- ✅ Essential context preserved in checkpoint artifact
- ✅ Can continue work with clean, focused context

**DO NOT consider success if:**

- ❌ Compacted without checkpoint (lossy compaction)
- ❌ Checkpoint incomplete or has placeholders
- ❌ Lost critical context and need to re-explore
- ❌ Checkpoint not self-contained (requires prior context to understand)

---

*Skill Version: 1.0.0*
*Part of Wolf Skills Marketplace*
*Integration: wolf-roles (coder-agent, research-agent, qa-agent)*
*Related: superpowers:verification-before-completion, wolf-governance*
