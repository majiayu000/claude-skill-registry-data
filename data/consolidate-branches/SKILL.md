---
name: consolidate-branches
description: Consolidate multiple PR branches onto a target branch using jj multi-parent rebase with intelligent AI-powered conflict resolution
---

# Consolidate Branches Skill

**Announce at start**: "I'm using the consolidate-branches skill to merge your PR branches."

## Overview

This skill consolidates multiple PR branches onto a target branch using jj's multi-parent rebase with intelligent conflict resolution. The primary use case is when you have multiple feature branches with expected conflicts that need to be merged together.

**Key principle**: Understand the intent behind each branch's changes and intelligently combine them, not just mechanically merge.

## Workflow

### Phase 1: Discovery

Discover all branches that might need consolidation:

1. Run `jj git fetch` to sync with remote
2. Display branch structure:
   ```bash
   JJ_CONFIG= jj log -r "trunk()..@ | trunk() | @.."
   ```
3. Parse the output to identify candidate branches
4. Show branches with metadata:
   - Branch name
   - Number of commits
   - Last modified date (if available)
   - Brief description from first/last commit

**Output**: Present a clear list of discovered branches to the user.

### Phase 2: Selection

Let the user choose what to consolidate:

1. Use AskUserQuestion tool with:
   - Multi-select question for branch selection
   - Separate question for target branch (suggest "main" as default)

2. Validate selections:
   - At least 2 branches must be selected
   - Target branch must exist
   - Selected branches should differ from target

3. Show confirmation summary:
   ```
   Consolidating branches [branch-a, branch-b, branch-c] onto main
   ```

**Ask**: "Ready to proceed with consolidation?"

### Phase 3: Analysis

Before merging, understand each branch's intent:

For each selected branch:

1. Read commit messages:
   ```bash
   jj log -r <branch>
   ```

2. Examine changes:
   ```bash
   jj diff -r <branch>
   ```

3. Categorize the changes:
   - What files are affected?
   - What type of change? (feature, bugfix, refactor, docs, etc.)
   - What is the goal of this branch?

4. Document intent for later conflict resolution

**Output**: Create a mental model of what each branch is trying to accomplish.

### Phase 4: Consolidation

Perform the multi-parent rebase:

1. Create new working commit on target:
   ```bash
   jj new <target-branch>
   ```

2. Multi-parent rebase to combine all branches:
   ```bash
   jj rebase -r @ -d <branch1> -d <branch2> -d <branch3> ...
   ```

3. Check the result:
   - Did the rebase succeed?
   - Are there conflicts?

### Phase 5: Intelligent Conflict Resolution

**This is the core value of the skill.**

When conflicts occur:

1. **Identify conflicting files**:
   - List all files with conflicts
   - Categorize by severity/complexity

2. **For each conflicting file**:

   a. **Show conflict context**:
      - Display the conflicting sections from each branch
      - Show surrounding code for context

   b. **Analyze intent**:
      - What was each branch trying to accomplish in this file?
      - Are the changes complementary or contradictory?
      - Can both goals be achieved simultaneously?

   c. **Propose resolution**:
      - Draft a merge that preserves both/all intents
      - Explain the reasoning behind the resolution
      - If intents are contradictory, explain the trade-offs and recommend the best approach

   d. **Apply resolution**:
      - Edit the file to implement the proposed merge
      - Remove conflict markers
      - Ensure code is syntactically correct

   e. **Document resolution**:
      - Track what conflict was resolved
      - Record why this resolution was chosen
      - Note any assumptions made

3. **Present resolutions to user**:
   - Summarize all conflicts found
   - Explain how each was resolved
   - Show the reasoning behind decisions
   - Ask for validation: "Do these conflict resolutions look correct?"

4. **Iterate if needed**:
   - If user requests changes, revise resolutions
   - Re-apply and re-validate

**Key Guidelines**:
- Don't just pick one side arbitrarily
- Look for ways to combine both changes
- Preserve functionality from all branches
- Maintain code quality and consistency
- When uncertain, explain options to user

### Phase 6: Verification

Verify all changes from all branches are present:

1. **Code presence check** for each branch:
   ```bash
   jj diff -r <branch>
   ```
   - Compare against final consolidated result
   - Verify the changes are present
   - Report any missing changes

2. **Generate summary report**:
   - List all branches consolidated
   - Show total number of commits included
   - List conflicts resolved with explanations
   - Display final diff of consolidated changes:
     ```bash
     jj diff -r <target-branch>..@
     ```

3. **Sanity checks**:
   - Are there any remaining conflict markers?
   - Does the code appear syntactically correct?
   - Are imports/dependencies resolved?

### Phase 7: Completion

Leave the workspace ready for user review:

1. **Summary message**:
   ```
   Branch consolidation complete!

   Consolidated branches: [list]
   Total commits: [count]
   Conflicts resolved: [count]

   The changes are ready for your review.
   ```

2. **Next steps guidance**:
   - "Review the changes with `jj diff`"
   - "When satisfied, you can:"
     - "Create a commit with `jj commit -m 'your message'`"
     - "Create a PR"
     - "Make further edits"
   - "The workspace is ready for your action"

3. **Don't auto-commit**: User maintains full control

## Error Handling

### If fetch fails
- Report the error
- Ask if user wants to continue without fetching
- Explain risks of stale branch info

### If no branches found
- Report that no branches were found
- Suggest checking if branches are pushed to remote
- Offer to show current branch status

### If multi-parent rebase fails
- Report the specific error
- Check if it's due to conflicts or other issues
- Guide user through resolution

### If conflicts seem irresolvable
- Explain why the conflict is challenging
- Present the conflicting code from each branch
- Ask user for guidance on resolution strategy
- Offer to abort if user prefers manual merge

## Key Principles

1. **Understanding over mechanics**: Always analyze intent before merging
2. **Preserve all functionality**: Don't drop changes from any branch
3. **Clear communication**: Explain what you're doing and why
4. **User control**: Present resolutions for validation, don't auto-commit
5. **Safety first**: Verify changes, check for missing code
6. **Helpful guidance**: Provide clear next steps

## Success Criteria

The consolidation is successful if:
- All selected branches are merged
- All conflicts are intelligently resolved
- All changes from all branches are present
- Code is syntactically correct
- User understands what was done and why
- Workspace is clean and ready for review
