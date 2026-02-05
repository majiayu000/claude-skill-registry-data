---
name: spec-authoring
description: Use this skill when proposing new features or changes via the Spec PR process. Manages the creation, refinement, and approval of feature specifications before any code is written. Triggers include "create spec", "propose change", "start spec PR", or beginning feature definition.
---

# Spec Authoring Skill

## Purpose

Manage the creation and refinement of feature specifications through the Spec PR process. This skill enables spec-driven development where all changes are defined, reviewed, and approved before implementation begins. Specifications are proposed in the `docs/changes/` directory, reviewed via Pull Request, and merged to `docs/specs/` upon approval.

## When to Use

Use this skill in the following situations:

- Proposing a new feature or significant change
- Defining requirements before implementation
- Creating a Spec PR for team review
- Updating a proposal based on review feedback
- Following the spec-driven development workflow

## Prerequisites

- Project initialized with SynthesisFlow structure (docs/specs, docs/changes directories exist)
- GitHub repository set up
- `gh` CLI tool installed and authenticated

## Spec PR Philosophy

**Specs as Code**: All specification changes follow the same rigor as code changes - proposed via branches, reviewed via PRs, and merged upon approval.

**Benefits**:
- **Review before implementation**: Catch design issues early when changes are cheap
- **Clear requirements**: Implementation has explicit acceptance criteria
- **Historical record**: Approved specs document what was intended and why
- **Team alignment**: Stakeholders review and approve before development starts

**Workflow**:
1. Changes proposed in `docs/changes/` directory (isolated from source-of-truth)
2. Spec PR opened for review
3. Team reviews and provides feedback
4. Proposal refined based on feedback
5. Spec PR approved and merged
6. Approved spec moves to `docs/specs/` (via change-integrator skill)

## The `propose` Command

### Purpose

Create a new change proposal with the necessary file structure.

### Workflow

#### Step 1: Define the Proposal Name

Discuss with the user what feature or change to propose. Choose a clear, descriptive name:
- "User Authentication System"
- "Real-time Notifications"
- "Performance Optimization"

#### Step 2: Run the Helper Script

Execute the script to create the proposal directory structure:

```bash
bash scripts/spec-authoring.sh propose "Feature Name"
```

The script will:
- Convert the name to kebab-case (e.g., "Feature Name" → "feature-name")
- Create `docs/changes/feature-name/` directory
- Create three empty files:
  - `proposal.md` - High-level overview and problem statement
  - `spec-delta.md` - Detailed specifications and requirements
  - `tasks.md` - Breakdown of implementation tasks

#### Step 3: Populate proposal.md

Work with the user to create a clear proposal:

```markdown
# Proposal: Feature Name

## Problem Statement
[What problem does this solve? Why is it needed?]

## Proposed Solution
[High-level approach to solving the problem]

## Benefits
[What value does this provide?]

## Success Criteria
[How do we know this is successful?]
```

#### Step 4: Populate spec-delta.md

Define detailed specifications:

```markdown
# Spec Delta: Feature Name

## Overview
[Detailed description of what's being added/modified/removed]

## Requirements
[Specific, testable requirements]

## Design Decisions
[Key architectural or design choices]

## Migration Path
[How to transition from current state if applicable]
```

#### Step 5: Populate tasks.md

Break down implementation into atomic tasks:

```markdown
# Tasks: Feature Name

## Task 1: Component A
- [ ] Subtask 1
- [ ] Subtask 2

**Acceptance Criteria**:
- Criteria 1
- Criteria 2

## Task 2: Component B
...
```

#### Step 6: Create Spec PR

After populating files:

1. Create feature branch: `git checkout -b spec/feature-name`
2. Add files: `git add docs/changes/feature-name/`
3. Commit: `git commit -m "spec: Propose Feature Name"`
4. Push: `git push -u origin spec/feature-name`
5. Create PR: `gh pr create --title "Spec: Feature Name" --body "..."`

Label as "spec" or "proposal" if labels are available.

## The `update` Command

### Purpose

Fetch review comments from a Spec PR to incorporate feedback.

### Workflow

#### Step 1: Identify the PR Number

Determine which Spec PR needs updates based on review feedback.

#### Step 2: Fetch Review Comments

Run the helper script to view all comments:

```bash
bash scripts/spec-authoring.sh update PR_NUMBER
```

This displays:
- All PR comments with context
- Review feedback from team members
- Suggestions and questions

#### Step 3: Discuss Feedback with User

Review the comments together and determine:
- Which suggestions to incorporate
- What clarifications are needed
- What changes to make to the proposal

#### Step 4: Update Proposal Files

Edit the files in `docs/changes/feature-name/` based on feedback:
- Clarify unclear sections
- Add missing requirements
- Adjust design decisions
- Refine task breakdown

#### Step 5: Push Updates

Commit and push changes to the same branch:

```bash
git add docs/changes/feature-name/
git commit -m "spec: Address review feedback for Feature Name"
git push
```

The Spec PR automatically updates with new changes.

#### Step 6: Request Re-review

If needed, request reviewers take another look at the updated proposal.

## Error Handling

### Proposal Directory Already Exists

**Symptom**: Script reports directory already exists

**Solution**:
- Check if proposal is already in progress: `ls docs/changes/`
- Either use a different name or work with existing proposal
- Consider if this is an update to existing proposal

### Missing GitHub CLI

**Symptom**: `gh: command not found` when using update command

**Solution**:
- Install GitHub CLI: https://cli.github.com/
- Authenticate: `gh auth login`
- Verify: `gh auth status`

### No Review Comments

**Symptom**: Update command shows no comments

**Solution**:
- Verify PR number is correct
- Check if PR has any comments yet
- Wait for reviewers to provide feedback

## Notes

- **Spec PRs are lightweight**: Focus on clarity over perfection - they can be refined
- **Iterate on feedback**: Multiple rounds of review are normal and healthy
- **Keep proposals focused**: One feature/change per proposal makes review easier
- **Link related work**: Reference existing specs or issues in the proposal
- **The `propose` command only creates structure**: You must populate the files with content
- **Spec PRs merge to main**: After approval, specs become source-of-truth in `docs/specs/`
- **Use change-integrator**: After code PR merges, run change-integrator to move approved specs
