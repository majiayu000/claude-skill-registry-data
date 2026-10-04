---
description: Run a cross-domain workflow template with progress tracking
---

# Workflow

Load and present a cross-domain workflow template for "$ARGUMENTS". Track progress by checking which artifacts already exist in `.metapowers/`.

## Prerequisites

None — utility skill, run anytime.

## Process

1. **Find the workflow template:**
   - Check `plugins/metapowers/shared/workflows/` for a file matching "$ARGUMENTS"
   - Available workflows: `launch-product`, `build-feature`, `rebrand`, `new-team`, `compliance-audit`
   - If no match found, list available workflows and ask the user to choose

2. **Read the workflow template:**
   - Read the matching `.md` file from the workflows directory

3. **Check progress:**
   - For each step in the workflow, check if the corresponding artifact exists in `.metapowers/`
   - Mark completed steps with a checkmark
   - Mark pending steps as to-do

4. **Present the workflow to the user:**
   - Show the workflow name and description
   - Show each step with its status (done/pending)
   - Highlight the next step to work on
   - Remind the user to replace placeholder names with their actual project names

5. **Offer guidance:**
   - If the user asks, explain what a specific step does
   - Suggest skipping steps that don't apply to their situation

## Output

Present the workflow checklist directly to the user with progress tracking. No artifact file created — this is a real-time guide.
