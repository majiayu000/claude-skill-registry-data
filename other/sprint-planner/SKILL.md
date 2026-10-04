---
name: sprint-planner
description: Use this skill to plan a new sprint. It uses the Gemini CLI to intelligently decompose approved specs into atomic GitHub issues for the development team. Triggers include "plan sprint", "create sprint", or "start new sprint".
---

# Sprint Planner Skill

## Purpose

To plan and initialize a new sprint by intelligently decomposing approved specifications into a comprehensive set of atomic GitHub issues. This skill bridges the gap between high-level specs and executable work items by using the **Gemini CLI** to analyze the spec's content and generate a thoughtful task breakdown. It then automates the creation of these tasks as GitHub issues within a new sprint milestone.

## When to Use

Use this skill in the following situations:

- Starting a new sprint or development cycle.
- Converting an approved spec into actionable GitHub issues.
- When you want an AI-assisted breakdown of an epic into atomic implementation tasks.

## Prerequisites

- Project board configured with an "Approved Backlog" status column.
- Approved spec files exist in the `docs/specs/` directory.
- An Epic issue exists on GitHub that links to the spec file in its body.
- `gh` CLI tool installed and authenticated.
- `jq` tool installed for JSON parsing.
- `gemini` CLI tool installed and authenticated.

## Workflow

### Step 1: Review Project Board

Check the project board for approved specs (represented as Epics) ready to be planned.

### Step 2: Discuss Sprint Scope with User

Engage the user to determine which epic(s) from the "Approved Backlog" to include in the sprint.

### Step 3: Define Sprint Metadata

Work with the user to establish the sprint name (e.g., "Sprint 4").

### Step 4: Run the Helper Script

Execute the sprint planning script to automate GitHub issue creation:

```bash
bash scripts/create-sprint-issues.sh
```

### Step 5: Understand What the Script Does

The helper script automates these steps:

1.  **Queries Project Board**: Fetches all items from the "Approved Backlog" and prompts you to select an Epic to plan.
2.  **Extracts Spec File**: Parses the selected Epic's body to find the associated spec file path.
3.  **Creates Milestone**: Prompts you for a sprint name and creates the corresponding GitHub milestone.
4.  **Decomposes Spec with AI**: Instead of relying on a rigid format, the script sends the full content of the spec file and the parent Epic to the **Gemini CLI**. It asks the AI to generate a list of atomic, actionable tasks based on its understanding of the document.
5.  **Creates GitHub Issues**: The script parses the structured task list from Gemini's response and creates a GitHub issue for each task. Each issue is automatically titled, assigned to the new milestone, and includes a description and references to the parent Epic and spec file.

### Step 6: Verify Issue Creation

After the script completes, review the newly created issues in your milestone.

```bash
gh issue list --milestone "Your Sprint Name"
```

### Step 7: Review Created Issues with User

Walk through the AI-generated issues with your team. The generated tasks provide a strong baseline, but you should review them to confirm completeness, adjust priorities, and make any necessary refinements.

## Error Handling

### jq or Gemini Not Installed

**Symptom**: Script reports that `jq` or `gemini` command is not found.
**Solution**: Install the required tool and ensure it's in your system's PATH.

### No Approved Epics Found

**Symptom**: Script reports no epics in the approved backlog.
**Solution**: Ensure your Epics are in the correct status column on your project board.

### Epic Body Missing Spec Reference

**Symptom**: Script cannot find a spec file path in the Epic's body.
**Solution**: Edit the Epic's issue body on GitHub to include a valid path to a spec file (e.g., `docs/specs/my-feature.md`).

### Gemini CLI Issues

**Symptom**: The script fails during the task decomposition step with an error from the `gemini` command.
**Solution**:
- Ensure the `gemini` CLI is installed and authenticated (`gemini auth`).
- Check for API outages or network issues.
- The quality of the task breakdown depends on a functional Gemini CLI.

## Notes

- **Intelligent Decomposition**: The skill no longer relies on a rigid task format in spec files. Gemini reads and understands the document to create tasks.
- **LLM guides strategy, script executes**: You decide which spec to plan; the script uses AI to handle the tedious decomposition and issue creation.
- **One epic per run**: Run the script once for each Epic you want to plan for the sprint.
- **Traceability is built-in**: Each created task issue automatically references the parent Epic and the source spec file.
- **Manual refinement is expected**: The AI-generated task list is a starting point. Review and adjust it with your team.