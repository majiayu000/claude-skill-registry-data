---
name: triage
description: >
  Create bead(s) from a user prompt. Investigates relevance, checks for duplicates,
  and may split complex requests into multiple focused beads. Use when given a
  feature request, bug report, or task description that should be tracked.
allowed-tools: "Read,Bash(bd:*),Grep,Glob,Task"
version: "1.0.0"
author: "flurdy"
---

# Triage - Smart Bead Creation from Prompts

Analyze user requests and create appropriate beads with intelligent investigation.

## When to Use

- User describes a feature, bug, or task to track
- Raw idea needs analysis before becoming actionable work
- Need to check if work is already tracked or duplicated
- Complex request might need to be split into multiple beads

## Usage

```
/triage <description of feature, bug, or task>
```

## What This Skill Does

1. **Investigate Relevance**
   - Search codebase to understand if request is feasible
   - Check if the feature/fix location is obvious
   - Identify any related existing code

2. **Check for Duplicates**
   - Run `bd list --status=open` to see existing work
   - Search bead titles and descriptions for similar items
   - Flag potential duplicates or related beads

3. **Analyze Complexity**
   - Determine if single bead or multiple beads needed
   - Identify natural task boundaries
   - Consider dependencies between potential beads

4. **Create Beads**
   - Create focused, actionable beads
   - Set appropriate type (task/bug/feature)
   - Set reasonable priority (P2 default, adjust based on context)
   - Add dependencies if creating multiple related beads

5. **Report Summary**
   - List newly created beads
   - Show current open beads count
   - Highlight any duplicates or related work found

## Examples

```bash
# Simple feature request
/triage Add dark mode toggle to settings page

# Bug report
/triage Users seeing 500 error when saving profile with emoji in name

# Complex request (may split)
/triage Implement user authentication with OAuth, session management, and password reset
```

## Output Format

After triage, provide:

1. **Investigation Summary**: What was checked, relevance assessment
2. **Duplicate Check**: Any similar existing beads found
3. **Created Beads**: List of new beads with IDs
4. **Open Beads Summary**: Quick stats on current workload

## Implementation

When invoked:

1. Parse the user's description to understand intent (feature/bug/task)

2. Quick codebase investigation:
   ```bash
   # Search for related code/files
   # Check if area of code exists
   ```

3. Check for duplicates:
   ```bash
   bd list --status=open
   bd search "<keywords from description>"
   ```

4. Decide on bead structure:
   - Single focused task → one bead
   - Multi-part work → multiple beads with dependencies
   - Vague request → ask clarifying questions first

5. Create bead(s):
   ```bash
   bd create --title="..." --type=feature|bug|task --priority=2 --description="..."
   ```

6. If multiple beads, set dependencies:
   ```bash
   bd dep add <dependent> <dependency>
   ```

7. Report results with summary of open beads

## Priority Guidelines

- **P0-P1**: Critical/urgent (user explicitly says urgent, or blocking issue)
- **P2**: Default for most work (standard feature/task)
- **P3**: Lower priority (nice-to-have, minor improvements)
- **P4**: Backlog (future work, ideas to consider)
