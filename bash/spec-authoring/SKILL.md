---
name: spec-authoring
description: Use this skill to propose changes via the Spec PR process. It uses the Gemini CLI to generate high-quality draft specifications and to analyze PR feedback, accelerating the spec-driven development workflow. Triggers include "create spec" or "propose change".
---

# Spec Authoring Skill

## Purpose

To manage the creation and refinement of feature specifications using a powerful, AI-assisted workflow. This skill leverages the **Gemini CLI** to accelerate the spec-driven development process by:
1.  **Generating Drafts**: Automatically creates high-quality, multi-file draft proposals for new features.
2.  **Analyzing Feedback**: Synthesizes review comments from Pull Requests into an actionable summary of recommended changes.

This approach allows developers and product managers to move from idea to an approved, implementation-ready specification with greater speed and clarity.

## When to Use

Use this skill in the following situations:

- Proposing a new feature or significant change.
- Generating a first draft of a specification for review.
- Processing and incorporating feedback from a Spec PR.

## Prerequisites

- Project initialized with SynthesisFlow structure (`docs/specs/` and `docs/changes/` directories exist).
- GitHub repository set up.
- `gh` CLI tool installed and authenticated.
- `gemini` CLI tool installed and authenticated.

## Spec PR Philosophy

**Specs as Code**: All specification changes follow the same rigor as code changes—proposed via branches, reviewed via PRs, and merged upon approval. This skill supercharges that philosophy with AI.

---

## The `propose` Command

### Purpose

Generate a comprehensive, multi-file draft proposal for a new feature from a single command.

### Workflow

#### Step 1: Define the Proposal Name

Choose a clear, descriptive name for your feature, such as "User Authentication System" or "Real-time Notifications".

#### Step 2: Run the Helper Script

Execute the script to generate the draft proposal:
```bash
bash scripts/spec-authoring.sh propose "Feature Name"
```

The script will:
1.  Create a new directory in `docs/changes/feature-name/`.
2.  Make three parallel calls to the **Gemini CLI** to generate drafts for `proposal.md`, `spec-delta.md`, and `tasks.md`.
    - **`proposal.md`**: A high-level overview with problem statement, proposed solution, and success criteria.
    - **`spec-delta.md`**: A detailed technical specification with requirements and design decisions.
    - **`tasks.md`**: A preliminary breakdown of implementation tasks.
3.  Save the AI-generated content into these files.

#### Step 3: Review and Refine the Drafts

The script provides you with a complete, context-aware first draft of your entire proposal. Your next step is to review and refine these documents to ensure they align with your vision before opening a Spec PR.

---

## The `update` Command

### Purpose

Intelligently process feedback from a Spec PR by using AI to analyze review comments and generate a summarized action plan.

### Workflow

#### Step 1: Identify the PR Number

Determine which Spec PR you need to update.

#### Step 2: Run the Feedback Analysis Script

Execute the script with the PR number:
```bash
bash scripts/spec-authoring.sh update PR_NUMBER
```

This command will:
1.  Find the local files associated with the PR's branch.
2.  Fetch all review comments from the PR.
3.  Send the full content of your spec files and all the comments to the **Gemini CLI**.
4.  Ask the AI to act as a reviewer and provide a summarized list of recommended changes for each file.

#### Step 3: Address the Synthesized Feedback

The script will output a clear, actionable plan that synthesizes all the reviewer feedback. Use this analysis to efficiently update your proposal files, address the comments, and push your changes for re-review.

---

## Error Handling

### Gemini CLI Issues

**Symptom**: The script fails during the `propose` or `update` commands with an error related to the `gemini` command.
**Solution**:
- Ensure the `gemini` CLI is installed and in your system's PATH.
- Verify you are authenticated (`gemini auth`).
- Check for Gemini API outages or network issues.

### Proposal Directory Already Exists

**Symptom**: The `propose` command reports that the directory already exists.
**Solution**: Choose a different name for your proposal or work with the existing one.

### Could Not Find Proposal Directory

**Symptom**: The `update` command cannot find the local files for the PR.
**Solution**: Ensure you have the correct PR branch checked out and that the local directory in `docs/changes/` matches the branch name.

## Notes

- **AI-Assisted Workflow**: This skill is designed to be a powerful assistant. It generates high-quality drafts and analyzes feedback, but the final strategic decisions and refinements are yours to make.
- **Speed and Quality**: By automating the initial drafting and feedback synthesis, this skill allows you to focus on the high-value work of design, review, and alignment.
- **Iterative Process**: Use the `propose` command to start, and the `update` command to iterate based on team feedback, creating a rapid and efficient spec development cycle.