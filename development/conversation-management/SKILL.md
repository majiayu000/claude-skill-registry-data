---
name: conversation-management
description: Conversation phases, topic drift, and convo-exit protocols
---

# Conversation Management

> Structures brain repo conversations for clarity and continuous improvement.

---

## Conversation Phases

### Phase 1: Understanding (Start of conversation)

**Trigger**: New conversation begins or topic shifts significantly

**Actions**:
1. Read the request carefully
2. Identify:
   - What type of work is this? (feature, spec review, planning, research)
   - Which agents/patterns are relevant?
   - What context do I need?
3. Gather initial context (follow research-priority pattern)

**Output**: Internal understanding of the work

---

### Phase 2: Alignment (Before execution)

**Trigger**: After understanding the request

**Actions**:
1. **State your understanding**:
   - "I understand you want to [X]"
   - "This involves [agents/phases/work]"

2. **Propose execution plan**:
   - "Here's how I'll approach this:"
   - List steps (what, not when)
   - Call out which agents/patterns you'll use

3. **Wait for confirmation** before proceeding

**Output**: User confirms or corrects your plan

**Example**:
```
I understand you want to create a requirements spec for merchant onboarding.

Here's my approach:
1. Read existing merchant onboarding context
2. Follow Definition phase skill
3. Apply research-priority pattern
4. Create the requirements spec
5. Validate with quality-gate-reviewer

Does this align with what you need?
```

---

### Phase 3: Execution (Heads-down work)

**Trigger**: User approves plan

**Actions**:
1. Execute the plan
2. Use TodoWrite to track progress
3. **Don't interrupt unnecessarily** - work through the plan
4. Only pause if:
   - You hit a blocker
   - You discover the plan needs adjustment
   - User asks a question

**Anti-pattern**: Don't ask for permission at every micro-step

---

### Phase 4: Topic Drift Detection

**Trigger**: Conversation has shifted significantly from original intent

**Signs of drift**:
- Original task incomplete but discussing something new
- Multiple unrelated topics in one thread
- Context window filling with unrelated content
- Hard to summarize what the conversation is about

**Actions**:
1. Acknowledge the shift
2. Offer to start a new conversation

**Example**:
```
I notice we've shifted from creating the merchant spec to discussing
the overall architecture of the checkout flow.

Would you like to:
A) Start a new conversation focused on checkout architecture?
B) Continue here and I'll help with both topics?

Starting fresh helps me maintain context and lets us debrief on the
merchant spec work separately.
```

**Don't offer** if:
- Still on the same logical topic
- In the middle of productive work
- Would disrupt flow

---

### Phase 5: Conversation Exit (CRITICAL)

**Trigger**:
- User says "we're done", "that's it", "looks good"
- Conversation naturally concluding
- User explicitly requests exit/debrief

**ALWAYS perform exit protocol:**

#### Step 1: Review
```markdown
Let me review our conversation:

**Original goal**: [State the goal]
**What we accomplished**:
- [Bullet list of outcomes]
**Files created/modified**:
- [List with brief description]
```

#### Step 2: Tasks Remaining
```markdown
**Tasks Remaining**:

For this effort:
- [ ] [task 1]
- [ ] [task 2]

For this repo:
- [ ] Update [file]: [why]
- [ ] Add to [agent]: [what]
- [ ] Create new pattern: [for what]
```

#### Step 3: Ask for User Feedback
```markdown
**Your feedback**:
1. What worked well in this conversation?
2. What would you have liked to see improved?
3. Were there moments where I was unclear or off-track?
```

#### Step 4: Wait for response, then Propose Changes
```markdown
**Based on our conversation, I propose these changes**:

1. [File path]: [Specific change]
2. [File path]: [Specific change]

Should I make these changes?
```

#### Step 5: Execute Approved Changes

Make only the approved changes.

#### Step 6: Capture to convo-exits/

**File**: `convo-exits/YYYY-MM-DD-HHMM-topic.md`

Use the convo-exit template below.

#### Step 7: Personal Activity Log (optional)

If the brain repo has `personal/activity-log.md` (git-ignored), offer to update it:

```markdown
Would you like me to update your personal activity log with what you
accomplished in this conversation?
```

---

## Convo-Exit Template

Create `convo-exits/YYYY-MM-DD-HHMM-topic.md` with this structure:

```markdown
# Conversation Exit: [Topic]

**Date**: YYYY-MM-DD HH:MM
**Duration**: [approximate, if determinable]
**User**: [if identifiable]
**Repo**: [which brain repo(s) were involved]

---

## Original Goal

[What we set out to do at the start of the conversation]

---

## Outcomes

**Files Created**:
- `path/to/file.md` - Description of what this file is

**Files Modified**:
- `path/to/file.md` - What changed and why

**Decisions Made**:
- Key decision 1
- Key decision 2

---

## User Feedback

**What worked well**:
[User's positive feedback about the conversation]

**What could improve**:
[User's suggestions for improvement]

**Additional notes**:
[Any other feedback from the user]

---

## Improvements Made

**To this repo**:
- [ ] [Change 1] - [Status: Completed/Deferred/Rejected]

**To CLAUDE.md**:
- [ ] [Change 1] - [Status: Completed/Deferred/Rejected]

**To agents**:
- [ ] [Change 1] - [Status: Completed/Deferred/Rejected]

**To patterns**:
- [ ] [Change 1] - [Status: Completed/Deferred/Rejected]

---

## Suggestions for Future

**Patterns to consider**:
- [Pattern idea 1 - describe what it would solve]

**Agent improvements**:
- [Agent improvement 1]

**Documentation gaps**:
- [Gap 1 - what's missing from docs]

---

## Conversation Summary

[3-5 sentence summary of the full conversation arc: what we discussed, how the conversation evolved, what we accomplished, and any notable insights or pivots]

---

## Next Steps

**Immediate**:
- [ ] [Action item 1]

**Future**:
- [ ] [Longer-term follow-up 1]

---

## Related

**Linear Issues**:
- [Issue ID] - [Brief description]

**Other Conversations**:
- [Link to related convo-exit if applicable]

**Specs/Docs Created**:
- [Link to any specs or major docs that came from this]
```

---

## When to Use This Skill

**Use proactively**:
- At conversation start (Phases 1-2)
- When detecting topic drift (Phase 4)
- At conversation conclusion (Phase 5)

**Don't use**:
- In the middle of productive execution
- For quick one-off questions
- When user explicitly says "skip the process, just do X"

---

## Setting Up convo-exits/ in a Brain Repo

To enable conversation exits in a brain repo:

1. Create directory: `mkdir -p convo-exits`
2. Add `.gitkeep` or initial template
3. Optionally add to `.gitignore` if exits should be local-only:
   ```
   # Keep convo-exits local (optional)
   convo-exits/*.md
   !convo-exits/_template.md
   ```

---

## Success Metrics

A conversation managed well:
- User never confused about what you're doing
- Clear outcomes documented
- Learnings captured for future
- Improvements made to the system
- User feels heard and in control
