---
name: refine-plan
description: Refines an existing implementation plan through discussion with the user. Takes a GitHub issue number. Use when the user wants to refine a plan, discuss a plan, change a plan, or says "refine plan X" or "let's discuss the plan for issue #Y".
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, AskUserQuestion
---

# Refine Plan

## Purpose

Iteratively refine an existing implementation plan through discussion with the user. Allows asking questions, requesting changes, and approving the final plan.

## Prerequisites

The ticket MUST have an implementation plan. If no plan exists, tell the user to run `/plan-ticket` first.

## Workflow

### Step 1: Verify Environment

Check we have a GitHub remote:

```bash
git remote -v
```

**STOP if:**
- No remote exists → "This skill requires a GitHub remote. Please add one with `git remote add origin <url>` first."

### Step 2: Identify the Ticket

User will provide a GitHub issue number (e.g., `#12` or `12`).

If not clear, ask which ticket to refine.

### Step 3: Read Ticket and Plan

```bash
gh issue view <number> --comments
```

Extract:
- The original issue description
- The implementation plan (look for "## Implementation Plan" section)
- The success criteria

If no implementation plan exists, STOP and tell user to run `/plan-ticket` first.

### Step 4: Present Current Plan

Display the current plan to the user clearly, including:
- The implementation steps
- The success criteria
- Any context from the original issue

### Step 5: Feedback Loop

Enter an iterative refinement loop:

1. **Ask for feedback** using AskUserQuestion:
   - "Do you have questions about the plan?"
   - "Would you like to change anything?"
   - "Is the plan ready to approve?"

2. **Handle response:**
   - **Questions**: Answer based on codebase exploration and plan context
   - **Change requests**: Revise the plan and present the updated version
   - **Approval**: Exit the loop and proceed to posting

3. **Loop back** if not approved, presenting the revised plan each time

Keep track of what has changed during refinement for the revision notes.

### Step 6: Post Revised Plan

Once approved, post the revised plan as a new comment:

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Revised Implementation Plan

### Revision Notes

<Summary of what changed from the original plan>

### Steps

1. **<Action>** - <What this accomplishes>
   - Files: `path/to/file.py`
   - <Brief description of the change>

...

### Success Criteria

- [ ] <Observable outcome 1>
- [ ] <Observable outcome 2>
EOF
)"
```

### Step 7: Report Back

Tell the user:
- The revised plan has been posted
- Summary of key changes made
- Next step is to run `/implement-ticket <number>`

## Guidelines

**DO**:
- Present the plan clearly before asking for feedback
- Answer questions thoroughly, exploring the codebase if needed
- Make requested changes accurately
- Keep revision notes concise but complete
- Allow multiple rounds of refinement

**DON'T**:
- Include source code in the plan
- Make changes the user didn't request
- Skip the approval step
- Post identical plans (if no changes were made, just confirm and don't post)

## Handling Common Scenarios

**User asks about a specific step:**
Explore the codebase to provide context and answer their question.

**User wants to add a step:**
Add it in the appropriate order and explain where it fits.

**User wants to remove a step:**
Remove it and adjust any dependent steps.

**User wants to change the approach:**
Revise affected steps and update success criteria if needed.

**No changes needed:**
If the user approves without changes, confirm and skip posting (no revision needed).

## Checklist

- [ ] Verify GitHub remote exists
- [ ] Identify which issue to refine
- [ ] Read issue and extract plan
- [ ] Verify plan exists (if not, stop)
- [ ] Present current plan to user
- [ ] Enter feedback loop
- [ ] Handle questions and changes
- [ ] Get user approval
- [ ] Post revised plan (if changes were made)
- [ ] Report back to user
