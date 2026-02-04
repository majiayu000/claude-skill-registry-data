---
name: ending-an-iteration
description: Use when concluding work on an open-ended goal to write iteration journal entry documenting work performed, decisions made, and state changes
---

# Ending an Iteration

## Overview

Conclude the current iteration by reviewing the conversation, documenting what happened, and preparing state for the next iteration.

**Core principle:** Comprehensive journaling enables continuity. Future iterations depend on accurate state capture.

## When to Use

Use this skill when:
- User runs `/end-iteration` command
- Agent suggests natural stopping point and user confirms
- Context limit approaching and good time to pause
- Subtask complete and ready to hand off to next iteration

**DO NOT use for:**
- Middle of active work (finish current subtask first)
- Before resolving critical blockers (unless blocked externally)

## Quick Reference

| Step | Action | Tool |
|------|--------|------|
| 1. Review conversation | Extract skills, decisions, artifacts | Manual review |
| 2. Identify stopping point | Why is this iteration ending? | User confirmation |
| 3. Complete journal entry | Update existing journal file | Read, Edit |
| 4. Update summary | If iteration 5, 10, 15, etc. | Task (journal-summarizer) |
| 5a. Git commit and tag | Commit journal to current branch | Bash |
| 5b. Announce completion | Confirm next steps | Direct output |

## Process

### Step 1: Review Conversation

Review the full conversation to extract key information:

**Skills & Workflows Used:**
- Scan conversation for `<invoke name="Skill">` tool calls
- Note which skills were used and for what purpose
- Generic detection - works with any plugin skills

Example findings:
```markdown
### Skills & Workflows Used
- `brainstorming`: Designed pricing tier alternatives
- `hypothesis-testing`: Validated annual billing preference
- `internet-researcher`: Found competitor pricing data
```

**Key Decisions Made:**
- Identify major choices: architecture, strategy, approach
- Note rationale: why was this chosen?
- Record alternatives considered

Example:
```markdown
### Key Decisions Made
- **Decision:** Implement usage-based pricing tier
  **Rationale:** Research showed power users want to scale gradually
  **Alternatives:** Flat enterprise tier (rejected: less flexible)
```

**Artifacts Created/Modified:**
- Files created or changed (use git status/diff if applicable)
- Git commits made during iteration
- Pull requests opened
- Documentation written

Example:
```markdown
### Artifacts Created/Modified
- `src/pricing/usage-tier.ts`: New usage-based pricing calculator
- `docs/pricing-strategy.md`: Documented pricing decision rationale
- Git commit: abc123f "Add usage-based pricing tier"
```

**External Context Gathered:**
- Web research findings
- User feedback received
- Documentation consulted
- Competitor analysis

Example:
```markdown
### External Context Gathered
- Research: Competitor X charges $0.10/unit, Competitor Y charges $0.15/unit
- User feedback: "Annual discount of 20% drives conversions"
- Documentation: Stripe API supports usage-based billing natively
```

**Reasoning & Strategy Changes:**
- Why certain approaches were chosen
- What alternatives were explored
- Where strategy pivoted and why

Example:
```markdown
### Reasoning & Strategy Changes
- Initially planned flat enterprise tier
- Research showed power users prefer scaling gradually
- Pivoted to usage-based model to reduce friction
- This aligns with SaaS best practices for 2026
```

**Blockers Encountered:**
- What's preventing progress?
- Dependencies on external factors
- Questions needing answers

Example:
```markdown
### Blockers Encountered
- Stripe webhook integration unclear: need to consult API docs
- Finance team needs to approve pricing before launch
- Usage tracking infrastructure not yet built (dependency)
```

**Open Questions:**
- What needs to be resolved next?
- Decisions deferred to future iterations
- Unknowns requiring investigation

Example:
```markdown
### Open Questions
- Should we offer annual discount on usage-based tier?
- What's the right per-unit price point?
- Do we need a minimum monthly commit?
```

### Step 2: Identify Stopping Point

Determine why this iteration is ending:

**Ask user to confirm:**
```
"Suggested stopping point: [reason]. Should we end this iteration?"

Reasons:
- Subtask complete: [what was finished]
- Blocked on: [external dependency]
- Context approaching limit
- Natural break point: [why this makes sense]
```

**User confirms** → Proceed to write journal

**User wants to continue** → Return to work, don't end iteration yet

### Step 3: Complete Journal Entry

The journal file was created by starting-an-iteration. Now complete it:

1. **Find current journal file:**
   ```bash
   # Use Glob to find iteration files
   pattern: "autonomy/*/iteration-*.md"
   ```

   Sort by iteration number and identify the most recent (should be today's date).

2. **Read existing journal:**
   ```bash
   # Use Read to load current content
   file: "autonomy/[goal-name]/iteration-NNNN-YYYY-MM-DD.md"
   ```

   Journal will have:
   - Beginning State (from starting-an-iteration)
   - Iteration Intention (from starting-an-iteration)
   - Work Performed (may be filled by checkpointing, or still empty)
   - Ending State (empty - we'll fill this)
   - Iteration Metadata (empty - we'll fill this)

3. **Update Work Performed section:**

   Using findings from Step 1, update the Work Performed subsections.

   **If Work Performed is empty:**
   Replace entire section with Step 1 findings.

   **If Work Performed has content (from checkpointing):**
   Merge Step 1 findings with existing:
   - Add any new skills/workflows used since checkpoint
   - Add any new decisions made since checkpoint
   - Add new artifacts created since checkpoint
   - Append new context gathered since checkpoint
   - Note any additional blockers or questions
   - Preserve all existing checkpoint content

4. **Fill Ending State section:**
   ```markdown
   ## Ending State
   [What is the state NOW at iteration end?]
   - Progress made during this iteration
   - What's complete vs. what remains
   - Updated metrics (if applicable)
   - How well did we achieve the iteration intention?
   - Recommended next steps for iteration N+1
   ```

5. **Fill Iteration Metadata section:**
   ```markdown
   ## Iteration Metadata
   - Context usage: [Note if approaching limits, if compaction occurred]
   - Checkpoints: [How many times was checkpoint-iteration used?]
   - Suggested next action: [What should iteration N+1 work on?]
   ```

6. **Update file using Edit tool:**
   - Replace Work Performed section (merge with existing)
   - Replace Ending State section (fill in)
   - Replace Iteration Metadata section (fill in)
   - Preserve Beginning State and Iteration Intention sections

### Step 4: Update Summary (if needed)

Check if summary update is needed:

**Update summary every 5 iterations:** 5, 10, 15, 20, etc.

```
If current iteration number % 5 == 0:
   Dispatch journal-summarizer agent to update summary.md
```

**Dispatch journal-summarizer:**
```
Task tool with subagent_type: "autonomy:journal-summarizer"
Prompt: "Update summary.md for goal '[goal-name]' to include iterations 1-[N].
        Previous summary covered iterations 1-[N-5].
        Add new learnings, update metrics, note new blockers."
Model: haiku
```

**Wait for agent** to update summary.md

### Step 5a: Git Commit and Tag

After journal is complete and summary is updated (if needed), commit to git:

1. **Extract iteration metadata:**
   - Goal name from journal path: `autonomy/[goal-name]/`
   - Iteration number from filename: `iteration-NNNN-YYYY-MM-DD.md`
   - Extract 2-3 line summary from Ending State section

2. **Determine iteration status:**

   Analyze Ending State section to determine status:
   - Look for explicit status indicators: "This is a dead end", "Approach invalidated", "Successfully completed", "Blocked by", etc.
   - **active** (default) - Normal progression, work continuing
   - **blocked** - Contains phrases like "blocked by", "waiting on", "cannot proceed until"
   - **concluded** - Contains phrases like "successfully completed", "goal achieved", "experiment succeeded"
   - **dead-end** - Contains phrases like "dead end", "not working", "abandoning approach", "invalidated"

3. **Extract quantitative metrics:**

   Parse Ending State for metrics with numbers:
   - Look for patterns like "MRR: $62k (+12%)", "Build time: 3.2min (-40%)", "Churn: 8% (from 13%)"
   - Collect all quantitative progress indicators
   - Format as single line: `Metrics: [metric1], [metric2], ...` or "None" if no metrics

4. **Summarize journal content:**

   Create 4-6 sentence summary from Work Performed and Ending State:
   - What was accomplished this iteration
   - Key decisions made and rationale
   - Major learnings or discoveries
   - How this iteration moved toward the goal
   - Be substantive but concise - this is for git log readers

5. **Build enhanced commit message:**
   ```
   journal: [goal-name] iteration NNNN

   [2-3 line summary from Ending State - as before]

   ## Journal Summary

   [4-6 sentence summary from step 4 above - what happened, what was learned, what changed]

   ## Iteration Metadata

   Status: [active|blocked|concluded|dead-end]
   Metrics: [quantitative metrics from step 3, or "None"]
   Blockers: [summary from Blockers Encountered section, or "None"]
   Next: [next iteration intention from Iteration Metadata section]

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

6. **Stage files:**
   ```bash
   # Always stage journal file
   git add autonomy/[goal-name]/iteration-NNNN-YYYY-MM-DD.md

   # If summary was updated this iteration (iteration % 5 == 0)
   git add autonomy/[goal-name]/summary.md
   ```

7. **Create commit:**
   ```bash
   # Use heredoc for multi-line message with enhanced format
   git commit -m "$(cat <<'EOF'
   journal: [goal-name] iteration NNNN

   [2-3 line summary from Ending State]

   ## Journal Summary

   [4-6 sentence summary of iteration]

   ## Iteration Metadata

   Status: [active|blocked|concluded|dead-end]
   Metrics: [metrics or "None"]
   Blockers: [blockers or "None"]
   Next: [next iteration intention]

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```

8. **Create annotated tag with branch-aware naming:**
   ```bash
   # Get current branch name
   current_branch=$(git branch --show-current)

   # Extract strategy name from branch
   # For autonomy branches: "autonomy/experiment-a" → "experiment-a"
   # For non-autonomy branches: use goal name as strategy
   if [[ "$current_branch" =~ ^autonomy/ ]]; then
     strategy_name=${current_branch#autonomy/}
   else
     # Use goal name from journal path
     strategy_name="[goal-name]"
   fi

   # Tag format: autonomy/<strategy-name>/iteration-NNNN (4 digits, zero-padded)
   git tag -a "autonomy/${strategy_name}/iteration-$(printf '%04d' NNNN)" \
     -m "journal: [goal-name] iteration NNNN"
   ```

9. **Handle errors gracefully:**
   - If git operations fail (not a repo, detached HEAD, permissions, etc.):
     - Capture error message
     - Continue to Step 5b anyway (journal is written, that's critical)
     - Report warning to user with manual commands

**Error reporting format:**
```markdown
⚠️ **Git Integration Warning:**
Failed to commit journal: [error message]

You can manually commit with:
  git add autonomy/[goal-name]/iteration-NNNN-YYYY-MM-DD.md
  git commit -m "journal: [goal-name] iteration NNNN ..."
  git tag -a "autonomy/[strategy-name]/iteration-NNNN" -m "journal: [goal-name] iteration NNNN"
```

**Success indicator:**
- If git operations succeed, note success for Step 5b announcement
- Tag `autonomy/[strategy-name]/iteration-NNNN` marks this iteration in git history

### Step 5b: Announce Completion

Report to user with git status:

**If git operations succeeded:**
```markdown
**Iteration [N] complete for goal: [goal-name]**

✓ Journal committed and tagged: `autonomy/[strategy-name]/iteration-NNNN`

Journal entry: `autonomy/[goal-name]/iteration-NNNN-YYYY-MM-DD.md`
Branch: [current-branch-name]
Status: [active|blocked|concluded|dead-end]

## Summary of This Iteration
- **Work completed:** [Brief summary]
- **Key decisions:** [Major choices made]
- **Blockers:** [What's preventing progress]
- **Next steps:** [Recommended for iteration N+1]

---

**Ready to resume in next conversation with `/start-iteration`**
```

**If git operations failed:**
```markdown
**Iteration [N] complete for goal: [goal-name]**

Journal entry written: `autonomy/[goal-name]/iteration-NNNN-YYYY-MM-DD.md`

⚠️ **Git Integration Warning:**
Failed to commit journal: [error message]

You can manually commit with:
  git add autonomy/[goal-name]/iteration-NNNN-YYYY-MM-DD.md
  git commit -m "journal: [goal-name] iteration NNNN ..."
  git tag -a "autonomy/[strategy-name]/iteration-NNNN" -m "journal: [goal-name] iteration NNNN"

## Summary of This Iteration
- **Work completed:** [Brief summary]
- **Key decisions:** [Major choices made]
- **Blockers:** [What's preventing progress]
- **Next steps:** [Recommended for iteration N+1]

---

**Ready to resume in next conversation with `/start-iteration`**
```

## Important Notes

### Journal File Already Exists

The journal file was created by starting-an-iteration with:
- Beginning State (from context loading)
- Iteration Intention (from user input)
- Empty Work Performed sections (to be filled)

Your job is to **complete** the journal, not create it from scratch.

### Merging with Checkpoint Content

If user ran `/checkpoint-iteration` during the iteration:
- Work Performed section will have partial content
- Merge your Step 1 findings with existing content
- Add new information discovered since checkpoint
- Don't overwrite or lose checkpoint data

### Comprehensive Documentation

**Critical:** Future iterations depend entirely on this journal. Include:
- Enough detail that iteration N+1 can pick up seamlessly
- Rationale for decisions (not just what, but why)
- All blockers, even minor ones
- Specific next steps, not vague "continue working"

### Date in Filename

Always use today's date (YYYY-MM-DD format):
```bash
# Get current date
date +%Y-%m-%d
```

### Don't Skip Sections

Even if a section is empty, include it with a note:
```markdown
### Blockers Encountered
None - iteration progressed smoothly
```

This shows the section was considered, not forgotten.

### Git Integration

**Automatic commits to current branch:**
- Journal file is committed to whatever branch you're currently on
- Does NOT create new branch or switch branches
- Uses enhanced commit message format with:
  - Brief summary (2-3 lines)
  - Journal Summary section (4-6 sentences)
  - Iteration Metadata section (status, metrics, blockers, next steps)
- Tags commit as `autonomy/<strategy-name>/iteration-NNNN` for branch-aware navigation

**Branch-aware tagging:**
- On autonomy branches: Tag uses branch name (e.g., `autonomy/experiment-a/iteration-0015`)
- On non-autonomy branches: Tag uses goal name (backward compatibility)
- Each branch has its own iteration namespace
- No tag collisions when multiple branches have same iteration number

**Error handling:**
- Git failures do NOT block iteration completion
- Journal is always written, even if commit fails
- User receives manual commands if git fails
- Graceful degradation ensures state is preserved

**What gets committed:**
- Always: `iteration-NNNN-YYYY-MM-DD.md` journal file
- Sometimes: `summary.md` (if iteration % 5 == 0)
- Never: Other files in working directory

**Tag benefits:**
- Navigate to iteration on specific branch: `git checkout autonomy/experiment-a/iteration-0042`
- List all iterations on a branch: `git tag -l 'autonomy/experiment-a/*'`
- List all autonomy iterations: `git tag -l 'autonomy/*/*'`
- Immutable history markers for CI/CD integration
- Enables branch management commands to query git log for metadata

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| "I'll create new journal file instead of updating existing" | NO. Journal was created by starting-an-iteration. Update it with Edit tool. |
| "I'll overwrite Work Performed that has checkpoint content" | NO. Merge with existing. Preserve checkpoint data. |
| "Journal is too detailed, I'll abbreviate" | NO. Be comprehensive. Future iterations need full context. |
| "No blockers this time, I'll skip that section" | NO. Write "None" to show you checked. |
| "Summary update can wait" | NO. If iteration % 5 == 0, update summary. |
| "I'll skip comparing against iteration intention" | NO. Ending State should assess how well intention was achieved. |
| "Git commit failed, so iteration failed" | NO. Journal writing is critical, git commit is helpful. Warn about git error but complete iteration. |
| "I'll create a new branch for the commit" | NO. Commit to current branch. User controls branching strategy. |

## After Ending

Once iteration is ended:
- Journal file completed with Ending State and Iteration Metadata
- Summary updated if needed (every 5 iterations)
- Git commit created and tagged as `autonomy/iteration-NNNN` (if git operations succeeded)
- Full iteration story captured for next iteration
- Can start new iteration anytime with `/start-iteration`
